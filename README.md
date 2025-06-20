# ChatBot.Lanches
Criado Para poupar o tempo de responder varias msg ao mesmo tempo
# chatBot1.py
# Chatbot simples para simular um cardápio de lanches no terminal
# chatBot1.py
# Chatbot simples para simular um cardápio de lanches no terminal
import sys

soma = 0.00
pedido = []
nome = input('Digite seu nome: ')
mesa = int(input('Digite o número da mesa: '))


def mostrar_pedido_lista():
    print('')
    print('cliente:', nome)
    print('mesa:', mesa)
    print(20 * '-' + 'PEDIDO' + 20 * '-')
    if not pedido:
        print("Nenhum item foi pedido.")
        return
    print("\nItens do seu pedido:")
    for idx, item in enumerate(pedido, 1):
        print(f"{idx}. {item}")
    print(f"Total: R$ {soma:.2f}")
    
def Cardapio():
    print(20* '-' + 'CARDÁPIO' + 20*'-')
    print('|' + 18*' ' +'1 - Espeto' + 18*' ' + '|')
    print('|' + 18*' ' +'2 - Porção' + 18*' ' + '|')
    print('|' + 18*' ' +'3 - Salgado' + 17*' ' + '|')
    print('|' + 18*' ' +'4 - Refrigerante' + 12*' ' + '|')
    print('|' + 18*' ' +'5 - Cervejas' + 16*' ' + '|')
    print('|' + 18*' ' +'6 - Copão' + 19*' ' + '|')
    print('|' + 18*' ' +'7 - Sair' + 20*' ' + '|')
    print(48*'-')

def Espeto():
    global soma
    print("Você escolheu Espeto!")
    print("1 - Espeto de Frango - R$ 10,00")
    print("2 - Espeto de Carne - R$ 10,00")
    print("3 - Espeto de Cafta - R$ 10,00")
    print("4 - Espeto de Cafta com Queijo - R$ 10,00")
    print("5 - Espeto de Queijo Coalho - R$ 10,00")
    print("6 - Espeto de Coração - R$ 10,00")
    escolha = input("Digite o número do espeto desejado:  ")
    if escolha == '1':
        soma += 10.00
        pedido.append("Espeto de Frango - R$ 10,00")
    elif escolha == '2':
        soma += 10.00
        pedido.append("Espeto de Carne - R$ 10,00")
    elif escolha == '3':
        soma += 10.00
        pedido.append("Espeto de Cafta - R$ 10,00")
    elif escolha == '4':
        soma += 10.00
        pedido.append("Espeto de Cafta com Queijo - R$ 10,00")
    elif escolha == '5':
        soma += 10.00
        pedido.append("Espeto de Queijo Coalho - R$ 10,00")
    elif escolha == '6':
        soma += 10.00
        pedido.append("Espeto de Coração - R$ 10,00")
    else:
        print("Opção inválida. Tente novamente.")
        return

def Porção():
    global soma
    print("Você escolheu Porção!")
    print("1 - Porção de Batata Frita - R$ 20,00")
    print("2 - Salgadinhos Fritos - R$ 20,00")
    escolha = input("Digite o número da porção desejada:  ")
    if escolha == '1':
        soma += 20.00
        pedido.append("Porção de Batata Frita - R$ 20,00")
    elif escolha == '2':
        soma += 20.00
        pedido.append("Porção de Salgadinhos fritos - R$ 20,00")
    else:
        print('Opção inválida. Tente novamente.')
        return

