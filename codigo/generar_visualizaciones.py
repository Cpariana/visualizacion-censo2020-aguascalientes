from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

# 1. RUTAS DEL PROYECTO

BASE_DIR = Path(__file__).resolve().parent.parent

ARCHIVO_DATOS = BASE_DIR / "datos" / "Personas01.CSV"
CARPETA_SALIDA = BASE_DIR / "visualizaciones"

CARPETA_SALIDA.mkdir(exist_ok=True)

# 2. CARGA DE DATOS
df = pd.read_csv(
    ARCHIVO_DATOS,
    low_memory=False
)

for columna in ["SEXO", "EDAD", "HIJOS_NAC_VIVOS"]:
    df[columna] = pd.to_numeric(df[columna], errors="coerce")

# 3. PREPARACIÓN DEL INDICADOR DE FECUNDIDAD

fec = df[
    (df["SEXO"] == 3) &
    (df["EDAD"].between(12, 20)) &
    (df["HIJOS_NAC_VIVOS"].between(0, 25))
].copy()

fec["CON_HIJO"] = (fec["HIJOS_NAC_VIVOS"] >= 1).astype(int)
tabla_fec = (fec.groupby("EDAD")["CON_HIJO"].agg(TOTAL_MUJERES="count",MUJERES_CON_HIJO="sum").reset_index())
tabla_fec["PORCENTAJE"] = (tabla_fec["MUJERES_CON_HIJO"] /tabla_fec["TOTAL_MUJERES"] *100)

# VISUALIZACIÓN ESTÁTICA 
# Fecundidad por edad
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(11, 6.5))

ax.plot(
    tabla_fec["EDAD"],
    tabla_fec["PORCENTAJE"],
    marker="o",
    linewidth=2.5,
    markersize=7,
    color="#24557A"
)

# Etiquetas de cada punto
for _, fila in tabla_fec.iterrows():
    ax.annotate(
        f'{fila["PORCENTAJE"]:.1f}%',
        (
            fila["EDAD"],
            fila["PORCENTAJE"]
        ),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        color="#334155"
    )

# Título y subtítulo
fig.suptitle(
    "La proporción de mujeres con al menos un hijo\n"
    "aumenta marcadamente entre los 16 y 20 años",
    x=0.125,
    y=0.965,
    ha="left",
    fontsize=16,
    fontweight="bold",
    color="#17202A"
)

fig.text(
    0.125,
    0.865,
    "Mujeres de 12 a 20 años · Aguascalientes · "
    "Censo de Población y Vivienda 2020",
    fontsize=10.5,
    color="#64748B"
)

# Ejes
ax.set_xlabel(
    "Edad",
    fontsize=11
)

ax.set_ylabel("Mujeres con al menos un hijo nacido vivo (%)",fontsize=11)
ax.set_xticks(tabla_fec["EDAD"])
ax.set_ylim(0,tabla_fec["PORCENTAJE"].max() + 7)

# Diseño visual
ax.grid(
    axis="y",
    alpha=0.20,
    linewidth=0.8
)

ax.grid(
    axis="x",
    visible=False
)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.spines["left"].set_color("#CBD5E1")
ax.spines["bottom"].set_color("#CBD5E1")

ax.tick_params(colors="#475569")

# Nota metodológica / fuente
fig.text(
    0.125,
    0.025,

    "Nota: porcentaje calculado sobre mujeres de cada edad "
    "incluidas en la muestra.\n"
    "Fuente: elaboración propia con microdatos del "
    "Censo de Población y Vivienda 2020, INEGI.",

    fontsize=8.5,
    color="#64748B"
)

plt.subplots_adjust(
    left=0.125,
    right=0.96,
    top=0.79,
    bottom=0.18
)
archivo_estatico = (
    CARPETA_SALIDA
    / "fecundidad_estatica.png"
)
plt.savefig(
    archivo_estatico,
    dpi=300,
    bbox_inches="tight",
    facecolor="white"
)
plt.close()

