import random, secrets

def user_list(x, y):
    lista = [secrets.randbelow(y - x + 1) + x for i in range(5)]
    print('Lista completa:', lista)

    nova_lista = [lista[0], lista [-1]]
    return nova_lista

print('Primeeiro e último número da lista são:', user_list(1, 50))






def lista_do_usuario():
    lista = []
    for i in range(5):    
        num_do_usuario = int(input('Digite 5 números: '))
        lista.append(num_do_usuario)
    print('Lista completa:', lista)    
    nova_lista = [lista[0], lista [-1]]
    return nova_lista
print('Primeiro e último número da lista são: ', lista_do_usuario())


