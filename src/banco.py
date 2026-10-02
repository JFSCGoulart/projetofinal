# src/banco.py
"""Todas as operações de banco de dados."""
from config import BANCO
import sqlite3
# ============ conexao ============
def conectar():
    """Abre conexao com o banco."""
    return sqlite3.connect(BANCO)
def criar_banco():
    """Executa a criação das tabelas."""
    conexao = sqlite3.connect(BANCO)
    cursor= conexao.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        turma TEXT,
        tipo TEXT NOT NULL DEFAULT 'publico'
            CHECK (tipo IN ('publico', 'professor', 'coordenador'))
    );

    CREATE TABLE IF NOT EXISTS projeto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT NOT NULL,
        area TEXT NOT NULL,
        tecnologias TEXT,
        usuario_id INTEGER NOT NULL,
        ano INTEGER NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuario(id)
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
    );

    CREATE TABLE IF NOT EXISTS avaliacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        projeto_id INTEGER NOT NULL,
        nota INTEGER NOT NULL CHECK (nota BETWEEN 1 AND 5),
        comentario TEXT,

        FOREIGN KEY (usuario_id) REFERENCES usuario(id)
            ON UPDATE NO ACTION
            ON DELETE NO ACTION,

        FOREIGN KEY (projeto_id) REFERENCES projeto(id)
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
    );

    CREATE TABLE IF NOT EXISTS salas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        andar TEXT NOT NULL,
        capacidade INTEGER NOT NULL,
        tipo TEXT NOT NULL DEFAULT 'sala_aula',
        status TEXT NOT NULL DEFAULT 'ATIVA'
    );

    CREATE TABLE IF NOT EXISTS reservas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sala_id INTEGER NOT NULL,
        usuario_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        horario TEXT NOT NULL,
        motivo TEXT,
        status TEXT NOT NULL DEFAULT 'ativa',

        FOREIGN KEY (sala_id) REFERENCES salas(id)
            ON UPDATE NO ACTION
            ON DELETE NO ACTION,

        FOREIGN KEY (usuario_id) REFERENCES usuario(id)
            ON UPDATE NO ACTION
            ON DELETE NO ACTION,

        UNIQUE (sala_id, data, horario)
    );
    """)
    conexao.commit()
    conexao.close()
        
# ============ USUÁRIOS (5) ============
def inserir_usuario(nome, email, senha_hash, turma, tipo):
    conexao = sqlite3.connect(BANCO)
    cursor= conexao.cursor()
    
    nome=input("Informe seu nome: ")
    email=input("Insira seu e-mail: ")
    senha_hash=input("Digite uma senha: ")
    turma=input("Informe a turma: ")
    tipo=input("Tipo: ")
    cursor.execute(
        """
        INSERT INTO usuarios (nome, email, senha, turma, tipo) VALUES(?,?,?,?,?)
        """,(nome, email, senha_hash, turma, tipo)
    )
    conexao.commit()
    conexao.close()
def buscar_usuario_por_email(email):
    conexao = sqlite3.connect(BANCO)
    cursor=conexao.cursor()

    busca=input("Insira o email: ")

    cursor.execute(
    """
        SELECT * FROM usuarios
        WHERE email = ?
    """,(busca)
    )
    for id, nome, email, turma, tipo in cursor.fetchall():
            print(f"{id} - {nome} - {email} - {turma} - {tipo}")
    conexao.close()

def buscar_usuario_por_id(usuario_id):
    """Retorna usuário (tupla) ou None."""
    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()
    cursor.execute ("""SELECT * FROM usuarios WHERE id = ?""", (usuario_id,))
    usuario = cursor.fetchone()
    conexao.close ()
    return usuario

def listar_usuarios():
    """Lista todos os usuários."""
    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()
    cursor.execute ("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    print(f"Lista de usuários: {usuarios}")
    conexao.close()
    return usuarios


def atualizar_tipo_usuario(usuario_id, novo_tipo):
    """Atualiza o tipo de um usuário."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("UPDATE usuarios SET tipo = ? WHERE id = ?", (novo_tipo, usuario_id))
    conexao.commit()
    conexao.close()
    return atualizar_tipo_usuario

