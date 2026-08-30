# NexusStock

Sistema simples de gestão de estoque para lojas, com foco em controle de produtos, movimentações e histórico de entradas/saídas.

## O que ele faz

- Cadastro de produtos com código, categoria, cor, tamanho, quantidade, preço e fornecedor
- Edição e exclusão de itens do estoque
- Controle de movimentações de entrada e saída
- Alertas de estoque baixo
- Dashboard com resumo geral do estoque
- Histórico de movimentações por produto
- Exportação dos dados para Excel

## Tecnologias

- Python
- Flask
- SQLite
- Pandas
- OpenPyXL

## Estrutura do projeto

```text
NexusStock/
├── estoque_loja/
│   ├── app.py
│   ├── database.py
│   ├── init_db.py
│   ├── static/
│   └── templates/
├── requirements.txt
└── README.md
```

## Como executar

1. Crie um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Inicialize o banco de dados:

```bash
python3 estoque_loja/init_db.py
```

4. Inicie a aplicação:

```bash
python3 estoque_loja/app.py
```

5. Acesse no navegador:

```text
http://127.0.0.1:5000
```

## Observação sobre Python e HTML

Esse projeto já está majoritariamente em Python na parte de regra de negócio, banco e rotas da aplicação. O HTML ainda é necessário porque ele usa Flask com templates para renderizar a interface web.

Em outras palavras:

- Python cuida da lógica e do fluxo do sistema
- HTML/CSS cuidam da tela do navegador
- SQLite guarda os dados localmente

Se a ideia for "aumentar o Python e diminuir o HTML", o melhor caminho não é remover o HTML por completo, e sim deixar a aplicação mais organizada e com menos lógica embutida nas páginas. Por exemplo:

- criar arquivos separados para regras de negócio
- separar acesso ao banco em serviços
- manter os templates bem enxutos
- usar Flask + Jinja da forma mais limpa possível

Se quiser um projeto 100% em Python, sem HTML, aí o ideal seria trocar o frontend para algo como:

- Streamlit
- NiceGUI
- Tkinter
- PySide

Essas opções reduzem ou eliminam HTML, mas mudam completamente a arquitetura da interface.

## Resumo

O NexusStock é um sistema leve de controle de estoque, ideal para pequenos negócios que precisam registrar produtos, acompanhar saídas e entradas e exportar o inventário para Excel.
