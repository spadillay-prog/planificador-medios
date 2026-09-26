import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Simulador de Medios Vía Pública & DOOH",
    page_icon="🎯",
    layout="wide"
)

# Base territorial con Residente y Flotante precargados
DATA_TERRITORIAL = {
    "Región Metropolitana": {
        # --- SECTORES MACRO ---
        "Sector Oriente (Las Condes, Providencia, Vitacura, Ñuñoa, La Reina, Lo Barnechea)": {"res": 1060000, "flot": 800000},
        "Sector Centro (Santiago Centro)": {"res": 500000, "flot": 1000000},
        "Sector Poniente (Maipú, Pudahuel, Est. Central, Cerrillos, Lo Prado, etc.)": {"res": 1600000, "flot": 550000},
        "Sector Norte (Huechuraba, Quilicura, Conchalí, Independencia, Recoleta, Renca)": {"res": 1250000, "flot": 450000},
        "Sector Sur (San Miguel, San Joaquín, La Cisterna, San Bernardo, El Bosque, etc.)": {"res": 1400000, "flot": 300000},
        "Sector Sur-Oriente (La Florida, Puente Alto, Peñalolén, Macul)": {"res": 1420000, "flot": 250000},
        
        # --- COMUNAS INDIVIDUALES Y NODOS ESPECÍFICOS ---
        "Las Condes / Apoquindo": {"res": 330000, "flot": 450000},
        "Providencia": {"res": 155000, "flot": 350000},
        "Ñuñoa": {"res": 255000, "flot": 80000},
        "Santiago Centro (Casco Histórico / Alameda)": {"res": 500000, "flot": 1000000},
        "Estación Central (Eje Alameda / Terminales)": {"res": 210000, "flot": 350000},
        "Maipú": {"res": 580000, "flot": 80000},
        "Pudahuel (Eje Logístico / Aeropuerto)": {"res": 255000, "flot": 120000},
        "Huechuraba / Ciudad Empresarial": {"res": 110000, "flot": 130000},
        "Quilicura (Eje Industrial)": {"res": 260000, "flot": 90000},
        "Independencia / Recoleta (Eje Hospitales / La Vega)": {"res": 310000, "flot": 180000},
        "San Miguel (Eje Gran Avenida)": {"res": 140000, "flot": 70000},
        "La Florida (Eje Vicuña Mackenna / Bellavista)": {"res": 400000, "flot": 110000},
        "Puente Alto": {"res": 650000, "flot": 60000},
        "Rotonda Quilín / Eje Vespucio Sur (DOOH)": {"res": 130000, "flot": 50000},
    },
    "Región de Valparaíso": {
        "Gran Valparaíso (Viña del Mar + Valparaíso + Concón)": {"res": 750000, "flot": 150000},
        "Viña del Mar": {"res": 360000, "flot": 120000},
        "Valparaíso": {"res": 315000, "flot": 90000},
        "Quilpué / Villa Alemana": {"res": 280000, "flot": 40000},
        "Concón": {"res": 65000, "flot": 35000},
    },
    "Región del Biobío": {
        "Gran Concepción (Concepción + Talcahuano + San Pedro + Hualpén)": {"res": 850000, "flot": 200000},
        "Concepción": {"res": 240000, "flot": 160000},
        "Talcahuano": {"res": 160000, "flot": 50000},
        "Los Ángeles": {"res": 220000, "flot": 40000},
    },
    "Región de Coquimbo": {
        "Conurbación Gran La Serena (La Serena + Coquimbo)": {"res": 530000, "flot": 60000},
        "La Serena": {"res": 260000, "flot": 40000},
        "Coquimbo": {"res": 270000, "flot": 35000},
        "Ovalle": {"res": 125000, "flot": 15000},
    },
    "Región de Antofagasta": {
        "Antofagasta": {"res": 440000, "flot": 50000},
        "Calama": {"res": 190000, "flot": 35000},
    },
    "Región de La Araucanía": {
        "Temuco / Padre Las Casas": {"res": 410000, "flot": 70000},
        "Temuco": {"res": 310000, "flot": 65000},
        "Villarrica / Pucón": {"res": 105000, "flot": 50000},
    },
    "Región de O'Higgins": {
        "Rancagua / Machalí": {"res": 320000, "flot": 60000},
        "San Fernando": {"res": 80000, "flot": 15000},
    },
    "Región del Maule": {
        "Talca / Maule": {"res": 290000, "flot": 50000},
        "Curicó": {"res": 165000, "flot": 25000},
        "Linares": {"res": 100000, "flot": 15000},
    },
    "Región de Los Lagos": {
        "Puerto Montt / Puerto Varas": {"res": 330000, "flot": 60000},
        "Osorno": {"res": 175000, "flot": 30000},
        "Castro (Chiloé)": {"res": 55000, "flot": 20000},
    },
    "Región de Tarapacá": {
        "Iquique / Alto Hospicio": {"res": 340000, "flot": 50000},
        "Iquique (ZOFRI / Borde Costero)": {"res": 225000, "flot": 60000},
        "Alto Hospicio": {"res": 135000, "flot": 15000},
    }
}

