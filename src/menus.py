"""Todos os menus e interação com o usuário."""
import os

from src import services
from src.config import AREAS_PROJETO, HORARIOS, ANDARES, TIPOS_SALA, TIPOS_USUARIO


# ============ AUXILIARES ============
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def linha(tamanho=60):
    print("-" * tamanho)


def titulo(texto):
    linha()
    print(texto.center(60))
    linha()


def mensagem(tipo, texto):
    icones = {"sucesso": "[OK] ", "erro": "[ERRO] ", "aviso": "[!] "}
    print(f"{icones.get(tipo, '')}{texto}")


def pausar():
    input("\nPressione ENTER para continuar...")


def ler_int(prompt):
    try:
        return int(input(prompt).strip())
    except ValueError:
        return None


# ============ MENU PRINCIPAL ============
def menu_principal(sistema):
    while True:
        limpar_tela()
        titulo("QUALIFICA HUB")
        if sistema.usuario_logado:
            print(f"Logado como: {sistema.usuario_logado['nome']} "
                  f"({sistema.usuario_logado['tipo']})")
            linha()
            print("1 - Menu do usuário")
            print("2 - Logout")
            print("0 - Sair")
        else:
            print("1 - Login")
            print("2 - Cadastro")
            print("3 - Buscar projetos (público)")
            print("4 - Ver salas")
            print("5 - Ranking de projetos")
            print("0 - Sair")

        op = input("Escolha: ").strip()

        if sistema.usuario_logado:
            if op == "1":
                menu_usuario(sistema)
            elif op == "2":
                sistema.logout()
                mensagem("aviso", "Sessão encerrada.")
                pausar()
            elif op == "0":
                break
            else:
                mensagem("erro", "Opção inválida.")
                pausar()
        else:
            if op == "1":
                menu_login(sistema)
            elif op == "2":
                menu_cadastro()
            elif op == "3":
                menu_buscar_publico()
            elif op == "4":
                menu_ver_salas()
            elif op == "5":
                menu_ranking()
            elif op == "0":
                mensagem("aviso", "Saindo...")
                break
            else:
                mensagem("erro", "Opção inválida.")
                pausar()


# ============ LOGIN / CADASTRO ============
def menu_login(sistema):
    titulo("LOGIN")
    email = input("E-mail: ").strip()
    senha = input("Senha: ").strip()
    usuario, msg = services.fazer_login(email, senha)
    if usuario:
        sistema.login(usuario)
        mensagem("sucesso", msg)
    else:
        mensagem("erro", msg)
    pausar()


def menu_cadastro():
    titulo("CADASTRO")
    nome = input("Nome: ").strip()
    email = input("E-mail: ").strip()
    senha = input("Senha: ").strip()
    turma = input("Turma (opcional): ").strip()
    print(f"Tipos válidos: {', '.join(TIPOS_USUARIO)}")
    tipo = input("Tipo: ").strip() or "publico"

    sucesso, msg, _ = services.cadastrar_usuario(nome, email, senha, turma, tipo)
    mensagem("sucesso" if sucesso else "erro", msg)
    pausar()


# ============ MENU POR TIPO DE USUÁRIO ============
def menu_usuario(sistema):
    tipo = sistema.usuario_logado["tipo"]
    if tipo == "coordenador":
        menu_coordenador(sistema)
    elif tipo == "professor":
        menu_professor(sistema)
    else:
        menu_publico(sistema)


def menu_publico(sistema):
    while True:
        limpar_tela()
        titulo("MENU PÚBLICO")
        print("1 - Buscar projetos")
        print("2 - Ver ranking")
        print("3 - Ver salas")
        print("0 - Voltar")
        op = input("Escolha: ").strip()
        if op == "1":
            menu_buscar_publico()
        elif op == "2":
            menu_ranking()
        elif op == "3":
            menu_ver_salas()
        elif op == "0":
            return
        else:
            mensagem("erro", "Opção inválida.")
            pausar()


def menu_professor(sistema):
    while True:
        limpar_tela()
        titulo("MENU PROFESSOR")
        print("1 - Cadastrar projeto")
        print("2 - Meus projetos")
        print("3 - Reservar sala")
        print("4 - Minhas reservas")
        print("5 - Cancelar reserva")
        print("6 - Avaliar projeto")
        print("7 - Ranking")
        print("0 - Voltar")
        op = input("Escolha: ").strip()

        if op == "1":
            menu_cadastrar_projeto(sistema)
        elif op == "2":
            menu_meus_projetos(sistema)
        elif op == "3":
            menu_reservar_sala(sistema)
        elif op == "4":
            menu_minhas_reservas(sistema)
        elif op == "5":
            menu_cancelar_reserva(sistema)
        elif op == "6":
            menu_avaliar(sistema)
        elif op == "7":
            menu_ranking()
        elif op == "0":
            return
        else:
            mensagem("erro", "Opção inválida.")
            pausar()


