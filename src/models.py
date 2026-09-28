# src/models.py
"""Classes de modelo do sistema."""
class Usuario:
        """Representa um usuário do sistema."""
<<<<<<< HEAD
def __init__(self, id, nome, email, senha, turma, tipo):

        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha          
        self.turma = turma
        self.tipo = tipo
def pode_avaliar(self):
        """Professor e coordenador podem avaliar."""
        return self.tipo in ["professor", "coordenador"]
def pode_reservar(self):
        """Professor e coordenador podem reservar."""
        return self.tipo in ["professor", "coordenador"]
def pode_gerenciar(self):
        """Somente coordenador pode gerenciar."""
        return self.tipo == "coordenador"
def __str__(self):
        return f"{self.nome} ({self.tipo})"
class Projeto:
        """Representa um projeto final."""
def __init__(self, id, titulo, descricao, area, tecnologias, usuario_id, ano):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.area = area
        self.tecnologias = tecnologias
        self.usuario_id = usuario_id
        self.ano = ano
def __str__(self):
        return f"[{self.id}] {self.titulo} ({self.area}, {self.ano})"
class Avaliacao:
        """Representa uma avaliação de projeto."""
def __init__(self, id, usuario_id, projeto_id, nota, comentario):
        self.id = id
        self.usuario_id = usuario_id
        self.projeto_id = projeto_id
        self.nota = nota
        self.comentario = comentario
def __str__(self):
        return f"Nota {self.nota}/5 - {self.comentario[:30]}"
class Sala:
        """Representa uma sala física."""
def __init__(self, id, curso, andar, capacidade, turno, ativa=1):
        self.id = id
        self.curso = curso
        self.andar = andar
        self.capacidade = capacidade
        self.turno = turno
        self.ativa = ativa
def __str__(self):
        return f"{self.nome} - {self.capacidade} lugares ({self.tipo})"
class Reserva:
        """Representa uma reserva de sala."""
def __init__(self, id, sala_id, usuario_id, data, horario, motivo, status, turno):
        self.id = id
        self.sala_id = sala_id
        self.usuario_id = usuario_id
        self.data = data
        self.horario = horario
        self.motivo = motivo
        self.status = status
        self.turno = turno
def __str__(self):
        return f"Reserva #{self.id} - {self.data} {self.horario}"
class Sistema:
        """Gerencia o estado da aplicação (usuário logado)."""
def __init__(self):
        self.usuario_logado = None
def esta_logado(self):
        """Retorna True se há usuário logado."""
        return self.usuario_logado is not None
def login(self, usuario):
        """Define o usuário logado."""
        self.usuario_logado = usuario
def logout(self):
        """Encerra a sessão."""
        self.usuario_logado = None
=======
        def __init__(self, id, nome, email, senha, turma, tipo):
                self.id = id
                self.nome = nome
                self.email = email
                self.senha = senha          
                self.turma = turma
                self.tipo = tipo

        def pode_avaliar(self):
                # Sem encapsulamento
                """Professor e coordenador podem avaliar."""
                return self.tipo in ["professor", "coordenador"]
        
        def pode_reservar(self):
                """Professor e coordenador podem reservar."""
                return self.tipo in ["professor", "coordenador"]
        
        def pode_gerenciar(self):
                """Somente coordenador pode gerenciar."""
                return self.tipo == "coordenador"
        
        def __str__(self):
                return f"{self.nome} ({self.tipo})"
        
class Projeto:
        """Representa um projeto final."""
        def __init__(self, id, titulo, descricao, area, tecnologias, usuario_id):
                self.id = id
                self.titulo = titulo
                self.descricao = descricao
                self.area = area
                self.tecnologias = tecnologias
                self.usuario_id = usuario_id
                self.ano = ano

        def __str__(self):
                return f"[{self.id}] {self.titulo} ({self.area}, {self.ano})"

class Avaliacao:
        """Representa uma avaliação de projeto."""
        def __init__(self, id, usuario_id, projeto_id, nota, comentario):
                self.id = id
                self.usuario_id = usuario_id
                self.projeto_id = projeto_id
                self.nota = nota
                self.comentario = comentario
        def __str__(self):
                return f"Nota {self.nota}/5 - {self.comentario[:30]}"
        
class Sala:
        """Representa uma sala física."""
        def __init__(self, id, nome, andar, capacidade, tipo, ativa=1):
                self.id = id
                self.nome = nome
                self.andar = andar
                self.capacidade = capacidade
                self.tipo = tipo
                self.ativa = ativa
        def __str__(self):
                return f"{self.nome} - {self.capacidade} lugares ({self.tipo})"

class Reserva:
        """Representa uma reserva de sala."""
        def __init__(self, id, sala_id, usuario_id, data, horario, motivo, st):
                self.id = id
                self.sala_id = sala_id
                self.usuario_id = usuario_id
                self.data = data
                self.horario = horario
                self.motivo = motivo
                self.status = status
        def __str__(self):
                return f"Reserva #{self.id} - {self.data} {self.horario}"

class Sistema:
        """Gerencia o estado da aplicação (usuário logado)."""
        def __init__(self):
                self.usuario_logado = None
        def esta_logado(self):
                """Retorna True se há usuário logado."""
                return self.usuario_logado is not None
        def login(self, usuario):
                """Define o usuário logado."""
                self.usuario_logado = usuario
        def logout(self):
                """Encerra a sessão."""
                self.usuario_logado = None
>>>>>>> 095002e0a9f9a1c9d8407251640d00c09a260bb2
