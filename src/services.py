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
    pass
def obter_grade_horarios(sala_id, data):
    """Retorna lista de dicts com horários e status."""
    pass
# ============ RESERVAS (3) ============
def reservar_sala(usuario_id, sala_id, data, horario, motivo):
    """Cria reserva. Retorna (sucesso, mensagem)."""
    pass
def cancelar_reserva(reserva_id, usuario_id, tipo_usuario):
    """Cancela reserva (dono ou coordenador)."""
    pass
def listar_minhas_reservas(usuario_id):
    """Lista reservas ativas do usuário."""
    pass
# ============ RELATÓRIOS (1) ============
def exportar_csv():
    """Exporta projetos e reservas para CSV."""
    pass