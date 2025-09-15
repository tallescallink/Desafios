def calcular_digitos_cpf(cpf: str):
    # pega apenas os 9 primeiros dígitos
    cpf_numeros = [int(x) for x in cpf[:9]]

    # 1º dígito
    soma = sum([cpf_numeros[i] * (10 - i) for i in range(9)])
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    # 2º dígito
    cpf_numeros.append(digito1)
    soma = sum([cpf_numeros[i] * (11 - i) for i in range(10)])
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    return f"{digito1}{digito2}"

# --- Testando ---
cpf_pessoa = input("Digite os 9 primeiros dígitos do CPF: ")
digitos = calcular_digitos_cpf(cpf_pessoa)
print("CPF completo:", cpf_pessoa + digitos)
