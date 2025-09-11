#List_Example: a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]


a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
for num in a:
    if num <=5:
        print(f'{num} - O número é igual ou menor que 5!')

meneores_ou_iguais_a_5 = [num for num in a 
                                if num <=5 ] #then
print('Números menores ou iguais a 5:', *meneores_ou_iguais_a_5, sep=', ')



# Pegar números do usúario e voltar apenas números menores que o dele da lista original
a = a
user_number = int(input('Digite um número: '))
menores_ou_iguais_a_user_number = [num for num in a 
                                if num <= user_number ] #then
print('Números menores ou iguais a', user_number, ':', *menores_ou_iguais_a_user_number, sep=', ')


a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
print(*[num for num in a if num <= int(input('Digite um número: '))], sep=', ')