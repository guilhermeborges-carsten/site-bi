from flask import Flask, render_template, redirect, url_for, request, flash, session, abort, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from collections import Counter, defaultdict
import pytz

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chamados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'xls', 'xlsx', 'txt', 'csv'}

BR_TZ = pytz.timezone('America/Sao_Paulo')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def to_brasilia(dt):
    if dt is None:
        return None
    if dt.tzinfo is None:
        return pytz.utc.localize(dt).astimezone(BR_TZ)
    return dt.astimezone(BR_TZ)

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# MODELOS
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(200))
    tipo = db.Column(db.String(20))  # 'admin' ou 'usuario'

class Chamado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    protocolo = db.Column(db.String(20), unique=True, nullable=True)  # permitir nulo na criação
    titulo = db.Column(db.String(200))
    descricao = db.Column(db.Text)
    urgencia = db.Column(db.String(20))
    status = db.Column(db.String(20), default='Aberto')
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    anexo = db.Column(db.String(255))  # nome do arquivo anexo
    cargo = db.Column(db.String(100))
    setor = db.Column(db.String(100))
    objetivo = db.Column(db.String(100))
    tipo_projeto = db.Column(db.String(100))
    segmentacao = db.Column(db.String(100))
    responsavel_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    responsavel = db.relationship('Usuario', foreign_keys=[responsavel_id])

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text)
    chamado_id = db.Column(db.Integer, db.ForeignKey('chamado.id'))
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    anexo = db.Column(db.String(255))  # nome do arquivo anexo

class ListaKanban(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    ordem = db.Column(db.Integer)  # para ordenar as listas
    cards = db.relationship('CardKanban', backref='lista', lazy=True)

class CardKanban(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200))
    descricao = db.Column(db.Text)
    responsavel_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    lista_id = db.Column(db.Integer, db.ForeignKey('lista_kanban.id'))
    ordem = db.Column(db.Integer)  # para ordenar os cards
    excluido = db.Column(db.Boolean, default=False)  # novo campo
    comentarios = db.relationship('ComentarioKanban', backref='card', lazy=True)
    chamado_id = db.Column(db.Integer, db.ForeignKey('chamado.id'))  # novo campo para vincular ao chamado

class ComentarioKanban(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text)
    card_id = db.Column(db.Integer, db.ForeignKey('card_kanban.id'))
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)

class ComentarioInternoKanban(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card_kanban.id'))
    autor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    conteudo = db.Column(db.Text)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)

