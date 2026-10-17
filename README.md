# Exploración visual de patrones demográficos para validaciones en captación censal

Proyecto académico desarrollado a partir de los microdatos del Censo
de Población y Vivienda 2020, Cuestionario Ampliado, Aguascalientes,
para mejorar visualizaciones exploratorias mediante herramientas de
visualización estática, interactiva y de Business Intelligence.

## Pregunta de análisis

¿Qué patrones y combinaciones se observan entre variables demográficas
y de captación como edad, discapacidad, escolaridad, fecundidad y
ubicación geográfica, y cuáles podrían resultar relevantes para el
diseño de validaciones de universo, consistencia o contexto en
aplicaciones de captación censal?

Una combinación poco frecuente no necesariamente constituye un error:
puede representar una inconsistencia, un caso que requiere confirmación
o un valor atípico válido.

## Estructura

``` text
Proyecto_Visualizacion_Censo2020/
codigo/
	generar_visualizaciones.py
	analisis_visualizacion_censo2020.ipynb
css/
	estilos.css
datos/
	Personas01.CSV
	01_aguascalientes.zip
	indicador_municipal.csv
 tableau/
	patrones_territoriales_aguascalientes.twbx
 visualizaciones/
	 fecundidad_estatica.png
	 fecundidad.html
	 discapacidad.html
	 territorio.html
 index.html
 README.md
 requirements.txt
```

## Visualizaciones

La visualización estática de fecundidad analiza la proporción de mujeres
de 12 a 20 años con al menos un hijo nacido vivo. La versión mejorada
incorpora etiquetas directas, jerarquía visual, una paleta monocromática
y una nota metodológica.

Las visualizaciones interactivas desarrolladas con Plotly permiten
consultar información mediante *hover*, alternar dinámicamente entre
actividades relacionadas con dificultades reportadas y explorar
territorialmente el indicador municipal.

## Business Intelligence

El tablero de Tableau Public incorpora comparación municipal, KPI global
dinámico, selección de municipios como filtro y *tooltips*.

https://public.tableau.com/views/Patronesterritorialesdedificultadesreportadas-Aguascalientes/PatronesterritorialesdedificultadesreportadasenAguascalientes

## Metodología territorial

Se consideran las variables relacionadas con ver, oír, caminar,
recordar, bañarse, hablar y condición mental. Se identifica alguna
dificultad cuando al menos una variable presenta código 2, 3 o 4. Para
el denominador se consideran registros con al menos una respuesta
sustantiva entre 1 y 4.

El indicador se pondera mediante `FACTOR` y se resume por municipio.

**Nota:** es un indicador exploratorio y no corresponde a una
estimación oficial de prevalencia de discapacidad.

## Fuentes

Instituto Nacional de Estadística y Geografía (INEGI). **Censo de
Población y Vivienda 2020**.

https://www.inegi.org.mx/programas/ccpv/2020/

Para la representación territorial se utiliza cartografía municipal del
**Marco Geoestadístico** de INEGI.

https://www.inegi.org.mx/temas/mg/


## Reproducibilidad

### 1. Crear y activar un entorno virtual

``` bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Instalar dependencias

``` bash
python -m pip install -r requirements.txt
```

### 3. Colocar los datos originales

En `datos/`:

``` text
Personas01.CSV
01_aguascalientes.zip
```

### 4. Ejecutar

Notebook documentado:

``` text
codigo/analisis_visualizacion_censo2020.ipynb
```

Script completo:

``` bash
python codigo/generar_visualizaciones.py
```

### 5. Visualizar el sitio local

Desde la raíz:

``` bash
python -m http.server 8000
```

Abrir `http://localhost:8000`.

## Plotly en PyCharm/Jupyter

En el entorno utilizado, las figuras Plotly del notebook se incrustan
como HTML:

``` python
from IPython.display import HTML, display
display(HTML(fig.to_html(include_plotlyjs="cdn", full_html=False)))
```

Esto conserva la interactividad dentro del notebook.

## Publicación

El repositorio público puede contener código, documentación,
visualizaciones derivadas y el archivo municipal agregado. Los
microdatos originales `Personas01.CSV` no se publican.

## Herramientas

Python, pandas, Matplotlib, Plotly, GeoPandas, Jupyter Notebook, Tableau
Public y HTML/CSS.
