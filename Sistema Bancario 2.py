from time import sleep
from random import randint
contas, entradas, saidas = [], 0, 0
menu = 'p'
usuario = "x"

# Dados com os títulos e chaves nomeadas com o CPF do usuário
usuario = {
    "dados": ["CPF", "Nome", "Data de Nascimento", "Endereço", "Cidade", "Estado", "Senha", "Conta"],
    "01357809425": ["013.578.094-25", "Igor Augusto", "15/01/1988", "Rua da Lavadeira, 56", "Olinda", "PE", "123456", "002536-9"],
}

conta_corrente = {
    "dados": ["cpf", "saldo", "depositos", "saques", "SaquesDiarios", "LimiteSaque", "TipoConta", "Status", "Entradas", "Saídas"],
    "002536-9": ["01357809425", 0, 0, 0, 3, 500, "UniConta", "Ativa", 0, 0]
}

movimentos = {
    "dados": [],
    "002536-9": []
}


def geraConta():
    return str(randint(111111, 999999))+"-"+str(randint(0, 9))


def opcoes():
    opcao = str(input('''
********** MENU PRINCIPAL **********
            
[ e ] Extrato de Transações
[ d ] Depósito
[ s ] Saque
[ c ] Sobre sua Conta
[ x ] Fechar o sistema

Digite a opção desejada => '''))
    return opcao


print("""
** Sistema Bancário Iniciado **
      v2.1 - 02/09/2023
      
Para acessar sua conta e ver suas movimentações,
digite seu usuário a seguir, logo depois insira
sua senha ou crie seu cadastro para ter acesso.
""")

while True:
    # Digitar o CPF para buscar
    cpf_busca = str(input("Digite o CPF: "))
    while len(cpf_busca) != 11:
        print("CPF inválido! Tente novamente.")
        cpf_busca = str(input("Digite o CPF: "))

    if (usuario.get(cpf_busca)) == None:
        inputcadastro = str(input(
            f'\nUsuário {cpf_busca} não encontrado.\nDeseja realizar este cadastro? S/N: ')).upper()
        if inputcadastro == "S":
            cad_cpf = cpf_busca[0:3]+"."+cpf_busca[3:6] + \
                "."+cpf_busca[6:9]+"-"+cpf_busca[9:11]
            print(f"Vamos criar um novo cadastro para {cad_cpf}:")
            cad_lista = [cpf_busca, str(input("\nNome do Cliente: ")), str(input("\nData de Nascimento (xx/xx/xxxx): ")),
                         str(input("\nEndereço: ")), str(input("\nCidade: ")), str(input("\nEstado: ")),
                         str(input("\nCrie uma senha: "))]
            print(f"\nO usuário é {cpf_busca}.")
            print("Gerando sua conta...")
            while True:
                c = geraConta()
                if c in contas == True:
                    c = geraConta()
                    print(".")
                else:
                    cad_lista.append(c)
                    contas.append(c)
                    usuario[cpf_busca] = cad_lista
                    conta_corrente[c] = [cpf_busca, 0, 0, 0, 0, 3, 500, "UniConta", "Ativa"]
                    break
            print(
                f"\nOlá, {cad_lista[1]}!\nSeu cadastro foi realizado com sucesso!\nSua conta é {c}\nTente acessar o sistema novamente.\n")
            print(usuario[cpf_busca])
        elif inputcadastro == "N":
            print("Para acessar o sistema você precisa ter um cadastro.\n")
        else:
            print("Digite uma opção válida\n")
    else:
        print(f"Bem vindo(a), {usuario[cpf_busca][1]}")
        #print(f"Senha da conta: {usuario[cpf_busca][6]}\n")
        s = str(input("Digite sua senha: "))
        if s == usuario[cpf_busca][6]:
            print("Carregando opções...")
            sleep(2)
            logUser = cpf_busca
            logConta = usuario[logUser][7]
            break
        else:
            menu = "x"
            print("Senha incorreta. Seu acesso foi encerrado.")
            break