def menu_coordenador(sistema):
    while True:
        limpar_tela()
        titulo("MENU COORDENADOR")
        print("1 - Gerenciar salas")
        print("2 - Ver todas as reservas")
        print("3 - Ver usuários")
        print("4 - Cadastrar projeto")
        print("5 - Meus projetos")
        print("6 - Reservar sala")
        print("7 - Minhas reservas")
        print("8 - Cancelar reserva")
        print("9 - Avaliar projeto")
        print("10 - Ranking")
        print("11 - Exportar relatório CSV")
        print("0 - Voltar")
        op = input("Escolha: ").strip()

        if op == "1":
            menu_gerenciar_salas(sistema)
        elif op == "2":
            menu_todas_reservas(sistema)
        elif op == "3":
            menu_listar_usuarios()
        elif op == "4":
            menu_cadastrar_projeto(sistema)
        elif op == "5":
            menu_meus_projetos(sistema)
        elif op == "6":
            menu_reservar_sala(sistema)
        elif op == "7":
            menu_minhas_reservas(sistema)
        elif op == "8":
            menu_cancelar_reserva(sistema)
        elif op == "9":
            menu_avaliar(sistema)
        elif op == "10":
            menu_ranking()
        elif op == "11":
            menu_relatorios()
        elif op == "0":
            return
        else:
            mensagem("erro", "Opção inválida.")
            pausar()


# ============ PROJETOS ============
def menu_cadastrar_projeto(sistema):
    titulo("CADASTRAR PROJETO")
    titulo_proj = input("Título: ").strip()
    descricao = input("Descrição: ").strip()
    print(f"Áreas válidas: {', '.join(AREAS_PROJETO)}")
    area = input("Área: ").strip()
    tecnologias = input("Tecnologias: ").strip()
    ano = input("Ano: ").strip()

    sucesso, msg = services.cadastrar_projeto(
        titulo_proj, descricao, area, tecnologias,
        sistema.usuario_logado["id"], ano
    )
    mensagem("sucesso" if sucesso else "erro", msg)
    pausar()


def menu_meus_projetos(sistema):
    titulo("MEUS PROJETOS")
    projetos = services.listar_projetos_por_usuario(sistema.usuario_logado["id"])
    if not projetos:
        mensagem("aviso", "Nenhum projeto cadastrado.")
    else:
        for p in projetos:
            print(f"#{p['id']} - {p['titulo']} ({p['area']}, {p['ano']})")
    pausar()


def menu_avaliar(sistema):
    titulo("AVALIAR PROJETO")
    projetos = services.buscar_projetos()
    if not projetos:
        mensagem("aviso", "Nenhum projeto disponível.")
        pausar()
        return
    for p in projetos:
        print(f"#{p['id']} - {p['titulo']}")
    pid = ler_int("ID do projeto: ")
    if pid is None:
        mensagem("erro", "ID inválido.")
        pausar()
        return
    nota = ler_int("Nota (1-5): ")
    if nota is None:
        mensagem("erro", "Nota inválida.")
        pausar()
        return
    comentario = input("Comentário: ").strip()
    sucesso, msg = services.avaliar_projeto(
        sistema.usuario_logado["id"], pid, nota, comentario
    )
    mensagem("sucesso" if sucesso else "erro", msg)
    pausar()


def menu_buscar_publico():
    titulo("BUSCAR PROJETOS")
    termo = input("Termo (título/tecnologia): ").strip()
    resultados = services.buscar_projetos(termo=termo if termo else None)
    if not resultados:
        mensagem("aviso", "Nenhum projeto encontrado.")
    for p in resultados:
        print(f"#{p['id']} - {p['titulo']} | {p['area']} | {p['tecnologias']}")
    pausar()


def menu_ranking():
    titulo("RANKING DE PROJETOS")
    ranking = services.obter_ranking(10)
    if not ranking:
        mensagem("aviso", "Nenhuma avaliação registrada.")
    for i, r in enumerate(ranking, 1):
        print(f"{i}º - {r['titulo']} | média: {r['media']} | "
              f"avaliações: {r['total']}")
    pausar()


