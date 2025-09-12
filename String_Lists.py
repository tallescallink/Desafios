v1 = str(input('Digite alguma coisa: '))
v1_invertida = v1[::-1]

if v1 == v1_invertida: #then
    print('É um palíndromo!')
else:
    print('Não é um palíndromo!')


string = "example"
for c in string: 
        print ("one letter: " + c, sep=', ')
        