print()
print("Visualización estática:")
print(archivo_estatico)


# 4. VISUALIZACIÓN INTERACTIVA

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=tabla_fec["EDAD"],
        y=tabla_fec["PORCENTAJE"],
        mode="lines+markers",
        customdata=tabla_fec[
            ["TOTAL_MUJERES", "MUJERES_CON_HIJO"]
        ],
        hovertemplate=(
            "<b>Edad: %{x} años</b><br><br>"
            "Mujeres en la muestra: %{customdata[0]:,.0f}<br>"
            "Con al menos un hijo: %{customdata[1]:,.0f}<br>"
            "Porcentaje: %{y:.2f}%"
            "<extra></extra>"
        )
    )
)

# 5. PRESENTACIÓN
fig.update_layout(
    title={
        "text": (
            "Mujeres de 12 a 20 años con al menos "
            "un hijo nacido vivo"
        ),
        "x": 0.5,
        "xanchor": "center"
    },
    xaxis_title="Edad",
    yaxis_title="Porcentaje en la muestra (%)",
    hovermode="closest",
    margin=dict(
        l=70,
        r=40,
        t=100,
        b=70
    )
)
fig.update_xaxes(
    tickmode="linear",
    dtick=1
)
fig.update_yaxes(
    rangemode="tozero"
)

# 6. EXPORTAR A HTML
archivo_salida = CARPETA_SALIDA / "fecundidad.html"

fig.write_html(
    archivo_salida,
    include_plotlyjs=True,
    full_html=True,
    config={
        "responsive": True,
        "displaylogo": False
    }
)

print()
print("Visualización creada correctamente:")
print(archivo_salida)
print()
print(tabla_fec)

# 7. DISCAPACIDAD / DIFICULTAD POR EDAD

VARIABLES_DISCAPACIDAD = {
    "Caminar": "DIS_CAMINAR",
    "Bañarse": "DIS_BANARSE",
    "Hablar": "DIS_HABLAR"
}

ETIQUETAS_DIFICULTAD = {
    1: "No tiene dificultad",
    2: "Lo hace con poca dificultad",
    3: "Lo hace con mucha dificultad",
    4: "No puede hacerlo"
}

datos_dis = []

for actividad, variable in VARIABLES_DISCAPACIDAD.items():
    temporal = df[
        (df["EDAD"].between(0, 5)) &
        (df[variable].isin([1, 2, 3, 4]))
    ].copy()

    resumen = (
        temporal
        .groupby(["EDAD", variable])
        .size()
        .reset_index(name="FRECUENCIA")
    )

    resumen["ACTIVIDAD"] = actividad
    resumen["CODIGO"] = resumen[variable]
    resumen["DIFICULTAD"] = resumen["CODIGO"].map(
        ETIQUETAS_DIFICULTAD
    )

    datos_dis.append(
        resumen[
            [
                "EDAD",
                "ACTIVIDAD",
                "CODIGO",
                "DIFICULTAD",
                "FRECUENCIA"
            ]
        ]
    )
tabla_dis = pd.concat(datos_dis, ignore_index=True)

# 8. VISUALIZACIÓN INTERACTIVA DE DISCAPACIDAD

from plotly.subplots import make_subplots

fig_dis = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.12,
    row_heights=[0.38, 0.62],
    subplot_titles=(
        "Sin dificultad reportada",
        "Grados de dificultad reportados"
    )
)

actividades = list(VARIABLES_DISCAPACIDAD.keys())
trazas_por_actividad = {
    actividad: [] for actividad in actividades
}

