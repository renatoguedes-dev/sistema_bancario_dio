menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
 
=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        valor_deposito = float(input("Valor a ser depositado: "))
        if valor_deposito > 0:
            saldo += valor_deposito
            extrato += f"Depósito: + R$ {valor_deposito:.2f}\n"
            print(f"\nVocê depositou R$ {valor_deposito:.2f} com sucesso.")
        
        else:
            print("\nOperação falhou! O valor informado é inválido.")

    elif opcao == "s":
        valor_saque = float(input("Valor que deseja sacar: "))
        
        if valor_saque > saldo:
            print("\nSaque não realizado. Saldo insuficiente.")

        elif valor_saque > limite:
            print("\nSaque não realizado. Valor excede o limite por operação.")

        elif numero_saques >= 3:
            print("\nSaque não realizado. Número máximo de saques já foi atingido.")
         
        elif valor_saque > 0 and valor_saque <= saldo:
            numero_saques += 1
            saldo -= valor_saque
            extrato += f"Saque: - R$ {valor_saque:.2f}\n"
            print(f"\nVocê sacou R$ {valor_saque:.2f} com sucesso.")
        
        else:
            print("\nOperação não concluída. Algo deu errado.")
    
    elif opcao == "e":
        titulo_extrato = " EXTRATO ".center(41, "=")
        print()
        print(titulo_extrato)
        print()
        print("\nNão foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:,.2f}")
        print()
        rodape_extrato = "=".center(41, "=")
        print(rodape_extrato)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")