def Salgado():
    global soma
    print("Você escolheu Salgado!")
    print("1 - Coxinha - R$ 8,00")
    print("2 - Esfirra de frango - R$ 8,00")
    print("3 - Esfirra de frango/c Catupiry - R$ 8,00")
    print("4 - Risoli - R$ 8,00")
    print("5 - Kibe - R$ 8,00")
    print("6 - Hamburgão - R$ 8,00")
    escolha = input("Digite o número do Salgado desejado: ")
    if escolha == '1':
        soma += 8.00
        pedido.append("Coxinha - R$ 8,00")
    elif escolha == '2':
        soma += 8.00
        pedido.append("Esfirra de Frango - R$ 8,00")
    elif escolha == '3':
        soma += 8.00
        pedido.append("Esfirra de Frango/c Catupiry - R$ 8,00")
    elif escolha == '4':
        soma += 8.00
        pedido.append("Risoli - R$ 8,00")
    elif escolha == '5':
        soma += 8.00
        pedido.append("Kibe - R$ 8,00")
    elif escolha == '6':
        soma += 8.00
        pedido.append("Hamburgão - R$ 8,00")
    else:
        print("Opção inválida. Tente novamente.")
        return

def Refrigerante():
    global soma
    print("Você escolheu Refrigerante!")
    print("1 - Guaraná Lata - R$ 6,00")
    print("2 - Fanta Lata - R$ 6,00")
    print("3 - Sprite Lata - R$ 6,00")
    print("4 - Coca-Cola Ks - R$ 10,00")
    print("5 - Guaraná Ks - R$ 10,00")
    print("6 - Coca-Cola 2L - R$ 15,00")
    print("7 - Guaraná 2L - R$ 12,00")
    escolha = input("Digite o número do refrigerante desejado: ")
    if escolha == '1':
        soma += 6.00
        pedido.append("Guaraná Lata - R$ 6,00")
    elif escolha == '2':
        soma += 6.00
        pedido.append("Fanta Lata - R$ 6,00")
    elif escolha == '3':
        soma += 6.00
        pedido.append("Sprite Lata - R$ 6,00")
    elif escolha == '4':
        soma += 10.00
        pedido.append("Coca-Cola Ks - R$ 10,00")
    elif escolha == '5':
        soma += 10.00
        pedido.append("Guaraná Ks - R$ 10,00")
    elif escolha == '6':
        soma += 15.00
        pedido.append("Coca-Cola 2L - R$ 15,00")
    elif escolha == '7':
        soma += 12.00
        pedido.append("Guaraná 2L - R$ 12,00")
    else:
        print('Opção inválida. Tente novamente.')
        return

def Cervejas():
    global soma
    print('Você escolheu Cervejas!')
    print('1 - Cerveja Skol 300ml - R$ 5,00')
    print('2 - Cerveja Original 300ml - R$ 5,00')
    print('3 - Cerveja Brahma 300ml - R$ 5,00')
    print('4 - Cerveja Skol Lata - R$ 8,00')
    print('5 - Cerveja Original Lata - R$ 8,00')
    print('6 - Cerveja Brahma Lata - R$ 8,00')
    print('7 - Cerveja Imperio Lata - R$ 8,00')
    print('8 - Cerveja Imperio 600ml - R$ 12,00')
    print('9 - Cerveja Skol 600ml - R$ 12,00')
    print('10 - Cerveja Original 600ml - R$ 12,00')
    print('11 - Cerveja Brahma 600ml - R$ 12,00')
    print('12 - Cerveja Heiniken 600ml - R$ 15,00')
    escolha = input('Digite o número da cerveja desejada: ')
    if escolha == '1':
        soma += 5.00
        pedido.append("Cerveja Skol 300ml - R$ 5,00")
    elif escolha == '2':
        soma += 5.00
        pedido.append("Cerveja Original 300ml - R$ 5,00")
    elif escolha == '3':
        soma += 5.00
        pedido.append("Cerveja Brahma 300ml - R$ 5,00")
    elif escolha == '4':
        soma += 8.00
        pedido.append("Cerveja Skol Lata - R$ 8,00")
    elif escolha == '5':
        soma += 8.00
        pedido.append("Cerveja Original Lata - R$ 8,00")
    elif escolha == '6':
        soma += 8.00
        pedido.append("Cerveja Brahma Lata - R$ 8,00")
    elif escolha == '7':
        soma += 8.00
        pedido.append("Cerveja Imperio Lata - R$ 8,00")
    elif escolha == '8':
        soma += 12.00
        pedido.append("Cerveja Imperio 600ml - R$ 12,00")
    elif escolha == '9':
        soma += 12.00
        pedido.append("Cerveja Skol 600ml - R$ 12,00")
    elif escolha == '10':
        soma += 12.00
        pedido.append("Cerveja Original 600ml - R$ 12,00")
    elif escolha == '11':
        soma += 12.00
        pedido.append("Cerveja Brahma 600ml - R$ 12,00")
    elif escolha == '12':
        soma += 15.00
        pedido.append("Cerveja Heiniken 600ml - R$ 15,00")
    else:
        print('Opção inválida. Tente novamente.')
        return