# ============ PROJETOS (7) ============
def inserir_projeto(titulo, descrição, area, tecnologias, usuario_id, ano):
    """Insere projeto. Retorna ID ou None."""
    conexao = conectar()
    cursor = conexao.cursor()
    try:    
        cursor.execute (""" INSERT INTO projeto (titulo, descrição, area, tecnologias, usuario_id, ano)
                VALUES (?,?,?,?,?,?)""", (titulo, descrição, area, tecnologias, usuario_id, ano))
        conexao.commit()
        return cursor.lastrowid
    except Exception as erro:
        print("Erro ao inserir projeto: ", erro)
        return None
    
def buscar_projeto_por_id(projeto_id):
    """Retorna projeto (tupla) ou None."""
    conexao = conectar()
    cursor = conexao.cursor()
    try: 
        sql = cursor.execute(sql, projeto_id)
        return cursor.fetchone()
    except Exception as erro:
        print("Erro ao buscar projeto:", erro)
        return None

def listar_projetos():
    """Lista todos os projetos."""
    conexao = conectar()
    cursor = conexao.cursor()
    try: 
        sql = cursor.execute(sql)
        return cursor.fetchall()
    except Exception as erro:
        print("Erro ao listar projetos:", erro)
        return []

def listar_projetos_por_usuario(usuario_id):
    """Lista projetos de um usuário."""
    conexao = conectar()
    cursor = conexao.cursor()
    try: 
        sql = cursor.execute(sql, usuario_id,)
        return cursor.fetchall
    except Exception as erro:
        print("Erro ao listar projetos do usuario:", erro)
        return []

def atualizar_projeto(projeto_id, titulo, descricao, area, tecnologias, ano):
    """Atualiza dados de um projeto."""
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        sql = cursor.execute (sql, (titulo, descricao, area, tecnologias, ano, projeto_id))
        conexao.commit()
        return cursor.rowcount > 0 
    except Exception as erro:
        print ("Erro ao atualizar projeto:", erro)
        return False


def deletar_projeto(projeto_id):
    """Remove um projeto."""
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        sql = cursor.execute(sql, projeto_id,)
        conexao.commit()
        return cursor.rowcount > 0 
    except Exception as erro:
        print ("Erro ao deletar projeto:", erro)
        return False

def buscar_projetos_por_termo(termo):
    """Busca por título OU tecnologia (LIKE)."""
    conexao = conectar()
    cursor = conexao.cursor()
    try: 
        sql = busca = f"%{termo}%"
        cursor.execute(sql, busca, busca)
        return cursor.fetchall()
    except Exception as erro:
        print ("Erro ao buscar projetos:", erro)
        return []



# ============ AVALIAÇÕES (5) ============
def inserir_avaliacao(usuario_id, projeto_id, nota, comentario):
    """Insere avaliação. Retorna True/False."""
    if ja_avaliou(usuario_id, projeto_id):
        return False

    if not 1 <= nota <= 5:
        return False

    try:
        conexao= conectar ()
        cursor= conexao.cursor ()

        cursor.execute("""
            INSERT INTO avaliacoes
            (usuario_id, projeto_id, nota, comentario)
            VALUES (?, ?, ?, ?)
        """, (usuario_id, projeto_id, nota, comentario))

        conexao.commit()
        conexao.close()

        return True

    except sqlite3.Error:
        return False


def listar_avaliacoes_projeto(projeto_id):
    """Lista avaliações de um projeto."""
    conexao= conectar()
    cursor= conexao.cursor()

    cursor.execute("""
        SELECT usuario_id, nota, comentario
        FROM avaliacoes
        WHERE projeto_id = ?
        ORDER BY rowid DESC
    """, (projeto_id,))

    avaliacoes = cursor.fetchall()
    conexao.close()

    return avaliacoes


