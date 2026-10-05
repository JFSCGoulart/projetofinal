"""Todas as operações de banco de dados (SQLite)."""
import sqlite3
from hashlib import sha256
from src.config import BANCO


# ============ MIGRAÇÃO ============
def esquema_legado_detectado(cursor):
    """Detecta se o banco local está em um esquema antigo/incompatível."""
    tabelas = {
        linha[0]
        for linha in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    }

    if "usuario" in tabelas or "projeto" in tabelas:
        return True

    if "salas" in tabelas:
        colunas_salas = {linha[1] for linha in cursor.execute("PRAGMA table_info(salas)")}
        if "status" not in colunas_salas:
            return True

    if "reservas" in tabelas:
        fks_reservas = {linha[2] for linha in cursor.execute("PRAGMA foreign_key_list(reservas)")}
        if "usuario" in fks_reservas:
            return True

    if "avaliacoes" in tabelas:
        fks_avaliacoes = {linha[2] for linha in cursor.execute("PRAGMA foreign_key_list(avaliacoes)")}
        if "usuario" in fks_avaliacoes or "projeto" in fks_avaliacoes:
            return True

    return False


# ============ CONEXÃO ============
def conectar():
    """Abre conexão com o banco."""
    conexao = sqlite3.connect(BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_banco():
    """Cria as tabelas, se não existirem."""
    conexao = conectar()
    cursor = conexao.cursor()
    if esquema_legado_detectado(cursor):
        cursor.executescript("""
        DROP TABLE IF EXISTS reservas;
        DROP TABLE IF EXISTS avaliacoes;
        DROP TABLE IF EXISTS projeto;
        DROP TABLE IF EXISTS projetos;
        DROP TABLE IF EXISTS salas;
        DROP TABLE IF EXISTS usuarios;
        DROP TABLE IF EXISTS usuario;
        """)

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        turma TEXT,
        tipo TEXT NOT NULL DEFAULT 'publico'
            CHECK (tipo IN ('publico', 'professor', 'coordenador'))
    );

    CREATE TABLE IF NOT EXISTS projetos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT NOT NULL,
        area TEXT NOT NULL,
        tecnologias TEXT,
        usuario_id INTEGER NOT NULL,
        ano INTEGER NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    );

    CREATE TABLE IF NOT EXISTS avaliacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        projeto_id INTEGER NOT NULL,
        nota INTEGER NOT NULL CHECK (nota BETWEEN 1 AND 5),
        comentario TEXT,
        UNIQUE (usuario_id, projeto_id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY (projeto_id) REFERENCES projetos(id)
    );

    CREATE TABLE IF NOT EXISTS salas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        andar INTEGER NOT NULL,
        capacidade INTEGER NOT NULL,
        tipo TEXT NOT NULL DEFAULT 'sala_aula',
        status TEXT NOT NULL DEFAULT 'ATIVA'
    );

    CREATE TABLE IF NOT EXISTS reservas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sala_id INTEGER NOT NULL,
        usuario_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        horario TEXT NOT NULL,
        motivo TEXT,
        status TEXT NOT NULL DEFAULT 'ativa',
        FOREIGN KEY (sala_id) REFERENCES salas(id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    );
    """)
    conexao.commit()
    conexao.close()


# ============ USUÁRIOS ============
def inserir_usuario(nome, email, senha_hash, turma, tipo):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, turma, tipo) VALUES (?, ?, ?, ?, ?)",
            (nome, email, senha_hash, turma, tipo)
        )
        conexao.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conexao.close()


def buscar_usuario_por_email(email):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        return cursor.fetchone()
    finally:
        conexao.close()


def buscar_usuario_por_id(usuario_id):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
        return cursor.fetchone()
    finally:
        conexao.close()


def listar_usuarios():
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios")
        return cursor.fetchall()
    finally:
        conexao.close()


def atualizar_tipo_usuario(usuario_id, novo_tipo):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute("UPDATE usuarios SET tipo = ? WHERE id = ?", (novo_tipo, usuario_id))
        conexao.commit()
        return cursor.rowcount > 0
    finally:
        conexao.close()


# ============ PROJETOS ============
def inserir_projeto(titulo, descricao, area, tecnologias, usuario_id, ano):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO projetos (titulo, descricao, area, tecnologias, usuario_id, ano) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (titulo, descricao, area, tecnologias, usuario_id, ano)
        )
        conexao.commit()
        return cursor.lastrowid
    except sqlite3.Error:
        return None
    finally:
        conexao.close()


def buscar_projeto_por_id(projeto_id):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM projetos WHERE id = ?", (projeto_id,))
        return cursor.fetchone()
    finally:
        conexao.close()


def listar_projetos():
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM projetos")
        return cursor.fetchall()
    finally:
        conexao.close()


def listar_projetos_por_usuario(usuario_id):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM projetos WHERE usuario_id = ?", (usuario_id,))
        return cursor.fetchall()
    finally:
        conexao.close()


def atualizar_projeto(projeto_id, titulo, descricao, area, tecnologias, ano):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE projetos SET titulo=?, descricao=?, area=?, tecnologias=?, ano=? WHERE id=?",
            (titulo, descricao, area, tecnologias, ano, projeto_id)
        )
        conexao.commit()
        return cursor.rowcount > 0
    finally:
        conexao.close()


def deletar_projeto(projeto_id):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM projetos WHERE id = ?", (projeto_id,))
        conexao.commit()
        return cursor.rowcount > 0
    finally:
        conexao.close()


def buscar_projetos_por_termo(termo):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        busca = f"%{termo}%"
        cursor.execute(
            "SELECT * FROM projetos WHERE titulo LIKE ? OR tecnologias LIKE ?",
            (busca, busca)
        )
        return cursor.fetchall()
    finally:
        conexao.close()


# ============ AVALIAÇÕES ============
def inserir_avaliacao(usuario_id, projeto_id, nota, comentario):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO avaliacoes (usuario_id, projeto_id, nota, comentario) VALUES (?, ?, ?, ?)",
            (usuario_id, projeto_id, nota, comentario)
        )
        conexao.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conexao.close()


def ja_avaliou(usuario_id, projeto_id):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT 1 FROM avaliacoes WHERE usuario_id = ? AND projeto_id = ? LIMIT 1",
            (usuario_id, projeto_id)
        )
        return cursor.fetchone() is not None
    finally:
        conexao.close()


def media_projeto(projeto_id):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT AVG(nota) FROM avaliacoes WHERE projeto_id = ?", (projeto_id,))
        media = cursor.fetchone()[0]
        return float(media) if media is not None else 0.0
    finally:
        conexao.close()


def ranking_projetos(limite=10):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT p.id, p.titulo, u.nome AS autor,
                   COUNT(a.id) AS total,
                   ROUND(AVG(a.nota), 2) AS media
            FROM projetos p
            JOIN usuarios u ON p.usuario_id = u.id
            LEFT JOIN avaliacoes a ON p.id = a.projeto_id
            GROUP BY p.id, p.titulo, u.nome
            HAVING total > 0
            ORDER BY media DESC, total DESC
            LIMIT ?
        """, (limite,))
        return cursor.fetchall()
    finally:
        conexao.close()