for actividad in actividades:

    datos_actividad = tabla_dis[
        tabla_dis["ACTIVIDAD"] == actividad
    ]
    
    # Panel superior

    sin_dificultad = datos_actividad[
        datos_actividad["CODIGO"] == 1
    ]

    fig_dis.add_trace(
        go.Scatter(
            x=sin_dificultad["EDAD"],
            y=sin_dificultad["FRECUENCIA"],
            mode="lines+markers",
            name="No tiene dificultad",
            customdata=sin_dificultad[["ACTIVIDAD", "DIFICULTAD"]],
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Edad: %{x} años<br>"
                "%{customdata[1]}<br>"
                "Frecuencia: %{y:,.0f}"
                "<extra></extra>"
            ),
            visible=(actividad == "Caminar")
        ),
        row=1,
        col=1
    )
    trazas_por_actividad[actividad].append(
        len(fig_dis.data) - 1
    )    
    # Panel inferior
    for codigo in [2, 3, 4]:
        categoria = datos_actividad[
            datos_actividad["CODIGO"] == codigo
        ]
        fig_dis.add_trace(
            go.Scatter(
                x=categoria["EDAD"],
                y=categoria["FRECUENCIA"],
                mode="lines+markers",
                name=ETIQUETAS_DIFICULTAD[codigo],
                customdata=categoria[
                    ["ACTIVIDAD", "DIFICULTAD"]
                ],
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Edad: %{x} años<br>"
                    "%{customdata[1]}<br>"
                    "Frecuencia: %{y:,.0f}"
                    "<extra></extra>"
                ),
                visible=(actividad == "Caminar")
            ),
            row=2,
            col=1
        )
        trazas_por_actividad[actividad].append(
            len(fig_dis.data) - 1
        )

# 9. BOTONES DE SELECCIÓN

botones = []
numero_trazas = len(fig_dis.data)
for actividad in actividades:
    visibilidad = [False] * numero_trazas
    for indice in trazas_por_actividad[actividad]:
        visibilidad[indice] = True
    botones.append(
        dict(
            label=actividad,
            method="update",
            args=[
                {"visible": visibilidad},
                {
                    "title": {
                        "text": (
                            "Dificultad reportada por edad: "
                            f"{actividad.lower()}"
                        ),
                        "x": 0.5
                    }
                }
            ]
        )
    )
fig_dis.update_layout(
    title={
        "text": "Dificultad reportada por edad: caminar",
        "x": 0.5
    },

    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            buttons=botones,
            x=0.5,
            xanchor="center",
            y=1.12,
            yanchor="top",
            showactive=True
        )
    ],
    height=720,
    margin=dict(
        l=70,
        r=40,
        t=150,
        b=70
    ),
    hovermode="closest",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.18,
        xanchor="center",
        x=0.5
    )
)
fig_dis.update_xaxes(
    title_text="Edad",
    tickmode="linear",
    dtick=1,
    row=2,
    col=1
)
fig_dis.update_yaxes(
    title_text="Frecuencia",
    row=1,
    col=1
)
fig_dis.update_yaxes(
    title_text="Frecuencia",
    row=2,
    col=1
)

# 10. EXPORTAR DISCAPACIDAD
archivo_dis = CARPETA_SALIDA / "discapacidad.html"
fig_dis.write_html(
    archivo_dis,
    include_plotlyjs=True,
    full_html=True,
    config={
        "responsive": True,
        "displaylogo": False
    }
)

print()
print("Visualización de discapacidad creada correctamente:")
print(archivo_dis)

# 11. TERRITORIO
#     Indicador exploratorio de dificultad por municipio

import geopandas as gpd
import zipfile
import plotly.express as px

archivo_geo = BASE_DIR / "datos" / "01_aguascalientes.zip"

print()
print("Leyendo Marco Geoestadístico...")
print(archivo_geo)

# Localizar la capa municipal dentro del ZIP
with zipfile.ZipFile(archivo_geo, "r") as zip_ref:
    archivos_zip = zip_ref.namelist()
    shp_municipales = [
        archivo
        for archivo in archivos_zip
        if archivo.lower().endswith(".shp")
        and "mun" in archivo.lower()
    ]
if not shp_municipales:
    raise FileNotFoundError(
        "No se encontró una capa municipal dentro de "
        "01_aguascalientes.zip"
    )
