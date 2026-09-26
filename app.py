import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(
    page_title="Planificador de Medios & Exportador JPG",
    page_icon="🎯",
    layout="wide"
)

# Paletas de color por cliente / marca
TEMAS_COLOR = {
    "Smart Fit (Amarillo / Negro)": {"primary": "#FFB800", "bg": "#121316", "card": "#1E1F24", "text": "#FFFFFF", "accent": "#FFB800"},
    "Corporativo Azul": {"primary": "#2D7FF9", "bg": "#0E131F", "card": "#182032", "text": "#FFFFFF", "accent": "#2D7FF9"},
    "Retail Rojo": {"primary": "#E50914", "bg": "#141414", "card": "#222222", "text": "#FFFFFF", "accent": "#E50914"},
    "Eco / Salud Verde": {"primary": "#00C853", "bg": "#0D1811", "card": "#18281D", "text": "#FFFFFF", "accent": "#00C853"},
    "Fintech Morado": {"primary": "#8A2BE2", "bg": "#120D1D", "card": "#211833", "text": "#FFFFFF", "accent": "#8A2BE2"},
}

# Base de datos simplificada para visualización y cálculo
DATA_TERRITORIAL = {
    "Coquimbo": {"res": 240000, "flot": 40000, "contexto": "Coquimbo concentra su movimiento en pocos ejes que todas las rutas terminan cruzando, por lo que las unidades alcanzan para que la gráfica aparezca varias veces al día a una misma persona."},
    "La Serena": {"res": 240000, "flot": 40000, "contexto": "Eje Balmaceda y Ruta 5 conectan el flujo intercomunal con alta retención en semáforos y centros comerciales."},
    "Antofagasta": {"res": 440000, "flot": 50000, "contexto": "Ciudad lineal encajonada entre cerro y mar; la concentración vehicular en Av. Costanera y Pedro Aguirre Cerda eleva los OTS diarios."},
    "Santiago Oriente": {"res": 1060000, "flot": 800000, "contexto": "Polo corporativo y financiero de máxima afluencia flotante de la capital, ideal para campañas de cobertura y frecuencia masiva."},
    "San Joaquín (Vespucio / Departamental)": {"res": 103000, "flot": 65000, "contexto": "Nudo estratégico con alta densidad comercial (Mall Florida Center) y conectividad con Metro Línea 5."},
}

FORMATOS = {
    "Lunetas Buses": {"base": 30, "c": 0.20, "m": 0.25, "o": 0.30, "tipo": "Cobertura móvil", "unidad": "lunetas"},
    "Pantalla Digital (DOOH)": {"base": 1, "c": 0.20, "m": 0.25, "o": 0.30, "tipo": "Gran impacto LED", "unidad": "pantallas"},
    "Buses Troncales": {"base": 70, "c": 0.30, "m": 0.35, "o": 0.40, "tipo": "Troncal móvil", "unidad": "buses"},
    "Valla Estática": {"base": 1, "c": 0.15, "m": 0.20, "o": 0.25, "tipo": "Soporte fijo", "unidad": "soportes"}
}

st.sidebar.header("🎨 Identidad del Cliente")
tema_sel = st.sidebar.selectbox("Tema de Color:", list(TEMAS_COLOR.keys()))
colores = TEMAS_COLOR[tema_sel]

st.sidebar.header("⚙️ Configuración del Soporte")
plaza_sel = st.sidebar.selectbox("Plaza / Territorio:", list(DATA_TERRITORIAL.keys()))
formato_sel = st.sidebar.selectbox("Formato Publicitario:", list(FORMATOS.keys()))

info_p = DATA_TERRITORIAL[plaza_sel]
info_f = FORMATOS[formato_sel]

cant_unidades = st.sidebar.number_input(f"Cantidad de {info_f['unidad']}:", min_value=1, value=info_f["base"], step=1)
dias_campana = st.sidebar.number_input("Días de Campaña:", min_value=1, value=30, step=1)
inversion_total = st.sidebar.number_input("Inversión Total ($ CLP):", min_value=100000, value=2500000, step=250000)

foto_soporte = st.sidebar.file_uploader("Subir foto del soporte (opcional para la lámina):", type=["jpg", "png", "jpeg"])

comentario_custom = st.sidebar.text_area(
    "Ventaja Estratégica / Comentarios:",
    value=info_p["contexto"],
    height=100
)

# Cálculos
universo = info_p["res"] + info_p["flot"]
factor_escala = cant_unidades / info_f["base"]

