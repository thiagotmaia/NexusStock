from database import get_connection
from repositories import listar_produtos


def gerar_relatorio_estoque():
    conn = get_connection()
    try:
        produtos = listar_produtos(conn)

        total_produtos = len(produtos)
        total_itens = sum(produto["quantidade"] for produto in produtos)
        valor_total = sum(produto["quantidade"] * produto["preco"] for produto in produtos)
        produtos_criticos = [produto for produto in produtos if produto["quantidade"] <= 5]

        return {
            "total_produtos": total_produtos,
            "total_itens": total_itens,
            "valor_total": valor_total,
            "produtos_criticos": produtos_criticos,
            "quantidade_produtos_criticos": len(produtos_criticos),
        }
    finally:
        conn.close()


def main():
    relatorio = gerar_relatorio_estoque()
    print("Resumo do estoque")
    print("-" * 30)
    print(f"Produtos cadastrados: {relatorio['total_produtos']}")
    print(f"Itens em estoque: {relatorio['total_itens']}")
    print(f"Valor total: R$ {relatorio['valor_total']:.2f}")
    print(f"Produtos em risco: {relatorio['quantidade_produtos_criticos']}")

    if relatorio["produtos_criticos"]:
        print("Produtos críticos:")
        for produto in relatorio["produtos_criticos"]:
            print(f"- {produto['nome_modelo']} ({produto['codigo']}): {produto['quantidade']} unidades")


if __name__ == "__main__":
    main()