capa_municipal = shp_municipales[0]
print("Capa municipal encontrada:")
print(capa_municipal)

municipios_geo = gpd.read_file(
    f"zip://{archivo_geo}!{capa_municipal}"
)

print()
print("Columnas de la capa geográfica:")
print(municipios_geo.columns.tolist())

# 12. INDICADOR EXPLORATORIO
VARIABLES_DIFICULTAD = [
    "DIS_VER",
    "DIS_OIR",
    "DIS_CAMINAR",
    "DIS_RECORDAR",
    "DIS_BANARSE",
    "DIS_HABLAR",
    "DIS_MENTAL"
]

# Convertir variables necesarias a numéricas
for variable in VARIABLES_DIFICULTAD + ["MUN", "FACTOR"]:

    df[variable] = pd.to_numeric(
        df[variable],
        errors="coerce"
    )



# Una respuesta 2, 3 o 4 representa algún grado de dificultad.
#
# IMPORTANTE:
# Este indicador es exploratorio y NO debe interpretarse como
# una estimación oficial de prevalencia de discapacidad.

respuestas_validas = df[
    VARIABLES_DIFICULTAD
].isin([1, 2, 3, 4]).any(axis=1)


alguna_dificultad = df[
    VARIABLES_DIFICULTAD
].isin([2, 3, 4]).any(axis=1)


territorial = df[
    respuestas_validas
    & df["MUN"].notna()
    & df["FACTOR"].notna()
].copy()


territorial["ALGUNA_DIFICULTAD"] = (
    alguna_dificultad.loc[territorial.index]
)


territorial["DIFICULTAD_PONDERADA"] = (
    territorial["FACTOR"]
    * territorial["ALGUNA_DIFICULTAD"].astype(int)
)



# 13. RESUMEN MUNICIPAL


municipal = (
    territorial
    .groupby("MUN")
    .agg(
        N_MUESTRA=("MUN", "size"),
        POBLACION_PONDERADA=("FACTOR", "sum"),
        DIFICULTAD_PONDERADA=(
            "DIFICULTAD_PONDERADA",
            "sum"
        )
    )
    .reset_index()
)


municipal["PORCENTAJE_PONDERADO"] = (
    municipal["DIFICULTAD_PONDERADA"]
    / municipal["POBLACION_PONDERADA"]
    * 100
)


# Clave municipal:
# entidad 01 + municipio de tres dígitos

municipal["CVE_MUN"] = (
    "01"
    + municipal["MUN"]
    .astype(int)
    .astype(str)
    .str.zfill(3)
)


print()
print("Resumen municipal:")

print(
    municipal[
        [
            "CVE_MUN",
            "N_MUESTRA",
            "POBLACION_PONDERADA",
            "PORCENTAJE_PONDERADO"
        ]
    ]
)



# 14. UNIÓN CON EL MARCO GEOESTADÍSTICO


if "CVEGEO" in municipios_geo.columns:

    municipios_geo["CVE_MUN"] = (
        municipios_geo["CVEGEO"].astype(str)
    )

elif (
    "CVE_ENT" in municipios_geo.columns
    and "CVE_MUN" in municipios_geo.columns
):

    municipios_geo["CVE_MUN"] = (
        municipios_geo["CVE_ENT"].astype(str)
        + municipios_geo["CVE_MUN"].astype(str)
    )

else:

    raise KeyError(
        "No fue posible identificar la clave municipal "
        "en el Marco Geoestadístico."
    )


mapa = municipios_geo.merge(
    municipal,
    on="CVE_MUN",
    how="left"
)


print()
print("Municipios después de la unión:")
print(len(mapa))



# 15. NOMBRE DEL MUNICIPIO


if "NOMGEO" in mapa.columns:

    mapa["MUNICIPIO"] = mapa["NOMGEO"]

elif "NOM_MUN" in mapa.columns:

    mapa["MUNICIPIO"] = mapa["NOM_MUN"]

