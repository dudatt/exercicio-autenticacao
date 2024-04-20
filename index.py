import json
import bcrypt
import getpass
import sys

global username 
global senha 
global loginUser
global loginSenha

def criarUsuarioJson(username, senha): # cria o objeto usuário
    return { "Username": username, "Password": senha }

def adicionarUserJson(users, username, senha): # adiciona o objeto usuário na lista 
    usuarioNovo = criarUsuarioJson(username, senha);
    users.append(usuarioNovo);

def salvarUserJson(users, arquivo): # salva a lista de usuários no arquivo json
    with open(arquivo, 'w') as f:
        json.dump(users, f);

def cadastrarUsuario():
    username = input("Digite seu nome de usuário: ")
    senha = getpass.getpass("Digite sua nova senha: ")

    salt = bcrypt.gensalt();
    hashSenha = bcrypt.hashpw(senha.encode(), salt);

    hashSenha = hashSenha.decode()

    users = []
    arquivoUsers = "usuarios.json"

    criarUsuarioJson(username, hashSenha)
    adicionarUserJson(users, username, hashSenha)
    salvarUserJson(users, arquivoUsers)
    print("Usuário cadastrado com sucesso!")
    print("----------------------")
    return

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
            print("Usuário não encontrado.")
            sys.exit();

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
    print("2 - Sair")
    print("----------------------")
    resp = input()
    print("----------------------")
    