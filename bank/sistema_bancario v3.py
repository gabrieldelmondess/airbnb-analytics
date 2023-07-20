import bcrypt
import os 
diretorio = os.getcwd()
print("Diretório:", diretorio)

class Usuario:
    def __init__(self, nome, cpf, renda_mensal):
        self.nome = nome
        self.cpf = cpf
        self.renda_mensal = renda_mensal

class Conta: 
    def __init__ (self, numero, tipo, saldo, senha, usuario):
        self.numero = numero
        self.tipo = tipo
        self.saldo = saldo
        self.usuario = usuario
        self.senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())

    def verificar_senha(self, senha):
        return bcrypt.checkpw(senha.encode(), self.senha_hash)

class SistemaBancario:
    def __init__(self):
        self.contas = []
        self.usuarios = []
        self.saldo = 0
        self.limite = 1000
        self.extrato = ""
        self.numero_saques = 0
        self.limite_saques = 5
        self.usuario_logado = None

    def exibir_menu(self):
        while True:
            menu = """
            [c] Criar conta
            [u] Cadastrar usuário
            [l] Login
            [d] Depositar
            [s] Sacar
            [t] Transferir 
            [e] Extrato
            [x] Logoff
            [q] Sair

            => """

            opcao = input(menu)

            if opcao == "c":
                self.criar_conta()
            elif opcao == "u":
                self.criar_usuario()
            elif opcao == "l":
                self.realizar_login()
            elif opcao == "d":
                self.depositar()
            elif opcao == "s":
                self.sacar()
            elif opcao == "t":
                self.transferir()
            elif opcao == "x":
                self.logoff()
            elif opcao == "e":
                self.exibir_extrato()
            elif opcao == "q":
                print("Saindo do sistema...")
                break
            else:
                print("Operação inválida. Por favor, selecione uma nova função")

    def criar_usuario(self):
        nome = input("Insira o seu nome: ")
        cpf = input("Insira o seu CPF: ")
        renda_mensal = float(input("Informe a sua renda mensal: "))

        usuario = Usuario(nome, cpf, renda_mensal)
        self.usuarios.append(usuario)
        print("Usuário cadastrado com sucesso!")

    def criar_conta(self):
        if len(self.usuarios) == 0:
            print("Operação falhou! Não existem usuários cadastrados no sistema")
            return

        cpf_usuario = input("Por favor, digite o seu CPF para verificação: ")

        verificar_usuario = None
        for usuario in self.usuarios:
            if usuario.cpf == cpf_usuario:
                verificar_usuario = usuario
                break

        if verificar_usuario:
            numero_conta = input("Digite o número da sua conta: ")
            tipo_conta = input("Selecione o tipo da conta: ")
            senha = input("Digite a sua senha: ")

            conta = Conta(numero_conta, tipo_conta, 0, senha, verificar_usuario)
            self.contas.append(conta)
            print("Conta criada com sucesso!")
        else:
            print("Desculpe, erro inesperado.")

    def realizar_login(self):
        numero_conta_login = input("Digite o número da sua conta: ")
        senha_login = input("Por favor, digite a sua senha: ")

        verificar_login = None

        for conta in self.contas:
            if conta.numero == numero_conta_login and conta.verificar_senha(senha_login):
                self.usuario_logado = conta.usuario
                print(f"Seja bem-vindo, {self.usuario_logado.nome}")
                return

        print("Credenciais incorretas. Tente novamente.")

    def depositar(self):
        if not self.usuario_logado:
            print("Operação falhou! Nenhum usuário está conectado.")
            return
        valor = float(input("Insira o valor que deseja depositar: "))
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito efetuado no valor de R$ {valor:.2f}\n"
            print("Depósito efetuado com sucesso!")
        else:
            print("Operação falhou: Valor inválido para depósito")

    def sacar(self):
        if not self.usuario_logado:
            print("Operação falhou! Nenhum usuário está conectado.")
            return
        valor = float(input("Insira o valor que deseja sacar: "))

        sem_saldo = valor > self.saldo
        sem_limite = valor > self.limite
        sem_saque = self.numero_saques >= self.limite_saques

        if sem_saldo:
            print("Operação falhou: Sem saldo disponível")
        elif sem_limite:
            print("Operação falhou: Sem limite disponível")
        elif sem_saque:
            print("Operação falhou: O usuário excedeu o limite de saque")
        elif valor > 0:
            self.saldo -= valor
            self.extrato += f"Saque efetuado no valor de R$ {valor:.2f}\n"
            self.numero_saques += 1
            print("Saque efetuado com sucesso")
        else:
            print("Operação falhou: Valor inválido para saque")

    def exibir_extrato(self):
        print("\n============= EXTRATO =============")
        if not self.extrato:
            print("Não foram realizadas operações.")
        else:
            print(self.extrato)
        print(f"\nSaldo: R$ {self.saldo:.2f}")
        print("===================================")
    
    def logoff(self):
        if self.usuario_logado:
            print(f"Usuário {self.usuario_logado.nome} foi desconectado.")

            self.usuario_logado = None
        else:
            print("Operação falhou! Nenhum usuário está conectado.")

    def transferir(self):
        if not self.usuario_logado:
            print("Operação falhou! Nenhum usuário está conectado.")
            return
        conta_origem = self.encontrar_conta_usuario(self.usuario_logado)

        if not conta_origem:
            print("Operação falhou! Conta do usuário não foi encontrada.")
            return
        
        numero_conta_origem = input("Digite o número da sua conta: ")
        conta_origem = self.encontrar_conta_destino(numero_conta_origem)
        if not conta_origem:
            print("Operação falhou! Conta não encontrada")
        
        conta_destino_numero = input("Digite o número da conta qual deseja transferir: ")

        conta_destino = self.encontrar_conta_destino(conta_destino_numero)

        if not conta_destino:
            print("Operação falhou! Conta de destino não encontrada, por favor digite novamente.")
            return
        
        valor = float(input("Digite o valor que deseja transferir: "))
        
        if valor > conta_origem.saldo:
            print("Operação falhou! Sem saldo para transferência.")
        else:

            conta_origem.saldo -= valor
            conta_destino.saldo += valor

        self.extrato += f"Transfência realizada no valor de R$ {valor:.2f} para a conta {conta_destino_numero}\n "
        print("Transferência realizada com sucesso!")

    def encontrar_conta_destino(self, numero_conta):
        for conta in self.contas:
            if conta.numero == numero_conta:
                return conta
        return None
    
    def encontrar_conta_usuario(self, usuario):
        for conta in self.contas:
            if conta.usuario == usuario:
                return conta
        return None

sistema_bancario = SistemaBancario()
sistema_bancario.exibir_menu()



