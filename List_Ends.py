import secrets

def user_list(x, y):
    lista = [secrets.randbelow(y - x + 1) + x for i in range(5)]
    print('Lista completa:', lista)
    nova_lista = [lista[0], lista [-1]]
    return nova_lista
print('Primeiro e último número da lista são:', user_list(1, 50))






def lista_do_usuario():
    lista = []
    for i in range(5):    
        num_do_usuario = int(input('Digite 5 números: '))
        lista.append(num_do_usuario)
    print('Lista completa:', lista)    
    nova_lista = [lista[0], lista [-1]]
    return nova_lista
print('Primeiro e último número da lista são: ', lista_do_usuario())

# USANDO TRY CATCH
def lista_do_usuario():
    lista = []
    while len(lista) < 5:
        try:
            num_do_usuario = int(input(f'Digite o número {len(lista)+1} de 5: '))
            
            if num_do_usuario < 1 or num_do_usuario > 100: # se ele não está entre 1 ou 100
                print('Número inválido! Digite um número entre 1 e 100.')
                continue  # volta para pedir o número novamente
            
            if num_do_usuario in lista: # se ele já existe
                print('Número repetido! Digite outro número.')
                continue  # volta para pedir outro número
            
            lista.append(num_do_usuario) # Adiciona na lista
        
        except ValueError:
            print('Isso não é um número! Digite um número entre 1 e 100.')

    print('Lista completa:', lista)
    nova_lista = [lista[0], lista[-1]]
    return nova_lista

print('Primeiro e último número da lista são:', lista_do_usuario())
