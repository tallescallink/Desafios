a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
print(*list(set(a) & set(b)), sep=', ') # Uma linha só de verdade 

# Listas originais
a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

# Solução sem duplicatas
c = list(set(num for num in a if num in b))
print('Números que aparecem em ambas as listas:', *c, sep=', ')

# Extra 1: Listas aleatórias
import random
a_random = [random.randint(1, 20) for _ in range(10)]
b_random = [random.randint(1, 20) for _ in range(12)]

print(f"Lista A: {a_random}")
print(f"Lista B: {b_random}")

c_random = list(set(num for num in a_random if num in b_random))
print('Elementos em comum:', *c_random, sep=', ')

# Extra 2: Uma linha só
resultado = list(set(num for num in a if num in b))
print('Em uma linha:', *resultado, sep=', ')




# c = [num for num in a 
#                     if num in b]
# print('Números que aparecem em ambas as listas:', *c, sep=', ')


# import random

# lista = [random.randint(1, 100) for _ in range(1)]
# print(lista)

# import secrets
# lista_segura = [secrets.randbelow(100) for _ in range(1)]
# print(lista)

