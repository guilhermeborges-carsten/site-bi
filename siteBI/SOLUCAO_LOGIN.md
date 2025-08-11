# 🔐 Guia de Solução de Problemas - Login Sistema BI

## 🚨 Problema: Não consigo fazer login

### ✅ **SOLUÇÃO RÁPIDA**

Use uma das seguintes credenciais:

#### 👤 **Administrador**
- **Email:** `admin@empresa.com`
- **Senha:** `admin123`

#### 👤 **Usuário**
- **Email:** `guilherme.borges@carsten.com.br`
- **Senha:** `123`

---

## 🔍 **DIAGNÓSTICO DETALHADO**

### 1. **Verificar se o Flask está rodando**
```bash
# No terminal, execute:
python app.py
```

**Resultado esperado:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### 2. **Verificar banco de dados**
```bash
# Execute o script de diagnóstico:
python debug_login.py
```

### 3. **Testar credenciais**
```bash
# Execute o script de teste:
python testar_login.py
```

---

## 🛠️ **SOLUÇÕES ESPECÍFICAS**

### **Problema 1: "Credenciais inválidas"**

#### ✅ **Solução:**
1. Use exatamente as credenciais listadas acima
2. Verifique se não há espaços extras
3. Certifique-se de que o Caps Lock está desligado

#### 🔍 **Debug:**
- Verifique o console do Flask para logs de debug
- Os logs mostrarão se o usuário foi encontrado e se a senha está correta

### **Problema 2: "Usuário não encontrado"**

#### ✅ **Solução:**
1. Verifique se digitou o email corretamente
2. Use um dos emails válidos:
   - `admin@empresa.com`
   - `guilherme.borges@carsten.com.br`

### **Problema 3: "Senha incorreta"**

#### ✅ **Solução:**
1. Use exatamente as senhas:
   - Para admin: `admin123`
   - Para usuário: `123`

### **Problema 4: Flask não inicia**

#### ✅ **Solução:**
1. Verifique se todas as dependências estão instaladas:
```bash
pip install -r requirements.txt
```

2. Verifique se o Python está na versão correta:
```bash
python --version
```

### **Problema 5: Banco de dados corrompido**

#### ✅ **Solução:**
1. Delete o arquivo do banco:
```bash
rm instance/chamados.db
```

2. Execute o Flask novamente (ele criará um novo banco):
```bash
python app.py
```

3. Crie um novo usuário através da página de cadastro

---

## 🆘 **CRIAR NOVO USUÁRIO**

Se nenhuma das credenciais funcionar:

### **Opção 1: Página de Cadastro**
1. Acesse: `http://localhost:5000/cadastro`
2. Preencha os dados
3. Faça login com as novas credenciais

### **Opção 2: Script de Criação**
```bash
python debug_login.py
```
O script criará automaticamente um usuário admin padrão.

---

## 📋 **CHECKLIST DE VERIFICAÇÃO**

- [ ] Flask está rodando na porta 5000
- [ ] Banco de dados existe e tem usuários
- [ ] Email digitado corretamente
- [ ] Senha digitada corretamente
- [ ] Não há espaços extras
- [ ] Caps Lock está desligado
- [ ] Console do Flask mostra logs de debug

---

## 🎯 **CREDENCIAIS CONFIRMADAS**

Após análise do banco de dados, estas são as credenciais válidas:

### **Admin**
- **Email:** `admin@empresa.com`
- **Senha:** `admin123`
- **Tipo:** Administrador

### **Usuário**
- **Email:** `guilherme.borges@carsten.com.br`
- **Senha:** `123`
- **Tipo:** Usuário comum

---

## 📞 **SUPORTE**

Se ainda não conseguir fazer login:

1. **Verifique os logs do Flask** no console
2. **Execute os scripts de diagnóstico** fornecidos
3. **Crie um novo usuário** através da página de cadastro
4. **Verifique se não há erros** no console do navegador

---

## 🔧 **COMANDOS ÚTEIS**

```bash
# Iniciar o Flask
python app.py

# Diagnosticar problemas
python debug_login.py

# Testar credenciais
python testar_login.py

# Verificar dependências
pip list

# Instalar dependências
pip install -r requirements.txt
```

---

*Última atualização: Sistema BI v2.0 - Interface Ultra-Moderna* 🚀 