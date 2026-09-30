# src/services.py
"""Regras de negócio do sistema."""
import hashlib
import csv
from datetime import datetime
from banco import *
from config import *
# ============ SEGURANÇA E VALIDAÇÕES (6) ============
def gerar_hash(senha_digitada):
    """Gera hash SHA-256 da senha."""

    from hashlib import sha256
    s_cod = senha_digitada.encode("utf-8")
    hash_salvo = hashlib.sha256(s_cod).hexdigest()


    pass
def verificar_senha(senha_digitada, hash_salvo):
    """Verifica se a senha corresponde ao hash."""
    
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
        return False, "Formato de e-mail inválido. Exemplo correto: nome@email.com"
def validar_senha(senha):
    """Valida tamanho mínimo. Retorna (bool, msg)."""
    pass
def validar_data(data):
    """Valida formato DD/MM/AAAA. Retorna (bool, msg)."""
    pass
def validar_campo(valor, nome_campo):
    """Valida se campo não está vazio."""
    pass
# ============ AUTENTICAÇÃO (2) ============
def cadastrar_usuario(nome, email, senha, turma, tipo="publico"):
    """Cadastra usuário. Retorna (sucesso, mensagem)."""
    pass
def fazer_login(email, senha):
    """Realiza login. Retorna (usuario, mensagem)."""
    pass
# ============ PROJETOS (5) ============
def cadastrar_projeto(titulo, descricao, area, tecnologias, usuario_id, ano):
    """Cadastra projeto. Retorna (sucesso, mensagem)."""
    pass
def remover_projeto(projeto_id, usuario_id, tipo_usuario):
    """Remove projeto (dono ou coordenador)."""
    pass
def buscar_projetos(termo=None, area=None):
    """Busca projetos combinando filtros."""
    pass
def obter_detalhes_projeto(projeto_id):
    """Retorna detalhes formatados de um projeto."""
    pass
def obter_ranking(limite=10):
    """Retorna top N projetos com médias."""
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