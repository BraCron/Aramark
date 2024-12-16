from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Cargar la base de datos desde el archivo Excel
df = pd.read_excel("base_datos.xlsx", sheet_name="SAPconsulta")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consultar', methods=['POST'])
def consultar():
    data = request.get_json()
    rut = data.get('rut')
    clave = data.get('clave')

    # Validar entradas
    if not rut or not clave:
        return jsonify({'success': False, 'error': 'Por favor, ingresa el RUT y la clave.'})

    # Filtrar la base de datos
    resultado = df[(df['RUT'] == rut) & (df['CLAVE'] == clave)]

    if not resultado.empty:  # Verifica si hay resultados
        codigo_sap = str(resultado['Código SAP'].values[0])  # Convertir a string
        return jsonify({'success': True, 'codigo_sap': codigo_sap})
    else:
        return jsonify({'success': False, 'error': 'RUT o clave incorrectos. Por favor, verifica tus datos.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)