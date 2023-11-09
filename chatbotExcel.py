from flask import Flask, render_template, request
import nltk
from nltk.tokenize import word_tokenize
import pandas as pd

app = Flask(__name__)

# Función para encontrar productos en la pregunta
def encontrar_productos(pregunta, productos):
    pregunta = pregunta.lower()
    productos_encontrados = [producto for producto in productos if pregunta in producto.lower()]
    return productos_encontrados

# Carga la planilla de Excel
df = pd.read_excel('Lista de Precios.xlsx', sheet_name='Hoja1')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pregunta_usuario = request.form['pregunta_usuario']

        if pregunta_usuario.lower() == 'salir':
            respuesta = "¡Hasta luego!"
        elif pregunta_usuario.lower() == 'productos':
            # Muestra todos los productos
            respuesta = "<ul>"
            for _, row in df.iterrows():
                respuesta += f"<li>El precio de {row['Producto']} es ${row['Precio']}. Stock disponible: {row['Stock']}.</li>"
            respuesta += "</ul>"
        else:
            # Encuentra los productos mencionados en la pregunta
            productos_mencionados = encontrar_productos(pregunta_usuario, df['Producto'])

            # Obtiene los precios de los productos mencionados
            precios = df[df['Producto'].str.lower().isin(map(str.lower, productos_mencionados))][['Producto', 'Precio', 'Stock']]
            # Genera la respuesta
            if not precios.empty:
                respuesta = "<ul>"
                for _, row in precios.iterrows():
                    # Truncar los centavos a 2 decimales
                    precio_truncado = round(row['Precio'], 2)
                    respuesta += f"<li>El precio de {row['Producto']} es ${precio_truncado}.Stock disponible: {row['Stock']}.</li>"
                respuesta += "</ul>"
            else:
                respuesta = "Lo siento, no tengo información sobre esos productos."
    else:
        respuesta = ""

    return render_template('index.html', respuesta=respuesta)

if __name__ == '__main__':
    app.run(debug=True)

