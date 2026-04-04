from flask import Flask, render_template, request, redirect, url_for, send_file
from database import get_connection
import pandas as pd
from io import BytesIO
app = Flask(__name__)


@app.route("/")
def index():
    conn = get_connection()

    produtos = conn.execute("""
        SELECT * FROM produtos
        ORDER BY id DESC
    """).fetchall()

    total_produtos = conn.execute("""
        SELECT COUNT(*) as total FROM produtos
    """).fetchone()["total"]

    total_itens = conn.execute("""
        SELECT SUM(quantidade) as total FROM produtos
    """).fetchone()["total"] or 0

    valor_total = conn.execute("""
        SELECT SUM(quantidade * preco) as total FROM produtos
    """).fetchone()["total"] or 0

    produtos_baixo_estoque = conn.execute("""
        SELECT COUNT(*) as total FROM produtos
        WHERE quantidade <= 5
    """).fetchone()["total"]

    conn.close()

    return render_template(
        "index.html",
        produtos=produtos,
        total_produtos=total_produtos,
        total_itens=total_itens,
        valor_total=valor_total,
        produtos_baixo_estoque=produtos_baixo_estoque
    )


@app.route("/produtos/novo", methods=["GET", "POST"])
def novo_produto():
    if request.method == "POST":
        codigo = request.form["codigo"]
        nome_modelo = request.form["nome_modelo"]
        categoria = request.form["categoria"]
        cor = request.form["cor"]
        tamanho = request.form["tamanho"]
        quantidade = request.form["quantidade"]
        preco = request.form["preco"]
        fornecedor = request.form["fornecedor"]

        conn = get_connection()
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
            codigo,
            nome_modelo,
            categoria,
            cor,
            tamanho,
            quantidade,
            preco,
            fornecedor
        ))
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("novo_produto.html")


@app.route("/produtos/<int:id>/editar", methods=["GET", "POST"])
def editar_produto(id):
    conn = get_connection()

    if request.method == "POST":
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
            request.form["codigo"],
            request.form["nome_modelo"],
            request.form["categoria"],
            request.form["cor"],
            request.form["tamanho"],
            request.form["quantidade"],
            request.form["preco"],
            request.form["fornecedor"],
            id
        ))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    produto = conn.execute("SELECT * FROM produtos WHERE id = ?", (id,)).fetchone()
    conn.close()

    return render_template("editar_produto.html", produto=produto)


@app.route("/produtos/<int:id>/excluir", methods=["POST"])
def excluir_produto(id):
    conn = get_connection()
    conn.execute("DELETE FROM produtos WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/produtos/<int:id>/movimentar", methods=["GET", "POST"])
def movimentar_produto(id):
    conn = get_connection()
    produto = conn.execute("SELECT * FROM produtos WHERE id = ?", (id,)).fetchone()

    if request.method == "POST":
        tipo_movimentacao = request.form["tipo_movimentacao"]
        quantidade = int(request.form["quantidade"])
        observacao = request.form["observacao"]

        nova_quantidade = produto["quantidade"]

        if tipo_movimentacao == "entrada":
            nova_quantidade += quantidade
        elif tipo_movimentacao == "saida":
            if quantidade > produto["quantidade"]:
                conn.close()
                return render_template(
                    "movimentar_produto.html",
                    produto=produto,
                    erro="Não é possível realizar saída maior do que a quantidade em estoque."
                )
            nova_quantidade -= quantidade

        conn.execute("""
            UPDATE produtos
            SET quantidade = ?
            WHERE id = ?
        """, (nova_quantidade, id))

        conn.execute("""
            INSERT INTO movimentacoes (
                produto_id,
                tipo_movimentacao,
                quantidade,
                observacao
            )
            VALUES (?, ?, ?, ?)
        """, (
            id,
            tipo_movimentacao,
            quantidade,
            observacao
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    conn.close()
    return render_template("movimentar_produto.html", produto=produto)

@app.route("/movimentacoes")
def historico_movimentacoes():
    conn = get_connection()
    movimentacoes = conn.execute("""
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
    conn.close()

    return render_template("historico_movimentacoes.html", movimentacoes=movimentacoes)

@app.route("/exportar/excel")
def exportar_excel():
    conn = get_connection()

    produtos = conn.execute("""
        SELECT
            codigo AS "Código",
            nome_modelo AS "Modelo",
            categoria AS "Categoria",
            cor AS "Cor",
            tamanho AS "Tamanho",
            quantidade AS "Quantidade",
            preco AS "Preço Unitário",
            fornecedor AS "Fornecedor",
            data_cadastro AS "Data de Cadastro"
        FROM produtos
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    dados = [dict(produto) for produto in produtos]
    df = pd.DataFrame(dados)

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Estoque")

    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="estoque_produtos.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
if __name__ == "__main__":
    app.run(debug=True)