def ja_avaliou(usuario_id, projeto_id):
    """Verifica se o usuário já avaliou."""
    conexao= conectar()
    cursor= conexao.cursor()

    cursor.execute("""
        SELECT 1
        FROM avaliacoes
        WHERE usuario_id = ? AND projeto_id = ?
        LIMIT 1
    """, (usuario_id, projeto_id))

    resultado= cursor.fetchone()
    conexao.close()

    return resultado is not None


def media_projeto(projeto_id):
    """Retorna média das notas (float) ou 0."""
    conexao= conectar()
    cursor= conexao.cursor()

    cursor.execute("""
        SELECT AVG(nota)
        FROM avaliacoes
        WHERE projeto_id = ?
    """, (projeto_id,))

    media= cursor.fetchone()[0]
    conexao.close()

    return float(media) if media is not None else 0.0


def ranking_projetos(limite=10):
    """Retorna top N projetos por média."""
    conexao= conectar()
    cursor= conexao.cursor()

    cursor.execute("""
        SELECT projeto_id, AVG(nota) AS media, COUNT(*) AS quantidade
        FROM avaliacoes
        GROUP BY projeto_id
        ORDER BY media DESC
        LIMIT ?
    """, (limite,))

    ranking= cursor.fetchall()
    conexao.close()

    return ranking

# ============ SALAS (5) ============
def inserir_sala(nome, andar, capacidade, tipo):
    """Insere nova sala (coordenador)."""
    conexao = sqlite3.connect(BANCO)
    cursor= conexao.cursor()
    for nome, andar, capacidade, tipo in cursor.fetchall():
        if inserir_sala=="coordenador":
            us=("Usuário: ")
            nome=input("Nome: ")
            andar=input("Andar: ")
            cap=input("Capacidade: ")
            tipo=input("Tipo: ")
            break
        else:
            print("Usuário não autorizado")
    cursor.execute(
        """
        INSERT INTO sala (nome, andar, capacidade, tipo) VALUES(?,?,?,?)
        """,(nome, andar, capacidade, tipo)
    )

    conexao.commit()
    conexao.close()

def buscar_sala_por_id():
    """Retorna dados de uma sala."""
    conexao = sqlite3.connect(BANCO)
    cursor=conexao.cursor()

    busca=input("Insira a sala: ")

    cursor.execute(
    """
        SELECT * FROM salas
        WHERE nome = ?
    """,(busca,)
    )
    for id, nome, andar, capacidade, tipo, ativa in cursor.fetchall():
            print(f"ID de Sala:{id}\n - Nome: {nome}\n - Andar: {andar}\n - Capacidade: {capacidade}\n - Tipo: {tipo}\n - Status: {ativa}")
    conexao.close()


def listar_salas():
    """Lista todas as salas ativas."""
    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()
    cursor.execute ("SELECT * FROM sala")
    sala = cursor.fetchall()
    conexao.close()
    return sala

def listar_salas_por_andar(andar):
    """Lista salas de um andar."""
    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()
    cursor.execute ("""SELECT * FROM sala""")
    sala = cursor.fetchall()
    conexao.close()
    return sala

def desativar_sala(sala_id):
    """Marca sala como inativa."""
    conexao = conectar()
    cursor=conexao.cursor()

    busca=input("Desativar sala(ID): ")
    cursor.execute("""
        DELETE FROM sala
        WHERE id =?
    """, (busca,))
    conexao.commit()
    conexao.close()


