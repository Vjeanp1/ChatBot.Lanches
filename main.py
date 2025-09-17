from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

# Configuração do MySQL (ajuste user, password, host, database)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:uninter@localhost:3306/TrailerLukinhas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CARDAPIO = {
    '1': {
        'nome': 'Espetos',
        'itens': [
            {'nome': 'Frango', 'preco': 8.0},
            {'nome': 'Carne', 'preco': 10.0},
            {'nome': 'Cafta', 'preco': 10.0},
            {'nome': 'Cafta com Queijo', 'preco': 10.0},
            {'nome': 'Queijo Coalho', 'preco': 10.0},
            {'nome': 'Coração', 'preco': 10.0}
        ]
    },
    '2': {
        'nome': 'Porções',
        'itens': [
            {'nome': 'Batata Frita', 'preco': 20.0},
            {'nome': 'Salgados Fritos', 'preco': 18.0}
        ]
    },
    '3': {
        'nome': 'Salgados',
        'itens': [
            {'nome': 'Coxinha', 'preco': 8.0},
            {'nome': 'Esfirra de Frango', 'preco': 8.0},
            {'nome': 'Esfirra de Frango/c Catupiry', 'preco': 8.0},
            {'nome': 'Risoli', 'preco': 8.0},
            {'nome': 'Bolinho de Carne', 'preco': 8.0},
            {'nome': 'Enroladinho de Salsicha', 'preco': 8.0}
        ]
    },
    '4': {
        'nome': 'Refrigerantes',
        'itens': [
            {'nome': 'Guaraná Lata', 'preco': 6.0},
            {'nome': 'Fanta Laranja Lata', 'preco': 6.0},
            {'nome': 'Fanta Uva Lata', 'preco': 6.0},
            {'nome': 'Sprite Lata', 'preco': 6.0},
            {'nome': 'Coca-Cola Lata', 'preco': 6.0},
            {'nome': 'Coca-Cola Zero Lata', 'preco': 6.0},
            {'nome': 'Coca-Cola Ks', 'preco': 5.0}
        ]
    },
    '5': {
        'nome': 'Cervejas',
        'itens': [
            {'nome': 'Original 269ml', 'preco': 5.0},
            {'nome': 'Imperio 269ml', 'preco': 5.0},
            {'nome': 'Original 300ml', 'preco': 5.0},
            {'nome': 'Skol 350ml', 'preco': 5.0},
            {'nome': 'Heineken long neck', 'preco': 10.0},
            {'nome': 'Skol 600ml', 'preco': 12.0},
            {'nome': 'Imperio 600ml', 'preco': 12.0},
            {'nome': 'Original 600ml', 'preco': 15.0},
            {'nome': 'Heineken 600ml', 'preco': 15.0}
        ]
    },
    '6': {
        'nome': 'Copão',
        'itens': [
            {'nome': 'Copão de Gin', 'preco': 10.0},
            {'nome': 'Gin de Melancia', 'preco': 10.0},
            {'nome': 'Gin de Maça-Verde', 'preco': 10.0},
            {'nome': 'Gin Tropical', 'preco': 10.0},
            {'nome': 'Passaport', 'preco': 20.0},
            {'nome': 'Passaport Honey', 'preco': 25.0},
            {'nome': 'Passaport Apple', 'preco': 25.0},
            {'nome': 'Cavalo Branco', 'preco': 20.0},
            {'nome': 'Red Label', 'preco': 25.0},
            {'nome': 'Jack Daniels', 'preco': 40.0},
            {'nome': 'Jack Daniels Honey', 'preco': 45.0}
        ]
    },
    '7': {
        'nome': 'Lanches',
        'itens': [
            {'nome': 'X-Burguer', 'preco': 20.0},
            {'nome': 'X-Salada', 'preco': 22.0},
            {'nome': 'X-Bacon', 'preco': 22.0}
        ]
    }
}

class Cliente(db.Model):
    idCliente = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(30), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    estiloPedido = db.Column(db.String(10), nullable=True)  # MESA | ENTREGA
    mesa = db.Column(db.String(10), nullable=True)
    endereco = db.Column(db.String(255), nullable=True)     # << NOVO
    formaDePagamento = db.Column(db.String(30), nullable=True)  # << NOVO
    soma = db.Column(db.Float, default=0.0)
    pedido = db.Column(db.Text, default='[]')
    estado = db.Column(db.String(50), default='inicio')

def get_response(text):
    return jsonify({"response": text})

