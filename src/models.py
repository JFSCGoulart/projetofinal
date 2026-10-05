"""Modelo de sessão do sistema."""


class Sistema:
    """Guarda o estado da sessão (usuário logado)."""

    def __init__(self):
        self.usuario_logado = None

    def login(self, usuario):
        self.usuario_logado = usuario

    def logout(self):
        self.usuario_logado = None