class MensagemLida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mensagem_id = db.Column(db.Integer, db.ForeignKey('mensagem.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    data_leitura = db.Column(db.DateTime, default=datetime.utcnow)

class AuditoriaLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    acao = db.Column(db.String(200))
    detalhes = db.Column(db.Text)
    data = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = Usuario.query.filter_by(email=email).first()
        if user and check_password_hash(user.senha, senha):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Credenciais inválidas')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.tipo == 'admin':
        return redirect(url_for('dailyboard'))
    else:
        # Filtros
        status = request.args.get('status')
        data_ini = request.args.get('data_ini')
        data_fim = request.args.get('data_fim')
        urgencia = request.args.get('urgencia')
        query = Chamado.query.filter_by(usuario_id=current_user.id)
        if status and status != 'todos':
            query = query.filter_by(status=status)
        if data_ini:
            try:
                data_ini_dt = datetime.strptime(data_ini, '%Y-%m-%d')
                chamados_ids = [c.id for c in query.all() 
                    if (msg := Mensagem.query.filter_by(chamado_id=c.id).order_by(Mensagem.data_envio).first()) and msg.data_envio >= data_ini_dt]
                query = query.filter(Chamado.id.in_(chamados_ids))
            except:
                pass
        if data_fim:
            try:
                data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d')
                chamados_ids = [c.id for c in query.all() 
                    if (msg := Mensagem.query.filter_by(chamado_id=c.id).order_by(Mensagem.data_envio).first()) and msg.data_envio <= data_fim_dt]
                query = query.filter(Chamado.id.in_(chamados_ids))
            except:
                pass
        if urgencia:
            query = query.filter_by(urgencia=urgencia)
        chamados = query.all()
        # Opções de categoria removidas
        # Identificar chamados com mensagens não lidas
        chamados_nao_lidos = set()
        for chamado in chamados:
            mensagens = Mensagem.query.filter_by(chamado_id=chamado.id).all()
            for msg in mensagens:
                if msg.autor_id != current_user.id and not MensagemLida.query.filter_by(mensagem_id=msg.id, usuario_id=current_user.id).first():
                    chamados_nao_lidos.add(chamado.id)
                    break
        return render_template('dashboard.html', chamados=chamados, filtros={
            'status': status, 'data_ini': data_ini, 'data_fim': data_fim, 'urgencia': urgencia
        }, chamados_nao_lidos=chamados_nao_lidos)

@app.route('/novo_chamado', methods=['GET', 'POST'])
@login_required
def novo_chamado():
    if request.method == 'POST':
        chamado = Chamado()
        chamado.titulo = request.form['titulo']
        chamado.descricao = request.form['descricao']
        chamado.cargo = request.form['cargo']
        chamado.setor = request.form['setor']
        chamado.segmentacao = request.form['segmentacao']
        chamado.tipo_projeto = request.form['tipo_projeto']
        chamado.objetivo = request.form['objetivo']
        chamado.urgencia = request.form.get('urgencia')
        chamado.usuario_id = current_user.id
        # Salvar anexo se enviado
        file = request.files.get('anexo')
        if file and file.filename and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            i = 1
            base, ext = os.path.splitext(filename)
            while os.path.exists(filepath):
                filename = f"{base}_{i}{ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                i += 1
            file.save(filepath)
            chamado.anexo = filename
        db.session.add(chamado)
        db.session.commit()
        # Protocolo sequencial a partir de 1001
        chamado.protocolo = str(chamado.id + 1000)
        db.session.commit()
        # Criar card no Kanban (Backlog)
        backlog = ListaKanban.query.filter_by(nome='Backlog').first()
        if backlog:
            card = CardKanban()
            card.titulo = chamado.titulo
            card.descricao = chamado.descricao
            card.lista_id = backlog.id
            card.ordem = 0  # ajuste se necessário
            card.responsavel_id = None
            card.chamado_id = chamado.id
            db.session.add(card)
            db.session.commit()
        flash(f'Chamado aberto com sucesso! Protocolo: {chamado.protocolo}')
        return redirect(url_for('dashboard'))
    return render_template('novo_chamado.html')

@app.route('/chamado/<int:id>', methods=['GET', 'POST'])
@login_required
def detalhes_chamado(id):
    chamado = Chamado.query.get_or_404(id)
    mensagens = Mensagem.query.filter_by(chamado_id=id).order_by(Mensagem.data_envio).all()
    # Marcar mensagens como lidas para o usuário atual
    for msg in mensagens:
        if not MensagemLida.query.filter_by(mensagem_id=msg.id, usuario_id=current_user.id).first():
            leitura = MensagemLida()
            leitura.mensagem_id = msg.id
            leitura.usuario_id = current_user.id
            db.session.add(leitura)
    db.session.commit()
    if request.method == 'POST':
        # Se admin, pode alterar status
        if current_user.tipo == 'admin' and 'novo_status' in request.form:
            chamado.status = request.form['novo_status']
            db.session.commit()
            flash('Status do chamado atualizado!')
            return redirect(url_for('detalhes_chamado', id=id))
        # Mensagem do chat
        conteudo = request.form.get('mensagem')
        if conteudo:
            msg = Mensagem()
            msg.conteudo = conteudo
            msg.chamado_id = id
            msg.autor_id = current_user.id
            db.session.add(msg)
            db.session.commit()
            return redirect(url_for('detalhes_chamado', id=id))
    usuarios = Usuario.query.all()
    return render_template('detalhes_chamado.html', chamado=chamado, mensagens=mensagens, usuarios=usuarios)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        if Usuario.query.filter_by(email=email).first():
            flash('Email já cadastrado')
            return render_template('cadastro.html')
        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario()
        novo_usuario.nome = nome
        novo_usuario.email = email
        novo_usuario.senha = senha_hash
        novo_usuario.tipo = 'usuario'
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça login.')
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/usuarios')
@login_required
def usuarios():
    if current_user.tipo != 'admin':
        abort(403)
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=lista_usuarios)

@app.route('/usuario/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    if current_user.tipo != 'admin':
        abort(403)
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        usuario.tipo = request.form['tipo']
        if request.form['senha']:
            usuario.senha = generate_password_hash(request.form['senha'])
        db.session.commit()
        # Log de auditoria
        log = AuditoriaLog()
        log.usuario_id = current_user.id
        log.acao = 'Editar usuário'
        log.detalhes = f'Usuário editado: id={usuario.id}, nome={usuario.nome}, email={usuario.email}, tipo={usuario.tipo}'
        db.session.add(log)
        db.session.commit()
        flash('Usuário atualizado com sucesso!')
        return redirect(url_for('usuarios'))
    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/usuario/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_usuario(id):
    if current_user.tipo != 'admin':
        abort(403)
    usuario = Usuario.query.get_or_404(id)
    if usuario.id == current_user.id:
        flash('Você não pode excluir a si mesmo!')
        return redirect(url_for('usuarios'))
    db.session.delete(usuario)
    db.session.commit()
    # Log de auditoria
    log = AuditoriaLog()
    log.usuario_id = current_user.id
    log.acao = 'Excluir usuário'
    log.detalhes = f'Usuário excluído: id={usuario.id}, nome={usuario.nome}, email={usuario.email}, tipo={usuario.tipo}'
    db.session.add(log)
    db.session.commit()
    flash('Usuário excluído com sucesso!')
    return redirect(url_for('usuarios'))

@app.route('/uploads/<filename>')
@login_required
def download_anexo(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/estatisticas')
@login_required
def estatisticas():
    if current_user.tipo != 'admin':
        abort(403)
    # Filtros
    status = request.args.get('status')
    data_ini = request.args.get('data_ini')
    data_fim = request.args.get('data_fim')
    urgencia = request.args.get('urgencia')
    colaborador = request.args.get('colaborador')
    query = Chamado.query
    # Filtros básicos
    print('DEBUG - status:', status, '| urgencia:', urgencia, '| colaborador:', colaborador)
    print('DEBUG - valores possíveis status:', [c.status for c in Chamado.query.all()])
    print('DEBUG - valores possíveis urgencia:', [c.urgencia for c in Chamado.query.all()])
    print('DEBUG - valores possíveis usuario_id:', [c.usuario_id for c in Chamado.query.all()])
    if status and status.lower() != 'todos':
        query = query.filter(Chamado.status == status)
    if urgencia and urgencia.lower() != 'todas':
        query = query.filter(Chamado.urgencia == urgencia)
    if colaborador and colaborador.lower() != 'todos':
        try:
            colaborador_id = int(colaborador)
            query = query.filter(Chamado.usuario_id == colaborador_id)
        except:
            pass
    chamados = query.all()
    # Só filtra por data se algum campo de data estiver preenchido
    if (data_ini and data_ini.strip()) or (data_fim and data_fim.strip()):
        chamados_filtrados = []
        for c in chamados:
            msg = Mensagem.query.filter_by(chamado_id=c.id).order_by(Mensagem.data_envio).first()
            if msg:
                if data_ini and data_ini.strip():
                    data_ini_dt = datetime.strptime(data_ini, '%Y-%m-%d')
                    if msg.data_envio < data_ini_dt:
                        continue
                if data_fim and data_fim.strip():
                    data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d')
                    if msg.data_envio > data_fim_dt:
                        continue
                chamados_filtrados.append(c)
            else:
                # Se não há mensagem, só mostra se não houver filtro de data
                if not (data_ini and data_ini.strip()) and not (data_fim and data_fim.strip()):
                    chamados_filtrados.append(c)
        chamados = chamados_filtrados
    # Por mês
    por_mes = defaultdict(int)
    for c in chamados:
        msg = Mensagem.query.filter_by(chamado_id=c.id).order_by(Mensagem.data_envio).first()
        if msg:
            mes = msg.data_envio.strftime('%Y-%m')
        else:
            mes = 'Sem data'
        por_mes[mes] += 1
    # Por colaborador
    por_colab = Counter([c.usuario_id for c in chamados])
    usuarios = {u.id: u.nome for u in Usuario.query.all()}
    # Novos gráficos
    por_urgencia = Counter([c.urgencia for c in chamados if c.urgencia])
    por_status = Counter([c.status for c in chamados if c.status])
    por_segmentacao = Counter([c.segmentacao for c in chamados if c.segmentacao])
    por_tipo_projeto = Counter([c.tipo_projeto for c in chamados if c.tipo_projeto])
    por_objetivo = Counter([c.objetivo for c in chamados if c.objetivo])
    colaboradores = Usuario.query.all()
    return render_template('estatisticas.html', por_mes=por_mes, por_colab=por_colab, usuarios=usuarios, colaboradores=colaboradores, filtros={
        'status': status, 'data_ini': data_ini, 'data_fim': data_fim, 'urgencia': urgencia, 'colaborador': colaborador
    },
    por_urgencia=por_urgencia,
    por_status=por_status,
    por_segmentacao=por_segmentacao,
    por_tipo_projeto=por_tipo_projeto,
    por_objetivo=por_objetivo
    )

@app.route('/dailyboard', methods=['GET', 'POST'])
@login_required
def dailyboard():
    if current_user.tipo != 'admin':
        abort(403)
    protocolo = request.args.get('protocolo')
    if protocolo:
        chamado = Chamado.query.filter_by(protocolo=protocolo).first()
        listas = ListaKanban.query.order_by(ListaKanban.ordem).all()
        if chamado:
            for lista in listas:
                lista.cards = [card for card in lista.cards if card.chamado_id == chamado.id]
        else:
            for lista in listas:
                lista.cards = []
    else:
        listas = ListaKanban.query.order_by(ListaKanban.ordem).all()
    usuarios = Usuario.query.all()
    # Montar dicionário de chamados para lookup rápido no template
    chamados_ids = [card.chamado_id for lista in listas for card in lista.cards if card.chamado_id]
    chamados = Chamado.query.filter(Chamado.id.in_(chamados_ids)).all() if chamados_ids else []
    chamados_dict = {c.id: c for c in chamados}
    # Adicionar relacionamento do usuário
    for chamado in chamados:
        chamado.usuario = Usuario.query.get(chamado.usuario_id)
    # Identificar chamados com mensagens não lidas para o admin
    chamados_nao_lidos = set()
    for chamado in chamados:
        mensagens = Mensagem.query.filter_by(chamado_id=chamado.id).all()
        for msg in mensagens:
            if msg.autor_id != current_user.id and not MensagemLida.query.filter_by(mensagem_id=msg.id, usuario_id=current_user.id).first():
                chamados_nao_lidos.add(chamado.id)
                break
    return render_template('dailyboard.html', listas=listas, usuarios=usuarios, chamados_dict=chamados_dict, chamados_nao_lidos=chamados_nao_lidos)

@app.route('/dailyboard/mover_card', methods=['POST'])
@login_required
def mover_card():
    if current_user.tipo != 'admin':
        abort(403)
    data = request.get_json()
    card_id = data.get('card_id')
    nova_lista_id = data.get('nova_lista_id')
    nova_ordem = data.get('nova_ordem')  # lista de ids na ordem final
    card = CardKanban.query.get(card_id)
    if card and nova_lista_id:
        card.lista_id = nova_lista_id
        # Se for coluna Finalizado (nome exato), atualizar status do chamado
        lista_finalizado = ListaKanban.query.get(nova_lista_id)
        if lista_finalizado and lista_finalizado.nome.strip().lower() == "finalizado":
            if card.chamado_id:
                chamado = Chamado.query.get(card.chamado_id)
                if chamado and chamado.status != 'Finalizado':
                    chamado.status = 'Finalizado'
        db.session.commit()
    # Atualizar ordem dos cards na lista
    if nova_ordem:
        for idx, cid in enumerate(nova_ordem):
            c = CardKanban.query.get(cid)
            if c:
                c.ordem = idx + 1
        db.session.commit()
    return jsonify({'success': True})

@app.route('/dailyboard/card/<int:card_id>', methods=['GET', 'POST'])
@login_required
def dailyboard_card(card_id):
    card = CardKanban.query.get_or_404(card_id)
    chamado = None
    mensagens = []
    comentarios_internos = ComentarioInternoKanban.query.filter_by(card_id=card_id).order_by(ComentarioInternoKanban.data_envio).all()
    if card.chamado_id:
        chamado = Chamado.query.get(card.chamado_id)
        if chamado:
            chamado.usuario = Usuario.query.get(chamado.usuario_id)
        mensagens = Mensagem.query.filter_by(chamado_id=card.chamado_id).order_by(Mensagem.data_envio).all()
        # Marcar mensagens como lidas para o usuário atual
        for msg in mensagens:
            if not MensagemLida.query.filter_by(mensagem_id=msg.id, usuario_id=current_user.id).first():
                leitura = MensagemLida()
                leitura.mensagem_id = msg.id
                leitura.usuario_id = current_user.id
                db.session.add(leitura)
        db.session.commit()
    # Alteração de status do chamado
    if request.method == 'POST' and request.form.get('tipo_form') == 'status' and current_user.tipo == 'admin' and chamado:
        novo_status = request.form.get('novo_status')
        if novo_status and novo_status != chamado.status:
            chamado.status = novo_status
            db.session.commit()
            flash('Status do chamado atualizado!')
            return redirect(url_for('dailyboard_card', card_id=card_id))
    # Comentário interno admin
    if request.method == 'POST' and request.form.get('tipo_form') == 'interno' and current_user.tipo == 'admin':
        conteudo = request.form.get('comentario_interno')
        if conteudo:
            ci = ComentarioInternoKanban()
            ci.card_id = card_id
            ci.autor_id = current_user.id
            ci.conteudo = conteudo
            db.session.add(ci)
            db.session.commit()
            return redirect(url_for('dailyboard_card', card_id=card_id))
    # Mensagem do chamado
    if request.method == 'POST' and card.chamado_id and request.form.get('tipo_form') != 'interno' and request.form.get('tipo_form') != 'status' and current_user.tipo == 'admin':
        conteudo = request.form.get('comentario')
        file = request.files.get('anexo')
        anexo_nome = None
        if file and file.filename and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            i = 1
            base, ext = os.path.splitext(filename)
            while os.path.exists(filepath):
                filename = f"{base}_{i}{ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                i += 1
            file.save(filepath)
            anexo_nome = filename
        if conteudo or anexo_nome:
            msg = Mensagem()
            msg.conteudo = conteudo
            msg.chamado_id = card.chamado_id
            msg.autor_id = current_user.id
            if anexo_nome:
                msg.anexo = anexo_nome
            db.session.add(msg)
            db.session.commit()
            return redirect(url_for('dailyboard_card', card_id=card_id))
    usuarios = Usuario.query.all()
    return render_template('card_kanban.html', card=card, usuarios=usuarios, mensagens=mensagens, comentarios_internos=comentarios_internos, chamado=chamado)

@app.route('/dailyboard/listas', methods=['GET', 'POST'])
@login_required
def dailyboard_listas():
    if current_user.tipo != 'admin':
        abort(403)
    if request.method == 'POST':
        # Se for criação de coluna
        if request.form.get('nome') and not request.form.get('titulo'):
            nome = request.form.get('nome')
            ordem = request.form.get('ordem')
            lista = ListaKanban()
            lista.nome = nome
            lista.ordem = ordem or 1
            db.session.add(lista)
            db.session.commit()
            return redirect(url_for('dailyboard_listas'))
        # Se for criação de card
        elif request.form.get('titulo') and request.form.get('lista_id'):
            titulo = request.form.get('titulo')
            descricao = request.form.get('descricao')
            responsavel_id = request.form.get('responsavel_id')
            lista_id = request.form.get('lista_id')
            lista = ListaKanban.query.get(lista_id)
            ordem = len(lista.cards) + 1 if lista else 1
            card = CardKanban()
            card.titulo = titulo
            card.descricao = descricao
            card.responsavel_id = responsavel_id or None
            card.lista_id = lista_id
            card.ordem = ordem
            db.session.add(card)
            db.session.commit()
            return redirect(url_for('dailyboard_listas'))
    listas = ListaKanban.query.order_by(ListaKanban.ordem).all()
    usuarios = Usuario.query.all()
    return render_template('listas_kanban.html', listas=listas, usuarios=usuarios)

@app.route('/dailyboard/listas/<int:lista_id>/editar', methods=['POST'])
@login_required
def editar_lista_kanban(lista_id):
    if current_user.tipo != 'admin':
        abort(403)
    lista = ListaKanban.query.get_or_404(lista_id)
    if lista.nome.strip().lower() == 'backlog':
        flash('A coluna Backlog não pode ser editada!')
        return redirect(url_for('dailyboard_listas'))
    nome = request.form.get('nome')
    ordem = request.form.get('ordem')
    if nome:
        lista.nome = nome
    if ordem:
        lista.ordem = ordem
    db.session.commit()
    return redirect(url_for('dailyboard_listas'))

@app.route('/dailyboard/listas/<int:lista_id>/excluir', methods=['POST'])
@login_required
def excluir_lista_kanban(lista_id):
    if current_user.tipo != 'admin':
        abort(403)
    lista = ListaKanban.query.get_or_404(lista_id)
    if lista.nome.strip().lower() == 'backlog':
        flash('A coluna Backlog não pode ser excluída!')
        return redirect(url_for('dailyboard_listas'))
    db.session.delete(lista)
    db.session.commit()
    # Log de auditoria
    log = AuditoriaLog()
    log.usuario_id = current_user.id
    log.acao = 'Excluir lista Kanban'
    log.detalhes = f'Lista excluída: id={lista.id}, nome={lista.nome}'
    db.session.add(log)
    db.session.commit()
    return redirect(url_for('dailyboard_listas'))

@app.route('/dailyboard/card/<int:card_id>/finalizar', methods=['POST'])
@login_required
def finalizar_card_kanban(card_id):
    if current_user.tipo != 'admin':
        abort(403)
    card = CardKanban.query.get_or_404(card_id)
    coluna_concluido = ListaKanban.query.filter(
        (ListaKanban.nome.ilike('%conclu%')) | (ListaKanban.nome.ilike('%finaliz%'))
    ).first()
    if coluna_concluido:
        card.lista_id = coluna_concluido.id
        card.ordem = (max([c.ordem for c in coluna_concluido.cards] or [0]) + 1)
        db.session.commit()
        # Log de auditoria
        log = AuditoriaLog()
        log.usuario_id = current_user.id
        log.acao = 'Finalizar card Kanban'
        log.detalhes = f'Card finalizado: id={card.id}, titulo={card.titulo}, chamado_id={card.chamado_id}'
        db.session.add(log)
        db.session.commit()
    return redirect(url_for('dailyboard'))

@app.route('/dailyboard/historico')
@login_required
def dailyboard_historico():
    if current_user.tipo != 'admin':
        abort(403)
    responsavel = request.args.get('responsavel')
    data_ini = request.args.get('data_ini')
    data_fim = request.args.get('data_fim')
    excluido = request.args.get('excluido', 'todos')
    query = CardKanban.query
    if responsavel and responsavel != 'todos':
        query = query.filter_by(responsavel_id=responsavel)
    if excluido == 'ativos':
        query = query.filter_by(excluido=False)
    elif excluido == 'excluidos':
        query = query.filter_by(excluido=True)
    if data_ini:
        try:
            from datetime import datetime
            from pytz import timezone
            tz = timezone('America/Sao_Paulo')
            data_ini_dt = tz.localize(datetime.strptime(data_ini, '%Y-%m-%d'))
            query = query.filter(CardKanban.id.in_([c.id for c in CardKanban.query.all() if c.comentarios and min([com.data_envio for com in c.comentarios]) >= data_ini_dt]))
        except:
            pass
    if data_fim:
        try:
            from datetime import datetime
            from pytz import timezone
            tz = timezone('America/Sao_Paulo')
            data_fim_dt = tz.localize(datetime.strptime(data_fim, '%Y-%m-%d'))
            query = query.filter(CardKanban.id.in_([c.id for c in CardKanban.query.all() if c.comentarios and min([com.data_envio for com in c.comentarios]) <= data_fim_dt]))
        except:
            pass
    cards = query.all()
    usuarios = Usuario.query.all()
    listas = ListaKanban.query.all()
    return render_template('historico_dailys.html', cards=cards, usuarios=usuarios, listas=listas, filtros={
        'responsavel': responsavel, 'data_ini': data_ini, 'data_fim': data_fim, 'excluido': excluido
    })

@app.route('/dailyboard/card/<int:card_id>/excluir', methods=['POST'])
@login_required
def excluir_card_kanban(card_id):
    if current_user.tipo != 'admin':
        abort(403)
    card = CardKanban.query.get_or_404(card_id)
    coluna = ListaKanban.query.get(card.lista_id)
    if coluna and (('conclu' in coluna.nome.lower()) or ('finaliz' in coluna.nome.lower())):
        card.excluido = True
        db.session.commit()
        # Log de auditoria
        log = AuditoriaLog()
        log.usuario_id = current_user.id
        log.acao = 'Excluir card Kanban'
        log.detalhes = f'Card excluído: id={card.id}, titulo={card.titulo}, chamado_id={card.chamado_id}'
        db.session.add(log)
        db.session.commit()
    return redirect(url_for('dailyboard'))

@app.route('/atribuir_responsavel/<int:chamado_id>', methods=['POST'])
@login_required
def atribuir_responsavel(chamado_id):
    if current_user.tipo != 'admin':
        abort(403)
    chamado = Chamado.query.get_or_404(chamado_id)
    responsavel_id = request.form.get('responsavel_id')
    if responsavel_id:
        chamado.responsavel_id = int(responsavel_id)
        db.session.commit()
        # Sincronizar responsável do card do Kanban
        card = CardKanban.query.filter_by(chamado_id=chamado.id).first()
        if card:
            card.responsavel_id = chamado.responsavel_id
            db.session.commit()
        # Log de auditoria
        log = AuditoriaLog()
        log.usuario_id = current_user.id
        log.acao = 'Atribuir responsável'
        log.detalhes = f'Responsável atribuído ao chamado {chamado.id} (protocolo {chamado.protocolo}): usuário_id={responsavel_id}'
        db.session.add(log)
        db.session.commit()
        flash('Responsável atribuído com sucesso!')
    return redirect(url_for('dashboard'))

@app.route('/dailyboard/card/<int:card_id>/em_andamento', methods=['POST'])
@login_required
def em_andamento_card_kanban(card_id):
    if current_user.tipo != 'admin':
        abort(403)
    card = CardKanban.query.get_or_404(card_id)
    coluna_andamento = ListaKanban.query.filter(ListaKanban.nome.ilike('%andamento%')).first()
    if coluna_andamento:
        card.lista_id = coluna_andamento.id
        card.ordem = (max([c.ordem for c in coluna_andamento.cards] or [0]) + 1)
        db.session.commit()
    return redirect(url_for('dailyboard'))

@app.route('/dailyboard/card/<int:card_id>/voltar_backlog', methods=['POST'])
@login_required
def voltar_backlog_card_kanban(card_id):
    if current_user.tipo != 'admin':
        abort(403)
    card = CardKanban.query.get_or_404(card_id)
    backlog = ListaKanban.query.filter(ListaKanban.nome.ilike('backlog')).first()
    if backlog:
        card.lista_id = backlog.id
        card.ordem = (max([c.ordem for c in backlog.cards] or [0]) + 1)
        db.session.commit()
        # Log de auditoria
        log = AuditoriaLog()
        log.usuario_id = current_user.id
        log.acao = 'Voltar card para Backlog'
        log.detalhes = f'Card voltou para Backlog: id={card.id}, titulo={card.titulo}, chamado_id={card.chamado_id}'
        db.session.add(log)
        db.session.commit()
    return redirect(url_for('dailyboard'))

@app.template_filter('to_brasilia')
def to_brasilia_filter(dt):
    return to_brasilia(dt)

@app.template_filter('formata_data')
def formata_data(dt, formato='%d/%m/%Y %H:%M'):
    if dt is None:
        return ''
    return dt.strftime(formato)

@app.route('/auditoria')
@login_required
def auditoria():
    if current_user.tipo != 'admin':
        abort(403)
    logs = AuditoriaLog.query.order_by(AuditoriaLog.data.desc()).all()
    usuarios = {u.id: u.nome for u in Usuario.query.all()}
    return render_template('auditoria.html', logs=logs, usuarios=usuarios)

# CRIAR BANCO DE DADOS INICIAL
if not os.path.exists('chamados.db'):
    with app.app_context():
        db.create_all()
        # Verifica se já existe o admin
        if not Usuario.query.filter_by(email='admin@empresa.com').first():
            admin = Usuario()
            admin.nome = 'Admin'
            admin.email = 'admin@empresa.com'
            admin.senha = generate_password_hash('admin123')
            admin.tipo = 'admin'
            db.session.add(admin)
            db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
