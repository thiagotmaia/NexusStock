from repositories import (
    contar_produtos_baixo_estoque,
    contar_total_produtos,
    listar_movimentacoes,
    listar_produtos,
    registrar_movimentacao,
    somar_total_itens,
    somar_valor_total,
    atualizar_produto,
    atualizar_quantidade_produto,
    excluir_produto,
    inserir_produto,
    obter_produto_por_id,
)


def obter_dashboard(conn):
    produtos = listar_produtos(conn)
    return {
        "produtos": produtos,
        "total_produtos": contar_total_produtos(conn),
        "total_itens": somar_total_itens(conn),
        "valor_total": somar_valor_total(conn),
        "produtos_baixo_estoque": contar_produtos_baixo_estoque(conn),
    }


def criar_produto(conn, formulario):
    dados = {
        "codigo": formulario["codigo"],
        "nome_modelo": formulario["nome_modelo"],
        "categoria": formulario["categoria"],
        "cor": formulario["cor"],
        "tamanho": formulario["tamanho"],
        "quantidade": int(formulario["quantidade"]),
        "preco": float(formulario["preco"]),
        "fornecedor": formulario["fornecedor"],
    }
    inserir_produto(conn, dados)
    return dados


def editar_produto(conn, id, formulario):
    dados = {
        "codigo": formulario["codigo"],
        "nome_modelo": formulario["nome_modelo"],
        "categoria": formulario["categoria"],
        "cor": formulario["cor"],
        "tamanho": formulario["tamanho"],
        "quantidade": int(formulario["quantidade"]),
        "preco": float(formulario["preco"]),
        "fornecedor": formulario["fornecedor"],
    }
    atualizar_produto(conn, id, dados)
    return dados


def remover_produto(conn, id):
    excluir_produto(conn, id)


def processar_movimentacao(conn, produto, tipo_movimentacao, quantidade, observacao):
    quantidade = int(quantidade)
    nova_quantidade = produto["quantidade"]

    if tipo_movimentacao == "entrada":
        nova_quantidade += quantidade
    elif tipo_movimentacao == "saida":
        if quantidade > produto["quantidade"]:
            raise ValueError("Não é possível realizar saída maior do que a quantidade em estoque.")
        nova_quantidade -= quantidade
    else:
        raise ValueError("Tipo de movimentação inválido.")

    atualizar_quantidade_produto(conn, produto["id"], nova_quantidade)
    registrar_movimentacao(conn, produto["id"], tipo_movimentacao, quantidade, observacao)

    return nova_quantidade


def obter_historico_movimentacoes(conn):
    return listar_movimentacoes(conn)


def obter_produto_para_edicao(conn, id):
    return obter_produto_por_id(conn, id)