# ============ SALAS ============
def menu_ver_salas():
    titulo("SALAS POR ANDAR")
    agrupadas = services.listar_salas_agrupadas()
    if not agrupadas:
        mensagem("aviso", "Nenhuma sala cadastrada.")
    for andar in sorted(agrupadas, key=lambda valor: str(valor)):
        try:
            andar_ref = int(andar)
        except (ValueError, TypeError):
            andar_ref = andar
        nome_andar = ANDARES.get(andar_ref, f"{andar}º Andar")
        print(f"\n== {nome_andar} ==")
        for s in agrupadas[andar]:
            print(
                f"  #{s.get('id', '?')} {s.get('nome', 'Sala sem nome')} | "
                f"cap: {s.get('capacidade', '?')} | "
                f"{s.get('tipo', 'tipo não informado')} | "
                f"{s.get('status', 'status não informado')}"
            )
    pausar()


def menu_grade_sala():
    titulo("GRADE DE HORÁRIOS")
    sid = ler_int("ID da sala: ")
    if sid is None:
        mensagem("erro", "ID inválido.")
        pausar()
        return
    data = input("Data (DD/MM/AAAA): ").strip()
    grade = services.obter_grade_horarios(sid, data)
    if grade is None:
        mensagem("erro", "Sala não encontrada.")
    else:
        for g in grade:
            print(f"  {g['horario']} - {g['status']}")
    pausar()


def menu_gerenciar_salas(sistema):
    while True:
        limpar_tela()
        titulo("GERENCIAR SALAS")
        print("1 - Cadastrar nova sala")
        print("2 - Desativar sala")
        print("0 - Voltar")
        op = input("Escolha: ").strip()

        if op == "1":
            nome = input("Nome: ").strip()
            andar = ler_int("Andar: ")
            cap = ler_int("Capacidade: ")
            print(f"Tipos válidos: {', '.join(TIPOS_SALA)}")
            tipo = input("Tipo: ").strip()
            if andar is None or cap is None:
                mensagem("erro", "Andar e capacidade devem ser números.")
                pausar()
                continue
            sucesso, msg = services.cadastrar_sala(
                nome, andar, cap, tipo, sistema.usuario_logado["id"]
            )
            mensagem("sucesso" if sucesso else "erro", msg)
            pausar()
        elif op == "2":
            sid = ler_int("ID da sala: ")
            if sid is None:
                mensagem("erro", "ID inválido.")
                pausar()
                continue
            sucesso, msg = services.desativar_sala(sid, sistema.usuario_logado["id"])
            mensagem("sucesso" if sucesso else "erro", msg)
            pausar()
        elif op == "0":
            return


# ============ RESERVAS ============
def menu_reservar_sala(sistema):
    titulo("RESERVAR SALA")
    sid = ler_int("ID da sala: ")
    if sid is None:
        mensagem("erro", "ID inválido.")
        pausar()
        return
    data = input("Data (DD/MM/AAAA): ").strip()
    print("Horários disponíveis:", ", ".join(HORARIOS))
    horario = input("Horário: ").strip()
    motivo = input("Motivo: ").strip()
    sucesso, msg = services.reservar_sala(
        sistema.usuario_logado["id"], sid, data, horario, motivo
    )
    mensagem("sucesso" if sucesso else "erro", msg)
    pausar()


def menu_minhas_reservas(sistema):
    titulo("MINHAS RESERVAS")
    reservas = services.listar_minhas_reservas(sistema.usuario_logado["id"])
    if not reservas:
        mensagem("aviso", "Você não possui reservas ativas.")
    for r in reservas:
        print(f"  #{r['id']} {r['sala']} (andar {r['andar']}) "
              f"{r['data']} {r['horario']}")
        print(f"       Motivo: {r['motivo']}")
    pausar()


def menu_cancelar_reserva(sistema):
    titulo("CANCELAR RESERVA")
    rid = ler_int("ID da reserva: ")
    if rid is None:
        mensagem("erro", "ID inválido.")
        pausar()
        return
    sucesso, msg = services.cancelar_reserva(
        rid, sistema.usuario_logado["id"], sistema.usuario_logado["tipo"]
    )
    mensagem("sucesso" if sucesso else "erro", msg)
    pausar()


def menu_todas_reservas(sistema):
    titulo("TODAS AS RESERVAS")
    reservas = services.listar_todas_reservas()
    if not reservas:
        mensagem("aviso", "Nenhuma reserva registrada.")
    for r in reservas:
        print(f"  #{r['id']} {r['sala']} | {r['usuario']} | "
              f"{r['data']} {r['horario']} | {r['status']}")
    pausar()


def menu_listar_usuarios():
    titulo("USUÁRIOS CADASTRADOS")
    for u in services.listar_usuarios():
        print(f"  #{u['id']} {u['nome']} | {u['email']} | {u['tipo']}")
    pausar()


# ============ RELATÓRIOS ============
def menu_relatorios():
    titulo("EXPORTAR RELATÓRIO")
    sucesso, msg = services.exportar_csv()
    mensagem("sucesso" if sucesso else "erro", msg)
    pausar()