import bcrypt; #pip install bcrypt
import json;

nameUser = input("Digite seu nome de usuário: ");
senha = input("Digite sua senha: ");

def criarUserJson(nameUser, senha):
    return { "UserName": nameUser, "Password": senha };

def criptografiaSenha(senha):
    salt = bcrypt.gensalt(8)  # Gera um salt (complexidade adicional) para a criptografia. 
    # sequência aleatória única misturada com a senha antes de ser criptorgrafada.

    hashSenha = bcrypt.hashpw(senha.encode(), salt);
    return hashSenha
    # Cria o hash da senha combinando a senha digitada pelo usuário com o "salt" gerado.
    #  O "encode()"" é usado para converter a senha de uma string para uma sequência de bytes, que é o formato necessário para a função "bcrypt.hashpw()".
def salvarUserJson(users, arquivo):
    with open(arquivo, 'w') as f:
        json.dump(users, f);

    # print(f"Senha original: {senha}")
    # print(f"Salt gerado: {salt.decode()}")
    # print(f"Hash da senha: {hashSenha.decode()}");
def adicionarUserJson(users, nameUser, senha):
    usuarioNovo = criarUserJson(nameUser, senha);
    users.append(usuarioNovo);

def criptografiaSenha(senha):
    salt = bcrypt.gensalt(8);
    hashSenha = bcrypt.hashpw(senha.encode(), salt);
    return hashSenha;

def autenticacao(user, senha, hashSenha):
    print("------------------");
    print("Login");
    print("------------------");
    loginUser = input("Insira seu nome de usuário: ");
    senhaUser = input("Insira sua senha: ");
    print("------------------");

    if loginUser != user:
        print("Usuário ou senha incorretos.");

def autenticacao(user, senha, hashSenha):
    print("Tente novamente mais tarde.")

print(autenticacao(nameUser, senha, criptografiaSenha(senha)));

print("----------------------");
print("Escolha uma opção: ")
print("1 - Cadastrar");
print("2 - Autenticar");
resp = input("3 - Sair  ");

if resp == "1" :
    print("----------------------");
    nameUser = input("Digite seu nome de usuário: ");
    senha = input("Digite sua senha: ");
    users = [];
    adicionarUserJson(users, nameUser, senha);
    print("1° parte feita");

elif resp == "2":
    print("----------------------");
    nameUser = input("Digite seu nome de usuário: ");
    senha = input("Digite sua senha: ");
    autenticacao(nameUser, senha, criptografiaSenha(senha))

else:
    print("Insira uma resposta válida.")

arquivoUsers = "usuarios.json";
salvarUserJson(users, arquivoUsers);

#print(autenticacao(nameUser, senha, criptografiaSenha(senha)));