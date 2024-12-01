# README.md

## API de Upload para Amazon S3

Este projeto é uma API simples construída em Flask com uma única rota que permite fazer upload de arquivos para um bucket no Amazon S3. A API retorna a URL pública do arquivo carregado, para que possa ser usado em aplicações frontend ou armazenado em um banco de dados.

---

## Requisitos

### Dependências do projeto:
- **Python** (versão 3.7 ou superior)
- **Bibliotecas Python**:
  - Flask
  - boto3

Instale as bibliotecas usando:

```bash
pip install flask boto3
```

### Pré-requisitos da AWS:
- Conta AWS ativa.
- Bucket no Amazon S3.
- Usuário IAM com permissões adequadas.

---

## Configuração do Bucket S3

1. **Criação do Bucket:

   - No console da AWS, vá para o serviço **S3**.
   - Clique em **"Create bucket"**.
   - Configure:
     - Nome do bucket: `pythonbucket-test-12315790` (ou um nome de sua escolha).
     - Região: `us-east-2` (ou a região desejada).
   - Desmarque a opção **"Block all public access"** se quiser permitir acesso público.

2. **Configuração de Permissões:**
   - Após criar o bucket, vá até a aba **Permissions**.
   - Role até **Bucket Policy** e adicione a seguinte política:

     ```json
     {
         "Version": "2012-10-17",
         "Statement": [
             {
                 "Effect": "Allow",
                 "Principal": "*",
                 "Action": "s3:GetObject",
                 "Resource": "arn:aws:s3:::pythonbucket-test-12315790/*"
             }
         ]
     }
     ```
   - Essa política garante que todos os objetos no bucket possam ser acessados publicamente.

---

## Configuração do Usuário IAM

1. **Criar Usuário IAM:**
   - No console da AWS, vá para o serviço **IAM**.
   - Clique em **"Users"** > **"Add users"**.
   - Nomeie o usuário como `krs-test` e marque a opção **"Access key - Programmatic access"**.

2. **Permissões do Usuário:**
   - Na etapa de permissões, escolha **"Attach policies directly"**.
   - Anexe a política gerenciada **AmazonS3FullAccess**.
   - Opcionalmente, crie uma política personalizada para restringir o acesso apenas ao bucket desejado:

     ```json
     {
         "Version": "2012-10-17",
         "Statement": [
             {
                 "Effect": "Allow",
                 "Action": [
                     "s3:PutObject",
                     "s3:GetObject",
                     "s3:ListBucket"
                 ],
                 "Resource": [
                     "arn:aws:s3:::pythonbucket-test-12315790",
                     "arn:aws:s3:::pythonbucket-test-12315790/*"
                 ]
             }
         ]
     }
     ```

3. **Salvar Chave de Acesso:**
   - Ao finalizar a criação do usuário, salve o **Access Key ID** e o **Secret Access Key**. Eles serão usados no backend.

---

## Backend Flask

### Configuração do Backend

1. **Estrutura do Projeto:**

```
project/
│
├── app.py         # Código principal da API
└── requirements.txt # Dependências do projeto
```

2. **Código do Backend:**


```python
from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)

# Configurações do S3
AWS_ACCESS_KEY = 'SUA_AWS_ACCESS_KEY'
AWS_SECRET_KEY = 'SUA_AWS_SECRET_KEY'
AWS_BUCKET_NAME = 'pythonbucket-test-12315790'
AWS_REGION = 'us-east-2'

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                  aws_secret_access_key=AWS_SECRET_KEY,
                  region_name=AWS_REGION)


@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "Nome do arquivo vazio"}), 400

        # Faz o upload do arquivo para o S3
        s3.upload_fileobj(
            file,
            AWS_BUCKET_NAME,
            file.filename,
            ExtraArgs={'ContentType': file.content_type}
        )

        file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file.filename}"
        
        return jsonify({"message": "Upload realizado com sucesso!", "file_url": file_url}), 200

    except NoCredentialsError:
        return jsonify({"error": "Credenciais inválidas"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

3. **Rodando o Servidor:**
   - Execute o servidor Flask:
     ```bash
     python app.py
     ```

---

## Teste com Postman

1. **Configurar Requisição:**
   - Método: `POST`
   - URL: `http://127.0.0.1:5000/upload`
   - Body: 
     - Tipo: `form-data`
     - Campo: `file` (tipo **File**) com o arquivo que deseja enviar.

2. **Resposta Esperada:**

```json
{
    "message": "Upload realizado com sucesso!",
    "file_url": "https://pythonbucket-test-12315790.s3.us-east-2.amazonaws.com/seu-arquivo.jpg"
}
```

---

## Conclusão

Este projeto demonstra como criar uma API para upload de arquivos para o Amazon S3 e configurá-lo para que os arquivos sejam acessíveis publicamente. Ele pode ser usado como base para integrar funcionalidades semelhantes em projetos maiores.
