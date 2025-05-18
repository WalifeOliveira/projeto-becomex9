import os
import win32com.client

def enviar_email_outlook():
    """
    Envia e-mail usando o Outlook logado na máquina do usuário.
    
    Parâmetros:
    - destinatario: string com e-mails separados por ; (ex: 'email1@ex.com; email2@ex.com')
    - assunto: título do e-mail
    - corpo: corpo do e-mail (texto simples)
    - anexos: Busca o arquivo no diretório atual do script e anexa ao e-mail.
    """
    outlook = win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)
    destinatario = "lucasroballo@hotmail.com"
    assunto = "Teste"
    corpo = "Teste de envio de e-mail com anexo"
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo = os.path.join(diretorio_atual, 'ENVIAR', 'dados_empresas.csv')
    if os.path.exists(caminho_arquivo):
        mail.Attachments.Add(caminho_arquivo)
    else:
        print(f"Arquivo não encontrado: {caminho_arquivo}")
    
    mail.To = destinatario
    mail.Subject = assunto
    mail.Body = corpo

    mail.Send()
    print("E-mail enviado com sucesso via Outlook.")