# ============ SALAS ============
def inserir_sala(nome, andar, capacidade, tipo):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO salas (nome, andar, capacidade, tipo) VALUES (?, ?, ?, ?)",
            (nome, andar, capacidade, tipo)
        )
        conexao.commit()
        return cursor.lastrowid
    finally:
        conexao.close()


def buscar_sala_por_id(sala_id):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM salas WHERE id = ?", (sala_id,))
        return cursor.fetchone()
    finally:
        conexao.close()


def listar_salas():
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM salas WHERE status = 'ATIVA'")
        return cursor.fetchall()
    finally:
        conexao.close()


def listar_salas_por_andar(andar):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT * FROM salas WHERE andar = ? AND status = 'ATIVA'",
            (andar,)
        )
        return cursor.fetchall()
    finally:
        conexao.close()


def desativar_sala(sala_id):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute("UPDATE salas SET status = 'DESATIVADA' WHERE id = ?", (sala_id,))
        conexao.commit()
        return cursor.rowcount > 0
    finally:
        conexao.close()


# ============ RESERVAS ============
def inserir_reserva(sala_id, usuario_id, data, horario, motivo):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO reservas (sala_id, usuario_id, data, horario, motivo) "
            "VALUES (?, ?, ?, ?, ?)",
            (sala_id, usuario_id, data, horario, motivo)
        )
        conexao.commit()
        return cursor.lastrowid
    except sqlite3.Error:
        return None
    finally:
        conexao.close()


def verificar_disponibilidade(sala_id, data, horario):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM reservas "
            "WHERE sala_id = ? AND data = ? AND horario = ? AND status = 'ativa'",
            (sala_id, data, horario)
        )
        return cursor.fetchone()[0] == 0
    finally:
        conexao.close()


