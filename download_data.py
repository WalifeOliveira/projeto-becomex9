import requests
import zipfile
import os

def download_file(url, filename):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
        "Referer": "https://portaldatransparencia.gov.br/download-de-dados",
        "Connection": "keep-alive"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Download concluído: {filename}")
    else:
        print(f"Erro ao baixar: {response.status_code}")
        print(f"URL usada: {url}")

def extract_zip(filename, extraction_path, arquivos_para_extrair):
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        arquivos_no_zip = zip_ref.namelist()
        print("Arquivos dentro do ZIP:")
        for arquivo in arquivos_no_zip:
            print(arquivo)

        os.makedirs(extraction_path, exist_ok=True)
        for arquivo in arquivos_para_extrair:
            if arquivo in arquivos_no_zip:
                zip_ref.extract(arquivo, extraction_path)
                print(f"Arquivo '{arquivo}' extraído com sucesso!")
            else:
                print(f"Arquivo '{arquivo}' não encontrado no ZIP.")
