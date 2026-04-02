from flask import Flask, render_template, request, redirect, url_for
from database import get_connection

app = Flask(__name__)


@app.route("/")
def index():
    conn = get_connection()
    produtos = conn.execute("""
        SELECT * FROM produtos
        ORDER BY id DESC
    """).fetchall()
    conn.close()

    return render_template("index.html", produtos=produtos)


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


if __name__ == "__main__":
    app.run(debug=True)