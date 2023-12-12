from flask import Flask, render_template, request,jsonify, redirect, url_for
import dab as db
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpld3

datab =db.dbConnection()

PartidoSeleccionado = ''
Ine = ''

app= Flask(__name__)

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/')
def login():
  return render_template('home.html')

@app.route('/presi')
def presi(): 
  return render_template('presi.html')

@app.route('/est')
def est():
  return render_template('est.html')

@app.route('/dele')
def dele():
  return render_template('dele.html')

@app.route('/validaVoto', methods=['POST'])
def validaVoto():
  if request.method == 'POST':
    field_value_to_search = request.form['campo_busqueda']
    urna = datab['Collect1']
    result = urna.find_one({'ClElec': field_value_to_search})
    NoExist = 'El usuario no existe'

    if(result== None):
      return jsonify({'htmlresponse': render_template('modal.html', employeelist=NoExist)})

    if(result['RegVoto'] == 'True'):
      return jsonify({'htmlresponse': render_template('modal.html')})
    else:
      graficas = getinfovoto2()
      html_grafica = graficar_pastel(graficas)
      graficar_puntos = graficar_puntos_V(graficas)
      return render_template('presi.html', html_grafica = html_grafica, resultado=field_value_to_search, showButton = True, graficar_puntos=graficar_puntos)
    
@app.route('/confirmvoto', methods=['POST'])
def confirmvoto():
  if request.method == 'POST':
    Partidovoto = request.form['Partidovoto']
    ine = request.form['INE']
    votoIne= {
        'voto': Partidovoto,
        'ine': ine
    }

    global PartidoSeleccionado
    PartidoSeleccionado = Partidovoto
    global Ine
    Ine = ine
    return jsonify({'htmlresponse': render_template('modal2.html', votoE=votoIne)})
   
        
@app.route('/savevoto', methods=['POST'])
def savevoto():    
  urna = datab['Vota_Presi']
  urna.insert_one({'Partido': PartidoSeleccionado})
  updatevoto()
  graficas = getinfovoto2()
  html_grafica = graficar_pastel(graficas)
  graficar_puntos = graficar_puntos_V(graficas)
  #print(html_grafica)
  return render_template('presi.html', html_grafica = html_grafica, showButton = False, returHome = True, graficar_puntos=graficar_puntos)

def updatevoto():
  urna = datab['Collect1']
  urna.update_one({'ClElec': Ine}, {'$set': {'RegVoto': 'True'}})

def getinfovoto2():
    # Configura tu conexión a MongoDB
    collection = datab['Vota_Presi']

    # Personaliza esta función según tu esquema de datos en MongoDB
    data = list(collection.find({}, {'_id': 0, 'Partido': 1}))
    return data
    
def graficar_pastel(data):
    categorias = [item['Partido'] for item in data]
    conteo_categorias = {Partido: categorias.count(Partido) for Partido in set(categorias)}

    labels = list(conteo_categorias.keys())
    sizes = list(conteo_categorias.values())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title('Gráfico de Pastel: Distribución de Categorías')

    # Convierte la gráfica de matplotlib a un formato HTML
    html_grafica = mpld3.fig_to_html(fig)

    return html_grafica


def graficar_puntos_V(data):
    categorias = [item['Partido'] for item in data]
    conteo_categorias = {Partido: categorias.count(Partido) for Partido in set(categorias)}

    print(conteo_categorias)
    # Separar las claves (partidos) y valores (número de votos)
    partidos = list(conteo_categorias.keys())
    votos = list(conteo_categorias.values())

    # Crear gráfico de dispersión (scatter plot) con Matplotlib
    fig, ax = plt.subplots()
    ax.scatter(partidos, votos, color='blue', marker='o')
    ax.set_xlabel('Partidos')
    ax.set_ylabel('Número de Votos')
    ax.set_title('Votos por Partido')

    # Convertir la figura de Matplotlib a una figura mpld3
    grafpunt = mpld3.fig_to_html(fig)


    return grafpunt




@app.route('/verResultados', methods=['POST'])
def verResultados():
  return render_template('login.html')

@app.route('/verResultados2', methods=['POST'])
def verResultados2():
  graficas = getinfovoto2()
  html_grafica = graficar_pastel(graficas)
  graficar_puntos = graficar_puntos_V(graficas)
  #print(html_grafica)
  return render_template('presi.html', html_grafica = html_grafica, showButton = False, returHome = False, graficar_puntos=graficar_puntos)
    
if __name__ == '__main__':
  app.run(debug=True)