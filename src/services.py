"""Regras de negócio do sistema."""
import hashlib
import csv
import os
import re
from datetime import datetime

from src import banco
from src.config import (
    AREAS_PROJETO, TIPOS_USUARIO, TIPOS_SALA, HORARIOS,
    MIN_SENHA, MIN_DESCRICAO, NOTA_MIN, NOTA_MAX, RELATORIO,
)


# ============ SEGURANÇA ============
def gerar_hash(senha):
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def verificar_senha(senha_digitada, hash_salvo):
    return gerar_hash(senha_digitada) == hash_salvo


# ============ VALIDAÇÕES ============
def validar_email(email):
    if not email or not email.strip():
        return False, "O e-mail não pode estar vazio."
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(padrao, email.strip()):
        return True, "E-mail válido."
    return False, "Formato de e-mail inválido."


def validar_senha(senha):
    if not senha or not senha.strip():
        return False, "A senha não pode estar vazia."
    if len(senha) < MIN_SENHA:
        return False, f"A senha deve ter no mínimo {MIN_SENHA} caracteres."
    return True, "Senha válida."


def validar_data(data):
    try:
        datetime.strptime(data.strip(), "%d/%m/%Y")
        return True, "Data válida."
    except (ValueError, AttributeError):
        return False, "Data inválida. Use DD/MM/AAAA."


def validar_campo(valor, nome_campo):
    if valor is None or (isinstance(valor, str) and not valor.strip()):
        return False, f"O campo '{nome_campo}' não pode estar vazio."
    return True, "OK"


# ============ AUTENTICAÇÃO ============
def cadastrar_usuario(nome, email, senha, turma, tipo="publico"):
    """Retorna (sucesso, mensagem, id)."""
    ok, msg = validar_campo(nome, "nome")
    if not ok:
        return False, msg, None
    ok, msg = validar_email(email)
    if not ok:
        return False, msg, None
    ok, msg = validar_senha(senha)
    if not ok:
        return False, msg, None
    if tipo not in TIPOS_USUARIO:
        return False, f"Tipo inválido. Use: {', '.join(TIPOS_USUARIO)}", None
    if banco.buscar_usuario_por_email(email.strip()):
        return False, "E-mail já cadastrado.", None

    senha_hash = gerar_hash(senha)
    uid = banco.inserir_usuario(nome.strip(), email.strip(), senha_hash, turma, tipo)
    if uid is None:
        return False, "Erro ao cadastrar usuário.", None
    return True, "Usuário cadastrado com sucesso!", uid


def fazer_login(email, senha):
    """Retorna (usuario_dict, mensagem)."""
    usuario = banco.buscar_usuario_por_email(email.strip())
    if not usuario:
        return None, "Usuário não encontrado."
    if not verificar_senha(senha, usuario["senha"]):
        return None, "Senha incorreta."
    return dict(usuario), "Login realizado com sucesso!"


# ============ PROJETOS ============
def cadastrar_projeto(titulo, descricao, area, tecnologias, usuario_id, ano):
    ok, msg = validar_campo(titulo, "título")
    if not ok:
        return False, msg
    ok, msg = validar_campo(descricao, "descrição")
    if not ok:
        return False, msg
    if len(descricao) < MIN_DESCRICAO:
        return False, f"A descrição deve ter pelo menos {MIN_DESCRICAO} caracteres."
    if area not in AREAS_PROJETO:
        return False, f"Área inválida. Use: {', '.join(AREAS_PROJETO)}"
    try:
        ano_int = int(ano)
    except (ValueError, TypeError):
        return False, "Ano inválido."
    pid = banco.inserir_projeto(titulo, descricao, area, tecnologias, usuario_id, ano_int)
    if pid is None:
        return False, "Erro ao cadastrar projeto."
    return True, f"Projeto cadastrado (ID {pid})."


def remover_projeto(projeto_id, usuario_id, tipo_usuario):
    projeto = banco.buscar_projeto_por_id(projeto_id)
    if not projeto:
        return False, "Projeto não encontrado."
    if projeto["usuario_id"] != usuario_id and tipo_usuario != "coordenador":
        return False, "Sem permissão para remover este projeto."
    if banco.deletar_projeto(projeto_id):
        return True, "Projeto removido."
    return False, "Erro ao remover."


def buscar_projetos(termo=None, area=None):
    if termo:
        return [dict(r) for r in banco.buscar_projetos_por_termo(termo)]
    todos = banco.listar_projetos()
    if area:
        return [dict(r) for r in todos if r["area"] == area]
    return [dict(r) for r in todos]


def listar_projetos_por_usuario(usuario_id):
    return [dict(p) for p in banco.listar_projetos_por_usuario(usuario_id)]


def obter_detalhes_projeto(projeto_id):
    p = banco.buscar_projeto_por_id(projeto_id)
    if not p:
        return None
    return {**dict(p), "media": banco.media_projeto(projeto_id)}


def obter_ranking(limite=10):
    return [dict(r) for r in banco.ranking_projetos(limite)]


def listar_usuarios():
    return [dict(u) for u in banco.listar_usuarios()]


