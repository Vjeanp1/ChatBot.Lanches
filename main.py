# chatBot1.py
# Chatbot simples para simular um cardápio de lanches no terminal
from flask import flask, request, jsonify

app = Flask(__name__)

# Dicionário para armazenar sessões dos usuários
usuarios = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    numero = data.get('from')
    mensagem = data.get('body', '').strip().lower()

    if numero not in usuarios:
        usuarios[numero] = {'soma': 0.0, 'pedido': [], 'estado': 'menu'}
        resposta = "Olá! Bem-vindo ao Trailer do Lukinhas!\nDigite 1 para ver o cardápio."
    else:
        user = usuarios[numero]
        if user.get('estado') == 'menu':
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
                user['estado'] = 'porcao'
                resposta = (
                    "Porções:\n"
                    "1 - Batata Frita (R$20)\n"
                    "2 - Salgadinhos Fritos (R$20)\n"
                    "Digite o número da porção desejada."
                )
            elif mensagem == '1':
                user['estado'] = 'espeto'
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
                user['estado'] = 'salgado'
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
                user['estado'] = 'refrigerante'
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
                user['estado'] = 'cerveja'
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
                user['estado'] = 'copao'
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
                resposta = f"Seu pedido: {user['pedido']}\nTotal: R$ {user['soma']:.2f}\nObrigado!"
                usuarios.pop(numero)
            else:
                resposta = "Opção inválida. Digite 1 para ver o cardápio."
        elif user.get('estado') == 'espeto':
            opcoes = [
                ("Frango", 10), ("Carne", 10), ("Cafta", 10), ("Cafta com Queijo", 10),
                ("Queijo Coalho", 10), ("Coração", 10)
            ]
            try:
                idx = int(mensagem) - 1
                nome, preco = opcoes[idx]
                user['soma'] += preco
                user['pedido'].append(f"Espeto de {nome} - R$ {preco},00")
                resposta = f"Espeto de {nome} adicionado! Digite 1 para ver o cardápio ou 0 para finalizar."
                user['estado'] = 'menu'
            except:
                resposta = "Opção inválida. Digite novamente o número do espeto."
        elif user.get('estado') == 'porcao':
            opcoes = [("Batata Frita", 20), ("Salgadinhos Fritos", 20)]
            try:
                idx = int(mensagem) - 1
                nome, preco = opcoes[idx]
                user['soma'] += preco
                user['pedido'].append(f"Porção de {nome} - R$ {preco},00")
                resposta = f"Porção de {nome} adicionada! Digite 1 para ver o cardápio ou 0 para finalizar."
                user['estado'] = 'menu'
            except:
                resposta = "Opção inválida. Digite novamente o número da porção."
        elif user.get('estado') == 'salgado':
            opcoes = [
                ("Coxinha", 8), ("Esfirra de Frango", 8), ("Esfirra de Frango/c Catupiry", 8),
                ("Risoli", 8), ("Kibe", 8), ("Hamburgão", 8)
            ]
            try:
                idx = int(mensagem) - 1
                nome, preco = opcoes[idx]
                user['soma'] += preco
                user['pedido'].append(f"{nome} - R$ {preco},00")
                resposta = f"{nome} adicionado! Digite 1 para ver o cardápio ou 0 para finalizar."
                user['estado'] = 'menu'
            except:
                resposta = "Opção inválida. Digite novamente o número do salgado."
        elif user.get('estado') == 'refrigerante':
            opcoes = [
                ("Guaraná Lata", 6), ("Fanta Lata", 6), ("Sprite Lata", 6), ("Coca-Cola Ks", 10),
                ("Guaraná Ks", 10), ("Coca-Cola 2L", 15), ("Guaraná 2L", 12)
            ]
            try:
                idx = int(mensagem) - 1
                nome, preco = opcoes[idx]
                user['soma'] += preco
                user['pedido'].append(f"{nome} - R$ {preco},00")
                resposta = f"{nome} adicionado! Digite 1 para ver o cardápio ou 0 para finalizar."
                user['estado'] = 'menu'
            except:
                resposta = "Opção inválida. Digite novamente o número do refrigerante."
        elif user.get('estado') == 'cerveja':
            opcoes = [
                ("Skol 300ml", 5), ("Original 300ml", 5), ("Brahma 300ml", 5), ("Skol Lata", 8),
                ("Original Lata", 8), ("Brahma Lata", 8), ("Imperio Lata", 8), ("Imperio 600ml", 12),
                ("Skol 600ml", 12), ("Original 600ml", 12), ("Brahma 600ml", 12), ("Heiniken 600ml", 15)
            ]
            try:
                idx = int(mensagem) - 1
                nome, preco = opcoes[idx]
                user['soma'] += preco
                user['pedido'].append(f"Cerveja {nome} - R$ {preco},00")
                resposta = f"Cerveja {nome} adicionada! Digite 1 para ver o cardápio ou 0 para finalizar."
                user['estado'] = 'menu'
            except:
                resposta = "Opção inválida. Digite novamente o número da cerveja."
        elif user.get('estado') == 'copao':
            opcoes = [
                ("Copão de Gin", 15), ("Gin de Melancia", 15), ("Gin de Maça-Verde", 15), ("Gin Tropical", 15),
                ("Whisky", 15), ("Whisky Maça-Verde", 15), ("Whisky De Mel", 15), ("Cavalo Branco", 20),
                ("Red Label", 25), ("Jack Daniels", 30)
            ]
            try:
                idx = int(mensagem) - 1
                nome, preco = opcoes[idx]
                user['soma'] += preco
                user['pedido'].append(f"{nome} - R$ {preco},00")
                resposta = f"{nome} adicionado! Digite 1 para ver o cardápio ou 0 para finalizar."
                user['estado'] = 'menu'
            except:
                resposta = "Opção inválida. Digite novamente o número do copão."
        else:
            resposta = "Opção inválida. Digite 1 para ver o cardápio."

    return jsonify({"reply": resposta})

if __name__ == '__main__':
    app.run(port=5000)

