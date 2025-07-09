from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:uninter@localhost:3306/TrailerLukinhas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(30), unique=True, nullable=False)
    mesa = db.Column(db.String(10))
    soma = db.Column(db.Float, default=0.0)
    estado = db.Column(db.String(20), default='mesa')
    pedido = db.Column(db.Text, default='[]')
    nome = db.Column(db.String(100))

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
    numero = data.get('From') or data.get('from')
    mensagem = data.get('Body') or data.get('body', '').strip().lower()

    cliente = Cliente.query.filter_by(numero=numero).first()
    if not cliente:
        cliente = Cliente(numero=numero, soma=0.0, pedido='[]', estado='mesa', mesa=None, nome=None)
        db.session.add(cliente)
        db.session.commit()
        resposta = "Olá! Bem-vindo ao Trailer do Lukinhas!\nPor favor, informe o número da sua mesa:"
    else:
        if cliente.estado == 'mesa':
            if mensagem.isdigit():
                cliente.mesa = mensagem
                cliente.estado = 'nome'
                db.session.commit()
                resposta = "Agora, por favor, informe seu nome:"
            else:
                resposta = "Por favor, informe apenas o número da mesa."
        elif cliente.estado == 'nome':
            cliente.nome = data.get('Body') or data.get('body', '').strip()
            cliente.estado = 'menu'
            db.session.commit()
            resposta = f"Obrigado, {cliente.nome}! Digite 1 para ver o cardápio."
        elif cliente.estado == 'menu':
            if mensagem == '1':
                resposta = (
                    "CARDÁPIO:\n"
                    "1 - Espeto\n"
                    "2 - Porção\n"
                    "3 - Salgado\n"
                    "4 - Refrigerante\n"
                    "5 - Cerveja\n"
                    "6 - Copão\n"
                    "7 - Lanches:\n"
                    "0 - Finalizar pedido\n"
                    "Digite o número da categoria desejada."
                )
            elif mensagem == '2':
                cliente.estado = 'porcao'
                db.session.commit()
                resposta = (
                    "Porções:\n"
                    "1 - Batata Frita (R$20)\n"
                    "2 - Salgados Fritos (coxinha e bolinha de queijo) (R$18)\n"
                    "Digite o número da porção desejada."
                )
            elif mensagem == '1':
                cliente.estado = 'espeto'
                db.session.commit()
                resposta = (
                    "Espetos:\n"
                    "1 - Frango (R$8)\n"
                    "2 - Carne (R$8)\n"
                    "3 - Cafta (R$10)\n"
                    "4 - Cafta com Queijo (R$10)\n"
                    "5 - Queijo Coalho (R$10)\n"
                    "6 - Coração (R$10)\n"
                    "Digite o número do espeto desejado."
                )
            elif mensagem == '3':
                cliente.estado = 'salgado'
                db.session.commit()
                resposta = (
                    "Salgados:\n"
                    "1 - Coxinha (R$8)\n"
                    "2 - Esfirra de Frango (R$8)\n"
                    "3 - Esfirra de Frango/c Catupiry (R$8)\n"
                    "4 - Risoli (R$8)\n"
                    "5 - Bolinho de Carne (R$8)\n"
                    "6 - Enroladinho de Salsicha (R$8)\n"
                    "Digite o número do salgado desejado."
                )
            elif mensagem == '4':
                cliente.estado = 'refrigerante'
                db.session.commit()
                resposta = (
                    "Refrigerantes:\n"
                    "1 - Guaraná Lata (R$6)\n"
                    "2 - Fanta Laranja Lata (R$6)\n"
                    "3 - Fanta Uva Lata (R$6)\n"
                    "4 - Sprite Lata (R$6)\n"
                    "5 - Coca-Cola Lata (R$6)\n"
                    "6 - Coca-Cola Zero Lata (R$6)\n"
                    "7 - Coca-Cola Ks (R$5)\n"
                    "Digite o número do refrigerante desejado."
                )
            elif mensagem == '5':
                cliente.estado = 'cerveja'
                db.session.commit()
                resposta = (
                    "Cervejas:\n"
                    "1 - Original 269ml (R$5)\n"
                    "2 - Imperio 269ml (R$5)\n"
                    "3 - Original 300ml (R$5)\n"
                    "4 - Skol 350ml (R$5)\n"
                    "5 - Heineken long neck  (R$10)\n"
                    "6 - Skol 600ml (R$12)\n"
                    "7 - Imperio 600ml (R$12)\n"
                    "8 - Original 600ml (R$15)\n"
                    "9 - Heineken 600(R$15)\n"
                    "Digite o número da cerveja desejada."
                )
            elif mensagem == '6':
                cliente.estado = 'copao'
                db.session.commit()
                resposta = (
                    "Copão:\n"
                    "1 - Copão de Gin (R$10)\n"
                    "2 - Gin de Melancia (R$10)\n"
                    "3 - Gin de Maça-Verde (R$10)\n"
                    "4 - Gin Tropical (R$10)\n"
                    "5 - Passaport (R$20)\n"
                    "6 - Passaport Honey (R$25)\n"
                    "7 - Passaport Aplle (R$25)\n"
                    "8 - Cavalo Branco (R$20)\n"
                    "9 - Red Label (R$25)\n"
                    "10 - Jack Daniels (R$40)\n"
                    "11 - Jack Daniels Honey (R$45)\n"
                    "Digite o número do copão desejado."
                )
            
            elif mensagem == '7':
                cliente.estado = 'lanches'
                db.session.commit()
                resposta = (                    "Lanches:\n"
                    "1 - X-Burguer (R$20)\n"
                    "2 - X-Salada (R$22)\n"
                    "3 - X-Bacon (R$22)\n"
                    "Digite o número do lanche desejado."
                )
            elif mensagem == '0':
                resposta = f"Mesa: {cliente.mesa}\nSeu pedido: {json.loads(cliente.pedido)}\nTotal: R$ {cliente.soma:.2f}\nObrigado!"
                db.session.delete(cliente)
                db.session.commit()
                return jsonify({"response": resposta})
            else:
                resposta = "Opção inválida. Digite 1 para ver o cardápio."
        elif cliente.estado == 'espeto':
            opcoes = [
                ("Frango", 8), ("Carne", 8), ("Cafta", 10), ("Cafta com Queijo", 10),
                ("Queijo Coalho", 10), ("Coração", 10)
            ]
            try:
                idx = int(mensagem) - 1
                nome, preco = opcoes[idx]
                cliente.soma += preco
                pedido = json.loads(cliente.pedido)
                pedido.append(f"Espeto de {nome} - R$ {preco},00")
                cliente.pedido = json.dumps(pedido)
                db.session.commit()
                resposta = f"Espeto de {nome} adicionado! Digite 1 para ver o cardápio ou 0 para finalizar."
                cliente.estado = 'menu'
            except:
                resposta = "Opção inválida. Digite novamente o número do espeto."
        elif cliente.estado == 'porcao':
            opcoes = [("Batata Frita", 20), ("Salgados Fritos", 18)]
            try:
                idx = int(mensagem) - 1
                nome, preco = opcoes[idx]
                cliente.soma += preco
                pedido = json.loads(cliente.pedido)
                pedido.append(f"Porção de {nome} - R$ {preco},00")
                cliente.pedido = json.dumps(pedido)
                db.session.commit()
                resposta = f"Porção de {nome} adicionada! Digite 1 para ver o cardápio ou 0 para finalizar."
                cliente.estado = 'menu'
            except:
                resposta = "Opção inválida. Digite novamente o número da porção."
        elif cliente.estado == 'salgado':
            opcoes = [
                ("Coxinha", 8), ("Esfirra de Frango", 8), ("Esfirra de Frango/c Catupiry", 8),
                ("Risoli", 8), ("Bolinho de Carne", 8), ("Enroladinho Salsicha", 8)
            ]
            try:
                idx = int(mensagem) - 1
                nome, preco = opcoes[idx]
                cliente.soma += preco
                pedido = json.loads(cliente.pedido)
                pedido.append(f"{nome} - R$ {preco},00")
                cliente.pedido = json.dumps(pedido)
                db.session.commit()
                resposta = f"{nome} adicionado! Digite 1 para ver o cardápio ou 0 para finalizar."
                cliente.estado = 'menu'
            except:
                resposta = "Opção inválida. Digite novamente o número do salgado."
        elif cliente.estado == 'refrigerante':
            opcoes = [
                ("Guaraná Lata", 6), ("Fanta Lata", 6), ("Sprite Lata", 6), ("Coca-Cola Ks", 10),
                ("Guaraná Ks", 10), ("Coca-Cola 2L", 15), ("Guaraná 2L", 12)
            ]
            try:
                idx = int(mensagem) - 1
                nome, preco = opcoes[idx]
                cliente.soma += preco
                pedido = json.loads(cliente.pedido)
                pedido.append(f"{nome} - R$ {preco},00")
                cliente.pedido = json.dumps(pedido)
                db.session.commit()
                resposta = f"{nome} adicionado! Digite 1 para ver o cardápio ou 0 para finalizar."
                cliente.estado = 'menu'
            except:
                resposta = "Opção inválida. Digite novamente o número do refrigerante."
        elif cliente.estado == 'cerveja':
            opcoes = [
                ("Original 269ml", 5), ("Imperio 269ml", 5), ("Original 300ml", 5), ("Skol 300ml", 5),
                ("Heiniken Long Neck", 10), ("Skol 600ml", 12), ("Imperio 600ml", 12),("Original 600ml", 15),
                ("Heiniken 600ml", 15)
            ]
            try:
                idx = int(mensagem) - 1
                nome, preco = opcoes[idx]
                cliente.soma += preco
                pedido = json.loads(cliente.pedido)
                pedido.append(f"Cerveja {nome} - R$ {preco},00")
                cliente.pedido = json.dumps(pedido)
                db.session.commit()
                resposta = f"Cerveja {nome} adicionada! Digite 1 para ver o cardápio ou 0 para finalizar."
                cliente.estado = 'menu'
            except:
                resposta = "Opção inválida. Digite novamente o número da cerveja."
        elif cliente.estado == 'copao':
            opcoes = [
                ("Copão de Gin", 10), ("Gin de Melancia", 10), ("Gin de Maça-Verde", 10), ("Gin Tropical", 10),
                ("Passaport", 20), ("Passaport Honey", 25), ("Passaport Apple", 25), ("Cavalo Branco", 20),
                ("Red Label", 25), ("Jack Daniels", 40), ("Jack Daniels Honey", 40)
            ]
            try:
                idx = int(mensagem) - 1
                nome, preco = opcoes[idx]
                cliente.soma += preco
                pedido = json.loads(cliente.pedido)
                pedido.append(f"{nome} - R$ {preco},00")
                cliente.pedido = json.dumps(pedido)
                db.session.commit()
                resposta = f"{nome} adicionado! Digite 1 para ver o cardápio ou 0 para finalizar."
                cliente.estado = 'menu'
            except:
                resposta = "Opção inválida. Digite novamente o número do copão."
        elif cliente.estado == 'lanches':
            opcoes = [
                ("X-Burguer", 20), ("X-Salada", 22), ("X-Bacon", 22)
            ]
            try:
                idx = int(mensagem) - 1
                nome, preco = opcoes[idx]
                cliente.soma += preco
                pedido = json.loads(cliente.pedido)
                pedido.append(f"{nome} - R$ {preco},00")
                cliente.pedido = json.dumps(pedido)
                db.session.commit()
                resposta = f"{nome} adicionado! Digite 1 para ver o cardápio ou 0 para finalizar."
                cliente.estado = 'menu'
            except:
                resposta = "Opção inválida. Digite novamente o número do lanche."

    return jsonify({"response": resposta})
@app.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    clientes_list = []
    for cliente in clientes:
        clientes_list.append({
            "id": cliente.id,
            "numero": cliente.numero,
            "mesa": cliente.mesa,
            "soma": cliente.soma,
            "estado": cliente.estado,
            "pedido": json.loads(cliente.pedido),
            "nome": cliente.nome
        })
    return jsonify(clientes_list)
@app.route('/cliente/<int:id>', methods=['GET'])
def obter_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"error": "Cliente não encontrado"}), 404
    return jsonify({
        "id": cliente.id,
        "numero": cliente.numero,
        "mesa": cliente.mesa,
        "soma": cliente.soma,
        "estado": cliente.estado,
        "pedido": json.loads(cliente.pedido),
        "nome": cliente.nome
    })

if __name__ == '__main__':
    print("Servidor Flask rodando! Use o endereço do ngrok para conectar seu webhook do WhatsApp.")

    app.run(host="0.0.0.0", port=5000)
