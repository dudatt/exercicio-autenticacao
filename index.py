import json
import bcrypt
import getpass
import sys
import os

def adicionarUserJson(users, username, senha):
    usuarioNovo = {"Username": username, "Password": senha};
    users.append(usuarioNovo);
    return users

def salvarUserJson(users, arquivo):
    with open(arquivo, 'w') as f:
        json.dump(users, f, indent=4);

def adicionarPermissaoJson(permissoes, username):
    permissoesNovas = {"Username": username, "Permissions": permissoes};
    permissoes.append(permissoesNovas);
    return permissoes

def salvarPermissaoJson(permissoes, arquivo):
    with open(arquivo, 'w') as f:
        json.dump(permissoes, f, indent=4);

def cadastrarUsuario():
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

    for user in users:
        if user["Username"] == username:
            print("Usuário já cadastrado.")

    users = adicionarUserJson(users, username, hashSenha)
    salvarUserJson(users, arquivoUsers)
    print("Usuário cadastrado com sucesso!")
    print("----------------------")

def autenticarUsuario():
    loginUser = input("Digite seu nome de usuário: ")
    loginSenha = input("Digite sua senha: ")

    arquivoUsersDados = "usuarios.json"
    with open(arquivoUsersDados, 'r') as f:
        users = json.load(f)

    for user in users:
        if user["Username"] != loginUser:
            print("Usuário não encontrado.")
            sys.exit();
        else: #user["Username"] == loginUser:
            if bcrypt.checkpw(loginSenha.encode(), user["Password"].encode()): #confirmação direta
                print("Usuário autenticado com sucesso!")
                print(f"Seja bem-vindo(a) {user["Username"]}!");
                return loginUser
            else: #loginSenha != bcrypt.checkpw(loginSenha.encode(), user["Password"].encode()): #confirmação com tentativas
                for i in range(5):
                    i += 1;

                    if bcrypt.checkpw(loginSenha.encode(), user["Password"].encode()):
                        print("Usuário autenticado com sucesso!")
                        print(f"Seja bem-vindo(a) {user["Username"]}!");
                        return loginUser
                    else:
                        print(f"Senha incorreta. Tente novamente. Total de tentativas ({i}/5)");
                        print("----------------------")
                        loginSenha = input("Insira sua senha: ");
                        if i == 5:
                            print("Tentativas máximas alcançadas. Tente novamente mais tarde.");
                            sys.exit();

def criarArquivo():
        nomeArquivo = input("Digite o nome do arquivo: ")
        try:
            with open(nomeArquivo, 'w') as f:
                print(f"Arquivo {nomeArquivo} criado com sucesso!")
                return nomeArquivo
        except PermissionError:
            print("Você não tem permissão para criar o arquivo.")

def escreverArquivo(arquivo):
    try:
        with open(arquivo, 'a') as f:
            conteudo = input("Digite o conteúdo que deseja escrever: ")
            f.write(conteudo)
            print(f"Conteúdo adicionado ao arquivo {arquivo} com sucesso!")
    except FileNotFoundError:
        print(f"Arquivo {arquivo} não encontrado.")
    except PermissionError:
        print(f"Você não tem permissão para escrever no arquivo {arquivo}.")
     
def lerArquivo():
    nomeArquivo = input("Digite o nome do arquivo que deseja ler: ")
    try:
        with open(nomeArquivo, 'r') as f:
            conteudo = f.read()
            print(f"Conteúdo do arquivo {nomeArquivo}:")
            print(conteudo)
    except FileNotFoundError:
        print(f"Arquivo {nomeArquivo} não encontrado.")

def excluirArquivo():
    nomeArquivo = input("Digite o nome do arquivo que deseja excluir: ")
    try:
        os.remove(nomeArquivo)
        print(f"Arquivo {nomeArquivo} excluído com sucesso!")
    except FileNotFoundError:
        print(f"Arquivo {nomeArquivo} não encontrado.")
    except PermissionError:
        print(f"Você não tem permissão para excluir o arquivo {nomeArquivo}.")

while True:
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
        continue
    elif resp == "2":
        usuario = autenticarUsuario()
        arquivoPermissoes = "permissoes.json"
        with open(arquivoPermissoes, 'r') as f:
            arqPermissoes = json.load(f)

        while True:
            usuarioEncontrado = False
            for permissao in arqPermissoes:
                if permissao["Username"] == usuario:
                    usuarioEncontrado = True
                    print("----------------------")
                    print(f"Comandos disponíveis para {usuario}: ")
                    for j in permissao["Permissions"]:
                        perm = j
                        if perm == "w":
                            print("1 - Criar arquivo")
                        elif perm == "r":
                            print("2 - ler arquivo")
                        elif perm == "d":
                            print("3 - Excluir arquivo")
                        
                    resp = input("Digite uma opção ou digite '4' para encerrar: ")
                    print("----------------------")
                    if resp == "1":
                        escreverArquivo(criarArquivo())
                    elif resp == "2":
                        lerArquivo()
                    elif resp == "3":
                        excluirArquivo()
                    elif resp == "4":
                        print("Até mais!")
                        sys.exit()
                    else:
                        print("Comando inválido.")
            if not usuarioEncontrado:
                print("Usuário não possui permissões.")
                continue 
            
    elif resp == "3":
        print("Até mais!")
        sys.exit()
    else:
        print("Comando inválido.")