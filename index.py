import json
import bcrypt
import getpass
import sys
import os

# def criarUsuarioJson(username, senha): # cria o objeto usuário
#    return { "Username": username, "Password": senha }

def adicionarUserJson(users, username, senha): # adiciona o usuário na lista 
    usuarioNovo = {"Username": username, "Password": senha};
    users.append(usuarioNovo);
    return users

def salvarUserJson(users, arquivo): # salva a lista de usuários no arquivo json
    with open(arquivo, 'w') as f:
        json.dump(users, f, indent=4);

def criarPermissiosJson():
    arquivoUsersDados = "usuarios.json"
    with open(arquivoUsersDados, 'r') as f:
        users = json.load(f)

    arquivoPermissao = "permissoes.json"


    for i in range(3): #ver isso aq
        permissao = []
        resp1 = input("Digite a permissão que deseja conceder (r, w, x): ").lower()
        permissao.append(resp1)
        for j in range(2):
           resp2 = input("Mais alguma permissão? (S/N) ").upper()
            if resp2 == "N":
                break
            elif resp2 == "S":
                continue
            else:
                print("Opção inválida.")
                sys.exit()

    for user in users:
        userPermissao = {"Username": user["Username"], "Permissions": permissao}

    salvarUserJson(userPermissao, arquivoPermissao)

def cadastrarUsuario():
    while True:
        username = input("Digite seu nome de usuário: ")
        senha = getpass.getpass("Digite sua nova senha: ")

        salt = bcrypt.gensalt();
        hashSenha = bcrypt.hashpw(senha.encode(), salt);
        hashSenha = hashSenha.decode()

        arquivoUsers = "usuarios.json"

        try:
            with open(arquivoUsers, 'r') as file:
                users = json.load(file)
        except FileNotFoundError:
            users = []

        #criarUsuarioJson(username, hashSenha)
        users = adicionarUserJson(users, username, hashSenha)
        salvarUserJson(users, arquivoUsers)
        criarPermissiosJson()
        #darPermissao()
        print("Usuário cadastrado com sucesso!")
        print("----------------------")
        print("Deseja cadastrar outro usuário? (S/N)")
        resp = input().upper()
        print("----------------------")
        if resp == "N":
            return False
        elif resp == "S":
            continue

def autenticarUsuario():
    loginUser = input("Digite seu nome de usuário: ")
    loginSenha = input("Digite sua senha: ")

    arquivoUsersDados = "usuarios.json"
    with open(arquivoUsersDados, 'r') as f:
        users = json.load(f)

    for user in users:
        if user["Username"] == loginUser:
            if bcrypt.checkpw(loginSenha.encode(), user["Password"].encode()): #confirmação direta
                print("Usuário autenticado com sucesso!")
                return
            elif loginSenha != bcrypt.checkpw(loginSenha.encode(), user["Password"].encode()): #confirmação com tentativas
                for i in range(5):
                    i += 1;

                    if bcrypt.checkpw(loginSenha.encode(), user["Password"].encode()):
                        print(f"Seja bem-vindo(a) {user["Username"]}!");
                        break;
                    else:
                        print(f"Senha incorreta. Tente novamente. Total de tentativas ({i}/5)");
                        print("----------------------")
                        loginSenha = input("Insira sua senha: ");
                        if i == 5:
                            print("Tentativas máximas alcançadas. Tente novamente mais tarde.");
                            sys.exit();
        else:
            print("Usuário ou senha inválidos.")
            sys.exit();

def verificarPermissaoArquivo(arquivo): #rever isso dps
    
    arquivoUsersDados = "usuarios.json"
    with open(arquivoUsersDados, 'r') as f:
        users = json.load(f)

    for user in users:
        if user["Username"].access(arquivo, user["Username"].R_OK):
            print("Você tem permissão de leitura para o arquivo.")
        else:
            print("Você não tem permissão de leitura para o arquivo.")

        if user["Username"].access(arquivo, user["Username"].W_OK):
            print("Você tem permissão de escrita para o arquivo.")
        else:
            print("Você não tem permissão de escrita para o arquivo.")

        if user["Username"].access(arquivo, user["Username"].X_OK):
            print("Você tem permissão de execução para o arquivo.")
        else:
            print("Você não tem permissão de execução para o arquivo.")

def criarArquivo():
        nomeArquivo = input("Digite o nome do arquivo: ")
        try:
            with open(nomeArquivo, 'w') as f:
                print(f"Arquivo {nomeArquivo} criado com sucesso!")
        except PermissionError:
            print("Você não tem permissão para criar o arquivo.")

print("----------------------")
print("Escolha uma opção: ")
print("1 - Cadastrar")
print("2 - Autenticar")
print("3 - Sair")
print("----------------------")
resp = input()
print("----------------------")

if resp == "1":
    cadastrarUsuario()
elif resp == "2":
    autenticarUsuario()
    print("----------------------")
    print("Comandos disponíveis: ")
    print("1 - Criar arquivo")
    print("2 - Ler arquivo")
    print("3 - Excluir arquivo")
    print("4 - Executar arquivo") #extra
    print("5 - Sair")
    print("----------------------")
    resp = input()
    print("----------------------")
    if resp == "1":
        criarArquivo()
    elif resp == "2":
        print("Ler arquivo")
    elif resp == "3":
        print("Excluir arquivo")
    elif resp == "4":
        print("Executar arquivo")
    elif resp == "5":
        print("Até mais!")
        sys.exit()