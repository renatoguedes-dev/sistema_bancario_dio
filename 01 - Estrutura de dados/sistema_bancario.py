def menu():
    menu = f"""
    {" MENU ".center(41, "=")}

    Escolha a opção desejada e pressione enter:\n
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Abrir nova conta
    [5] Listar suas contas
    [6] Cadastro de novo usuário
    [7] Sair
    
    Opção: """
    
    return input(menu)

def depositar(saldo, valor_depositado, extrato):
    saldo += valor_depositado
    extrato += f"Depósito: + R$ {valor_depositado:.2f}\n"
    print(f"\n>>> Você depositou R$ {valor_depositado:.2f} com sucesso.")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, numero_saques):
    numero_saques += 1
    saldo -= valor
    extrato += f"Saque: - R$ {valor:.2f}\n"
    print(f"\nVocê sacou R$ {valor:.2f} com sucesso.")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    titulo_extrato = " EXTRATO ".center(41, "=")
    print()
    print(titulo_extrato)
    print()
    print("\nNão foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:,.2f}")
    print()
    rodape_extrato = "=".center(41, "=")
    print(rodape_extrato)

def abrir_conta(agencia, usuarios, contas):
    cpf_nova_conta = input("\n>>> Informe o CPF para o qual deseja abrir uma nova conta: ")

    if usuarios:
        for user in usuarios:
            if cpf_nova_conta == user["CPF"]:
                nova_conta = criar_nova_conta(contas)
                contas.append({"agencia": agencia, "numero_conta": nova_conta, "nome": user["Usuário"],"CPF Usuario": user["CPF"]})
                print(f"\n>>> Conta nr {nova_conta} aberta com sucesso para o CPF {user["CPF"]}.")
            
            else:
                print("\n>>> CPF não possui usuário cadastrado. Cadastre o usuário antes.")
    else:
        print("\n>>> CPF não possui usuário cadastrado. Cadastre o usuário antes.")

def criar_nova_conta(contas):
    
    if contas:
        ultima_conta = contas[-1]["numero_conta"]
        nova_conta = ultima_conta + 1
        return nova_conta
    else:
        return 1
    
def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Agência:\t{conta["agencia"]}
            C/C:\t\t{conta["numero_conta"]}
            Titular:\t{conta["nome"]}
            CPF:\t{conta["CPF Usuario"]}
        """
        
        print(linha)

def cadastro_usuario(usuarios):
    cpf = input("\n>>> Informe o CPF (somente números): ")
    data_nascimento = input(">>> Informe a data de nascimento: ")
    nome_usuario = input(">>> Informe o nome do usuário: ")
    endereco = input(">>> Informe o endereço completo (logradouro, nro - bairro - cidade/sigla estado): ")

    # verifica se a lista de usuarios está vazia ou ja possui algum cadastro
    if usuarios:
        for user in usuarios:
            if cpf == user["CPF"]:
                print("\n>>> Não foi possível concluir o cadastro. Esse CPF ja está cadastrado.")
                return usuarios
        
        # se não existir o cpf já cadastrado, segue com o cadastramento
        usuario = {
            "CPF": cpf,
            "Data de Nascimento": data_nascimento,
            "Usuário": nome_usuario,
            "Endereço": endereco,
        }
        usuarios.append(usuario)
        print("\n>>> Usuário cadastrado com sucesso.")
        return usuarios
    
    # cadastrar primeiro usuario
    else:
        usuario = {
            "CPF": cpf,
            "Data de Nascimento": data_nascimento,
            "Usuário": nome_usuario,
            "Endereço": endereco,
        }
        usuarios.append(usuario)
        print("\n>>> Usuário cadastrado com sucesso.")
        return usuarios


def checar_opcao(n):
    if n.isdigit():
        n = int(n)
        if 0 < n < 8:
            return n
        
        else:
            return "Número inválido"

    else:
        return "Opção inválida"

def checar_deposito():
    valor_deposito = input("\n>>> Valor a ser depositado: ")
    if is_number(valor_deposito):

        valor_deposito_validado = float(valor_deposito)

        if valor_deposito_validado > 0:
            return valor_deposito_validado
        
        else:
            return "Valor para deposito inválido."
    
    else:
        return "Valor para deposito inválido."
    
def checar_saque(saldo, limite, numero_saques, limite_saques):
    valor_saque = input("\n>>> Valor que deseja sacar: ")

    if is_number(valor_saque):
        valor_saque_validado = float(valor_saque)
        
        if valor_saque_validado > saldo:
            return "\n>>> Saque não realizado. Saldo insuficiente."

        elif valor_saque_validado > limite:
            return "\n>>> Saque não realizado. Valor excede o limite por operação."
        
        elif valor_saque_validado <= 0:
            return "\n>>> Saque não realizado. Valor informado é inválido."

        elif numero_saques >= limite_saques:
            return "\n>>> Saque não realizado. Número máximo de saques já foi atingido."
            
        else:
            return valor_saque_validado
    else:
        return "\n>>> Operação não concluída. Valor informado não é um número."

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def main():

    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    numero_saques = 0
    extrato = ""
    usuarios = []
    contas = []

    while True:

        # abrir menu e armazenar opção selecionada
        opcao = menu()

        # armazenar resultado da checagem se opção selecionada é valida ou não
        opcao_validada = checar_opcao(opcao)

        # opção invalida. Vai repetir o menu e solicitar opção novamente
        if opcao_validada == "Número inválido" or opcao_validada == "Opção inválida":
            print(f"\n>>> {opcao_validada}, tente novamente.")
            continue

        # opção valida. Dará prosseguimento à solicitação
        else:
            
            # opção referente ao deposito
            if opcao_validada == 1:
                valor_depositado = checar_deposito()
                if valor_depositado != "Valor para deposito inválido.":
                    saldo, extrato = depositar(saldo, valor_depositado, extrato)
                else:
                    print("\n>>> Operação não concluída. Valor para deposito inválido.")

            # opção referente ao saque
            elif opcao_validada == 2:
                valor_saque = checar_saque(saldo, limite, numero_saques, LIMITE_SAQUES)
                
                # ação caso saque foi validado corretamente
                if is_number(valor_saque):
                    saldo, extrato, numero_saques = sacar(
                        saldo=saldo, 
                        valor=valor_saque, 
                        extrato=extrato, 
                        numero_saques=numero_saques,
                    )
                
                # ação caso saque não tenha sido validado e tenha ocorrido algum erro.
                else:
                    print(valor_saque)
            
            # exibir extrato 
            elif opcao_validada == 3:
                exibir_extrato(saldo, extrato=extrato)


            elif opcao_validada == 4:
                abrir_conta(AGENCIA, usuarios, contas)
            
            elif opcao_validada == 5:
                listar_contas(contas)
            
            elif opcao_validada == 6:
                cadastro_usuario(usuarios)
            
            elif opcao_validada == 7:
                break
        
main()