def buscar_reserva_por_id(reserva_id):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM reservas WHERE id = ?", (reserva_id,))
        return cursor.fetchone()
    finally:
        conexao.close()


def listar_reservas_usuario(usuario_id):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT r.id, s.nome AS sala, s.andar, r.data, r.horario, r.motivo, r.status
            FROM reservas r
            JOIN salas s ON s.id = r.sala_id
            WHERE r.usuario_id = ? AND r.status = 'ativa'
            ORDER BY r.data, r.horario
        """, (usuario_id,))
        return cursor.fetchall()
    finally:
        conexao.close()


def listar_todas_reservas():
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT r.id, s.nome AS sala, u.nome AS usuario,
                   r.data, r.horario, r.motivo, r.status
            FROM reservas r
            JOIN salas s ON s.id = r.sala_id
            JOIN usuarios u ON u.id = r.usuario_id
            ORDER BY r.data, r.horario
        """)
        return cursor.fetchall()
    finally:
        conexao.close()


def cancelar_reserva(reserva_id):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE reservas SET status = 'cancelada' WHERE id = ?",
            (reserva_id,)
        )
        conexao.commit()
        return cursor.rowcount > 0
    finally:
        conexao.close()


# ============ DADOS DE TESTE ============
def inserir_dados_teste():
    """Insere dados de exemplo (idempotente)."""
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        senha_hash = sha256("123456".encode("utf-8")).hexdigest()

        cursor.executemany("""
            INSERT OR IGNORE INTO usuarios (id, nome, email, senha, turma, tipo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            (1, 'Coordenador Padrão', 'admin@qualifica.com', senha_hash, None, 'coordenador'),
            (2, 'João Silva', 'joao@qualifica.com', senha_hash, 'Turma A', 'professor'),
            (3, 'Maria Santos', 'maria@qualifica.com', senha_hash, 'Turma A', 'publico'),
            (4, 'Pedro Oliveira', 'pedro@qualifica.com', senha_hash, 'Turma B', 'publico'),
        ])

        cursor.executemany("""
            INSERT OR IGNORE INTO projetos
                (id, titulo, descricao, area, tecnologias, usuario_id, ano)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [
            (1, 'Sistema de Biblioteca',
             'Sistema para gerenciamento de livros e empréstimos.',
             'Outros', 'Python, SQLite, Flask', 3, 2026),
            (2, 'Aplicativo Educacional',
             'Aplicativo para auxiliar alunos nos estudos.',
             'Educação', 'Python, JavaScript', 4, 2026),
            (3, 'Controle de Estoque',
             'Sistema para controle de produtos e estoque.',
             'Financeiro', 'Python, SQLite', 3, 2026),
        ])

        cursor.executemany("""
            INSERT OR IGNORE INTO avaliacoes
                (id, usuario_id, projeto_id, nota, comentario)
            VALUES (?, ?, ?, ?, ?)
        """, [
            (1, 2, 1, 5, 'Excelente projeto.'),
            (2, 2, 2, 4, 'Boa ideia.'),
            (3, 3, 3, 5, 'Projeto muito útil.'),
        ])

        cursor.executemany("""
            INSERT OR IGNORE INTO salas
                (id, nome, andar, capacidade, tipo, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            (1, 'Sala 101', 1, 30, 'sala_aula', 'ATIVA'),
            (2, 'Sala 102', 1, 30, 'sala_aula', 'ATIVA'),
            (3, 'Laboratório 103', 1, 20, 'laboratorio', 'ATIVA'),
            (4, 'Sala 201', 2, 40, 'sala_aula', 'ATIVA'),
            (5, 'Laboratório 202', 2, 25, 'laboratorio', 'ATIVA'),
            (6, 'Auditório 301', 3, 50, 'auditorio', 'ATIVA'),
        ])

        cursor.executemany("""
            INSERT OR IGNORE INTO reservas
                (id, sala_id, usuario_id, data, horario, motivo, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [
            (1, 1, 1, '2026-10-01', '08:00 - 09:00', 'Aula de programação', 'ativa'),
            (2, 3, 2, '2026-10-01', '14:00 - 15:00', 'Aula prática', 'ativa'),
        ])

        conexao.commit()
    except Exception as erro:
        conexao.rollback()
        print(f"[ERRO] ao inserir dados de teste: {erro}")
    finally:
        conexao.close()