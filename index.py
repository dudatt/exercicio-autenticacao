import json
import bcrypt
import getpass
import sys
import os

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
    permissao = []
     
    print("1 - Conceder permissões")
    print("2 - Voltar") #fazer voltar pro começo
    resp = input()
        
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

    users = adicionarUserJson(users, username, hashSenha)

    for user in users:
        if user["Username"] != username: 
            print("Usuário cadastrado com sucesso!")
            salvarUserJson(users, arquivoUsers)
            criarPermissiosJson()
        else:
            print("----------------------")
            print("Usuário já cadastrado.")
            sys.exit()

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
    elif resp == "2":
        autenticarUsuario()
        while True:
            print("----------------------")
            print("Comandos disponíveis: ")
            print("1 - Criar arquivo")
            print("2 - Ler arquivo")
            print("3 - Excluir arquivo")
            print("4 - Voltar")
            print("----------------------")
            resp = input()
            print("----------------------")

            if resp == "1":
                escreverArquivo(criarArquivo())
            elif resp == "2":
                lerArquivo()
            elif resp == "3":
                excluirArquivo()
            elif resp == "4":
                break
            else:
                print("Comando inválido.")
    elif resp == "3":
        print("Até mais!")
        sys.exit()
    else:
        print("Comando inválido.")