from tkinter.filedialog import askopenfilename
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import tkinter as tk
import pandas as pd

class PriceChecker:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Análise de Preços")
        self.root.geometry("400x300")
        
        self.setup_gui(self.root)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        # Salvar os dados por aqui (opção)
        print("Fechando a aplicação...")
        self.root.destroy()


    def setup_gui(self, root):
        label_titulo = tk.Label(self.root, text="Analisador de Preços", font=("Arial", 16, "bold"))
        label_titulo.pack(pady=10)
        
        self.localizar_button = tk.Button(self.root, text = "Selecionar arquivo XLSX", command=self.locale)
        self.localizar_button.pack(pady=10)

        self.caminho_arquivo = tk.StringVar()
        self.label_caminho = tk.Label(self.root, textvariable=self.caminho_arquivo)
        self.label_caminho.pack()

        self.analisar_button = tk.Button(self.root, text="Analisar Preço", command=self.extrair_dados_magalu)
        self.analisar_button.pack(pady=5)

        self.analisar_ordem = tk.StringVar()
        self.label_analisar_ordem = tk.Label(self.root, textvariable=self.analisar_ordem)
        self.label_analisar_ordem.pack()

    #

        # self.analisar_ordem = tk.StringVar()
        # self.label_analisar_ordem = tk.Label(self.root, textvariable=self.analisar_ordem)
        # self.label_analisar_ordem.pack()

        # self.analisar_button = tk.Button(self.root, text="Analisar Preço", command=self.extrair_dados_magalu)
        # self.analisar_button.pack(pady=5)

    #

        

        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)
        
    def extrair_dados_magalu(url):

        def extrair_data():
            data = datetime.now().strftime('%d-%m-%Y')
            hora = datetime.now().strftime('%H:%M:%S')
            return data, hora

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status() 

            soup = BeautifulSoup(response.content, 'html.parser')

            preco_elemento = soup.find('p', {'data-testid': 'price-value'}) 
            nome_elemento = soup.find('h1', {'data-testid': 'heading-product-title'})
            preco1 = preco_elemento.get_text(strip=True) if preco_elemento else "Preço indisponível"
            preco = preco1.replace("\xa0", " ") if preco1 != "Preço indisponível" else preco1
            nome_produto = nome_elemento.get_text(strip=True) if nome_elemento else "Nome indisponível"
            data, hora = extrair_data()

            return {
                'nome': nome_produto,
                'preco': preco,
                'data': data,
                'hora': hora
            }
        except Exception as e:
            return {'erro': str(e)}
        
    def locale(self):
        tipos_arquivos = [("Arquivos CSV e Excel", "*.csv;*.xlsx")]
        filename = askopenfilename(title="Selecionar Arquivo",filetypes=tipos_arquivos)
        return filename

    # url = "https://www.magazineluiza.com.br/kit-composto-lacteo-milnutri-profutura-original-800g-2-unidades/p/229864500/me/cptl/"
    url = "https://www.magazineluiza.com.br/bebida-lactea-uht-com-15g-de-proteinas-yopro-morango-sem-lactose-zero-acucar-250ml/p/234133400/me/bebp/"

    def extrair_url_xlsx(path, nome_coluna):
        workbook = load_workbook(filename=path)
        planilha = workbook.active
        valores_coluna = []

        for linha in planilha.iter_rows(values_only=True):
            if not valores_coluna:
                cabecalhos = list(linha)
                if nome_coluna not in cabecalhos:
                    raise ValueError(f"Coluna '{nome_coluna}' não encontrada no arquivo.")
                indice_coluna = cabecalhos.index(nome_coluna)
            else:
                valores_coluna.append(linha[indice_coluna])
            
                return valores_coluna[1:] if valores_coluna else []
            try:
                print(f"Itens da coluna '{nome_coluna}':")
                for item in nome_coluna:
                    print(item)
            except Exception as e:
                print(f"Erro: {e}")
            
            

    caminho = r".\test\Links Magalu e Qualidoc.xlsx"
    coluna_desejada = "LINK"
    itens = extrair_url_xlsx(caminho, coluna_desejada)

    dados = extrair_dados_magalu(url)
    print(dados)

if __name__ == "__main__":
    app = PriceChecker()
