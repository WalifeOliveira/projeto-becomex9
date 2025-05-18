# projeto-becomex9
# 📬 Projeto Becomex - Sistema de Mensageria

Este projeto simula um sistema de mensageria entre APIs, com foco em modularidade e boas práticas de desenvolvimento em Python. Foi desenvolvido como parte do curso da Escola DNC.

---

## 🧩 Estrutura do Projeto

O sistema é dividido em 3 etapas principais, cada uma implementada em um módulo separado:

1. **Coleta dos dados** (`download_data.py`)  
   Faz o download de dados simulando uma API de origem.

2. **Processamento dos dados** (`process_data.py`)  
   Realiza o tratamento e transformação dos dados baixados.

3. **Envio dos dados** (`send_data.py`)  
   Envia os dados processados para uma API de destino.

---

## 🚀 Como executar o projeto

1. **Clone o repositório:**

```bash
git clone https://github.com/WalifeOliveira/projeto-becomex.git
cd projeto-becomex
---
# 2. Crie e ative um ambiente virtual:
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
---
# 3. Instale as dependências:
pip install -r requirements.txt
---
# 4. Execute os módulos:
python download_data.py
python process_data.py
python send_data.py
---
🛠️ Tecnologias Utilizadas
Python 3
requests
json
os e outras libs nativas
---

📁 Estrutura dos Arquivos
bash
Copiar
Editar
projeto-becomex/
├── download_data.py      # Módulo 1: coleta
├── process_data.py       # Módulo 2: processamento
├── send_data.py          # Módulo 3: envio
├── requirements.txt      # Dependências
├── main.py               # Arquivo opcional para integrar tudo
├── README.md             # Documentação
└── LICENSE               # Licença MIT

📄 Licença
Este projeto está licenciado sob a Licença MIT.
