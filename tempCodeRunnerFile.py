import random, secrets

def user_list(x, y):
    lista = [secrets.randint(x,y) for i in range(5)]
    print('Lista completa:', lista)

    nova_lista = [lista[0], lista [-1]]
    return nova_lista

print('Primeeiro e último número da lista são:', user_list(1, 50))