costo_unitario = inversion_total / cant_unidades if cant_unidades > 0 else 0
imp_diarios_m = universo * info_f["m"] * factor_escala
imp_totales_m = imp_diarios_m * dias_campana
cpm_m = (inversion_total / imp_totales_m * 1000) if imp_totales_m > 0 else 0
costo_impacto_m = inversion_total / imp_totales_m if imp_totales_m > 0 else 0

tabla_esc = [
    {"esc": "Conservador", "rate": info_f["c"], "dia": universo * info_f["c"] * factor_escala, "tot": universo * info_f["c"] * factor_escala * dias_campana},
    {"esc": "Medio", "rate": info_f["m"], "dia": imp_diarios_m, "tot": imp_totales_m},
    {"esc": "Optimista", "rate": info_f["o"], "dia": universo * info_f["o"] * factor_escala, "tot": universo * info_f["o"] * factor_escala * dias_campana}
]

# --- GENERADOR DE IMAGEN PIL (LÁMINA EJECUTIVA 1920x1080) ---
def render_lamina_jpg():
    W, H = 1920, 1080
    im = Image.new("RGB", (W, H), colores["bg"])
    draw = ImageDraw.Draw(im)

    # Cabecera
    title_text = f"{plaza_sel.upper()} — {formato_sel.upper()}"
    subtitle_text = f"{cant_unidades} {info_f['unidad']} · {dias_campana} días"
    
    draw.text((60, 50), title_text, fill=colores["primary"], font_size=42)
    draw.text((W - 380, 60), subtitle_text, fill="#CCCCCC", font_size=24)
    draw.line([(60, 115), (W - 60, 115)], fill=colores["primary"], width=2)

    # Espacio para foto del soporte
    foto_box = (60, 150, 720, 960)
    if foto_soporte is not None:
        try:
            uploaded_img = Image.open(foto_soporte).convert("RGB")
            uploaded_img = uploaded_img.resize((660, 810))
            im.paste(uploaded_img, (60, 150))
        except Exception:
            draw.rectangle(foto_box, fill=colores["card"])
    else:
        draw.rectangle(foto_box, fill=colores["card"])
        draw.text((220, 530), "[ FOTO SOPORTE ]", fill="#777777", font_size=28)

    # 3 Tarjetas Superiores
    card_w, card_h = 360, 130
    x_offset = 760
    
    # Tarjeta 1: Inversión
    draw.rounded_rectangle([(x_offset, 150), (x_offset + card_w, 150 + card_h)], radius=12, fill=colores["card"])
    draw.text((x_offset + 25, 170), "Inversión mensual", fill="#999999", font_size=18)
    draw.text((x_offset + 25, 205), f"${inversion_total:,.0f}".replace(",", "."), fill="#FFFFFF", font_size=34)

    # Tarjeta 2: Costo Unitario
    draw.rounded_rectangle([(x_offset + card_w + 30, 150), (x_offset + card_w*2 + 30, 150 + card_h)], radius=12, fill=colores["card"])
    draw.text((x_offset + card_w + 55, 170), f"Costo por {info_f['unidad'][:-1]} / mes", fill="#999999", font_size=18)
    draw.text((x_offset + card_w + 55, 205), f"${costo_unitario:,.0f}".replace(",", "."), fill="#FFFFFF", font_size=34)

    # Tarjeta 3: Impactos Totales (Destacada en color de marca)
    draw.rounded_rectangle([(x_offset + card_w*2 + 60, 150), (x_offset + card_w*3 + 60, 150 + card_h)], radius=12, fill=colores["primary"])
    draw.text((x_offset + card_w*2 + 85, 170), f"Impactos {dias_campana} días (caso medio)", fill="#000000", font_size=18)
    draw.text((x_offset + card_w*2 + 85, 205), f"{imp_totales_m:,.0f}".replace(",", "."), fill="#000000", font_size=36)

    # Tabla de Escenarios
    t_y = 320
    draw.text((x_offset + 20, t_y), "Escenario", fill="#AAAAAA", font_size=18)
    draw.text((x_offset + 270, t_y), "% Exposición diaria", fill="#AAAAAA", font_size=18)
    draw.text((x_offset + 520, t_y), "Contactos diarios", fill="#AAAAAA", font_size=18)
    draw.text((x_offset + 750, t_y), f"Impactos {dias_campana} días", fill="#AAAAAA", font_size=18)
    draw.text((x_offset + 990, t_y), "CPM Efectivo", fill="#AAAAAA", font_size=18)
    draw.line([(x_offset + 20, t_y + 35), (W - 60, t_y + 35)], fill="#333333", width=1)

    row_y = t_y + 55
    for item in tabla_esc:
        is_medio = item["esc"] == "Medio"
        c_fill = colores["primary"] if is_medio else "#FFFFFF"
        cpm_val = (inversion_total / item["tot"] * 1000) if item["tot"] > 0 else 0
        
        draw.text((x_offset + 20, row_y), item["esc"], fill=c_fill, font_size=20)
        draw.text((x_offset + 300, row_y), f"{int(item['rate']*100)}%", fill="#DDDDDD", font_size=20)
        draw.text((x_offset + 520, row_y), f"{int(item['dia']):,}".replace(",", "."), fill="#DDDDDD", font_size=20)
        draw.text((x_offset + 750, row_y), f"{int(item['tot']):,}".replace(",", "."), fill="#DDDDDD", font_size=20)
        draw.text((x_offset + 990, row_y), f"${int(round(cpm_val)):,}".replace(",", "."), fill="#DDDDDD", font_size=20)
        row_y += 45

    # 3 Tarjetas Inferiores
    b_y = 510
    draw.rounded_rectangle([(x_offset, b_y), (x_offset + card_w, b_y + card_h)], radius=12, fill=colores["card"])
    draw.text((x_offset + 25, b_y + 20), "Universo activo diario", fill="#999999", font_size=18)
    draw.text((x_offset + 25, b_y + 55), f"{universo:,.0f}".replace(",", "."), fill=colores["primary"], font_size=34)

    draw.rounded_rectangle([(x_offset + card_w + 30, b_y), (x_offset + card_w*2 + 30, b_y + card_h)], radius=12, fill=colores["card"])
    draw.text((x_offset + card_w + 55, b_y + 20), "Costo x impacto (medio)", fill="#999999", font_size=18)
    draw.text((x_offset + card_w + 55, b_y + 55), f"${costo_impacto_m:.1f} CLP", fill=colores["primary"], font_size=34)

    draw.rounded_rectangle([(x_offset + card_w*2 + 60, b_y), (x_offset + card_w*3 + 60, b_y + card_h)], radius=12, fill=colores["card"])
    draw.text((x_offset + card_w*2 + 85, b_y + 20), "Naturaleza del formato", fill="#999999", font_size=18)
    draw.text((x_offset + card_w*2 + 85, b_y + 55), info_f["tipo"], fill=colores["primary"], font_size=32)

    # Contenedor de Comentarios Estratégicos
    com_y = 680
    draw.rounded_rectangle([(x_offset, com_y), (W - 60, 960)], radius=12, fill=colores["card"])
    draw.line([(x_offset, com_y), (x_offset, 960)], fill=colores["primary"], width=6)
    
    draw.text((x_offset + 30, com_y + 25), f"Universo activo diario: {info_p['res']:,} habitantes + {info_p['flot']:,} flotante = {universo:,}".replace(",", "."), fill="#DDDDDD", font_size=18)
    draw.text((x_offset + 30, com_y + 70), "VENTAJA ESTRATÉGICA DEL FORMATO", fill=colores["primary"], font_size=20)
    
    # Texto multilinea para el comentario
    words = comentario_custom.split()
    lines, current_line = [], ""
    for w in words:
        if len(current_line + " " + w) < 95:
            current_line += " " + w
        else:
            lines.append(current_line.strip())
            current_line = w
    if current_line:
        lines.append(current_line.strip())
        
    line_y = com_y + 115
    for l in lines[:4]:
        draw.text((x_offset + 30, line_y), l, fill="#CCCCCC", font_size=18)
        line_y += 32

    # Pie de página
    draw.text((60, 1010), f"Inversión mensual total: ${inversion_total:,.0f} CLP · Flota: {cant_unidades} unidades · Valores en CLP neto.".replace(",", "."), fill="#777777", font_size=16)

    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=95)
    return buf.getvalue()

# --- VISTA STREAMLIT ---
st.title("🎯 Generador de Láminas de Propuesta OOH")
st.markdown("Visualiza la lámina ejecutiva y descárgala directamente en formato JPG en alta calidad.")

img_bytes = render_lamina_jpg()

st.image(img_bytes, caption=f"Vista previa de la lámina — {plaza_sel} ({tema_sel})", use_container_width=True)

st.download_button(
    label="📥 Descargar Lámina en JPG (Alta Resolución)",
    data=img_bytes,
    file_name=f"propuesta_{plaza_sel.lower().replace(' ', '_')}_{formato_sel.lower().replace(' ', '_')}.jpg",
    mime="image/jpeg",
    type="primary"
)