# ============ AVALIAÇÕES ============
def avaliar_projeto(usuario_id, projeto_id, nota, comentario):
    if not isinstance(nota, int) or isinstance(nota, bool):
        return False, "A nota deve ser um número inteiro."
    if not NOTA_MIN <= nota <= NOTA_MAX:
        return False, f"A nota deve estar entre {NOTA_MIN} e {NOTA_MAX}."
    if not banco.buscar_projeto_por_id(projeto_id):
        return False, "Projeto não encontrado."
    if banco.ja_avaliou(usuario_id, projeto_id):
        return False, "Você já avaliou este projeto."
    if banco.inserir_avaliacao(usuario_id, projeto_id, nota, comentario):
        return True, "Avaliação registrada."
    return False, "Erro ao registrar avaliação."


# ============ SALAS ============
def listar_salas_agrupadas():
    salas = banco.listar_salas()
    agrupadas = {}
    for s in salas:
        agrupadas.setdefault(s["andar"], []).append(dict(s))
    return agrupadas


def cadastrar_sala(nome, andar, capacidade, tipo, usuario_id):
    u = banco.buscar_usuario_por_id(usuario_id)
    if not u:
        return False, "Usuário não encontrado."
    if u["tipo"] != "coordenador":
        return False, "Apenas coordenadores podem cadastrar salas."
    if tipo not in TIPOS_SALA:
        return False, f"Tipo inválido. Use: {', '.join(TIPOS_SALA)}"
    try:
        andar = int(andar)
        capacidade = int(capacidade)
    except (ValueError, TypeError):
        return False, "Andar e capacidade devem ser números."
    if capacidade <= 0:
        return False, "Capacidade deve ser maior que zero."
    sid = banco.inserir_sala(nome, andar, capacidade, tipo)
    if sid is None:
        return False, "Erro ao cadastrar sala."
    return True, f"Sala cadastrada (ID {sid})."


def desativar_sala(sala_id, usuario_id):
    u = banco.buscar_usuario_por_id(usuario_id)
    if not u:
        return False, "Usuário não encontrado."
    if u["tipo"] != "coordenador":
        return False, "Apenas coordenadores podem desativar salas."
    if banco.desativar_sala(sala_id):
        return True, "Sala desativada."
    return False, "Sala não encontrada."


def obter_grade_horarios(sala_id, data):
    sala = banco.buscar_sala_por_id(sala_id)
    if not sala:
        return None
    grade = []
    for h in HORARIOS:
        livre = banco.verificar_disponibilidade(sala_id, data, h)
        grade.append({"horario": h, "status": "LIVRE" if livre else "OCUPADO"})
    return grade


# ============ RESERVAS ============
def reservar_sala(usuario_id, sala_id, data, horario, motivo):
    u = banco.buscar_usuario_por_id(usuario_id)
    if not u:
        return False, "Usuário não encontrado."
    if u["tipo"] not in ("professor", "coordenador"):
        return False, "Apenas professores e coordenadores podem reservar."
    sala = banco.buscar_sala_por_id(sala_id)
    if not sala or sala["status"] != "ATIVA":
        return False, "Sala inexistente ou inativa."
    if not banco.verificar_disponibilidade(sala_id, data, horario):
        return False, "Horário já reservado."
    rid = banco.inserir_reserva(sala_id, usuario_id, data, horario, motivo)
    if rid is None:
        return False, "Erro ao reservar."
    return True, f"Reserva {rid} criada."


def cancelar_reserva(reserva_id, usuario_id, tipo_usuario):
    r = banco.buscar_reserva_por_id(reserva_id)
    if not r:
        return False, "Reserva não encontrada."
    if r["status"] != "ativa":
        return False, "Reserva já cancelada."
    if r["usuario_id"] != usuario_id and tipo_usuario != "coordenador":
        return False, "Sem permissão para cancelar."
    if banco.cancelar_reserva(reserva_id):
        return True, "Reserva cancelada."
    return False, "Erro ao cancelar."


def listar_minhas_reservas(usuario_id):
    return [dict(r) for r in banco.listar_reservas_usuario(usuario_id)]


def listar_todas_reservas():
    return [dict(r) for r in banco.listar_todas_reservas()]


# ============ RELATÓRIOS ============
def exportar_csv():
    try:
        os.makedirs(os.path.dirname(RELATORIO), exist_ok=True)
        with open(RELATORIO, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Tipo", "ID", "Título/Sala", "Autor/Usuário",
                        "Data/Horário", "Detalhes"])
            for r in banco.ranking_projetos(1000):
                w.writerow(["Projeto", r["id"], r["titulo"], r["autor"], "",
                            f"Média: {r['media']} ({r['total']} aval.)"])
            for r in banco.listar_todas_reservas():
                w.writerow(["Reserva", r["id"], r["sala"], r["usuario"],
                            f"{r['data']} {r['horario']}", r["motivo"]])
        return True, f"Relatório salvo em {RELATORIO}."
    except Exception as e:
        return False, f"Erro ao exportar: {e}"