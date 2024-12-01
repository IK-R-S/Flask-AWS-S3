from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)

# Configurações do S3
AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''
AWS_BUCKET_NAME = ''
AWS_REGION = ''

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                  aws_secret_access_key=AWS_SECRET_KEY,
                  region_name=AWS_REGION)


@app.route('/')
def index():
    return 'Amazon Web Services Test'

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Verifica se há um arquivo na requisição
        if 'file' not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "Nome do arquivo vazio"}), 400

        # Faz o upload do arquivo para o S3 (sem ACL, já gerenciado pelo bucket policy)
        s3.upload_fileobj(
            file,
            AWS_BUCKET_NAME,
            file.filename,
            ExtraArgs={
                'ContentType': file.content_type
            }
        )

        # Gera a URL pública do arquivo
        file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file.filename}"
        
        return jsonify({"message": "Upload realizado com sucesso!", "file_url": file_url}), 200

    except NoCredentialsError:
        return jsonify({"error": "Credenciais inválidas"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
