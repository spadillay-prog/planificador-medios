import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Simulador de Medios Vía Pública & DOOH",
    page_icon="🎯",
    layout="wide"
)

# Base territorial
DATA_TERRITORIAL = {
    "Región Metropolitana": {
        "Santiago Oriente (Las Condes, Vitacura, Providencia, Ñuñoa, La Reina, Lo Barnechea)": 1060000,
        "Santiago Centro": 500000,
        "Puente Alto": 650000,
        "Maipú": 580000,
        "La Florida": 400000,
        "Rotonda Quilín / Eje Vespucio Sur (DOOH)": 130000,
        "San Bernardo": 335000,
        "Independencia / Recoleta": 310000,
    },
    "Región de Valparaíso": {
        "Gran Valparaíso (Viña del Mar + Valparaíso + Concón)": 750000,
        "Viña del Mar": 360000,
        "Valparaíso": 315000,
        "Quilpué / Villa Alemana": 280000,
        "Concón": 65000,
    },
    "Región del Biobío": {
        "Gran Concepción (Concepción + Talcahuano + San Pedro + Hualpén)": 850000,
        "Concepción": 240000,
        "Talcahuano": 160000,
        "Los Ángeles": 220000,
    },
    "Región de Coquimbo": {
        "Conurbación Gran La Serena (La Serena + Coquimbo)": 530000,
        "La Serena": 260000,
        "Coquimbo": 270000,
        "Ovalle": 125000,
    },
    "Región de Antofagasta": {
        "Antofagasta": 440000,
        "Calama": 190000,
    },
    "Región de La Araucanía": {
        "Temuco / Padre Las Casas": 410000,
        "Temuco": 310000,
        "Villarrica / Pucón": 105000,
    },
    "Región de O'Higgins": {
        "Rancagua / Machalí": 320000,
        "San Fernando": 80000,
    },
    "Región del Maule": {
        "Talca / Maule": 290000,
        "Curicó": 165000,
        "Linares": 100000,
    },
    "Región de Los Lagos": {
        "Puerto Montt / Puerto Varas": 330000,
        "Osorno": 175000,
        "Castro (Chiloé)": 55000,
    },
    "Región de Tarapacá": {
        "Iquique / Alto Hospicio": 340000,
        "Iquique": 225000,
        "Alto Hospicio": 135000,
    }
}

# Formatos con su base de referencia para el cálculo de tasas
FORMATOS = {
    "Buses Troncales / Gran Impacto": {
        "c": 0.30, "m": 0.35, "o": 0.40,
        "base_unidades": 70,
        "unidad_nombre": "buses",
        "desc": "Presencia dominante en avenidas estructurantes (Tasa base calibrada para flota estándar de 70 buses)."
    },
    "Lunetas en Microbuses": {
        "c": 0.25, "m": 0.30, "o": 0.35,
        "base_unidades": 40,
        "unidad_nombre": "lunetas",
        "desc": "Alta saturación visual vehicular (Tasa base calibrada para circuito estándar de 40 lunetas)."
    },
    "Pantalla Digital Gran Formato (DOOH)": {
        "c": 0.20, "m": 0.25, "o": 0.30,
        "base_unidades": 1,
        "unidad_nombre": "pantallas",
        "desc": "Impacto dinámico en nudos de tráfico y detención (Tasa base por cada pantalla individual)."
    },
    "Valla / Monoposte Estático": {
        "c": 0.15, "m": 0.20, "o": 0.25,
        "base_unidades": 1,
        "unidad_nombre": "soportes",
        "desc": "Exposición continua en puntos estratégicos (Tasa base por cada soporte unitario)."
    }
}

st.title("🎯 Planificador & Simulador de Medios OOH / DOOH")
st.markdown("Herramienta para estimar impactos brutos, alcance y CPM por cantidad de elementos en Chile.")

st.sidebar.header("⚙️ Configuración del Plan")

