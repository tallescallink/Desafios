num = int(input("Qual é o seu número?\n"))

if num % 4 ==0:
        print("Su número é múltiplo de 4")
elif num % 2 == 0:
        print("Seu número é par")
else:
    print("Seu número é ímpar")
check = int(input('Digite um número para dividir:'))

if num % check == 0:
    print("Divide")
else:
    print("Não divide!")