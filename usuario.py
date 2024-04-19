from conexao import Conexao
from hashlib import sha256

class Usuario:

    def __init__ (self):
        self.telefone = None
        self.nome = None
        self.senha = None
        self.logado = False

    def cadastrar (self, telefone, nome, senha):

        # CRIPTOGRAFANDO A SENHA
        senha = sha256(senha.encode()).hexdigest()


        try:
            # conectando o banco de dados
            mydb = Conexao.conectar()

            mycursor = mydb.cursor()
        
            #inserir os dados na tabela 
            dados = f"INSERT INTO tb_usuario (tel, nome, senha) VALUES ('{telefone}', '{nome}', '{senha}')"

            #executar
            mycursor.execute(dados)

            mydb.commit()

            self.telefone = telefone
            self.nome = nome
            self.senha = senha
            self.logado = True

            mydb.close()

            return True

        except:
            return False

    def logar (self, telefone, senha):

        # CRIPTOGRAFANDO A SENHA
        senha = sha256(senha.encode()).hexdigest()

        mydb = Conexao.conectar()

        # result = mydb.query("SELECT * FROM tb_usuario WHERE tel=? AND senha=?", [telefone, senha])

        mycursor = mydb.cursor()

        #pesquisar no banco se existe esse telefone e a senha
        dados = f" SELECT * FROM crabiz.tb_usuario WHERE tel = '{telefone}' AND senha = '{senha}'"   

        mycursor.execute(dados)
        
        resultado = mycursor.fetchone()

        #se encontrou um usuário com esses dados
        if not resultado == None: 
            self.logado = True
            self.nome = resultado[1]
            self.telefone = resultado[0]
            self.senha = resultado[2]
        else: 
            self.logado = False
              
        mydb.commit()  