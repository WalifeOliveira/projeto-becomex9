import pandas as pd
import os

def filtrar_cnaes():
    # Lê o arquivo CSV 
    caminho_virtual = os.path.dirname(os.path.abspath(__file__))
    caminho_pasta_Enviar = os.path.join(caminho_virtual,"ENVIAR")
    caminho_completo = os.path.join(caminho_pasta_Enviar,"dados_empresas.csv")
    df_cnaes = pd.read_csv(caminho_completo)
    
    print(df_cnaes.head())  # Mostra as primeiras linhas do DataFrame

    # Garante que a coluna COD_CNAE está como inteiro
    df_cnaes["COD_CNAE"] = df_cnaes["COD_CNAE"].astype(int)

    # Solicita o CNAE que o usuário quer filtrar
    try:
        nome_cnae = int(input("Informe a CNAE: "))
    except ValueError:
        print("Por favor, insira um número válido.")
        return

    # Filtra os dados
    resultado_pesquisa_cnae = df_cnaes[df_cnaes["COD_CNAE"] == nome_cnae]

    # Verifica se encontrou resultado
    if resultado_pesquisa_cnae.empty:
        print("Nenhum registro encontrado com esse CNAE.")
    else:
        # Salva o resultado em CSV
        resultado_pesquisa_cnae.to_csv("filtro_cnae.csv", index=False)
        print("Arquivo 'filtro_cnae.csv' gerado com sucesso.")
        print("caminho:",caminho_completo)

# Chamada da funcao
filtrar_cnaes()