import pandas as pd
import plotly.express as px
import streamlit as st


df = pd.read_excel(
    io='ventas_supermercado_modif.xlsx',
    engine='openpyxl',
)
# emojis - https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(               # configura la pagina entera
    page_title="Tablero de ventas",
    layout="wide")

# Panel lateral
st.sidebar.header("Opciones de filtrado")
st.markdown(
    """
<style>
span[data-baseweb="tag"] {
  background-color: blue !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# Seleccion de tipo de cliente
membresia = st.sidebar.multiselect(
    "Determine si el cliente es miembro del comercio",
    options=df["membresia"].unique(),
    default=df["membresia"].unique()
)
# Seleccion de sucursal
sucursal = st.sidebar.multiselect(
    "Seleccione la sucursal",
    options=df["sucursal"].unique(),
    default=df["sucursal"].unique()
)
# Seleccion de genero
genero = st.sidebar.multiselect(
    "Seleccione el genero del cliente",
    options=df["genero"].unique(),
    default=df["genero"].unique()
)
# Implementar el filtrado
df_selection = df.query(
    "sucursal == @sucursal & membresia == @membresia & genero == @genero"
)
# Pagina principal
st.title(":bar_chart: Tablero de ventas")
st.markdown("##")           # negrita grande

ventas_totales = round(df_selection["total"].sum(), 2)   # suma columna total

valor_medio_transaccion = round(df_selection["total"].mean(), 2) # promedio columna total
st.dataframe(df_selection)               # despliega un DF en pantalla
st.caption('Tabla fuente de los datos, modificado del archivo "supermarket_sales.csv" que se encuentra en el repositorio Kaggle.')
st.divider()
left_column, right_column = st.columns([0.3,0.7])   # crea dos columnas de distinto ancho
with left_column:
    st.subheader("Ventas totales")
    st.subheader(f":green[$ {ventas_totales}]")

with right_column:
    st.subheader("Valor medio por transaccion")
    st.subheader(f":red[$ {valor_medio_transaccion}]")
st.text('Estadísticos esenciales derivados de la tabla. \nSe calcula la suma total de las ventas y el valor promedio de las ventas.')

# Separador
st.divider()    

# Insertar graficos
venta_linea_producto = (df_selection.groupby(by=["linea"]))[["total"]].sum().sort_values(by="total")
fig_ventas_productos = px.bar(
    venta_linea_producto,
    y="total",
    x=venta_linea_producto.index,
    orientation="v",
    color_discrete_sequence=["blue"] * len(venta_linea_producto),
    template="plotly_white",
)
#fig_ventas_productos.update_layout(title=dict(font=dict(size=30)))
fig_ventas_productos.update_layout(
        height=400,          # altura de barras
)
fig_ventas_productos.update_traces(width=0.5)
fig_ventas_productos.update_layout(
title_text="<b>Ventas por linea de producto</b>",
title_xanchor="left",
title=dict(font=dict(size=30)),        # letra titulo
title_font_color="red",    
title_font_family= "Courier New",            # color titulo
xaxis_title="Linea de producto",
yaxis_title="Ventas",
)
fig_ventas_productos.update_layout(
xaxis = dict(tickfont = dict(size=14)))   # tamaño etiquetas eje X
fig_ventas_productos.update_xaxes(tickangle=45) # inclinacion etiquetas eje X
st.plotly_chart(fig_ventas_productos)
st.caption('Gráfico de barras interactivo mostrando el total de ventas por cada línea de producto. Los valores se dan en miles de pesos. Sobrevolar el cursor por las barras para ver los valores.')
