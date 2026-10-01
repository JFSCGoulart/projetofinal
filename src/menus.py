# src/menus.py
"""Todos os menus e interação com o usuário."""
from services import *
from models import Sistema
from config import AREAS_PROJETO, HORARIOS, ANDARES
import os
# ============ AUXILIARES (4) ============
def limpar_tela():
    """Limpa o terminal."""
    os.system("cls" if os.name == "nt" else "clear")
    
def titulo(texto):
    """Exibe título formatado."""
    linha()
    print(texto.center(60))
    linha()
    

def linha(tamanho=60):
    """Gera uma linha horizontal com o tamanho especificado."""
    print("-" * tamanho)

# Testando a função
    linha()         # Usa o valor padrão (60 traços)
    linha(30)        # Usa um tamanho personalizado (30 traços)


def mensagem(tipo, texto):
    """Exibe mensagem (tipo: 'sucesso', 'erro', 'aviso')."""
    icones = {"sucesso": "[OK] ", "erro": "[ERRO] ", "aviso": "[!] "}
    print(f"{icones.get(tipo, '')}{texto}")
    pass

# ============ MENU PRINCIPAL (3) ============
def menu_principal(sistema):
    """Menu inicial do sistema."""
    while True:
        limpar_tela()
        titulo("SISTEMA DE PROJETOS E RESERVAS")
        print("1 - Login")
        print("2 - Cadastro")
        print("3 - Buscar projetos (público)")
        print("4 - Ver salas")
        print("5 - Ranking de projetos")
        print("0 - Sair")
        op = input("Escolha: ").strip()

        match op:
            case "1":
                menu_login(sistema)
            case "2":
                menu_cadastro()
            case "3":
                menu_buscar_publico()
            case "4":
                menu_ver_salas()
            case "5":
                ranking_projetos()
            case "0":
                mensagem("aviso", "Saindo...")
                break
            case _:
                mensagem("erro", "Opção inválida.")
                
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