else:

    mapa["MUNICIPIO"] = mapa["CVE_MUN"]



# 16. EXPORTAR DATOS MUNICIPALES PREPARADOS


archivo_csv_municipal = (
    BASE_DIR
    / "datos"
    / "indicador_municipal.csv"
)



# DATOS PREPARADOS PARA BUSINESS INTELLIGENCE


datos_bi = mapa[
    [
        "CVE_MUN",
        "MUNICIPIO",
        "N_MUESTRA",
        "POBLACION_PONDERADA",
        "DIFICULTAD_PONDERADA",
        "PORCENTAJE_PONDERADO"
    ]
].copy()

datos_bi.to_csv(
    archivo_csv_municipal,
    index=False,
    encoding="utf-8-sig"
)

print("\nArchivo preparado para Tableau:")
print(archivo_csv_municipal)
print(datos_bi)


print()
print("Datos municipales preparados:")
print(archivo_csv_municipal)



# 17. MAPA INTERACTIVO MUNICIPAL


# Plotly trabaja mejor con coordenadas geográficas WGS84

mapa_wgs84 = mapa.to_crs(epsg=4326)

geojson_municipios = mapa_wgs84.__geo_interface__



# Crear mapa coroplético


fig_mapa = px.choropleth(
    mapa_wgs84,

    geojson=geojson_municipios,

    locations="CVE_MUN",

    featureidkey="properties.CVE_MUN",

    color="PORCENTAJE_PONDERADO",

    # Rango fijo para mantener una interpretación
    # consistente de los colores.
    range_color=(10, 22),

    hover_name="MUNICIPIO",

    color_continuous_scale=[
        [0.00, "#c6dbef"],
        [0.25, "#9ecae1"],
        [0.50, "#6baed6"],
        [0.75, "#3182bd"],
        [1.00, "#08519c"]
    ]
)



# 18. DISEÑO DEL MAPA


fig_mapa.update_geos(
    fitbounds="locations",
    visible=False,

    showcountries=False,
    showcoastlines=False,
    showland=False,

    projection_type="mercator"
)


fig_mapa.update_traces(

    # Cuando se selecciona un municipio,
    # éste conserva toda su intensidad.
    selected=dict(
        marker=dict(
            opacity=1
        )
    ),

    # Los municipios no seleccionados pierden protagonismo.
    unselected=dict(
        marker=dict(
            opacity=0.35
        )
    ),

    # Datos adicionales para el tooltip.
    customdata=mapa_wgs84[
        [
            "MUNICIPIO",
            "N_MUESTRA",
            "POBLACION_PONDERADA"
        ]
    ].to_numpy(),

    marker_line_width=1.0,
    marker_line_color="#5f6b76",

    hovertemplate=(
        "<b>%{hovertext}</b>"
        "<extra></extra>"
    )
)


fig_mapa.update_layout(

    title={
        "text": (
            "<b>La presencia de dificultades reportadas "
            "varía entre los municipios de Aguascalientes</b>"
            "<br>"
            "<sup>Porcentaje ponderado de población con "
            "al menos una dificultad reportada</sup>"
        ),
        "x": 0.5,
        "xanchor": "center"
    },

    # Permite seleccionar municipios mediante clic.
    clickmode="event+select",

    height=650,

    margin=dict(
        l=20,
        r=20,
        t=110,
        b=70
    ),

    coloraxis_colorbar=dict(
    title={
        "text": "Porcentaje<br>ponderado"
    },
    ticksuffix="%",
    x=0.79,
    y=0.50,
    len=0.60,
    thickness=28
),

    annotations=[
        dict(
            text=(
                "Indicador exploratorio elaborado a partir de los "
                "microdatos. No corresponde a una estimación oficial "
                "de prevalencia de discapacidad."
            ),
            x=0.5,
            y=-0.04,
            xref="paper",
            yref="paper",
            showarrow=False,
            xanchor="center",
            font=dict(
                size=11,
                color="#64748B"
            )
        )
    ]
)



