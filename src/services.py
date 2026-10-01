"""Regras de negócio do sistema."""
import hashlib
import csv
from datetime import datetime
from banco import *
from config import *
import re
# ============ SEGURANÇA E VALIDAÇÕES (6) ============
def gerar_hash(senha_digitada):
    #Gera hash SHA-256 codifica em utf e retorna uma hash em forma hexadecimal.

    from hashlib import sha256
    s_codidifcada = senha_digitada.encode("utf-8")
    hash_salvo = hashlib.sha256(s_cod).hexdigest()
    return hash_salvo

    pass
def verificar_senha(senha_digitada, hash_salvo):
    #Verifica se a senha corresponde ao hash do banco.
    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor

    cursor.execute(""" SELECT senha FROM usuarios
    """)
    
    for cod in cursor.fetchall():
        if cod==gerar_hash(senha_digitada):
            print("Senha correta!")
            return True
        else:
            print("Senha inválida!")
            return False
    conexao.close()
    pass
def validar_email(email):
    """Valida formato do email. Retorna (bool, msg)."""
    email = email.strip()

    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not email:
        return False, "O e-mail não pode estar vazio!"

    elif re.match(padrao, email):
        return True, "E-mail válido."

    else:
        return False, "Formato de e-mail inválido. Insira uma e-mail conforme o exemplo correto: 'nome@email.com' "
        
def validar_senha(senha_digitada):
    """Valida tamanho mínimo. Retorna (bool, msg)."""

    senha_formatada = senha_digitada.strip()

    if not senha_formatada:
        print("Campo da senha vazio!")
        return False
    if len(senha_formatada) < 8:
        print("A senha deve conter no mínimo 8 caracteres.")
        return False
    else:
        return True, "Senha válida"
    
    pass
def validar_data(data):
    """Valida formato DD/MM/AAAA. Retorna (bool, msg)."""

    data_formatada = data.strip()
    try:
        datetime.strptime(data_formatada, "%d/%m/%Y")
        return True, "Data válida."

    except ValueError:
        return False, "Data inválida. Use o formato DD/MM/AAAA ex: 30/09/2026."
    pass

def validar_campo(valor, nome_campo):
    """Valida se campo não está vazio."""
    
    if valor is None or (isinstance(valor, str) and not valor.strip()):
            print(f"O campo '{nome_campo}' não pode estar vazio.")
    pass
# ============ AUTENTICAÇÃO (2) ============
def cadastrar_usuario(nome, email, senha, turma, tipo="publico"):
    """Cadastra usuário. Retorna (sucesso, mensagem)."""
    nome = input("Informe seu nome e sobre-nome:")
    email = input("Informe seu e-mail:")
    senha = input()
    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor

    cursor.execute(""" INSERT INTO usuarios 
    """)


    pass
def fazer_login(email, senha):
    """Realiza login. Retorna (usuario, mensagem)."""
    pass
# ============ PROJETOS (5) ============
def cadastrar_projeto(titulo, descricao, area, tecnologias, usuario_id, ano):
    """Cadastra projeto. Retorna (sucesso, mensagem)."""
    conexao = conectar()

    cursor= conexao.cursor()
    descricao=input("descricao: ")
    area=input("area: ")
    tecnologias=input("tecnologias: ")
    usuario_id=input("usuario_id: ")
    ano=input("ano: ")
    cursor.execute(
        """
        INSERT INTO projetos (titulo, descricao, area, tecnologias, usuario_id, ano) VALUES(?,?,?,?,?,?)
        """,(titulo, descricao, area, tecnologias, usuario_id, ano)
    )
    conexao.commit()
    conexao.close()

    pass
def remover_projeto(projeto_id, usuario_id, tipo_usuario):
    """Remove projeto (dono ou coordenador)."""
    conexao = conectar()
    cursor=conexao.cursor()

    busca=input("Insira o ID do projeto: ")
    busca=input("Insira o ID do usuario: ")
    busca=input("Insira o tipo_usuario: ")

    cursor.execute("""
        DELETE FROM projetos
        WHERE projeto_id=? and usuario_id=? and tipo_usuario=?
    """, (busca, busca, busca))
    conexao.commit()
    conexao.close()

    pass
def buscar_projetos(termo=None, area=None):
    """Busca projetos combinando filtros."""
    conexao = conectar()
    cursor=conexao.cursor()
    busca=input("Insira o ano: ")
    area=input("Insira o area: ")

    cursor.execute(
    """
        SELECT * FROM projetos
        WHERE area = ? And ano = ?
    """,(busca, area)
    )
    for titulo, descricao, area, tecnologias, usuario_id, ano in cursor.fetchall():
            print(f"{titulo} - {descricao} - {area} - {tecnologias} - {usuario_id} - {ano}")
    conexao.close()
    
    pass
