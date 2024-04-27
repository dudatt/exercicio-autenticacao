import json
import bcrypt
import getpass
import sys
import os

def adicionarUsuarioJson(users, username, senha):
    usuarioNovo = {"Username": username, "Password": senha};
    users.append(usuarioNovo);
    return users

def salvarDadosUsuariosJson(users, arquivo):
    with open(arquivo, 'w') as f:
        json.dump(users, f, indent=4);

def adicionarPermissaoUsuarioJson(permissoes, username):
    arquivoUsuarios = "usuarios.json"
    with open(arquivoUsuarios, 'r') as f:
        arqUsuarios = json.load(f)

    username = arqUsuarios["Username"]

    UsuariosPermissoesNovas = {"Username": username, "Permissions": permissoes};
    permissoes.append(UsuariosPermissoesNovas);
    return permissoes

def salvarPermissaoUsuarioJson(permissoes, arquivo):
    with open(arquivo, 'w') as f:
        json.dump(permissoes, f, indent=4);

def cadastrarUsuario():
    username = input("Digite seu nome de usuário: ")
    senha = input("Digite sua nova senha: ")

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
            sys.exit()

    users = adicionarUsuarioJson(users, username, hashSenha)
    salvarDadosUsuariosJson(users, arquivoUsers)
    print("Usuário cadastrado com sucesso!")
    print("----------------------")

def autenticarUsuario():
    loginUser = input("Digite seu nome de usuário: ")
    loginSenha = getpass.getpass("Digite sua senha: ")
    print("----------------------")

    arquivoUsersDados = "usuarios.json"
    try:
        with open(arquivoUsersDados, 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []

    import sys

    for user in users:
        if user["Username"] == loginUser:
            if bcrypt.checkpw(loginSenha.encode(), user["Password"].encode()): # confirmação direta
                print("Usuário autenticado com sucesso!")
                print(f"Seja bem-vindo(a) {user['Username']}!")
                return loginUser
            else:
                for i in range(1, 6):
                    print(f"Tentativa {i}/5:")
                    loginSenha = input("Insira sua senha: ")
                    if bcrypt.checkpw(loginSenha.encode(), user["Password"].encode()):
                        print("Usuário autenticado com sucesso!")
                        print(f"Seja bem-vindo(a) {user['Username']}!")
                        return loginUser
                    else:
                        if i == 5:
                            print("Tentativas máximas alcançadas. Tente novamente mais tarde.")
                            sys.exit()
                        else:
                            print("Senha incorreta. Tente novamente.")
                            print("----------------------")
                break
    else:
        print("Usuário não encontrado.")
        sys.exit()

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
    print("2 - Entrar")
    print("3 - Sair")
    print("----------------------")
    resp = input()
    print("----------------------")

    if resp == "1":
        cadastrarUsuario()
    elif resp == "2":
        usuario = autenticarUsuario()

        arquivoPermissoes = "permissoes.json"
        with open(arquivoPermissoes, 'r') as f:
            arqPermissoes = json.load(f)

        while True:
            usuarioEncontrado = False
            for userEncontrado in arqPermissoes:
                if userEncontrado["Username"] == usuario:
                    usuarioEncontrado = True
                    print("----------------------")
                    print(f"Comandos disponíveis para {usuario}: ")
                    print("1 - Criar arquivo")
                    print("2 - Ler arquivo")
                    print("3 - Excluir arquivo")
                    print("4 - Sair")
                    resp = input("Digite uma opção: ")
                    print("----------------------")
                    for permissao in userEncontrado["Permissions"]:
                        tiposPermissoes = permissao
                        if tiposPermissoes not in ["w", "r", "d"]:
                            print("Permissão inválida.")
                            break
                        elif resp == "1" and tiposPermissoes == "w":
                            if "w" in userEncontrado["Permissions"]:
                                escreverArquivo(criarArquivo())
                            else:
                                print("Sem permissão para criar arquivo.")
                            break
                        elif resp == "2" and tiposPermissoes == "r":
                            if "r" in userEncontrado["Permissions"]:
                                lerArquivo()
                            else:
                                print("Sem permissão para ler arquivo.")
                            break
                        elif resp == "3" and tiposPermissoes == "d":
                            if "d" in userEncontrado["Permissions"]:
                                excluirArquivo()
                            else:
                                print("Sem permissão para excluir arquivo.")
                            break
                    else:
                        if resp == "4":
                            print("Até mais!")
                            sys.exit()
                        else:
                            print("Sem permissão para executar o comando.")
                    break
            if not usuarioEncontrado:
                print("Usuário não encontrado ou não possui permissões.")
                continue
             
    elif resp == "3":
        print("Até mais!")
        sys.exit()
    else:
        print("Comando inválido.")