# 19. EXPORTAR MAPA INTERACTIVO


archivo_mapa = (
    CARPETA_SALIDA
    / "territorio.html"
)



# Generar HTML base de Plotly


html_mapa = fig_mapa.to_html(
    include_plotlyjs=True,
    full_html=True,
    config={
        "responsive": True,
        "displaylogo": False,
        "scrollZoom": True
    },
    div_id="mapa-territorial"
)



# Panel de información que se mostrará al hacer clic


panel_informacion = """
<style>

#panel-municipio {

    position: fixed;

    top: 145px;
    left: 35px;

    width: 250px;

    background: rgba(255, 255, 255, 0.98);

    border: 1px solid #cbd5e1;
    border-radius: 12px;

    padding: 22px;

    box-shadow:
        0 8px 25px rgba(15, 23, 42, 0.16);

    font-family: Arial, sans-serif;

    display: none;

    z-index: 1000;
}


#panel-municipio h3 {

    margin:
        0
        25px
        14px
        0;

    color: #17202A;

    font-size: 19px;
}


.valor-principal {

    font-size: 30px;

    font-weight: bold;

    color: #24557A;

    margin-bottom: 2px;
}


.descripcion-principal {

    font-size: 12px;

    color: #64748B;

    margin-bottom: 18px;
}


.etiqueta {

    font-size: 12px;

    color: #64748B;

    margin-top: 12px;
}


.valor {

    font-size: 16px;

    font-weight: 600;

    color: #334155;

    margin-top: 2px;
}


#cerrar-panel {

    position: absolute;

    top: 10px;
    right: 12px;

    border: none;

    background: transparent;

    font-size: 21px;

    color: #64748B;

    cursor: pointer;
}

</style>


<div id="panel-municipio">

    <button
        id="cerrar-panel"
        onclick="cerrarPanel()">
        ×
    </button>

    <h3 id="panel-nombre">
    </h3>

    <div
        id="panel-porcentaje"
        class="valor-principal">
    </div>

    <div class="descripcion-principal">
        con alguna dificultad reportada
    </div>

    <div class="etiqueta">
        Personas en la muestra
    </div>

    <div
        id="panel-muestra"
        class="valor">
    </div>

    <div class="etiqueta">
        Población ponderada
    </div>

    <div
        id="panel-poblacion"
        class="valor">
    </div>

</div>


<script>

const mapa = document.getElementById(
    'mapa-territorial'
);


mapa.on(
    'plotly_click',

    function(data) {

        if (!data.points || data.points.length === 0) {
            return;
        }


        const punto = data.points[0];


        const municipio =
            punto.customdata[0];

        const muestra =
            Number(punto.customdata[1]);

        const poblacion =
            Number(punto.customdata[2]);

        const porcentaje =
            Number(punto.z);


        document.getElementById(
            'panel-nombre'
        ).textContent =
            municipio;


        document.getElementById(
            'panel-porcentaje'
        ).textContent =
            porcentaje.toFixed(2) + '%';


        document.getElementById(
            'panel-muestra'
        ).textContent =
            muestra.toLocaleString('es-MX');


        document.getElementById(
            'panel-poblacion'
        ).textContent =
            poblacion.toLocaleString('es-MX');


        document.getElementById(
            'panel-municipio'
        ).style.display =
            'block';
    }
);


function cerrarPanel() {

    document.getElementById(
        'panel-municipio'
    ).style.display =
        'none';


    Plotly.restyle(
        mapa,
        {
            selectedpoints: [null]
        }
    );
}

</script>
"""



# Insertar el panel antes del cierre del BODY


html_mapa = html_mapa.replace(
    "</body>",
    panel_informacion + "</body>"
)



# Guardar HTML final


with open(
    archivo_mapa,
    "w",
    encoding="utf-8"
) as archivo:

    archivo.write(html_mapa)


print()
print("Mapa interactivo creado correctamente:")
print(archivo_mapa)