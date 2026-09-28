# src/menus.py
"""Todos os menus e interação com o usuário."""
from services import *
from models import Sistema
from config import AREAS_PROJETO, HORARIOS, ANDARES
# ============ AUXILIARES (4) ============
def limpar_tela():
    """Limpa o terminal."""
    pass

def titulo(texto):
    """Exibe título formatado."""
    pass

def linha(tamanho=60):
    """Exibe linha separadora."""
    pass

def mensagem(tipo, texto):
    """Exibe mensagem (tipo: 'sucesso', 'erro', 'aviso')."""
    pass

# ============ MENU PRINCIPAL (3) ============
def menu_principal(sistema):
    """Menu inicial do sistema."""
    pass

def menu_visitante():
    """Menu para quem não fez login."""
    pass

def menu_buscar_publico():
    """Busca pública de projetos."""
    pass

# ============ LOGIN / CADASTRO (2) ============
def menu_cadastro():
    """Fluxo de cadastro de usuário."""
    pass

def menu_login(sistema):
    """Fluxo de login."""
    pass

# ============ MENUS POR TIPO (3) ============
def menu_publico(sistema):
    """Menu do usuário público logado."""
    pass

def menu_professor(sistema):
    """Menu do professor."""
    pass

def menu_coordenador(sistema):
    """Menu do coordenador."""
    pass
# ============ PROJETOS (3) ============
def menu_cadastrar_projeto(sistema):
    """Fluxo de cadastro de projeto."""
    pass

def menu_meus_projetos(sistema):
    """Lista projetos do usuário."""
    pass

def menu_avaliar(sistema):
    """Fluxo de avaliação."""
    pass

# ============ SALAS (2) ============
def menu_ver_salas():
    """Mostra salas agrupadas por andar."""
    pass

def menu_grade_sala():
    """Mostra grade de horários."""
    pass

# ============ RESERVAS (3) ============
def menu_reservar_sala(sistema):
    """Fluxo de reserva."""
    pass

def menu_minhas_reservas(sistema):
    """Lista reservas do usuário."""
    pass

def menu_cancelar_reserva(sistema):
    """Cancela reserva."""
    pass

# ============ COORDENADOR (2) ============
def menu_gerenciar_salas(sistema):
    """Cadastrar / desativar salas."""
    pass

def menu_todas_reservas(sistema):
    """Ver todas as reservas."""
    pass

# ============ RELATÓRIOS (1) ============
def menu_relatorios(sistema):
    """Exportar CSV."""
    pass