a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
menores_ou_iguais_a_5 = [num for num in a 
                        if num <=5 ] #then
print('Números menores ou iguais a 5:', *menores_ou_iguais_a_5, sep=', ')