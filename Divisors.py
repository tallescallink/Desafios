

num = int(input('Digite um número de 1 a 100: \n'))
divisores = [i for i in range(1, num + 1) 
                        if num % i == 0]
print(*divisores, sep=', ')