def Copão():
    global soma
    print('Você escolheu Copão! ')
    print('1 - Copão de Gin - R$ 15,00')
    print('2 - Gin de Melancia - R$ 15,00')
    print('3 - Gin de Maça-Verde - R$ 15,00')
    print('4 - Gin Tropical - R$ 15,00')
    print('5 - Whisky - R$ 15,00')
    print('6 - Whisky Maça-Verde - R$ 15,00')
    print('7 - Whisky De Mel - R$ 15,00')
    print('8 - Cavalo Branco - R$ 20,00')
    print('9 - Red Label - R$ 25,00')
    print('10 - Jack Daniels - R$ 30,00')
    escolha = input('Digite o número do copão desejado: ')
    if escolha == '1':
        soma += 15.00
        pedido.append("Copão de Gin - R$ 15,00")
    elif escolha == '2':
        soma += 15.00
        pedido.append("Gin de Melancia - R$ 15,00")
    elif escolha == '3':
        soma += 15.00
        pedido.append("Gin de Maça-Verde - R$ 15,00")
    elif escolha == '4':
        soma += 15.00
        pedido.append("Gin Tropical - R$ 15,00")
    elif escolha == '5':
        soma += 15.00
        pedido.append("Whisky - R$ 15,00")
    elif escolha == '6':
        soma += 15.00
        pedido.append("Whisky Maça-Verde - R$ 15,00")
    elif escolha == '7':
        soma += 15.00
        pedido.append("Whisky De Mel - R$ 15,00")
    elif escolha == '8':
        soma += 20.00
        pedido.append("Cavalo Branco - R$ 20,00")
    elif escolha == '9':
        soma += 25.00
        pedido.append("Red Label - R$ 25,00")
    elif escolha == '10':
        soma += 30.00
        pedido.append("Jack Daniels - R$ 30,00")
    else:
        print('Opção inválida. Tente novamente.')
        return

def Sair():
    print("Obrigado por usar o chatbot! Até a próxima!")
    sys.exit()




nome = nome.strip().title()
print(f"Olá {nome}, bem-vindo ao Trailer do Lukinhas!")
print(f"Seu número de mesa é: {mesa}")
print("Aqui está o nosso cardápio:")
Cardapio()
while True:
    escolha = input('Digite o que você deseja: ')
    if escolha == '1':
        Espeto()
    elif escolha == '2':
        Porção()
    elif escolha == '3':
        Salgado()
    elif escolha == '4':
        Refrigerante()
    elif escolha == '5':
        Cervejas()
    elif escolha == '6':
        Copão()
    elif escolha == '7':
        Sair()
    else:
        print("Opção inválida. Tente novamente.")
        continue

   while True:
        continuar = input('Deseja pedir mais alguma coisa? (S/N): ').strip().upper()
        if continuar == 'S':
            Cardapio()
            break
        elif continuar == 'N':
            mostrar_pedido_lista()
            print('Obrigado por comprar no Trailer do Lukinhas. Volte sempre!')
            sys.exit()
        else:
            print("Opção inválida. Tente novamente.")

