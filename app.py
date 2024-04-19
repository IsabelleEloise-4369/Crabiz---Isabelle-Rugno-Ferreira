from flask import Flask, render_template, request, redirect, session, jsonify
from usuario import Usuario 
import sqlite3 
from chat import Chat
from contato import Contato

app = Flask(__name__)
app.secret_key = 'batata'  # Chave secreta para criptografar os dados da sessão


@app.route("/", methods = ["GET", "POST"])
def pagina_cadastro():
    if request.method == "GET":
        return render_template("cadastro.html")
    if request.method == "POST":
        telefone = request.form["telefone"]
        nome = request.form["nome"]
        senha = request.form["senha"]
        usuario = Usuario()
        if usuario.cadastrar(telefone, nome, senha):
            return render_template("login.html")
        else:
            return ("ENTRE EM CONTATO COM O SERVIDOR")
      
        

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        telefone = request.form['telefone']
        senha = request.form['senha']

        usuario = Usuario()
        usuario.logar(telefone, senha)
        if usuario.logado:
            session['usuario_logado'] = {'nome':usuario.nome,
                                         'telefone':usuario.telefone}
            return redirect('/chat')
        else:
            session.clear()
            return 'Telefone ou senha incorretos.'
        
@app.route("/chat", methods=["GET"])
def chat():
    if request.method == "GET":
        return render_template("chat.html")
    
    usuario = Usuario()
    if usuario.logado:
            # Redireciona para a rota do chat após o login bem sucedido
            return redirect ("/") 
    else:
         return 'Telefone ou senha incorretos.'

@app.route("/get/usuarios")
def api_get_usuarios():
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session ["usuario_logado"]["telefone"]
    chat = Chat(nome_usuario, telefone_usuario)

    contatos = chat.retorna_contatos()

    return jsonify(contatos), 200

@app.route("/get/mensagens/<tel_destinatario>")
def api_get_mensagens(tel_destinatario):
    quantidade = 0
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session ["usuario_logado"]["telefone"]
    chat = Chat(nome_usuario, telefone_usuario)
    destinario = Contato("", tel_destinatario)
    verifica = chat.verificar_mensagem(quantidade, destinario)

    return jsonify(verifica), 200


@app.route("/post/enviamensagens", methods=["POST"])
def api_post_enviamensagens():

    #Pegando os dados que foram enviados
    dados = request.get_json()

    mensagem = dados['mensagem']
    telefone = dados ['usuario']
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session ["usuario_logado"]["telefone"]
    chat = Chat(nome_usuario, telefone_usuario)
    destinario = Contato("", telefone)
    
    enviar = chat.enviar_mensagem(mensagem, destinario)

    return jsonify({}), 200


app.run(debug=True)