def get_cardapio_list():
    menu_text = "CARDÁPIO:\n"
    for key, value in CARDAPIO.items():
        menu_text += f"{key} - {value['nome']}\n"
    menu_text += "\n0 - Voltar ao menu principal\n"
    menu_text += "Digite o número da categoria desejada."
    return menu_text

def get_categoria_itens(categoria_id):
    categoria = CARDAPIO.get(categoria_id)
    if not categoria:
        return None
    itens_text = f"{categoria['nome']}:\n"
    for i, item in enumerate(categoria['itens'], 1):
        itens_text += f"{i} - {item['nome']} (R${item['preco']:.2f})\n"
    itens_text += "\nDigite o número do item que deseja pedir."
    return itens_text

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json() or request.form.to_dict()

    numero = data.get('From') or data.get('from')
    raw_msg = (data.get('Body') or data.get('body') or '').strip()
    msg = raw_msg.lower()  # apenas para comparações

    if not numero:
        return jsonify({"error": "Número do cliente não informado"}), 400

    cliente = Cliente.query.filter_by(numero=numero).first()

    if not cliente:
        if msg in ['mesa', 'entrega']:
            cliente = Cliente(numero=numero, estiloPedido=msg.upper(), estado=msg)
            db.session.add(cliente)
            db.session.commit()
            if msg == 'mesa':
                return get_response("Olá! Bem-vindo ao Trailer do Lukinhas!\nPor favor, informe o número da sua mesa:")
            else:
                return get_response("Pedido para entrega! Informe seu nome completo:")
        else:
            return get_response("Olá! Bem-vindo ao Trailer do Lukinhas! Digite 'mesa' para consumir no local ou 'entrega' para pedir para entrega.")

    # FLUXO DE CONVERSA
    if cliente.estado == 'mesa':
        if msg.isdigit():
            cliente.mesa = raw_msg  # número da mesa como digitado
            cliente.estado = 'nome'
            db.session.commit()
            return get_response("Agora, por favor, informe seu nome:")
        else:
            return get_response("Por favor, informe apenas o número da mesa.")

    elif cliente.estado == 'entrega':
        cliente.nome = raw_msg
        cliente.estado = 'telefone'
        db.session.commit()
        return get_response("Informe seu telefone para contato:")

    elif cliente.estado == 'telefone':
        cliente.telefone = raw_msg
        cliente.estado = 'endereco'
        db.session.commit()
        return get_response("Informe seu endereço (rua, número, bairro):")

    elif cliente.estado == 'endereco':
        cliente.endereco = raw_msg
        cliente.estado = 'pagamento'
        db.session.commit()
        return get_response("Qual a forma de pagamento? (pix, dinheiro, cartão)")

    elif cliente.estado == 'pagamento':
        cliente.formaDePagamento = raw_msg
        cliente.estado = 'menu_principal'
        db.session.commit()
        return get_response("Cadastro para entrega realizado! Digite 1 para ver o cardápio ou 0 para finalizar.")

    elif cliente.estado == 'nome':
        cliente.nome = raw_msg
        cliente.estado = 'menu_principal'
        db.session.commit()
        return get_response(f"Obrigado, {cliente.nome}! Digite 1 para ver o cardápio ou 0 para finalizar.")

    # Lógica de estados para o cardápio
    if cliente.estado == 'menu_principal':
        if msg == '1':
            cliente.estado = 'aguardando_categoria'
            db.session.commit()
            return get_response(get_cardapio_list())
        elif msg == '0':
            return finalizar_pedido(cliente)
        else:
            return get_response("Opção inválida. Digite 1 para ver o cardápio ou 0 para finalizar.")

    elif cliente.estado == 'aguardando_categoria':
        if msg == '0':
            cliente.estado = 'menu_principal'
            db.session.commit()
            return get_response("Ok. Digite 1 para ver o cardápio ou 0 para finalizar.")
        if msg in CARDAPIO:
            cliente.estado = f'aguardando_quantidade_{msg}'
            db.session.commit()
            return get_response(get_categoria_itens(msg))
        else:
            return get_response("Categoria inválida. Por favor, digite o número da categoria desejada.")

    # Lógica para adicionar itens do cardápio e pedir a quantidade
    for categoria_id, categoria_info in CARDAPIO.items():
        if cliente.estado.startswith(f'aguardando_quantidade_{categoria_id}'):
            try:
                item_idx = int(msg) - 1
                if 0 <= item_idx < len(categoria_info['itens']):
                    item = categoria_info['itens'][item_idx]
                    cliente.estado = f"finalizando_item_{categoria_id}_{item_idx}"
                    db.session.commit()
                    return get_response(f"Você escolheu {item['nome']}. Quantas unidades você quer?")
                else:
                    return get_response(f"Opção inválida. Digite o número do item da categoria {categoria_info['nome']}.")
            except (ValueError, IndexError):
                return get_response(f"Opção inválida. Digite o número do item da categoria {categoria_info['nome']}.")

    # Lógica para finalizar a adição do item com a quantidade
    if cliente.estado.startswith('finalizando_item_'):
        try:
            quantidade = int(msg)
            if quantidade <= 0:
                return get_response("A quantidade deve ser um número maior que zero. Por favor, digite novamente.")
            estado_parts = cliente.estado.split('_')
            categoria_id = estado_parts[2]
            item_idx = int(estado_parts[3])
            item = CARDAPIO[categoria_id]['itens'][item_idx]
            pedido_list = json.loads(cliente.pedido or '[]')
            pedido_list.append({
                'nome': item['nome'],
                'preco': item['preco'],
                'quantidade': quantidade
            })
            cliente.pedido = json.dumps(pedido_list)
            cliente.soma = float(cliente.soma or 0) + item['preco'] * quantidade
            cliente.estado = 'menu_principal'
            db.session.commit()
            return get_response(f"Adicionado {quantidade} unidade(s) de {item['nome']} ao seu pedido! Digite 1 para ver o cardápio ou 0 para finalizar.")
        except (ValueError, IndexError):
            return get_response("Quantidade inválida. Por favor, digite um número inteiro.")

    return get_response("Não entendi sua mensagem. Digite 'mesa' para começar ou 'entrega' para pedir para entrega.")

