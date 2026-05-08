import sqlite3


def conectar():
    return sqlite3.connect("precificacao.db")


def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            custo_ingredientes REAL NOT NULL,
            embalagem REAL NOT NULL,
            mao_obra REAL NOT NULL,
            margem_lucro REAL NOT NULL,
            custo_total REAL NOT NULL,
            lucro REAL NOT NULL,
            preco_venda REAL NOT NULL,
            estoque INTEGER NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


def salvar_produto(
    nome,
    custo_ingredientes,
    embalagem,
    mao_obra,
    margem_lucro,
    custo_total,
    lucro,
    preco_venda,
    estoque
):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO produtos (
            nome,
            custo_ingredientes,
            embalagem,
            mao_obra,
            margem_lucro,
            custo_total,
            lucro,
            preco_venda,
            estoque
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        nome,
        custo_ingredientes,
        embalagem,
        mao_obra,
        margem_lucro,
        custo_total,
        lucro,
        preco_venda,
        estoque
    ))

    conexao.commit()
    conexao.close()


def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT nome, preco_venda, custo_total, lucro, estoque
        FROM produtos
        ORDER BY nome
    """)

    produtos = cursor.fetchall()

    conexao.close()

    return produtos