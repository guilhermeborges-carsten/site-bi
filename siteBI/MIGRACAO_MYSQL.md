# 🚀 Migração para MySQL - Sistema de BI

## 📋 Pré-requisitos

1. **MySQL/MariaDB rodando** na porta 3306
2. **Banco de dados 'BI' criado** (já feito via bi.sql)
3. **Usuário MySQL com permissões** no banco 'BI'

## ⚙️ Configuração

### 1. Verificar config.py
O arquivo `config.py` já está configurado com:
- Host: localhost
- Porta: 3306
- Usuário: root
- Senha: (vazia - ajuste se necessário)
- Banco: BI

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

## 🧪 Testando a Conexão

### 1. Teste rápido
```bash
python test_db.py
```

### 2. Se der erro, verifique:
- MySQL está rodando?
- Usuário tem permissões?
- Banco 'BI' existe?

### 3. Criar usuário MySQL (se necessário)
```sql
CREATE USER 'root'@'localhost' IDENTIFIED BY 'sua_senha';
GRANT ALL PRIVILEGES ON BI.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

## 🚀 Executando o Sistema

### 1. Primeira execução
```bash
python app.py
```

O sistema irá:
- Conectar ao MySQL
- Verificar se o usuário admin existe
- Criar coluna Backlog se necessário

### 2. Login inicial
- **Email**: guilherme.borges@carsten.com.br
- **Senha**: admin123

## 🔧 Solução de Problemas

### Erro de conexão
```
❌ Erro ao conectar com o banco de dados: (2003, "Can't connect to MySQL server")
```
**Solução**: Verifique se o MySQL está rodando

### Erro de acesso negado
```
❌ Erro ao conectar com o banco de dados: (1045, "Access denied for user")
```
**Solução**: Verifique usuário e senha no config.py

### Erro de banco não encontrado
```
❌ Erro ao conectar com o banco de dados: (1049, "Unknown database 'BI'")
```
**Solução**: Execute o arquivo bi.sql para criar o banco

## 📊 Estrutura do Banco

O sistema usa as seguintes tabelas (já criadas):
- `usuario` - Usuários do sistema
- `chamado` - Chamados/tickets
- `mensagem` - Mensagens dos chamados
- `lista_kanban` - Colunas do Kanban
- `card_kanban` - Cards/tarefas do Kanban
- `comentario_kanban` - Comentários dos cards
- `comentario_interno_kanban` - Comentários internos
- `mensagem_lida` - Controle de leitura
- `auditoria_log` - Log de auditoria

## ✅ Verificação Final

Após a migração, verifique:
1. ✅ Login funcionando
2. ✅ Dashboard carregando
3. ✅ Criação de chamados
4. ✅ Sistema Kanban funcionando
5. ✅ Estatísticas funcionando

## 🆘 Suporte

Se encontrar problemas:
1. Execute `python test_db.py` para diagnóstico
2. Verifique os logs do console
3. Confirme as configurações do MySQL
