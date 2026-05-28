from google.adk.agents.llm_agent import Agent
from trello import TrelloClient
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

API_KEY = os.getenv('TRELLO_API_KEY')
API_SECRET = os.getenv('TRELLO_API_SECRET')
TOKEN = os.getenv('TOKEN_TRELLO')


def get_temporal_context():
    now = datetime.now()
    return now.strftime('%Y/%m/%d %H:%M:%S')


def adicionar_tarefa(nome_da_task: str, descricao_da_task: str, due_date: str):
    try:
        date_obj = datetime.strptime(due_date, "%d/%m/%Y")
        due_date = date_obj.strftime("%Y-%m-%dT23:59:00.000Z")
    except ValueError:
        due_date = None
    
    client = TrelloClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        token=TOKEN
    )
    
    client.list_boards()
    
    boards = client.list_boards()
    meu_board = [b for b in boards if b.name == 'Tasks'][0]

    
    listas = meu_board.list_lists()

    minha_lista = [l for l in listas if l.name.upper() == 'TO DO' or l.name.upper()== 'A FAZER'][0]
    
 
    minha_lista.add_card(
        name=nome_da_task,
        desc=descricao_da_task,
        due=due_date
    )

def listar_tarefas(status: str = "todas"):
    client = TrelloClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        token=TOKEN
    )

    boards = client.list_boards()
    meu_board = [b for b in boards if b.name == 'Tasks'][0]
    listas = meu_board.list_lists()        

    if status.lower() == "todas":
        listas_filtradas = listas
    elif status.lower() == "a fazer":
        listas_filtradas = [l for l in listas if l.name.upper() in ['A FAZER', 'TO DO', 'TODO']]
    elif status.lower() == "em andamento":
        listas_filtradas = [l for l in listas if l.name.upper() in ['EM ANDAMENTO', 'DOING']]
    elif status.lower() == "concluido":
        listas_filtradas = [l for l in listas if l.name.upper() in ['CONCLUÍDO', 'CONCLUIDO', 'DONE']]
    else:
        listas_filtradas = listas

    tarefas = []

    for lista in listas_filtradas:
        cards = lista.list_cards()
        for card in cards:
            tarefas.append({
                "nome": card.name,
                "descricao": card.desc,
                "vencimento": card.due,
                "status": lista.name,
                "id": card.id
            })
    
    return tarefas

def mudar_status_tarefa(nome_da_task: str, novo_status: str) -> str:
    try:
        client = TrelloClient(
            api_key=API_KEY,
            api_secret=API_SECRET,
            token=TOKEN
        )

        boards = client.list_boards()
        meu_board = [b for b in boards if b.name == 'Tasks'][0]
        listas = meu_board.list_lists()
                       
    
        status_map = {
            "a fazer": "A FAZER",
            "em andamento": "EM ANDAMENTO",
            "concluido": "CONCLUÍDO"
        }
        
        nome_lista_destino = status_map.get(novo_status.lower())

        if not nome_lista_destino:
            return f"Status inválido. Use: 'a fazer', 'em andamento' ou 'concluido'"
        
        # Encontrar lista de destino
        lista_destino = next(
            (l for l in listas if l.name.upper() == nome_lista_destino.upper()), 
            None
        )

        if not lista_destino:
            return f"Lista '{nome_lista_destino}' não encontrada no board"
        
        
        card_encontrado = None
        lista_origem = None

        for lista in listas:
            cards = lista.list_cards()
            card_encontrado = next(
                (c for c in cards if c.name.lower() == nome_da_task.lower()), 
                None
            )
            if card_encontrado:
                lista_origem = lista
                break
        
        if not card_encontrado:
            return f"Card '{nome_da_task}' não encontrado"
        
        card_encontrado.change_list(lista_destino.id)
        return f"'{nome_da_task}': {lista_origem.name} → {lista_destino.name}"
    except Exception as e:
        return f"Erro: {str(e)}"


def deletar_tarefa(nome_da_task:str) -> str:
    try:
        client = TrelloClient(
            api_key= API_KEY,
            api_secret= API_SECRET,
            token = TOKEN
        )
        boards = client.list_boards()
        meu_board = [b for b in boards if b.name == 'Tasks'][0]
        listas = meu_board.list_lists()

        for lista in listas:
            card = next(
                (e for e in lista.list_cards() if e.name.upper() == nome_da_task.upper()),
                None
            )
            if card:
                card.delete()
                return f"Card '{nome_da_task}' deletado com sucesso"
        return f"Card '{nome_da_task}' não encontrado"
    except Exception as e:
        return f"Erro: {str(e)}"

def editar_tarefa(nome_da_task: str, novo_nome: str = None, nova_descricao: str = None, novo_due_date: str = None) -> str:
    try:
        client = TrelloClient(
            api_key=API_KEY,
            api_secret=API_SECRET,
            token=TOKEN
        )

        boards = client.list_boards()
        meu_board = [b for b in boards if b.name == 'Tasks'][0]
        listas = meu_board.list_lists()

        for lista in listas:
            cards = lista.list_cards()
            card = next(
                (c for c in cards if c.name.lower() == nome_da_task.lower()),
                None
            )
            if card:
                if novo_nome:
                    card.set_name(novo_nome)
                if nova_descricao:
                    card.set_description(nova_descricao)
                if novo_due_date:
                    try:
                        date_obj = datetime.strptime(novo_due_date, "%d/%m/%Y")
                        formatted = date_obj.strftime("%Y-%m-%dT23:59:00.000Z")
                        card.set_due(formatted)
                    except ValueError:
                        return "Data inválida. Use o formato DD/MM/AAAA."

                return f"'{nome_da_task}' atualizada com sucesso."

        return f"Card '{nome_da_task}' não encontrado."
    except Exception as e:
        return f"Erro: {str(e)}"
                
            




root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Agente de organização de tarefas',
    instruction="""
    Você é um agente de organização de tarefas.
    Sua função é receber uma tarefa e criar um card no Trello com o nome e descrição da tarefa.
    Você deve me perguntar as atividades que tenho no dia e criar um card para cada atividade.
    Sempre inicia uma conversa perguntando quais as tarefas do dia informando a data pela tool get_temporal_context,
    e depois vá perguntando se tem mais tarefas para o dia até que o usuário diga que não tem mais tarefas para o dia.
    Sempre fale que a tarefa foi criada com sucesso.
    Ao perguntar a data de vencimento de uma tarefa, peça no formato DD/MM/AAAA.
    Deletar tarefas quando o usuário pedir para remover ou excluir
    Editar tarefas existentes = pode alterar nome, descrição e data de vencimento
    1. Adicionar novas tarefas com nome e descrição
          2. Listar todas as tarefas ou filtrar por status
          3. Marcar tarefas como concluídas
          4. Remover tarefas da lista
          5. Mudar o status da tarefa (ex: de "A Fazer" para "Em Andamento" e de "Em Andamento" para "Concluído")
          6. Gerar contexto temporal (data e hora atual) para organizar as tarefas do dia
    
    
    """,
   tools=[get_temporal_context, adicionar_tarefa, listar_tarefas, mudar_status_tarefa, deletar_tarefa, editar_tarefa],
)

