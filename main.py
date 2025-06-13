from flask import Flask, request
import openai
import os

app = Flask(__name__)

# Cargar API key desde las variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    # Verificar que la solicitud tenga formato JSON
    if not request.is_json:
        return {"error": "La solicitud debe ser JSON"}, 400

    data = request.get_json()
    pregunta = data.get('mensaje', '')

    if not pregunta:
        return {"error": "No se envió mensaje"}, 400

    try:
        # Llamar a la API de OpenAI
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": pregunta}
            ]
        )
        texto = respuesta['choices'][0]['message']['content']
        print("RESPUESTA:", texto)
        return {"respuesta": texto}, 200

    except Exception as e:
        return {"error": str(e)}, 500

# Usar el puerto dinámico de Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("⚙️ Usando el puerto:", port)
    app.run(host="0.0.0.0", port=port)