# ============ RESERVAS (6) ============
def inserir_reserva(sala_id, usuario_id, data, horario, motivo):
    conexao=sqlite3.connect(BANCO)
    cursor=conexao.cursor()

    sala_id=input("Sala Id: ")
    usuario_id=input("Usario Id: ")
    data=input("Data: ")
    horario=input("Horario: ")
    motivo=input("Motivo: ")

    cursor.execute(
        """
        INSERT INTO reserva (sala_id, usuario_id, data, horario, motivo) VALUES (?,?,?,?,?)
        """,(sala_id, usuario_id, data, horario, motivo)
    )

    conexao.commit()
    conexao.close()
    

  

def verificar_disponibilidade(sala_id, data, horario):
    """Verifica se está livre. Retorna True/False."""
    conexao = conectar()
    try:
        with conexao.cursor() as cursor:
            # Conta quantas reservas já existem para a mesma sala, data e horário
            query = """
                SELECT COUNT(*) 
                FROM reservas 
                WHERE sala_id = ? AND data = ? AND horario = ?
            """
            cursor.execute(query, (sala_id, data, horario))
            resultado = cursor.fetchone()
            
            # Se o contador for 0, a sala está disponível (retorna True)
            return resultado[0] == 0
    finally:
        conexao.close()

def menu_consulta():
    conexao=conectar()
    cursor=conexao.cursor()
    while True:
        print("\n" + "*" * 40)
        print("CONSULTA DE DISPONIBILIDADE DE SALAS")
        print("*" * 40)
        print("1. Verificar se uma sala específica está livre")
        print("0. Voltar")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "0":
            break
        elif opcao == "1":
            sala_id = input("Digite o ID da sala: ")
            cursor.execute(
                    """
                    SELECT *  FROM salas
                    where id = ?
                    """, (int(sala_id),)
            )
            for id, nome, andar, capacidade, tipo, ativa in cursor.fetchall():
                print(f"ID de Sala:{id}\n - Nome: {nome}\n - Andar: {andar}\n - Capacidade: {capacidade}\n - Tipo: {tipo}\n - Status: {"Vazio" if ativa==0 else "Preenchida"}")
            conexao.close()



def listar_reservas_usuario(usuario_id):
    """Lista reservas ativas de um usuário."""

