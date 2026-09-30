import json
import os

# ==========================================
# CLASSES DE MODELO
# ==========================================

class Usuario:
    def __init__(self, id, nome, email, senha, turma, tipo):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha          
        self.turma = turma
        self.tipo = tipo

    def pode_reservar(self):
        return self.tipo in ["professor", "coordenador"]

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, dados):
        return cls(**dados)


class Sala:
    def __init__(self, id, curso, andar, capacidade, turno, ativa=1):
        self.id = id
        self.curso = curso
        self.andar = andar
        self.capacidade = capacidade
        self.turno = turno
        self.ativa = ativa

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, dados):
        return cls(**dados)


class Reserva:
    def __init__(self, id, sala_id, usuario_id, data, horario, motivo, status, turno):
        self.id = id
        self.sala_id = sala_id
        self.usuario_id = usuario_id
        self.data = data
        self.horario = horario
        self.motivo = motivo
        self.status = status
        self.turno = turno

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, dados):
        return cls(**dados)


# ==========================================
# SISTEMA CENTRAL (GERENCIADOR DE DADOS)
# ==========================================

class Sistema:
    def __init__(self):
        self.usuario_logado = None
        self.usuarios = []
        self.salas = []
        self.reservas = []
        self.carregar_dados()

    # --- Persistência JSON ---
    def carregar_dados(self):
        if os.path.exists("usuarios.json"):
            with open("usuarios.json", "r", encoding="utf-8") as f:
                self.usuarios = [Usuario.from_dict(u) for u in json.load(f)]
        else:
            # Usuários padrão se o arquivo não existir
            self.usuarios = [
                Usuario(1, "Carlos Aluno", "aluno@email.com", "123", "3A", "aluno"),
                Usuario(2, "Prof. Roberto", "roberto@email.com", "123", "Nenhum", "professor"),
                Usuario(3, "Ana Coord", "coord@email.com", "123", "Nenhum", "coordenador")
            ]
            self.salvar_dados()

        if os.path.exists("salas.json"):
            with open("salas.json", "r", encoding="utf-8") as f:
                self.salas = [Sala.from_dict(s) for s in json.load(f)]
        else:
            # Salas padrão
            self.salas = [
                Sala(101, "TI", 1, 30, "Noturno"),
                Sala(102, "TI", 1, 40, "Matutino"),
                Sala(201, "Design", 2, 25, "Noturno")
            ]
            self.salvar_dados()

        if os.path.exists("reservas.json"):
            with open("reservas.json", "r", encoding="utf-8") as f:
                self.reservas = [Reserva.from_dict(r) for r in json.load(f)]

    def salvar_dados(self):
        with open("usuarios.json", "w", encoding="utf-8") as f:
            json.dump([u.to_dict() for u in self.usuarios], f, indent=4, ensure_ascii=False)
        with open("salas.json", "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in self.salas], f, indent=4, ensure_ascii=False)
        with open("reservas.json", "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in self.reservas], f, indent=4, ensure_ascii=False)

    # --- Autenticação ---
    def login(self, email, senha):
        for u in self.usuarios:
            if u.email == email and u.senha == senha:
                self.usuario_logado = u
                return True
        return False

    def logout(self):
        self.usuario_logado = None

    # --- Lógica de Disponibilidade ---
    def listar_salas_disponiveis(self, data, turno, curso_filtro=None):
        """Busca salas ativas que não possuem reservas aprovadas na data e turno especificados."""
        salas_ocupadas_ids = [
            r.sala_id for r in self.reservas 
            if r.data == data and r.turno.lower() == turno.lower() and r.status.lower() == "aprovada"
        ]
        
        disponiveis = []
        for sala in self.salas:
            if sala.ativa == 1 and sala.id not in salas_ocupadas_ids:
                if curso_filtro and curso_filtro.lower() != sala.curso.lower():
                    continue
                disponiveis.append(sala)
        return disponiveis

    def nova_reserva(self, sala_id, data, horario, motivo, turno):
        if not self.usuario_logado or not self.usuario_logado.pode_reservar():
            return False, "Usuário sem permissão para reservar salas."

        # Validar conflito de reserva idêntica
        for r in self.reservas:
            if r.sala_id == sala_id and r.data == data and r.turno.lower() == turno.lower() and r.status == "Aprovada":
                return False, "Esta sala já está reservada para esta data e turno!"

        novo_id = len(self.reservas) + 1
        reserva = Reserva(novo_id, sala_id, self.usuario_logado.id, data, horario, motivo, "Aprovada", turno)
        self.reservas.append(reserva)
        self.salvar_dados()
        return True, "Reserva realizada com sucesso!"


# ==========================================
# INTERFACE DE TERMINAL (MENU)
# ==========================================

def menu_principal():
    sys = Sistema()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*45)
        print("     SISTEMA DE GESTÃO DE RESERVAS E SALAS    ")
        print("="*45)
        
        if sys.usuario_logado:
            print(f" Logado como: {sys.usuario_logado.nome} [{sys.usuario_logado.tipo.upper()}]")
            print("-"*45)
            print(" [1] Verificar Salas Disponíveis")
            print(" [2] Solicitar Nova Reserva de Sala")
            print(" [3] Listar Todas as Reservas Atuais")
            print(" [4] Fazer Logout")
        else:
            print(" [1] Fazer Login")
            print(" [0] Sair do Programa")
        print("="*45)
        
        opcao = input("Escolha uma opção: ").strip()

        if not sys.usuario_logado:
            if opcao == "1":
                print("\n--- TELA DE LOGIN ---")
                print("Dica: Use 'roberto@email.com' e senha '123' (Professor)")
                email = input("E-mail: ").strip()
                senha = input("Senha: ").strip()
                if sys.login(email, senha):
                    input("\n[+] Login efetuado! Pressione ENTER para continuar...")
                else:
                    input("\n[-] Credenciais incorretas. Pressione ENTER...")
            elif opcao == "0":
                print("\nSaindo do sistema de forma segura. Até logo!")
                break
        else:
            if opcao == "1":
                print("\n--- BUSCA DE SALAS DISPONÍVEIS ---")
                data = input("Data desejada (Ex: 30/09/2026): ").strip()
                turno = input("Turno (Matutino/Vespertino/Noturno): ").strip()
                curso = input("Filtrar por Curso (Deixe em branco para todos): ").strip()
                curso_filtro = curso if curso else None
                
                salas = sys.listar_salas_disponiveis(data, turno, curso_filtro)
                print(f"\nSalas livres encontradas para o turno {turno} em {data}:")
                if not salas:
                    print(" Nenhuma sala livre atende a esses critérios.")
                for s in salas:
                    print(f" -> ID: {s.id} | Curso: {s.curso} | Cap: {s.capacidade} lugares | Andar: {s.andar}º")
                input("\nPressione ENTER para voltar ao menu...")

            elif opcao == "2":
                print("\n--- NOVA RESERVA ---")
                try:
                    sala_id = int(input("ID da Sala que deseja reservar: "))
                    data = input("Data (Ex: 30/09/2026): ").strip()
                    turno = input("Turno (Matutino/Vespertino/Noturno): ").strip()
                    horario = input("Horário específico (Ex: 19:15): ").strip()
                    motivo = input("Motivo da reserva: ").strip()
                    
                    sucesso, msg = sys.nova_reserva(sala_id, data, horario, motivo, turno)
                    if sucesso:
                        print(f"\n[✓] {msg}")
                    else:
                        print(f"\n[X] Erro: {msg}")
                except ValueError:
                    print("\n[X] Erro: O ID da sala precisa ser um número inteiro.")
                input("\nPressione ENTER para continuar...")

            elif opcao == "3":
                print("\n--- LISTA DE RESERVAS CADASTRADAS ---")
                if not sys.reservas:
                    print(" Nenhuma reserva encontrada no histórico.")
                for r in sys.reservas:
                    print(f" -> Reserva #{r.id} | Sala ID: {r.sala_id} | Data: {r.data} ({r.turno}) | Motivo: {r.motivo}")
                input("\nPressione ENTER para voltar ao menu...")

            elif opcao == "4":
                sys.logout()
                input("\n[-] Sessão encerrada. Pressione ENTER...")

if __name__ == "__main__":
    menu_principal()