def obter_detalhes_projeto(projeto_id):
    """Retorna detalhes formatados de um projeto."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute ("SELECT * FROM projeto WHERE id = ?", (projeto_id,))
    projeto = cursor.fetchone()
    conexao.close ()
    return projeto
    pass

def obter_ranking(limite=10):
    """Retorna top N projetos com médias."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
            SELECT
                p.id,
                p.titulo AS projeto,
                u.nome AS autor,
                COUNT(a.id) AS total_avaliacoes,
                ROUND(AVG(a.nota), 2) AS media_notas

            FROM projeto p

            INNER JOIN usuarios u
                ON p.usuario_id = u.id

            INNER JOIN avaliacoes a
                ON p.id = a.projeto_id

            GROUP BY
                p.id,
                p.titulo,
                u.nome

            ORDER BY
                media_notas DESC,
                total_avaliacoes DESC;
        """)
    conexao.close ()
    return projeto
    pass
# ============ AVALIAÇÕES (1) ============
def avaliar_projeto(usuario_id, projeto_id, nota, comentario):
    """Registra avaliação. Retorna (sucesso, mensagem)."""
    conexao = conectar()
    cursor = conexao.cursor()

    if not isinstance(nota, int) or isinstance(nota, bool):
        return False, "A nota deve ser um número inteiro."

    if not 1 <= nota <= 5:
        return False, "A nota deve estar entre 1 e 5."

    try:
        with conectar() as conexao:
            conexao.execute("PRAGMA foreign_keys = ON")
            cursor = conexao.cursor()

            # Verifica se o usuário existe
            cursor.execute(
                "SELECT id FROM usuarios WHERE id = ?",
                (usuario_id,)
            )

            if cursor.fetchone() is None:
                return False, "Usuário não encontrado."

            # Verifica se o projeto existe
            cursor.execute(
                "SELECT id FROM projeto WHERE id = ?",
                (projeto_id,)
            )

            if cursor.fetchone() is None:
                return False, "Projeto não encontrado."

            # Registra a avaliação
            cursor.execute("""
                INSERT INTO avaliacoes
                    (usuario_id, projeto_id, nota, comentario)
                VALUES (?, ?, ?, ?)
            """, (usuario_id, projeto_id, nota, comentario))

            conexao.commit()

            return True, "Avaliação registrada com sucesso!"

    except sqlite3.Error as erro:
        return False, f"Erro ao registrar avaliação: {erro}"

    pass
# ============ SALAS (4) ============
def listar_salas_agrupadas():
    """Retorna salas agrupadas por andar."""
    pass
def cadastrar_sala(nome, andar, capacidade, tipo):
    """Cadastra nova sala (coordenador)."""
    pass
def desativar_sala(sala_id):
    """Desativa sala (coordenador)."""
    conexao = sqlite3.connect(BANCO)
    cursor = conexao.cursor
    
    cursor.execute(""" comando para selecionar cordenador


    """)
    confirmacao = input(f"Deseja realmente desativa a seguinte sala: {sala_id}???\nDigite SIM ou NÃO: ").upper()
    
    if confirmacao == "SIM":
        cursor.execute("""
            UPDATE salas
            SET = "DESATIVADA"
            WHERE status = "ATIVA"
            """)
        conexao.commit()
        conexao.close()    
    else:
        print("Nenhuma ateração realizada.")
        conexao.close()
    pass
def obter_grade_horarios(sala_id, data):
    """Retorna lista de dicts com horários e status."""
    pass
# ============ RESERVAS (3) ============
from src.banco import conectar
def reservar_sala(usuario_id, sala_id, data, horario, motivo):
    """Cria reserva. Retorna (sucesso, mensagem)."""

    conexao = conectar()
    cursor = conexao.cursor()

    #verifica se a sala existe e está ativa
    cursor.execute("""
        SELECT id
        FROM salas
        WHERE id = ? AND status = 'ATIVA'
    """, (sala_id,))

    sala = cursor.fetchone()

    if sala is None:
        conexao.close()
        return False, "Sala não encontrada ou está inativa."

    #verifica se já existe reserva para a sala naquele horário
    cursor.execute("""
        SELECT id
        FROM reservas
        WHERE sala_id = ?
        AND data = ?
        AND horario = ?
        AND status = 'ativa'
    """, (sala_id, data, horario))

    reserva_existente = cursor.fetchone()

    if reserva_existente is not None:
        conexao.close()
        return False, "A sala já está reservada nesse horário."

    #cria a reserva
    cursor.execute("""
        INSERT INTO reservas
        (sala_id, usuario_id, data, horario, motivo)
        VALUES (?, ?, ?, ?, ?)
    """, (sala_id, usuario_id, data, horario, motivo))

    conexao.commit()
    conexao.close()

    return True, "Reserva realizada com sucesso."

    
def cancelar_reserva(reserva_id, usuario_id, tipo_usuario):
    """Cancela reserva (dono ou coordenador)."""

    conexao = conectar()
    cursor = conexao.cursor()

    #procura a reserva
    cursor.execute("""
        SELECT usuario_id, status
        FROM reservas
        WHERE id = ?
    """, (reserva_id,))

    reserva = cursor.fetchone()

    if reserva is None:
        conexao.close()
        return False, "Reserva não encontrada."

    dono_id = reserva[0]
    status = reserva[1]

    #verifica se já está cancelada
    if status != "ativa":
        conexao.close()
        return False, "Essa reserva já foi cancelada."

    #verifica permissão
    if dono_id != usuario_id and tipo_usuario != "coordenador":
        conexao.close()
        return False, "Você não tem permissão para cancelar esta reserva."

    #cancela
    cursor.execute("""
        UPDATE reservas
        SET status = 'cancelada'
        WHERE id = ?
    """, (reserva_id,))

    conexao.commit()
    conexao.close()

    return True, "Reserva cancelada com sucesso."



def listar_minhas_reservas(usuario_id):
    """Lista reservas ativas do usuário."""

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            reservas.id,
            salas.nome,
            salas.andar,
            reservas.data,
            reservas.horario,
            reservas.motivo
        FROM reservas
        JOIN salas ON salas.id = reservas.sala_id
        WHERE reservas.usuario_id = ?
        AND reservas.status = 'ativa'
        ORDER BY reservas.data, reservas.horario
    """, (usuario_id,))

    reservas = cursor.fetchall()

    conexao.close()

    return reservas




# ============ RELATÓRIOS (1) ============
def exportar_csv():
    """Exporta projetos e reservas para CSV."""
    pass