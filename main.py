from download_data import download_file, extract_zip
from process_data import load_data, filter_by_cnae, new_columns, process_cnpj_data
from send_data import enviar_email_outlook
from utils.date_utils import get_ano_mes

def main():
    ano_mes = get_ano_mes()
    
    url = f"https://portaldatransparencia.gov.br/download-de-dados/favorecidos-pj/{ano_mes}"
    filename = "favorecidos.zip"
    extraction_path = "CNPJ"
    arquivos_para_extrair = [f'{ano_mes}_CNPJ.csv']

    download_file(url, filename)
    extract_zip(filename, extraction_path, arquivos_para_extrair)

    arquivo_csv = f"CNPJ/{ano_mes}_CNPJ.csv"
    df = load_data(arquivo_csv)

    lista_cod_cnae = [5250803, 5231102, 5250804]
    base_cnae = filter_by_cnae(df, lista_cod_cnae)
    base_cnae = new_columns(base_cnae)
    print(f"Total de linhas após filtro por CNAE: {base_cnae.shape[0]}")

    nome_arquivo = "dados_empresas.csv"
    process_cnpj_data(base_cnae)


    enviar_email_outlook()

if __name__ == "__main__":
    main()
