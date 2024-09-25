import sqlite3


# Função para conectar ao banco de dados
def conectar():
    return sqlite3.connect('tarefas.db')


# Criar tabela de tarefas (se não existir)
def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status INTEGER NOT NULL DEFAULT 0,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


# Adicionar nova tarefa
def adicionar_tarefa(titulo, descricao):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tarefas (titulo, descricao)
            VALUES (?, ?)
        ''', (titulo, descricao))
        conn.commit()
    except Exception as e:
        print(f"Erro ao adicionar tarefa: {e}")
    finally:
        conn.close()


# Listar todas as tarefas
def listar_tarefas():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tarefas')
        tarefas = cursor.fetchall()
        conn.close()

        # Exibir as tarefas de forma organizada
        for tarefa in tarefas:
            status = "Concluída" if tarefa[3] else "Pendente"
            print(f"ID: {tarefa[0]} | Título: {tarefa[1]} | Status: {status} | Criada em: {tarefa[4]}")
    except Exception as e:
        print(f"Erro ao listar tarefas: {e}")


# Atualizar uma tarefa (título e descrição)
def atualizar_tarefa(id_tarefa, novo_titulo, nova_descricao):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tarefas
            SET titulo = ?, descricao = ?
            WHERE id = ?
        ''', (novo_titulo, nova_descricao, id_tarefa))
        conn.commit()
        if cursor.rowcount == 0:
            print("Tarefa não encontrada.")
    except Exception as e:
        print(f"Erro ao atualizar tarefa: {e}")
    finally:
        conn.close()


# Excluir uma tarefa
def excluir_tarefa(id_tarefa):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tarefas WHERE id = ?', (id_tarefa,))
        conn.commit()
        if cursor.rowcount == 0:
            print("Tarefa não encontrada.")
    except Exception as e:
        print(f"Erro ao excluir tarefa: {e}")
    finally:
        conn.close()


# Marcar tarefa como concluída
def marcar_como_concluida(id_tarefa):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tarefas
            SET status = 1
            WHERE id = ?
        ''', (id_tarefa,))
        conn.commit()
        if cursor.rowcount == 0:
            print("Tarefa não encontrada.")
        else:
            print("Tarefa marcada como concluída.")
    except Exception as e:
        print(f"Erro ao marcar tarefa: {e}")
    finally:
        conn.close()


# Menu principal
def menu():
    criar_tabela()  # Garantir que a tabela existe

    while True:
        print("\nGerenciador de Tarefas")
        print("1. Adicionar Tarefa")
        print("2. Listar Tarefas")
        print("3. Atualizar Tarefa")
        print("4. Excluir Tarefa")
        print("5. Marcar como Concluída")
        print("6. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            titulo = input("Título da Tarefa: ")
            descricao = input("Descrição: ")
            adicionar_tarefa(titulo, descricao)
        elif opcao == '2':
            listar_tarefas()
        elif opcao == '3':
            id_tarefa = input("ID da Tarefa a atualizar: ")
            novo_titulo = input("Novo Título: ")
            nova_descricao = input("Nova Descrição: ")
            atualizar_tarefa(id_tarefa, novo_titulo, nova_descricao)
        elif opcao == '4':
            id_tarefa = input("ID da Tarefa a excluir: ")
            excluir_tarefa(id_tarefa)
        elif opcao == '5':
            id_tarefa = input("ID da Tarefa a marcar como concluída: ")
            marcar_como_concluida(id_tarefa)
        elif opcao == '6':
            break
        else:
            print("Opção inválida. Tente novamente.")


# Iniciar o menu
menu()
