class Cliente:

    clientes = []

    def __init__(self, endereco):
        self.endereco = endereco
        self.contas_do_cliente = []

    def listar_clientes():
        for cliente in Cliente.clientes:
            print(f"\n>>> {str(cliente)}")

    def filtrar_cliente():
        cpf = input("\n>>> Informe o CPF (somente números): ")
        for pessoa in Cliente.clientes:
            if pessoa._cpf == cpf:
                return pessoa
        else:
            return f"\n>>> CPF não encontrado."


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento

        # checa se o CPF ja está registrado em clientes.
        # Se não estiver(cliente novo portanto), registra o novo cliente
        if not PessoaFisica.cpf_existe(cpf):
            PessoaFisica.clientes.append(self)
        else:
            print(
                "\n>>> Não foi possível concluir o cadastro. Esse CPF ja está cadastrado."
            )

    def __str__(self):
        contas_info = "\n".join(str(conta) for conta in self.contas_do_cliente)
        return f"\n>>> Nome: {self._nome}   CPF: {self._cpf}\n>>> Contas:\n>>> {contas_info}\n"

    def cadastro_cliente():
        cpf = input("\n>>> Informe o CPF (somente números): ")
        data_nascimento = input(">>> Informe a data de nascimento: ")
        nome_cliente = input(">>> Informe o nome do cliente: ")
        endereco = input(
            ">>> Informe o endereço completo (logradouro, nro - bairro - cidade/sigla estado): "
        )

        cliente = PessoaFisica(nome_cliente, cpf, data_nascimento, endereco)
        print(f"\n>>> Cliente {cliente._nome} cadastrado com sucesso.")
        return cliente

    @classmethod
    def cpf_existe(cls, cpf):
        # verifica se CPF ja existe no cadastro de clientes. O código comentado
        # também poderia ser usado. O código abaixo nao comentado significa o mesmo
        # for pessoa in cls.clientes:
        #     if pessoa._cpf == cpf:
        #         return True
        # else:
        #     return False
        return any(pessoa._cpf == cpf for pessoa in cls.clientes)

    @property
    def get_nome(self):
        return self._nome

    @property
    def get_cpf(self):
        return self._cpf

    @property
    def get_data_nascimento(self):
        return self._data_nascimento

    @property
    def get_contas(self):
        return self.contas_do_cliente


