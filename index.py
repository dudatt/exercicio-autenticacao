import bcrypt; #pip install bcrypt

nameUser = input("Digite seu nome de usuário: ");
senha = input("Digite sua senha: ");

def criptografiaSenha(senha):
    salt = bcrypt.gensalt(8)  # Gera um salt (complexidade adicional) para a criptografia. 
    # sequência aleatória única misturada com a senha antes de ser criptorgrafada.

    hashSenha = bcrypt.hashpw(senha.encode(), salt);
    return hashSenha
    # Cria o hash da senha combinando a senha digitada pelo usuário com o "salt" gerado.
    #  O "encode()"" é usado para converter a senha de uma string para uma sequência de bytes, que é o formato necessário para a função "bcrypt.hashpw()".

    # print(f"Senha original: {senha}")
    # print(f"Salt gerado: {salt.decode()}")
    # print(f"Hash da senha: {hashSenha.decode()}");

def autenticacao(user, senha, hashSenha):
    print("------------------");
    print("Login");
    print("------------------");
    loginUser = input("Insira seu nome de usuário: ");
    senhaUser = input("Insira sua senha: ");
    print("------------------");

    if loginUser != user:
        print("Usuário ou senha incorretos.");
    elif senhaUser != senha:
        for i in range(5):
            i += 1;

            if bcrypt.checkpw(senhaUser.encode(), hashSenha):
                print(f"Seja bem-vindo(a) {user}!");
                break;
            else:
                print("Senha incorreta. Tente novamente.");
                senhaUser = input("Insira sua senha: ");
                bcrypt.checkpw(senhaUser.encode(), hashSenha);
                print(f"Total de tentativas ({i}/5)");
                if i == 5:
                    print("Tentativas máximas alcançadas. Tente novamente mais tarde.");
                continue;

    elif bcrypt.checkpw(senhaUser.encode(), hashSenha) and loginUser == user:
        print(f"Seja bem-vindo(a) {user}!");
    else:
        print("Tente novamente mais tarde.")

print(autenticacao(nameUser, senha, criptografiaSenha(senha)));