def finalizar_pedido(cliente):
    if not cliente.pedido or cliente.pedido == '[]':
        db.session.delete(cliente)
        db.session.commit()
        return get_response("Você não adicionou nenhum item. Pedido cancelado. Para começar, digite 'mesa' ou 'entrega'.")

    pedido_items = json.loads(cliente.pedido)
    pedido_detalhado = "\n".join([
        f"{item['quantidade']}x {item['nome']} - R$ {item['preco']:.2f} (Subtotal: R$ {item['preco'] * item['quantidade']:.2f})"
        for item in pedido_items
    ])

    total = float(cliente.soma or 0.0)

    if cliente.estiloPedido == 'MESA':
        resposta = (
            f"Mesa: {cliente.mesa or '-'}\n"
            f"Nome: {cliente.nome or '-'}\n"
            f"Seu pedido:\n{pedido_detalhado}\n"
            f"Total: R$ {total:.2f}\n"
            "Obrigado!"
        )
    else:  # ENTREGA
        resposta = (
            "Muito obrigado por comprar no trailer do Lukinhas!\n"
            f"Nome: {cliente.nome or '-'}\n"
            f"Endereço: {cliente.endereco or '-'}\n"
            f"Pagamento: {cliente.formaDePagamento or '-'}\n"
            f"Seu pedido:\n{pedido_detalhado}\n"
            f"Total: R$ {total:.2f}\n"
            "A entrega irá demorar em torno de 40min a 1h."
        )

    # reset de sessão
    cliente.estado = 'inicio'
    cliente.soma = 0.0
    cliente.pedido = '[]'
    db.session.commit()
    return get_response(resposta)

@app.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    clientes_list = []
    for c in clientes:
        clientes_list.append({
            "id": c.idCliente,
            "numero": c.numero,
            "nome": c.nome,
            "estiloPedido": c.estiloPedido,
            "mesa": c.mesa,
            "endereco": c.endereco,
            "pagamento": c.formaDePagamento,
            "total": c.soma,
            "pedido": json.loads(c.pedido or '[]'),
            "estado": c.estado
        })
    return jsonify(clientes_list)

@app.route('/cliente/<int:id>', methods=['GET'])
def obter_cliente(id):
    c = Cliente.query.get(id)
    if not c:
        return jsonify({"error": "Cliente não encontrado"}), 404
    return jsonify({
        "id": c.idCliente,
        "numero": c.numero,
        "nome": c.nome,
        "estiloPedido": c.estiloPedido,
        "mesa": c.mesa,
        "endereco": c.endereco,
        "pagamento": c.formaDePagamento,
        "total": c.soma,
        "pedido": json.loads(c.pedido or '[]'),
        "estado": c.estado
    })

if __name__ == '__main__':
    print("Servidor Flask rodando! Use o endereço do ngrok para conectar seu webhook do WhatsApp.")
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)