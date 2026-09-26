import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Simulador de Medios Vía Pública & DOOH",
    page_icon="🎯",
    layout="wide"
)

# Base de datos de las 10 regiones más pobladas y sus principales comunas/conurbaciones
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

# Parámetros sugeridos de exposición diaria según formato
FORMATOS = {
    "Buses Troncales / Gran Impacto": {"c": 0.30, "m": 0.35, "o": 0.40, "desc": "Presencia dominante en avenidas estructurantes."},
    "Lunetas en Microbuses": {"c": 0.25, "m": 0.30, "o": 0.35, "desc": "Alta saturación visual para flujo vehicular y semáforos."},
    "Pantalla Digital Gran Formato (DOOH)": {"c": 0.20, "m": 0.25, "o": 0.30, "desc": "Impacto visual dinámico en nudos de tráfico y detención."},
    "Valla / Monoposte Estático": {"c": 0.15, "m": 0.20, "o": 0.25, "desc": "Exposición continua en puntos estratégicos."}
}

st.title("🎯 Planificador & Simulador de Medios OOH / DOOH")
st.markdown("Herramienta para estimar impactos brutos, alcance y CPM en las principales plazas de Chile.")

st.sidebar.header("⚙️ Configuración del Plan")

# Selector de Región y Comuna
region_sel = st.sidebar.selectbox("1. Selecciona Región:", list(DATA_TERRITORIAL.keys()))
comunas_dict = DATA_TERRITORIAL[region_sel]
comuna_sel = st.sidebar.selectbox("2. Selecciona Comuna o Conurbación:", list(comunas_dict.keys()))

pop_base = comunas_dict[comuna_sel]

# Población flotante opcional
st.sidebar.markdown("---")
st.sidebar.subheader("Población y Audiencia")
flotante = st.sidebar.number_input(
    "Población Flotante Adicional (trabajo, compras, turismo):",
    value=800000 if "Santiago Oriente" in comuna_sel else (50000 if "Antofagasta" in comuna_sel else 0),
    step=25000
)

universo_total = pop_base + flotante
st.sidebar.info(f"**Universo Total Activo Diario:** {universo_total:,.0f} personas")

# Configuración del soporte
st.sidebar.markdown("---")
st.sidebar.subheader("Soporte Publicitario")
formato_sel = st.sidebar.selectbox("3. Formato Vía Pública:", list(FORMATOS.keys()))
info_formato = FORMATOS[formato_sel]

dias_campana = st.sidebar.slider("Días de Campaña (Exhibición):", min_value=1, max_value=90, value=30)
inversion_neta = st.sidebar.number_input("Inversión Neta ($ CLP):", value=4500000, step=500000)

# Ajuste fino de tasas (opcional con sliders)
with st.sidebar.expander("Ajuste manual de tasas (% de exposición diaria)"):
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
    contactos_dia_brutos = universo_total * esc["tasa"]
    contactos_dia_ajustados = contactos_dia_brutos * factor_castigo
    impactos_totales = contactos_dia_ajustados * dias_campana
    
    costo_impacto = (inversion_neta / impactos_totales) if impactos_totales > 0 else 0
    cpm = costo_impacto * 1000
    
    resultados.append({
        "Escenario": esc["nombre"],
        "Tasa Diaria": f"{int(esc['tasa'] * 100)}%",
        "Contactos Diarios": f"{int(contactos_dia_ajustados):,}".replace(",", "."),
        f"Impactos Totales ({dias_campana} días)": f"{int(impactos_totales):,}".replace(",", "."),
        "Costo x Impacto": f"${costo_impacto:.2f}",
        "CPM ($ CLP)": f"${int(round(cpm)):,}".replace(",", ".")
    })

df_res = pd.DataFrame(resultados)

# --- VISTA PRINCIPAL ---
col1, col2, col3 = st.columns(3)
col1.metric("Universo Activo Diario", f"{universo_total:,.0f}".replace(",", "."))
col2.metric("Duración Campaña", f"{dias_campana} días")
col3.metric("Inversión Neta", f"${inversion_neta:,.0f}".replace(",", "."))

st.markdown("---")
st.subheader(f"📊 Proyección: {formato_sel} en {comuna_sel}")
st.caption(f"{info_formato['desc']} " + (f"(Aplica castigo técnico del {castigo_pct}%)" if castigo_pct > 0 else ""))

st.table(df_res)

# Resumen tipo propuesta para copiar
st.markdown("---")
st.subheader("📋 Resumen Ejecutivo para Propuesta")
esc_medio = resultados[1]
texto_propuesta = f"""**Resumen de Campaña:**
- **Plaza / Territorio:** {comuna_sel} ({region_sel})
- **Soporte:** {formato_sel}
- **Duración:** {dias_campana} días
- **Universo Activo Diario:** {universo_total:,.0f} personas
- **Inversión Neta:** ${inversion_neta:,.0f} CLP
- **Contactos Diarios Estimados (Escenario Medio):** {esc_medio['Contactos Diarios']}
- **Impactos Brutos Totales (OTS):** {esc_medio[f'Impactos Totales ({dias_campana} días)']}
- **CPM Estimado:** {esc_medio['CPM ($ CLP)']} CLP
"""
st.code(texto_propuesta, language="markdown")