# 1. Selección Territorial
region_sel = st.sidebar.selectbox("1. Selecciona Región:", list(DATA_TERRITORIAL.keys()))
comunas_dict = DATA_TERRITORIAL[region_sel]
comuna_sel = st.sidebar.selectbox("2. Selecciona Comuna o Conurbación:", list(comunas_dict.keys()))

pop_base = comunas_dict[comuna_sel]

# Audiencia Flotante
st.sidebar.markdown("---")
st.sidebar.subheader("Población y Audiencia")
flotante = st.sidebar.number_input(
    "Población Flotante Adicional (trabajo, compras, turismo):",
    value=800000 if "Santiago Oriente" in comuna_sel else (50000 if "Antofagasta" in comuna_sel else 0),
    step=25000
)
universo_total = pop_base + flotante
st.sidebar.info(f"**Universo Total Activo Diario:** {universo_total:,.0f} personas")

# 2. Soporte y Cantidad de Elementos
st.sidebar.markdown("---")
st.sidebar.subheader("Soporte y Cantidad")
formato_sel = st.sidebar.selectbox("3. Formato Vía Pública:", list(FORMATOS.keys()))
info_formato = FORMATOS[formato_sel]

# Input para cantidad de elementos
cant_elementos = st.sidebar.number_input(
    f"Cantidad de {info_formato['unidad_nombre'].capitalize()} contratadas:",
    min_value=1,
    max_value=500,
    value=info_formato["base_unidades"],
    step=1
)

dias_campana = st.sidebar.slider("Días de Campaña (Exhibición):", min_value=1, max_value=90, value=30)
inversion_neta = st.sidebar.number_input("Inversión Neta ($ CLP):", value=4500000, step=500000)

# Factor de escala por volumen de soportes
factor_elementos = cant_elementos / info_formato["base_unidades"]

# Ajuste fino de tasas (opcional con sliders)
with st.sidebar.expander("Ajuste manual de tasas base (% exposición diaria)"):
    t_c = st.slider("Escenario Conservador (%)", 5, 50, int(info_formato["c"] * 100)) / 100
    t_m = st.slider("Escenario Medio (%)", 5, 60, int(info_formato["m"] * 100)) / 100
    t_o = st.slider("Escenario Optimista (%)", 5, 70, int(info_formato["o"] * 100)) / 100

# Descuento / Castigo técnico
castigo_pct = st.sidebar.slider("Castigo Técnico / Descuento Duplicidad (%):", min_value=0, max_value=25, value=0, step=5)
factor_castigo = (100 - castigo_pct) / 100

# --- CÁLCULOS ---
escenarios = [
    {"nombre": "Conservador", "tasa": t_c},
    {"nombre": "Medio (Base Recomendado)", "tasa": t_m},
    {"nombre": "Optimista", "tasa": t_o}
]

resultados = []
for esc in escenarios:
    # Contactos ajustados por cantidad de soportes y castigo
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
st.caption(f"{info_formato['desc']} | Factor de escala de flota: {factor_elementos:.2f}x" + (f" | Castigo técnico: {castigo_pct}%" if castigo_pct > 0 else ""))

st.table(df_res)

# Resumen tipo propuesta
st.markdown("---")
st.subheader("📋 Resumen Ejecutivo para Propuesta")
esc_medio = resultados[1]
texto_propuesta = f"""**Resumen de Propuesta Comercial:**
- **Plaza / Territorio:** {comuna_sel} ({region_sel})
- **Soporte:** {formato_sel} ({cant_elementos} {info_formato['unidad_nombre']})
- **Duración:** {dias_campana} días
- **Universo Activo Diario:** {universo_total:,.0f} personas
- **Inversión Neta:** ${inversion_neta:,.0f} CLP
- **Contactos Diarios Estimados (Escenario Medio):** {esc_medio['Contactos Diarios']}
- **Impactos Brutos Totales (OTS):** {esc_medio[f'Impactos Totales ({dias_campana} días)']}
- **Costo por Impacto:** {esc_medio['Costo x Impacto']} CLP
- **CPM Estimado:** {esc_medio['CPM ($ CLP)']} CLP
"""
st.code(texto_propuesta, language="markdown")
