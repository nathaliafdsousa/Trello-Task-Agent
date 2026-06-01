# 🤖 Trello Task Agent



## ✨ O que ele faz

Ao iniciar uma conversa, o agente pergunta quais são suas tarefas do dia e cria automaticamente os cards no Trello. Além disso, ele consegue:

-  **Adicionar** tarefas com nome, descrição e data de vencimento
-  **Listar** tarefas por status (A Fazer, Em Andamento, Concluído)
-  **Mover** tarefas entre listas via linguagem natural
-  **Informar** a data e hora atual para contextualizar o planejamento
-  **Editar tarefas com novo nome,descrição e data**
-  **Deletar Tarefas por nomes**

---

## 🗂️ Estrutura do Projeto

```
agent_Tasks/
├── agent.py          # Agente e ferramentas
├── .env              # Credenciais (não versionar)
├── requirements.txt  # Dependências
└── README.md
```

---

## ⚙️ Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/nome-do-repo.git
cd nome-do-repo
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv .lab
# Windows
.lab\Scripts\activate
# Linux/macOS
source .lab/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
TRELLO_API_KEY=sua_api_key
TRELLO_API_SECRET=seu_api_secret
TOKEN_TRELLO=seu_token
```

### 5. Passo a Passo para obter suas credenciais

#### 5.1 Acessar o portal Power-Ups

1- Acesse o portal adminstrador de Power-Ups do Trello
  ```
   https://trello.com/power-ups/admin/
```
 Clique no botão **"New"** ou **"Criar novo Power-Up"**

#### 5.2 Preencher Informações do Aplicativo

Na tela "Novo aplicativo", preencha os seguintes campos:

| Campo | Valor Exemplo | Descrição |
|-------|---------------|-----------|
| **Nome do aplicativo** | `Agent Tasks` ou `Trello Agent` | Nome que identificará seu aplicativo |
| **Área de trabalho** | Selecione seu workspace | Workspace onde o app será gerenciado |
| **Email** | `me@company.com` | Email para contato sobre o aplicativo |
| **Contato de suporte** | `support@company.com` | Email ou link para suporte aos usuários |
| **Autor** | `Seu Nome` ou `Sua Empresa` | Nome do desenvolvedor/empresa |
| **URL de conector iframe** | `https://seu-dominio.com/` | URL do iframe (opcional para API básica) |

#### Passo 2: Obter a API Key

Após criar o Power-Up:

1. Na página de gerenciamento do seu Power-Up, procure pela seção **"API Key"** ou **"Chave de API"**

2. Você verá sua **API Key** ou **chave de API**(uma string alfanumérica longa) e o ** Secret ** ou ** Segredo **

## Passo 3: Gerar o Token de Autorização

#### 5.3 Construir a URL de Autorização

Agora você precisa gerar um token de acesso para fazer requisições em nome do usuário.

Use a seguinte URL, substituindo `SUA_API_KEY_AQUI` pela sua API Key:

```
https://trello.com/1/authorize?expiration=never&name=AppDio&scope=read,write&response_type=token&key=SUA_API_KEY_AQUI
```

### 6 Prepare o board no Trello

#### Crie um board chamado Tasks.

### ▶️ Como Executar
```` 
 adk web
`````
Acesse http://localhost:8000 e selecione o agente.



## Status do Projeto
#### Em fase de aprimoração.