# Formatos y bases unitarias de cálculo
FORMATOS = {
    "Buses Troncales / Gran Impacto": {
        "c": 0.30, "m": 0.35, "o": 0.40,
        "base_unidades": 70,
        "unidad_nombre": "buses",
        "desc": "Presencia en avenidas estructurantes (Tasa base para flota de 70 buses)."
    },
    "Lunetas en Microbuses": {
        "c": 0.25, "m": 0.30, "o": 0.35,
        "base_unidades": 40,
        "unidad_nombre": "lunetas",
        "desc": "Alta saturación visual vehicular y semáforos (Tasa base para 40 lunetas)."
    },
    "Pantalla Digital Gran Formato (DOOH)": {
        "c": 0.20, "m": 0.25, "o": 0.30,
        "base_unidades": 1,
        "unidad_nombre": "pantallas",
        "desc": "Impacto visual dinámico en nudos de tráfico (Tasa base por pantalla individual)."
    },
    "Valla / Monoposte Estático": {
        "c": 0.15, "m": 0.20, "o": 0.25,
        "base_unidades": 1,
        "unidad_nombre": "soportes",
        "desc": "Exposición continua en puntos fijos (Tasa base por cada soporte unitario)."
    }
}

st.title("🎯 Planificador & Simulador de Medios OOH / DOOH")
st.markdown("Herramienta para estimar impactos brutos, alcance y CPM por sector, comuna y cantidad de elementos.")

st.sidebar.header("⚙️ Configuración del Plan")

# 1. Selector Territorial
region_sel = st.sidebar.selectbox("1. Selecciona Región:", list(DATA_TERRITORIAL.keys()))
comunas_dict = DATA_TERRITORIAL[region_sel]
comuna_sel = st.sidebar.selectbox("2. Selecciona Sector o Comuna:", list(comunas_dict.keys()))

datos_plaza = comunas_dict[comuna_sel]
pop_residente_default = datos_plaza["res"]
pop_flotante_default = datos_plaza["flot"]

# 2. Población y Audiencia
st.sidebar.markdown("---")
st.sidebar.subheader("Población y Audiencia")
pop_residente = st.sidebar.number_input("Población Residente:", value=pop_residente_default, step=10000)
pop_flotante = st.sidebar.number_input("Población Flotante Estimada (trabajo/estudio/tráfico):", value=pop_flotante_default, step=10000)

universo_total = pop_residente + pop_flotante
st.sidebar.info(f"**Universo Total Activo Diario:** {universo_total:,.0f} personas".replace(",", "."))

# 3. Soporte y Cantidad
st.sidebar.markdown("---")
st.sidebar.subheader("Soporte y Cantidad")
formato_sel = st.sidebar.selectbox("3. Formato Vía Pública:", list(FORMATOS.keys()))
info_formato = FORMATOS[formato_sel]

