from database import get_connection


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL UNIQUE,
            nome_modelo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            cor TEXT NOT NULL,
            tamanho TEXT NOT NULL,
            quantidade INTEGER NOT NULL DEFAULT 0,
            preco REAL NOT NULL,
            fornecedor TEXT,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            tipo_movimentacao TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            observacao TEXT,
            data_movimentacao DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
    """)

    conn.commit()
    conn.close()
    print("Banco inicializado com sucesso.")


if __name__ == "__main__":
    init_db()