class Conta:

    contas_do_banco = []
    total_de_contas = 1
    saque_solicitado = False
    deposito_solicitado = False

    def __init__(self, cliente):
        if cliente:
            self._saldo = 0
            self._agencia = "0001"
            self._numero = Conta.total_de_contas
            self._cliente = cliente
            self._cpf = cliente._cpf
            self._extrato = ""
            self._numero_saques = 0
            self._limite_de_saques = 3
            self._limite_por_saque = 500
            cliente.contas_do_cliente.append(self)
            print(
                f"\n>>> Conta nr {self._numero} aberta com sucesso para o CPF {cliente._cpf}."
            )
            self.contas_do_banco.append(self)
            Conta.total_de_contas += 1
        else:
            print(f"\n>>> CPF não encontrado.")

    def abrir_nova_conta():
        cliente = Cliente.filtrar_cliente()
        Conta(cliente)

    def verificar_conta():
        cliente_filtrado = Cliente.filtrar_cliente()

        if cliente_filtrado:
            for cliente in Cliente.clientes:
                if cliente.contas_do_cliente:
                    cpf = cliente_filtrado._cpf
                    for conta in Conta.contas_do_banco:
                        if conta._cpf == cpf:
                            print("\n>>> Cliente encontrado e possui conta(s).")
                            print(cliente_filtrado._cpf)
                            return conta
                    else:
                        return False

                else:
                    print("\n>>> Cliente encontrado, mas não possui conta.")
                    return False

        else:
            # Se nenhum cliente com o CPF informado for encontrado retorna falso
            print(f"\n>>> CPF não encontrado.")
            return False

    def depositar(self, valor_depositado):
        self._saldo += valor_depositado
        self.deposito_solicitado = True
        print(
            f"\n>>> Você depositou R$ {valor_depositado:.2f} com sucesso.\n>>> Seu saldo atual é de R$ {self._saldo:.2f}"
        )

    def checar_deposito():
        conta_verificada = Conta.verificar_conta()

        if conta_verificada:
            valor_deposito = input("\n>>> Valor a ser depositado: ")
            if is_number(valor_deposito):

                valor_deposito_validado = float(valor_deposito)

                if valor_deposito_validado > 0:
                    conta_verificada.depositar(valor_deposito_validado)
                    conta_verificada.atualizar_extrato(valor_deposito_validado)

                else:
                    return "\n>>> Valor para deposito inválido."

            else:
                return "\n>>> Valor para deposito inválido."
        else:
            return

    def sacar(self, valor_sacado):
        self._saldo -= valor_sacado
        self.saque_solicitado = True
        print(
            f"\n>>> Você sacou R$ {valor_sacado:.2f} com sucesso.\n>>> Seu saldo atual é de R$ {self._saldo:.2f}"
        )
        self._numero_saques += 1

    def checar_saque():
        conta_verificada = Conta.verificar_conta()
        if conta_verificada:
            valor_saque = input("\n>>> Valor que deseja sacar: ")

            if is_number(valor_saque):
                valor_saque_validado = float(valor_saque)

            if valor_saque_validado > conta_verificada._saldo:
                print("\n>>> Saque não realizado. Saldo insuficiente.")

            elif valor_saque_validado > conta_verificada._limite_por_saque:
                print("\n>>> Saque não realizado. Valor excede o limite por operação.")

            elif valor_saque_validado <= 0:
                print("\n>>> Saque não realizado. Valor informado é inválido.")

            elif conta_verificada._numero_saques >= conta_verificada._limite_de_saques:
                print("\n>>> Saque não realizado. Número máximo de saques já foi atingido.")

            else:
                conta_verificada.sacar(valor_saque_validado)
                conta_verificada.atualizar_extrato(valor_saque_validado)
        else:
            return

    def atualizar_extrato(self, valor):

        if self.deposito_solicitado == True:
            self._extrato += f"Depósito: + R$ {valor:.2f}\n"
            self.deposito_solicitado = False

        if self.saque_solicitado == True:
            self._extrato += f"Saque: - R$ {valor:.2f}\n"
            self.saque_solicitado = False

    def exibir_extrato():
        conta_verificada = Conta.verificar_conta()
        if conta_verificada:
            titulo_extrato = " EXTRATO ".center(41, "=")
            print()
            print(titulo_extrato)
            print()
            print(
                "\nNão foram realizadas movimentações."
                if not conta_verificada._extrato
                else conta_verificada._extrato
            )
            print(f"\nSaldo: R$ {conta_verificada._saldo:,.2f}")
            print()
            rodape_extrato = "=".center(41, "=")
            print(rodape_extrato)

    def __str__(self):
        return f"Agencia: {self._agencia} Conta: {self._numero}\n"


class ContaCorrente(Conta): ...


def menu():
    menu = f"""
    {" MENU ".center(41, "=")}

    Escolha a opção desejada e pressione enter:\n
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Abrir nova conta (se ja possuir CPF cadastrado)
    [5] Listar suas contas
    [6] Cadastro de novo Cliente/CPF
    [7] Sair
    
    Opção: """

    return input(menu)


def checar_opcao(n):
    if n.isdigit():
        n = int(n)
        if 0 < n < 8:
            return n

        else:
            return "Número inválido"

    else:
        return "Opção inválida"


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def main():

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
                Conta.checar_deposito()

            # opção referente ao saque
            elif opcao_validada == 2:
                Conta.checar_saque()

            # exibir extrato
            elif opcao_validada == 3:
                Conta.exibir_extrato()

            # abrir nova conta
            elif opcao_validada == 4:
                Conta.abrir_nova_conta()

            # listar contas
            elif opcao_validada == 5:
                print(Cliente.filtrar_cliente())

            # cadastrar novo usuário
            elif opcao_validada == 6:
                PessoaFisica.cadastro_cliente()

            # sair
            elif opcao_validada == 7:
                break


if __name__ == "__main__":
    main()
