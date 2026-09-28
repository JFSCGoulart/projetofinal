# main.py
"""Ponto de entrada do Qualifica Hub."""
from src.banco import criar_banco
from src.models import Sistema
from src.menus import menu_principal
def main():
"""Função principal."""
    criar_banco()
    sistema = Sistema()
    menu_principal(sistema)
if __name__ == "__main__":
    main()