while menu != 'x':
    # Exibe as opções disponíveis
    menu = opcoes()

    # Depositar dinheiro
    if menu == 'd':
        Depositar_Valor = 0
        while True:
            Depositar_Valor = float(input('''
********** DEPOSITAR **********

Utilize esta opção para inserir
dinheiro em sua conta.
                                          
Para voltar ao menu principal
        digite 0
                                     
Digite o valor a ser depositado: R$ '''))
            if Depositar_Valor > 0:
                print(
                    f'\n\nProcessando depósito no valor de R${Depositar_Valor:.2f}...')
                conta_corrente[logConta][2] += 1 #quantidades
                conta_corrente[logConta][1] += Depositar_Valor #valor ao saldo
                movimentos[logConta].append('Depósito') #adiciona ao movimento
                movimentos[logConta].append(Depositar_Valor) #adiciona o valor ao movimento
                conta_corrente[logConta][8] += Depositar_Valor
                sleep(2)
                print(
                    '\nDepósito confirmado!\nO valor já está disponível em sua conta.\nAcesse o Extrato para mais informações.')
                sleep(2)
            else:
                print('Retornando ao menu principal...')
                sleep(2)
            break

    # Sacar dinheiro
    elif menu == 's':
        Sacar_Valor = 0
        while True:
            Sacar_Valor = float(input(f'''
********** SACAR **********

Utilize esta opção para retirar
dinheiro de sua conta.
                                          
Para voltar ao menu principal
        digite 0
                                      
Saldo atual: R$ {conta_corrente[logConta][1]:.2f}
                                     
Digite o valor a ser retirado: R$ '''))
            if Sacar_Valor > 0:
                print(
                    f'\n\nProcessando saque no valor de R${Sacar_Valor:.2f}...')
                if conta_corrente[logConta][3] <= conta_corrente[logConta][4]:
                    sleep(1)
                    if Sacar_Valor <= conta_corrente[logConta][5]:
                        sleep(1)
                        if Sacar_Valor <= conta_corrente[logConta][1]:
                            conta_corrente[logConta][3] += 1
                            conta_corrente[logConta][1] -= Sacar_Valor
                            movimentos[logConta].append('Saque')
                            movimentos[logConta].append(Sacar_Valor)
                            print(
                                '\nSaque confirmado!\nAcesse o Extrato para mais informações.')
                            sleep(2)
                            conta_corrente[logConta][9] += Sacar_Valor
                        else:
                            print(
                                f'\nSaldo insuficiente para realizar o saque de R$ {Sacar_Valor:.2f}')
                    else:
                        print(
                            '\nVocê está tentando sacar um valor maior que o permitido para sua conta.')
                else:
                    print(
                        '\nVocê atingiu o limite de saques diários permitidos para sua conta.')

            else:
                print('Retornando ao menu principal...')
                sleep(2)
            break

    # Extrato de movimentações
    elif menu == 'e':
        print('''
************ EXTRATO ************

Todas as movimentações de entrada e
saída da sua conta aparecem aqui.

''')
        sleep(1)
        # Checa se há movimentações na conta para exibir
        if len(movimentos[logConta]) > 0:

            # Listar as movimentações Dep/Saq
            for m in range(1, len(movimentos[logConta]), 2):
                if movimentos[logConta][m-1] == 'Depósito':
                    print(f'{movimentos[logConta][m-1]}: {movimentos[logConta][m]:.2f}+')
                else:
                    print(f'{movimentos[logConta][m-1]}: {movimentos[logConta][m]:.2f}-')

            print(f'''\nSaldo atual: R$ {conta_corrente[logConta][1]:.2f}

Fim do extrato.

''')
            sleep(2)

        else:
            print('\nNão houve movimentação.')
            print('''

Fim do extrato.

''')
            sleep(2)

    # Dados da Conta
    elif menu == 'c':
        print(f'''
********** MINHA CONTA **********

Sua conta está ATIVADA!
              
Operações realizadas na data de hoje
Depósitos: {conta_corrente[logConta][2]}
Saques: {conta_corrente[logConta][3]} de {conta_corrente[logConta][4]}

Saldo atual: R$ {conta_corrente[logConta][1]:.2f}

Balanço:
Entradas R$ {conta_corrente[logConta][8]:.2f} x R$ {conta_corrente[logConta][9]:.2f} Saídas

Lembre-se que sua conta tem limite de
R${conta_corrente[logConta][5]:.2f} por saque. Valores acima disso
não serão aceitos pelo sistema do banco.''')
        if conta_corrente[logConta][3] >= conta_corrente[logConta][4]:
            print('Você já atingiu seu limite diário de saques.\n\n\n')
        sleep(5)

    # Encerrar o sistema
    elif menu == 'x':
        print('\nObrigado por utilizar nossos serviços.\nSeu acesso foi encerrado. Até a próxima!\n')

    # Nenhuma das opções válidas
    else:
        print('Não foi digitada uma opção válida! Tente novamente.\n')
