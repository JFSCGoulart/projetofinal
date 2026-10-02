# src/menus.py
"""Todos os menus e interação com o usuário."""
from . import services
from .models import Sistema
from .config import AREAS_PROJETO, HORARIOS, ANDARES
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

    while True:
    print("\n--- MENU PÚBLICO ---")
    print("consultar projetos")
    print("buscar por área/tecnologia")
    print("ver rancking dos projetos")
    print("consultar salas por andar")
    print("voltar")
    op=input("escolha  uma opção:")

# ============ LOGIN / CADASTRO (2) ============

def menu_cadastro():
    print("\n===== CADASTRO =====")
    nome = input("Digite seu nome: ")
    usuario = input("Digite seu usuário: ")
    senha = input("Digite sua senha: ")
    tipo = input("Digite o tipo (publico/professor/coordenador): ")

    cadastro = {
        "nome": nome,
        "usuario": usuario,
        "senha": senha,
        "tipo": tipo
    }

    print("\nCadastro realizado com sucesso!")
    return cadastro


def menu_login(sistema):
    print("\n===== LOGIN =====")
    usuario = input("Digite seu usuário: ")
    senha = input("Digite sua senha: ")

    if usuario == sistema["usuario"] and senha == sistema["senha"]:
        print("\nLogin realizado com sucesso!")
        print("Bem-vindo,", sistema["nome"])

        if sistema["tipo"] == "publico":
            return menu_publico(sistema)

        elif sistema["tipo"] == "professor":
            return menu_professor(sistema)

        elif sistema["tipo"] == "coordenador":
            return menu_coordenador(sistema)

    else:
        print("\nUsuário ou senha incorretos!")
        return None



# ============ MENUS POR TIPO (3) ============
def menu_publico( sistema):
    opcoes = [
        "1- CONSULTAR SALAS"
        "2- VER PROJETOS",
        "3- RAKING DOS PROJETOS",
        "4- FAZER LOGIN"
    ]
    return opcoes

def menu_professor(sistema):
    opcoes =[ 
        "1- VER ALUNOS",
        "2- REGISTRAR NOTAS",
        "3- REGISTRAR FREQUENCIAS"
    ]
    return opcoes

def menu_coordenador(sistema):
    opcoes =[
        "1- VER PROFESSORES",
        "2- VER ALUNOS",
        "3- GERAR RELATORIOS"
    ]
    return opcoes
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
def menu_cadastrar_projeto(sistema):
    """Fluxo de cadastro de projeto."""

    projeto = {}

    projeto= input("Nome do projeto: ")
    projeto= input("Descrição do projeto: ")
    projeto= input("Categoria: ")

    sistema["projetos"].append(projeto)

    print("\nProjeto cadastrado com sucesso!")


def menu_meus_projetos(sistema):
    """Lista projetos do usuário."""

    projetos = sistema["projetos"]

    if not projetos:
        print("\nNenhum projeto cadastrado.")
        return

    print("\n===== MEUS PROJETOS =====")

    for i, projeto in enumerate(projetos, 1):
        print(f"\n{i}. {projeto['nome']}")
        print(f"   Descrição: {projeto['descricao']}")
        print(f"   Categoria: {projeto['categoria']}")


def menu_avaliar(sistema):
    """Fluxo de avaliação."""

    projetos = sistema["projetos"]

    if not projetos:
        print("\n Nenhum projeto para avaliar.")
        return

    print("\n===== PROJETOS PARA AVALIAR =====")

    for i, projeto in enumerate(projetos, 1):
        print(f"{i}. {projeto['nome']}")

    escolha = int(input("\nEscolha o projeto: "))

    if 1 <= escolha <= len(projetos):
        nota = float(input("Digite a nota de 0 a 10: "))
        projetos[escolha - 1]["nota"] = nota
        print("Avaliação registrada!")
    else:
        print("Projeto inválido.")

########################################################################

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
