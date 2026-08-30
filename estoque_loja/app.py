from flask import Flask, render_template, request, redirect, url_for, send_file
from database import get_connection
import pandas as pd
from io import BytesIO
from services import (
    obter_dashboard,
    criar_produto as criar_produto_service,
    editar_produto as editar_produto_service,
    remover_produto as remover_produto_service,
    processar_movimentacao as processar_movimentacao_service,
    obter_historico_movimentacoes,
    obter_produto_para_edicao,
)

app = Flask(__name__)


@app.route("/")
def index():
    conn = get_connection()
    try:
        dashboard = obter_dashboard(conn)
    finally:
        conn.close()

    return render_template(
        "index.html",
        produtos=dashboard["produtos"],
        total_produtos=dashboard["total_produtos"],
        total_itens=dashboard["total_itens"],
        valor_total=dashboard["valor_total"],
        produtos_baixo_estoque=dashboard["produtos_baixo_estoque"],
    )


@app.route("/produtos/novo", methods=["GET", "POST"])
def novo_produto():
    if request.method == "POST":
        conn = get_connection()
        try:
            criar_produto_service(conn, request.form)
        finally:
            conn.close()

        return redirect(url_for("index"))

    return render_template("novo_produto.html")


@app.route("/produtos/<int:id>/editar", methods=["GET", "POST"])
def editar_produto(id):
    conn = get_connection()

    if request.method == "POST":
        try:
            editar_produto_service(conn, id, request.form)
        finally:
            conn.close()
        return redirect(url_for("index"))

    try:
        produto = obter_produto_para_edicao(conn, id)
    finally:
        conn.close()

    return render_template("editar_produto.html", produto=produto)


@app.route("/produtos/<int:id>/excluir", methods=["POST"])
def excluir_produto(id):
    conn = get_connection()
    try:
        remover_produto_service(conn, id)
    finally:
        conn.close()

    return redirect(url_for("index"))


@app.route("/produtos/<int:id>/movimentar", methods=["GET", "POST"])
def movimentar_produto(id):
    conn = get_connection()
    try:
        produto = obter_produto_para_edicao(conn, id)

        if request.method == "POST":
            tipo_movimentacao = request.form["tipo_movimentacao"]
            quantidade = request.form["quantidade"]
            observacao = request.form["observacao"]

            try:
                processar_movimentacao_service(conn, produto, tipo_movimentacao, quantidade, observacao)
            except ValueError as exc:
                return render_template(
                    "movimentar_produto.html",
                    produto=produto,
                    erro=str(exc),
                )

            conn.close()
            return redirect(url_for("index"))

        return render_template("movimentar_produto.html", produto=produto)
    finally:
        if conn:
            conn.close()

@app.route("/movimentacoes")
def historico_movimentacoes():
    conn = get_connection()
    try:
        movimentacoes = obter_historico_movimentacoes(conn)
    finally:
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