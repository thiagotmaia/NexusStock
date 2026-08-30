def listar_produtos(conn):
    return conn.execute("""
        SELECT * FROM produtos
        ORDER BY id DESC
    """).fetchall()


def contar_total_produtos(conn):
    return conn.execute("""
        SELECT COUNT(*) as total FROM produtos
    """).fetchone()["total"]


def somar_total_itens(conn):
    return conn.execute("""
        SELECT SUM(quantidade) as total FROM produtos
    """).fetchone()["total"] or 0


def somar_valor_total(conn):
    return conn.execute("""
        SELECT SUM(quantidade * preco) as total FROM produtos
    """).fetchone()["total"] or 0


def contar_produtos_baixo_estoque(conn):
    return conn.execute("""
        SELECT COUNT(*) as total FROM produtos
        WHERE quantidade <= 5
    """).fetchone()["total"]


def obter_produto_por_id(conn, id):
    return conn.execute("SELECT * FROM produtos WHERE id = ?", (id,)).fetchone()


def inserir_produto(conn, dados):
    conn.execute("""
        INSERT INTO produtos (
            codigo,
            nome_modelo,
            categoria,
            cor,
            tamanho,
            quantidade,
            preco,
            fornecedor
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        dados["codigo"],
        dados["nome_modelo"],
        dados["categoria"],
        dados["cor"],
        dados["tamanho"],
        dados["quantidade"],
        dados["preco"],
        dados["fornecedor"],
    ))
    conn.commit()


def atualizar_produto(conn, id, dados):
    conn.execute("""
        UPDATE produtos
        SET codigo = ?,
            nome_modelo = ?,
            categoria = ?,
            cor = ?,
            tamanho = ?,
            quantidade = ?,
            preco = ?,
            fornecedor = ?
        WHERE id = ?
    """, (
        dados["codigo"],
        dados["nome_modelo"],
        dados["categoria"],
        dados["cor"],
        dados["tamanho"],
        dados["quantidade"],
        dados["preco"],
        dados["fornecedor"],
        id,
    ))
    conn.commit()


def excluir_produto(conn, id):
    conn.execute("DELETE FROM produtos WHERE id = ?", (id,))
    conn.commit()


def listar_movimentacoes(conn):
    return conn.execute("""
        SELECT
            movimentacoes.id,
            produtos.nome_modelo,
            produtos.codigo,
            movimentacoes.tipo_movimentacao,
            movimentacoes.quantidade,
            movimentacoes.observacao,
            movimentacoes.data_movimentacao
        FROM movimentacoes
        INNER JOIN produtos
            ON movimentacoes.produto_id = produtos.id
        ORDER BY movimentacoes.data_movimentacao DESC
    """).fetchall()


def registrar_movimentacao(conn, produto_id, tipo_movimentacao, quantidade, observacao):
    conn.execute("""
        INSERT INTO movimentacoes (
            produto_id,
            tipo_movimentacao,
            quantidade,
            observacao
        )
        VALUES (?, ?, ?, ?)
    """, (
        produto_id,
        tipo_movimentacao,
        quantidade,
        observacao,
    ))
    conn.commit()


def atualizar_quantidade_produto(conn, id, nova_quantidade):
    conn.execute("""
        UPDATE produtos
        SET quantidade = ?
        WHERE id = ?
    """, (nova_quantidade, id))
    conn.commit()
