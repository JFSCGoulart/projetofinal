"""Ponto de entrada do Qualifica Hub."""
from src.banco import criar_banco, inserir_dados_teste
from src.models import Sistema
from src.menus import menu_principal


def main():
    criar_banco()
    inserir_dados_teste()
    sistema = Sistema()
    menu_principal(sistema)


if __name__ == "__main__":
    main()