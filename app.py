from flask import Flask
import os

app = Flask(__name__)

# Define a porta usando a variável de ambiente PORT ou um valor padrão
port = int(os.environ.get("PORT", 10000))

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
