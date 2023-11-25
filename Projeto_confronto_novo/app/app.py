# imports do sistema
import os
import sys
from flask import Flask, render_template, request, send_from_directory
import sqlalchemy



# linha para detecar a pasta onde estão os arquibos .py
sys.path.append('arquivos_py')

# impots arquivos .py
import arquivos_py.arquivos_para_bd
import arquivos_py.conexao_bd
import arquivos_py.path_arquivos

# atribuindo o Flask para o objeto app

app = Flask(__name__)

# caminho da pasta com os arquivos

caminho_arquivo_enviado_confronto = arquivos_py.path_arquivos.path_arquivos.caminho_arquivos_enviados_cofronto


# definindo a pasta para realizar o upload dos arquivos
app.config['UPLOAD_FOLDER'] = caminho_arquivo_enviado_confronto

# pagina home

@app.route('/')
def homepage():
    return render_template("homepage.html")


# pagina de upload

@app.route('/upload')
def upload():
    # verificar os arquivos na pasta e exibir na tabela
    arquivos = os.listdir(caminho_arquivo_enviado_confronto)
    return render_template('upload.html', arquivos=arquivos)


# metodo para a pagina upload , fazer o upload dos arquivos selecionados para o servidor

@app.route('/upload', methods=['POST'])  # Certifique-se de que apenas o método POST seja permitido aqui
def upload_files():
    if request.method == 'POST':  # Verifique o método da solicitação
        uploaded_files = request.files.getlist('btn_upload_arquivos')
        if uploaded_files:
            for file in uploaded_files:
                if file.filename != '':
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                    file.save(file_path)
            arquivos = os.listdir(caminho_arquivo_enviado_confronto)
            return render_template('upload.html', arquivos=arquivos)
    return 'Nenhum arquivo selecionado.'

@app.route('/processar_arquivo')
def processar_arquivo():

    # chamando nosso metodo para adicionar os dados do arquivos em excel no banco
    processar = arquivos_py.arquivos_para_bd.Arquivos_para_bd()
    processar.arquivos_bd()
    return 'Arquivos importados para o banco'


# fazer download dos arquivos enviados para o servidor

@app.route('/upload/<nome_arquivo>')
def download_arquivo_enviado(nome_arquivo):

    return send_from_directory(directory=caminho_arquivo_enviado_confronto, path=nome_arquivo, as_attachment=True)

@app.route('/processos')
def exibir_arquivos_importador():

    busca_dados = arquivos_py.conexao_bd.Conexao_bd()

    busca_dados = busca_dados.arquivos_importados_banco()


    return render_template('processos.html', busca_dados=busca_dados)


@app.route('/processos')
def processos():
    arquivos = os.listdir(caminho_arquivo_enviado_confronto)
    return render_template("processos.html", arquivos=arquivos)

# processar arquivos armazenados no servidor e guardar no banco


@app.route('/processos/<nome_arquivo>')
def download_arquivo_processado(nome_arquivo):

    return send_from_directory(directory=caminho_arquivo_enviado_confronto, path=nome_arquivo, as_attachment=True)

@app.route('/processos', methods=['POST'])
def gerar_arquivo():

    dt_incio = request.form.get('dt_inicio')
    return dt_incio


# metodo principal para executar o flask

if __name__ == '__main__':
    app.run(debug=True)
