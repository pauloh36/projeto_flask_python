import sqlite3
import pandas as pd
import path_arquivos


class Conexao_bd:

    def __init__(self):
        self.nome_banco = 'confronto'
        self.conexao = sqlite3.connect(path_arquivos.path_arquivos.caminho_bd)
        self.cursor = self.conexao.cursor()

    def conectar(self):
        self.conexao = sqlite3.connect(self.nome_banco)
        self.cursor = self.conexao.cursor()

    def desconectar(self):
        if self.conexao:
            self.conexao.close()

    def executar_query(self, query, parametros=None):
        if not self.conexao:
            raise Exception("Conexão com o banco de dados não estabelecida.")

        if parametros:
            self.cursor.execute(query, parametros)
        else:
            self.cursor.execute(query)

        self.conexao.commit()

    def buscar_dados(self, query, parametros=None):
        if not self.conexao:
            raise Exception("Conexão com o banco de dados não estabelecida.")

        if parametros:
            self.cursor.execute(query, parametros)
        else:
            self.cursor.execute(query)

        return self.cursor.fetchall()

    def __enter__(self):
        self.conectar()
        return self

    def excel_para_bd(self, df, nome_arquivo_atual):

        df_bd = pd.DataFrame(df)

        df_bd['ARQUIVO'] = nome_arquivo_atual

        df_bd.to_sql('confronto', self.conexao , index='False' , if_exists='append')

        print('arquivo inserido no banco')

    def arquivos_importados_banco(self):

        query = 'SELECT DISTINCT ARQUIVO, FILIAL FROM confronto'

        self.cursor.execute(query)
        dados = self.cursor.fetchall()

        return dados





