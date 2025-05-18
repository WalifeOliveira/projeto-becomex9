import pandas as pd
import requests
import time
import os
from datetime import datetime

def load_data(arquivo_csv):
    df = pd.read_csv(arquivo_csv, encoding='latin1', delimiter=';', quotechar='"', escapechar='\\', on_bad_lines='skip', low_memory=False)
    df['COD_CNAE'] = pd.to_numeric(df['COD_CNAE'], errors='coerce')
    df = df.dropna(subset=['COD_CNAE'])
    return df

def filter_by_cnae(df, lista_cod_cnae):
    return df[df['COD_CNAE'].isin(lista_cod_cnae)].copy()

def new_columns(df):
    for coluna in ['NOME', 'EMAIL', 'TELEFONE', 'SITUACAO_CADASTRAL', 'TIPO', 'ULTIMA_ATUALIZACAO', 'DATA DA SITUAÇÃO CADASTRAL', "ABERTURA"]:
        df[coluna] = ''
    return df

def salvar_csv_inicial(base_cnae: pd.DataFrame, arquivo_destino: str) -> None:
    """Cria a pasta de destino (se necessário) e salva o DataFrame inicial."""
    pasta_destino = os.path.dirname(arquivo_destino)
    if pasta_destino and not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
        print(f"Pasta '{pasta_destino}' criada com sucesso.")
    
    if base_cnae.empty:
        raise ValueError("base_cnae está vazia. Verifique o carregamento dos dados.")
    if 'CNPJ' not in base_cnae.columns:
        raise ValueError("A coluna 'CNPJ' é obrigatória no DataFrame.")
    
    base_cnae.to_csv(arquivo_destino, index=False)
    print(f"Arquivo salvo em: {arquivo_destino}")

def carregar_arquivo_csv(arquivo_destino: str) -> pd.DataFrame:
    """Carrega o arquivo CSV e garante as colunas extras."""
    df = pd.read_csv(arquivo_destino, dtype=str)
    colunas_extras = [
        'NOME', 'EMAIL', 'TELEFONE', 'SITUACAO_CADASTRAL', 'TIPO',
        'ULTIMA_ATUALIZACAO', 'DATA DA SITUAÇÃO CADASTRAL', 'ABERTURA'
    ]
    for coluna in colunas_extras:
        if coluna not in df.columns:
            df[coluna] = ''
    return df

def consultar_api_cnpj(cnpj: str) -> dict:
    """Consulta a API da ReceitaWS para o CNPJ dado."""
    response = requests.get(
        f"https://www.receitaws.com.br/v1/cnpj/{cnpj}",
        headers={"User-Agent": "Mozilla/5.0"}
    )
    if response.status_code == 429:
        print("Limite de requisições atingido. Aguardando 60 segundos...")
        time.sleep(60)
        return consultar_api_cnpj(cnpj)
    return response.json()

def process_cnpj_data(base_cnae: pd.DataFrame, arquivo_destino: str = "ENVIAR/dados_empresas.csv", salvar_apos_linha: bool = True) -> None:
    """Processa os CNPJs, consulta a API e atualiza os dados linha a linha."""
    salvar_csv_inicial(base_cnae, arquivo_destino)
    df = carregar_arquivo_csv(arquivo_destino)

    colunas_consulta = [
        'NOME', 'EMAIL', 'TELEFONE', 'SITUACAO_CADASTRAL', 'TIPO',
        'ULTIMA_ATUALIZACAO', 'DATA DA SITUAÇÃO CADASTRAL', 'ABERTURA'
    ]

    for index, row in df.iterrows():
        if row[colunas_consulta].notna().all() and row[colunas_consulta].astype(str).str.strip().ne('').all():
            continue

        cnpj = str(row['CNPJ']).zfill(14)
        print(f"Consultando CNPJ: {cnpj}")

        try:
            dados = consultar_api_cnpj(cnpj)

            df.loc[index, 'NOME'] = dados['qsa'][0]['nome'] if 'qsa' in dados and dados['qsa'] else ''
            df.loc[index, 'EMAIL'] = dados.get('email', '')
            df.loc[index, 'TELEFONE'] = dados.get('telefone', '')
            df.loc[index, 'SITUACAO_CADASTRAL'] = dados.get('situacao', '')
            df.loc[index, 'TIPO'] = dados.get('tipo', '')
            df.loc[index, 'ULTIMA_ATUALIZACAO'] = dados.get('ultima_atualizacao', '')
            df.loc[index, 'DATA DA SITUAÇÃO CADASTRAL'] = dados.get('data_situacao', '')
            df.loc[index, 'ABERTURA'] = dados.get('abertura', '')

            if salvar_apos_linha:
                df.to_csv(arquivo_destino, index=False)

            time.sleep(1.5)

        except Exception as e:
            print(f"Erro ao consultar CNPJ {cnpj}: {e}")
            continue

    if not salvar_apos_linha:
        df.to_csv(arquivo_destino, index=False)

    print("Consulta concluída. Arquivo CSV atualizado.")