from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from parsel import Selector

app = Flask(__name__)
CORS(app)

@app.route('/scrape', methods=['POST'])  # Cambiado a POST
def scrape():
    data = request.json  # Obtener el cuerpo de la solicitud como JSON
    url = data.get('url')  # Obtener la URL del JSON
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.google.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    session = requests.Session()

    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # Lanza un error si la respuesta no es 200

        # Usar Parsel para parsear el contenido HTML
        selector = Selector(text=response.text)
        nodos = selector.css('.upload-link')  # Seleccionar nodos con clase 'upload-link'
        
        # Extraer el texto de los enlaces dentro de los nodos seleccionados
        capitulos = [nodo.css('a::text').get() for nodo in nodos if nodo.css('a')]
        
        return jsonify({'capitulos': capitulos, 'total': len(capitulos)})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error al acceder a la página: {str(e)}'}), 500

    except Exception as e:
        return jsonify({'error': f'Ocurrió un error inesperado: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)