def listar_reservas_usuario(usuario_id):
 
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT id, data_reserva, status 
        FROM reservas 
        WHERE usuario_id = ? AND status = 'ativo'
        """, 
        (usuario_id,)
    )
                
        
    resultado = cursor.fetchall() 
    
    conexao.close()

    return resultado

def listar_reservas_por_data(data):
    """Lista reservas de uma data."""
    conexao = conectar()
    cursor = conexao.cursor()
    
   
    cursor.execute("""
    SELECT id, data_reserva, status FROM reservas WHERE data_id = ? AND status ='ativo'
    """, (data_id,)),

    resultado = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return resultado


def listar_todas_reservas():
    """Lista todas as reservas (coordenador)."""
 
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute ("""SELECT * FROM reserva""",(data, horario, motivo,status ))

    listar_todas_reservas=cursor.resultado()
    conexao.close()

    return todas_reservas

    conexao.commit()
    conexao.close()


def cancelar_reserva(reserva_id):
    """Muda status para 'cancelada'."""
    pass


def inserir_dados_iniciais():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO usuarios (id, nome, email, senha, turma, tipo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            1,
            'Coordenador Padrão',
            'admin@qualifica.com',
            'hash_admin',
            None,
            'coordenador'
        ))

        cursor.execute("""
            INSERT INTO salas (nome, andar, capacidade, tipo) VALUES
                ('Sala 101', 1, 30, 'sala_aula'),
                ('Sala 102', 1, 30, 'sala_aula'),
                ('Sala 103', 1, 20, 'laboratorio'),
                ('Sala 201', 2, 40, 'sala_aula'),
                ('Sala 202', 2, 25, 'laboratorio'),
                ('Sala 203', 2, 30, 'sala_aula'),
                ('Sala 301', 3, 50, 'auditorio'),
                ('Sala 302', 3, 30, 'sala_aula'),
                ('Sala 401', 4, 100, 'auditorio'),
                ('Sala 402', 4, 25, 'reuniao')
        """)

        conexao.commit()
        print("Dados iniciais inseridos com sucesso!")

    except Exception as e:
        conexao.rollback()
        print("ERRO AO INSERIR DADOS:", e)

    finally:
        conexao.close()


def inserir_dados_teste():
    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor()

    try:
        # Usuários
        cursor.executemany("""
            INSERT OR IGNORE INTO usuarios
            (id, nome, email, senha, turma, tipo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            (
                1,
                'Coordenador Padrão',
                'admin@qualifica.com',
                '123456',
                None,
                'coordenador'
            ),
            (
                2,
                'João Silva',
                'joao@qualifica.com',
                '123456',
                'Turma A',
                'professor'
            ),
            (
                3,
                'Maria Santos',
                'maria@qualifica.com',
                '123456',
                'Turma A',
                'publico'
            ),
            (
                4,
                'Pedro Oliveira',
                'pedro@qualifica.com',
                '123456',
                'Turma B',
                'publico'
            )
        ])

        # Projetos
        cursor.executemany("""
            INSERT OR IGNORE INTO projeto
            (id, titulo, descricao, area, tecnologias, usuario_id, ano)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [
            (
                1,
                'Sistema de Biblioteca',
                'Sistema para gerenciamento de livros e empréstimos.',
                'Tecnologia',
                'Python, SQLite, Flask',
                3,
                2026
            ),
            (
                2,
                'Aplicativo Educacional',
                'Aplicativo para auxiliar alunos nos estudos.',
                'Educação',
                'Python, JavaScript, HTML, CSS',
                4,
                2026
            ),
            (
                3,
                'Controle de Estoque',
                'Sistema para controle de produtos e estoque.',
                'Administração',
                'Python, SQLite',
                3,
                2026
            )
        ])

        # Avaliações
        cursor.executemany("""
            INSERT OR IGNORE INTO avaliacoes
            (id, usuario_id, projeto_id, nota, comentario)
            VALUES (?, ?, ?, ?, ?)
        """, [
            (
                1,
                2,
                1,
                5,
                'Excelente projeto e muito bem organizado.'
            ),
            (
                2,
                2,
                2,
                4,
                'Boa ideia e apresentação.'
            ),
            (
                3,
                3,
                3,
                5,
                'Projeto muito útil.'
            )
        ])

        # Salas
        cursor.executemany("""
            INSERT OR IGNORE INTO salas
            (id, nome, andar, capacidade, tipo, ativa)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            (1, 'Sala 101', 1, 30, 'sala_aula', 1),
            (2, 'Sala 102', 1, 30, 'sala_aula', 1),
            (3, 'Laboratório 103', 1, 20, 'laboratorio', 1),
            (4, 'Sala 201', 2, 40, 'sala_aula', 1),
            (5, 'Laboratório 202', 2, 25, 'laboratorio', 1),
            (6, 'Auditório 301', 3, 50, 'auditorio', 1)
        ])

        # Reservas
        cursor.executemany("""
            INSERT OR IGNORE INTO reservas
            (id, sala_id, usuario_id, data, horario, motivo, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [
            (
                1,
                1,
                1,
                '2026-10-01',
                '08:00-10:00',
                'Aula de programação',
                'ativa'
            ),
            (
                2,
                3,
                2,
                '2026-10-01',
                '14:00-16:00',
                'Aula prática de Python',
                'ativa'
            ),
            (
                3,
                6,
                1,
                '2026-10-05',
                '18:00-20:00',
                'Apresentação de projetos',
                'ativa'
            )
        ])

        conexao.commit()
        print("Dados de teste inseridos com sucesso!")

    except Exception as erro:
        conexao.rollback()
        print("Erro ao inserir dados de teste:", erro)

    finally:
        conexao.close()

criar_banco()
inserir_dados_teste()

