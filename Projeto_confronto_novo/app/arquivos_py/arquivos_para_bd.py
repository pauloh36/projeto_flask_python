import pandas as pd
import path_arquivos
import os
import conexao_bd


class Arquivos_para_bd:

    def __init__(self):
        self.caminho = path_arquivos.path_arquivos.caminho_arquivos_enviados_cofronto
        self.conexao = conexao_bd.Conexao_bd()
        self.login = ''
        self.senha = ''
        self.porta = ''

    def arquivos_bd(self):

        for file in os.listdir(self.caminho):

            print('inserindo dados no banco')

            df = pd.read_excel(os.path.join(self.caminho, file))

            self.conexao.excel_para_bd(df, file)

            os.remove(os.path.join(self.caminho, file))




        self.conexao.desconectar()