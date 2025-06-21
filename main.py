# chatBot1.py
# Chatbot simples para simular um cardápio de lanches no terminal
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

# Configuração do MySQL (ajuste user, password, host, database)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:uninter@localhost:3306/TrailerLukinhas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(30), unique=True, nullable=False)
    mesa = db.Column(db.String(10))
    soma = db.Column(db.Float, default=0.0)
    estado = db.Column(db.String(20), default='mesa')
    pedido = db.Column(db.Text, default='[]')  # Salva como JSON string

# Para criar as tabelas (execute uma vez no início do projeto):
# with app.app_context():
#     db.create_all()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    numero = data.get('from')
    mensagem = data.get('body', '').strip().lower()

    cliente = Cliente.query.filter_by(numero=numero).first()
    if not cliente:
        cliente = Cliente(numero=numero, soma=0.0, pedido='[]', estado='mesa', mesa=None)
        db.session.add(cliente)
        db.session.commit()
        resposta = "Olá! Bem-vindo ao Trailer do Lukinhas!\nPor favor, informe o número da sua mesa:"
    else:
        if cliente.estado == 'mesa':
            if mensagem.isdigit():
                cliente.mesa = mensagem
                cliente.estado = 'menu'
                db.session.commit()
                resposta = "Digite 1 para ver o cardápio."
            else:
                resposta = "Por favor, informe apenas o número da mesa."
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
                    "0 - Finalizar pedido\n"
                    "Digite o número da categoria desejada."
                )
            elif mensagem == '2':
                cliente.estado = 'porcao'
                db.session.commit()
                resposta = (
                    "Porções:\n"
                    "1 - Batata Frita (R$20)\n"
                    "2 - Salgadinhos Fritos (R$20)\n"
                    "Digite o número da porção desejada."
                )
            elif mensagem == '1':
                cliente.estado = 'espeto'
                db.session.commit()
                resposta = (
                    "Espetos:\n"
                    "1 - Frango (R$10)\n"
                    "2 - Carne (R$10)\n"
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
                    "5 - Kibe (R$8)\n"
                    "6 - Hamburgão (R$8)\n"
                    "Digite o número do salgado desejado."
                )
            elif mensagem == '4':
                cliente.estado = 'refrigerante'
                db.session.commit()
                resposta = (
                    "Refrigerantes:\n"
                    "1 - Guaraná Lata (R$6)\n"
                    "2 - Fanta Lata (R$6)\n"
                    "3 - Sprite Lata (R$6)\n"
                    "4 - Coca-Cola Ks (R$10)\n"
                    "5 - Guaraná Ks (R$10)\n"
                    "6 - Coca-Cola 2L (R$15)\n"
                    "7 - Guaraná 2L (R$12)\n"
                    "Digite o número do refrigerante desejado."
                )
            elif mensagem == '5':
                cliente.estado = 'cerveja'
                db.session.commit()
                resposta = (
                    "Cervejas:\n"
                    "1 - Skol 300ml (R$5)\n"
                    "2 - Original 300ml (R$5)\n"
                    "3 - Brahma 300ml (R$5)\n"
                    "4 - Skol Lata (R$8)\n"
                    "5 - Original Lata (R$8)\n"
                    "6 - Brahma Lata (R$8)\n"
                    "7 - Imperio Lata (R$8)\n"
                    "8 - Imperio 600ml (R$12)\n"
                    "9 - Skol 600ml (R$12)\n"
                    "10 - Original 600ml (R$12)\n"
                    "11 - Brahma 600ml (R$12)\n"
                    "12 - Heiniken 600ml (R$15)\n"
                    "Digite o número da cerveja desejada."
                )
            elif mensagem == '6':
                cliente.estado = 'copao'
                db.session.commit()
                resposta = (
                    "Copão:\n"
                    "1 - Copão de Gin (R$15)\n"
                    "2 - Gin de Melancia (R$15)\n"
                    "3 - Gin de Maça-Verde (R$15)\n"
                    "4 - Gin Tropical (R$15)\n"
                    "5 - Whisky (R$15)\n"
                    "6 - Whisky Maça-Verde (R$15)\n"
                    "7 - Whisky De Mel (R$15)\n"
                    "8 - Cavalo Branco (R$20)\n"
                    "9 - Red Label (R$25)\n"
                    "10 - Jack Daniels (R$30)\n"
                    "Digite o número do copão desejado."
                )
            elif mensagem == '0':
                resposta = f"Mesa: {cliente.mesa}\nSeu pedido: {cliente.pedido}\nTotal: R$ {cliente.soma:.2f}\nObrigado!"
                db.session.delete(cliente)
                db.session.commit()
            else:
                resposta = "Opção inválida. Digite 1 para ver o cardápio."
        elif cliente.estado == 'espeto':
            opcoes = [
                ("Frango", 10), ("Carne", 10), ("Cafta", 10), ("Cafta com Queijo", 10),
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
            opcoes = [("Batata Frita", 20), ("Salgadinhos Fritos", 20)]
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
                ("Risoli", 8), ("Kibe", 8), ("Hamburgão", 8)
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
                ("Skol 300ml", 5), ("Original 300ml", 5), ("Brahma 300ml", 5), ("Skol Lata", 8),
                ("Original Lata", 8), ("Brahma Lata", 8), ("Imperio Lata", 8), ("Imperio 600ml", 12),
                ("Skol 600ml", 12), ("Original 600ml", 12), ("Brahma 600ml", 12), ("Heiniken 600ml", 15)
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
                ("Copão de Gin", 15), ("Gin de Melancia", 15), ("Gin de Maça-Verde", 15), ("Gin Tropical", 15),
                ("Whisky", 15), ("Whisky Maça-Verde", 15), ("Whisky De Mel", 15), ("Cavalo Branco", 20),
                ("Red Label", 25), ("Jack Daniels", 30)
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
        else:
            resposta = "Opção inválida. Digite 1 para ver o cardápio."

    return jsonify({"reply": resposta})

if __name__ == '__main__':
    app.run(port=5000)