cant_elementos = st.sidebar.number_input(
    f"Cantidad de {info_formato['unidad_nombre'].capitalize()} contratadas:",
    min_value=1,
    max_value=500,
    value=info_formato["base_unidades"],
    step=1
)

dias_campana = st.sidebar.slider("Días de Campaña (Exhibición):", min_value=1, max_value=90, value=30)
inversion_neta = st.sidebar.number_input("Inversión Neta ($ CLP):", value=4500000, step=500000)

# Factor de escala de unidades
factor_elementos = cant_elementos / info_formato["base_unidades"]

# Descuento / Castigo técnico
castigo_pct = st.sidebar.slider("Castigo Técnico / Descuento Duplicidad (%):", min_value=0, max_value=25, value=0, step=5)
factor_castigo = (100 - castigo_pct) / 100

# Tasas base
t_c, t_m, t_o = info_formato["c"], info_formato["m"], info_formato["o"]

# --- CÁLCULOS ---
escenarios = [
    {"nombre": "Conservador", "tasa": t_c},
    {"nombre": "Medio (Base Recomendado)", "tasa": t_m},
    {"nombre": "Optimista", "tasa": t_o}
]

resultados = []
for esc in escenarios:
    contactos_dia_base = universo_total * esc["tasa"]
    contactos_dia_ajustados = contactos_dia_base * factor_elementos * factor_castigo
    impactos_totales = contactos_dia_ajustados * dias_campana
    
    costo_impacto = (inversion_neta / impactos_totales) if impactos_totales > 0 else 0
    cpm = costo_impacto * 1000
    
    resultados.append({
        "Escenario": esc["nombre"],
        "Tasa Base Diaria": f"{int(esc['tasa'] * 100)}%",
        "Contactos Diarios": f"{int(contactos_dia_ajustados):,}".replace(",", "."),
        f"Impactos Totales ({dias_campana} días)": f"{int(impactos_totales):,}".replace(",", "."),
        "Costo x Impacto": f"${costo_impacto:.2f}",
        "CPM ($ CLP)": f"${int(round(cpm)):,}".replace(",", ".")
    })

df_res = pd.DataFrame(resultados)

# --- VISTA PRINCIPAL ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Universo Activo Diario", f"{universo_total:,.0f}".replace(",", "."))
col2.metric("Soportes Contratados", f"{cant_elementos} {info_formato['unidad_nombre']}")
col3.metric("Duración Campaña", f"{dias_campana} días")
col4.metric("Inversión Neta", f"${inversion_neta:,.0f}".replace(",", "."))

st.markdown("---")
st.subheader(f"📊 Proyección: {cant_elementos} {info_formato['unidad_nombre'].capitalize()} en {comuna_sel}")
st.caption(f"{info_formato['desc']} | Factor de escala: {factor_elementos:.2f}x" + (f" | Castigo técnico: {castigo_pct}%" if castigo_pct > 0 else ""))

st.table(df_res)

# Resumen tipo propuesta
st.markdown("---")
st.subheader("📋 Resumen Ejecutivo para Propuesta")
esc_medio = resultados[1]
texto_propuesta = f"""**Resumen de Propuesta Comercial:**
- **Plaza / Territorio:** {comuna_sel} ({region_sel})
- **Población Residente:** {pop_residente:,.0f} | **Población Flotante:** {pop_flotante:,.0f}
- **Universo Activo Diario:** {universo_total:,.0f} personas
- **Soporte:** {formato_sel} ({cant_elementos} {info_formato['unidad_nombre']})
- **Duración:** {dias_campana} días
- **Inversión Neta:** ${inversion_neta:,.0f} CLP
- **Contactos Diarios Estimados (Escenario Medio):** {esc_medio['Contactos Diarios']}
- **Impactos Brutos Totales (OTS):** {esc_medio[f'Impactos Totales ({dias_campana} días)']}
- **Costo por Impacto:** {esc_medio['Costo x Impacto']} CLP
- **CPM Estimado:** {esc_medio['CPM ($ CLP)']} CLP
"""
st.code(texto_propuesta, language="markdown")
