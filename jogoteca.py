from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

class Jogo:
    def __init__(self, nome, categoria, console):
        self._nome = nome
        self._categoria = categoria
        self._console = console

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha
        self.jogos = []
        
usuario1 = Usuario("Erik Martins", 'EM', '123')


usuarios = [usuario1]

re2 = Jogo('Resident Evil 2', 'Terror', 'PS2 / XBOX')
sm = Jogo('Spider man', 'Marvel', 'PS2 / XBOX')
gta = Jogo('GTA 5', 'Ação', 'PS2 / XBOX')
lista = [re2, sm, gta]

'''Iniciando o flask na variavel app'''
app = Flask(__name__)

'''Configurando a chave secreta para implementação nos cookes do navegador'''
app.secret_key = 'alura'

'''Conectando ao banco de dados'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://HORUSCDA\erik.martins:Kinka3779@HCDAPC001\DETRANBA/ambiente_teste'

'''Instanciando o objeto de banco de dados'''
db = SQLAlchemy(app)

'''Definindo a rota home do site'''
@app.route("/")
def index():
    try:
        for index, usuario in enumerate(usuarios):
            if(session['usuario_logado'] == usuario.nickname):
                indice = index
        return render_template('lista.html', titulo='Jogos', jogos=usuarios[indice].jogos)
    except:
        return redirect(url_for('login'))

'''
@app.route('/adicionar')
def adicionar():
    return redirect(url_for('novo'))
'''

'''Cirando a rota -novo- para trazer a pagina html'''
@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('novo')))
    else:
        return render_template('novo.html', titulo='Novo Jogo')

'''Cirando a rota -criar- para realizar o cadastro do jogo pela rota -novo-'''
@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    for index, usuario in enumerate(usuarios):
        if(session['usuario_logado'] == usuario.nickname):
            indice = index
    usuarios[indice].jogos.append(jogo)
    return redirect(url_for('index'))

'''Cirando a rota -login- para trazer a pagina html'''
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='Faça seu login', proxima=proxima)

'''Cirando a rota -autenticar- para realizar a autenticação de usuário pela rota -login-'''
@app.route('/autenticar', methods=['POST'])
def autenticar():
    for usuario in usuarios:
        if(request.form['usuario'] == usuario.nickname and request.form['senha'] == usuario.senha):
            session['usuario_logado'] = request.form['usuario']
            flash(session['usuario_logado'] + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            print(proxima_pagina)
            if(proxima_pagina == 'None'):
                return redirect(url_for('index'))
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado!')
        return redirect(url_for('login'))

'''Cirando a rota -logout- para realizar o logout do usuario'''
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuário deslogado!')
    return redirect(url_for('novo'))
    
'''Cirando a rota -create_user- para trazer a pagina html'''
@app.route('/create_user')
def create_user():
    return render_template('cadastro.html', titulo='Faça o seu cadastro')

'''Cirando a rota -register- para realizar a criação do usuário pela rota -create_user-'''
@app.route('/register',  methods=['POST'])
def register():
    nome = request.form['usuario']
    nickname = request.form['nickname']
    senha = request.form['senha']
    confirma_senha = request.form['confirma senha']
    if(senha == confirma_senha):
        usuario = Usuario(nome, nickname, senha)
        usuarios.append(usuario)
        return redirect(url_for('login'))
    else:
        flash('Senha incompativeis!')
        return redirect(url_for('create_user'))
    
'''Rodando a aplicação flask'''
app.run(debug=True)