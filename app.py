import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io
import os
import urllib.request

st.set_page_config(
    page_title="Planificador de Medios & Exportador JPG",
    page_icon="🎯",
    layout="wide"
)

# Descargar y cargar tipografía Roboto para garantizar tildes y caracteres latinos
@st.cache_resource
def cargar_fuentes():
    rutas = {
        "regular": "Roboto-Regular.ttf",
        "bold": "Roboto-Bold.ttf"
    }
    urls = {
        "regular": "https://github.com/google/fonts/raw/main/apache/roboto/Roboto%5Bwdth%2Cwght%5D.ttf",
        "bold": "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Bold.ttf"
    }
    
    for k in ["bold", "regular"]:
        if not os.path.exists(rutas[k]):
            try:
                urllib.request.urlretrieve(urls[k], rutas[k])
            except Exception:
                pass

cargar_fuentes()

def obtener_fuente(size=20, bold=False):
    f_path = "Roboto-Bold.ttf" if bold else "Roboto-Regular.ttf"
    if os.path.exists(f_path):
        try:
            return ImageFont.truetype(f_path, size)
        except Exception:
            pass
    # Fallback Linux estándar
    candidatos = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
    ]
    for c in candidatos:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()

# Colores base para acentos de marca
COLORES_BASE = {
    "Negro Corporativo": "#1A1A1A",
    "Amarillo (Smart Fit)": "#FFB800",
    "Azul Intenso": "#0052CC",
    "Rojo Retail": "#D9383A",
    "Verde Esmeralda": "#00875A",
    "Naranjo Enérgico": "#FF5630",
    "Azul Marino Oscuro": "#091E42"
}

DATA_TERRITORIAL = {
    "Coquimbo": {"res": 240000, "flot": 40000, "contexto": "Coquimbo concentra su movimiento en pocos ejes viales principales que la flota cruza de forma recurrente, logrando alta repeticion y memorabilidad sobre conductores y peatones."},
    "La Serena": {"res": 240000, "flot": 40000, "contexto": "Ejes Balmaceda y Ruta 5 conectan el flujo intercomunal con alta retencion en semaforos y centros comerciales."},
    "Antofagasta": {"res": 440000, "flot": 50000, "contexto": "Ciudad lineal encajonada entre cerro y mar; la concentracion vehicular en Av. Costanera y Pedro Aguirre Cerda eleva los OTS diarios."},
    "Santiago Oriente": {"res": 1060000, "flot": 800000, "contexto": "Polo corporativo y financiero de maxima afluencia flotante de la capital, ideal para campanas de cobertura y frecuencia masiva."},
    "San Joaquín (Vespucio / Departamental)": {"res": 103000, "flot": 65000, "contexto": "Nudo estrategico con alta densidad comercial (Mall Florida Center) y conectividad con Metro Linea 5."},
}

FORMATOS = {
    "Lunetas Buses": {"base": 30, "c": 0.20, "m": 0.25, "o": 0.30, "tipo": "Cobertura móvil", "unidad": "lunetas"},
    "Pantalla Digital (DOOH)": {"base": 1, "c": 0.20, "m": 0.25, "o": 0.30, "tipo": "Gran impacto LED", "unidad": "pantallas"},
    "Buses Troncales": {"base": 70, "c": 0.30, "m": 0.35, "o": 0.40, "tipo": "Troncal móvil", "unidad": "buses"},
    "Valla Estática": {"base": 1, "c": 0.15, "m": 0.20, "o": 0.25, "tipo": "Soporte fijo", "unidad": "soportes"}
}

# --- CONFIGURACIÓN VISUAL ---
st.sidebar.header("🎨 Diseño de la Lámina")
modo_fondo = st.sidebar.radio("Estilo de Fondo:", ["Fondo Oscuro", "Fondo Claro (Blanco)"])
color_acento_nombre = st.sidebar.selectbox("Color de Acento / Cliente:", list(COLORES_BASE.keys()))
color_acento = COLORES_BASE[color_acento_nombre]

if modo_fondo == "Fondo Claro (Blanco)":
    c_bg = "#F8F9FA"
    c_card = "#FFFFFF"
    c_border = "#E2E8F0"
    c_text_primary = "#1A202C"
    c_text_muted = "#718096"
    c_accent = color_acento
    c_card_highlight_bg = color_acento
    c_card_highlight_text = "#FFFFFF" if color_acento_nombre in ["Negro Corporativo", "Azul Intenso", "Rojo Retail", "Azul Marino Oscuro"] else "#000000"
else:
    c_bg = "#121316"
    c_card = "#1E1F24"
    c_border = "#2D3139"
    c_text_primary = "#FFFFFF"
    c_text_muted = "#9AA0A6"
    c_accent = color_acento
    c_card_highlight_bg = color_acento
    c_card_highlight_text = "#000000" if color_acento_nombre in ["Amarillo (Smart Fit)", "Naranjo Enérgico"] else "#FFFFFF"

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Datos de la Campaña")
plaza_sel = st.sidebar.selectbox("Plaza / Territorio:", list(DATA_TERRITORIAL.keys()))
formato_sel = st.sidebar.selectbox("Formato Publicitario:", list(FORMATOS.keys()))

info_p = DATA_TERRITORIAL[plaza_sel]
info_f = FORMATOS[formato_sel]

cant_unidades = st.sidebar.number_input(f"Cantidad de {info_f['unidad']}:", min_value=1, value=info_f["base"], step=1)
dias_campana = st.sidebar.number_input("Días de Campaña:", min_value=1, value=30, step=1)
inversion_total = st.sidebar.number_input("Inversión Total ($ CLP):", min_value=100000, value=2500000, step=250000)

foto_soporte = st.sidebar.file_uploader("Subir foto del soporte (opcional):", type=["jpg", "png", "jpeg"])

comentario_custom = st.sidebar.text_area(
    "Ventaja Estratégica / Comentarios:",
    value=info_p["contexto"],
    height=90
)

# Cálculos
universo = info_p["res"] + info_p["flot"]
factor_escala = cant_unidades / info_f["base"]

costo_unitario = inversion_total / cant_unidades if cant_unidades > 0 else 0
imp_diarios_m = universo * info_f["m"] * factor_escala
imp_totales_m = imp_diarios_m * dias_campana
costo_impacto_m = inversion_total / imp_totales_m if imp_totales_m > 0 else 0

tabla_esc = [
    {"esc": "Conservador", "rate": info_f["c"], "dia": universo * info_f["c"] * factor_escala, "tot": universo * info_f["c"] * factor_escala * dias_campana},
    {"esc": "Medio", "rate": info_f["m"], "dia": imp_diarios_m, "tot": imp_totales_m},
    {"esc": "Optimista", "rate": info_f["o"], "dia": universo * info_f["o"] * factor_escala, "tot": universo * info_f["o"] * factor_escala * dias_campana}
]

# --- RENDERIZADOR PIL ---
def render_lamina_jpg():
    W, H = 1920, 1080
    im = Image.new("RGB", (W, H), c_bg)
    draw = ImageDraw.Draw(im)

    f_title = obtener_fuente(38, bold=True)
    f_sub = obtener_fuente(22, bold=False)
    f_num_big = obtener_fuente(34, bold=True)
    f_label = obtener_fuente(17, bold=False)
    f_table_head = obtener_fuente(17, bold=True)
    f_table_row = obtener_fuente(19, bold=False)
    f_comment_title = obtener_fuente(20, bold=True)
    f_comment_body = obtener_fuente(18, bold=False)

    # Cabecera con guion estándar compatible
    title_text = f"{plaza_sel.upper()} - {formato_sel.upper()}"
    subtitle_text = f"{cant_unidades} {info_f['unidad']} · {dias_campana} días"
    
    draw.text((60, 50), title_text, fill=c_accent, font=f_title)
    draw.text((W - 390, 62), subtitle_text, fill=c_text_muted, font=f_sub)
    draw.line([(60, 115), (W - 60, 115)], fill=c_accent, width=2)

    # Foto soporte
    foto_box = [(60, 150), (720, 960)]
    if foto_soporte is not None:
        try:
            uploaded_img = Image.open(foto_soporte).convert("RGB")
            uploaded_img = uploaded_img.resize((660, 810))
            im.paste(uploaded_img, (60, 150))
        except Exception:
            draw.rectangle(foto_box, fill=c_card, outline=c_border, width=1)
    else:
        draw.rectangle(foto_box, fill=c_card, outline=c_border, width=1)
        draw.text((220, 530), "[ FOTO SOPORTE ]", fill=c_text_muted, font=f_sub)

    # 3 Tarjetas Superiores
    card_w, card_h = 360, 130
    x_offset = 760
    
    # Tarjeta 1: Inversión
    draw.rounded_rectangle([(x_offset, 150), (x_offset + card_w, 150 + card_h)], radius=12, fill=c_card, outline=c_border, width=1)
    draw.text((x_offset + 25, 172), "Inversión mensual", fill=c_text_muted, font=f_label)
    draw.text((x_offset + 25, 205), f"${inversion_total:,.0f}".replace(",", "."), fill=c_text_primary, font=f_num_big)

    # Tarjeta 2: Costo Unitario
    draw.rounded_rectangle([(x_offset + card_w + 30, 150), (x_offset + card_w*2 + 30, 150 + card_h)], radius=12, fill=c_card, outline=c_border, width=1)
    draw.text((x_offset + card_w + 55, 172), f"Costo por {info_f['unidad'][:-1]} / mes", fill=c_text_muted, font=f_label)
    draw.text((x_offset + card_w + 55, 205), f"${costo_unitario:,.0f}".replace(",", "."), fill=c_text_primary, font=f_num_big)

    # Tarjeta 3: Impactos Totales (Destacada)
    draw.rounded_rectangle([(x_offset + card_w*2 + 60, 150), (x_offset + card_w*3 + 60, 150 + card_h)], radius=12, fill=c_card_highlight_bg)
    draw.text((x_offset + card_w*2 + 85, 172), f"Impactos {dias_campana} días (caso medio)", fill=c_card_highlight_text, font=f_label)
    draw.text((x_offset + card_w*2 + 85, 205), f"{imp_totales_m:,.0f}".replace(",", "."), fill=c_card_highlight_text, font=f_num_big)

    # Tabla de Escenarios
    t_y = 320
    draw.text((x_offset + 20, t_y), "Escenario", fill=c_text_muted, font=f_table_head)
    draw.text((x_offset + 270, t_y), "% Exposición diaria", fill=c_text_muted, font=f_table_head)
    draw.text((x_offset + 520, t_y), "Contactos diarios", fill=c_text_muted, font=f_table_head)
    draw.text((x_offset + 750, t_y), f"Impactos {dias_campana} días", fill=c_text_muted, font=f_table_head)
    draw.text((x_offset + 990, t_y), "CPM Efectivo", fill=c_text_muted, font=f_table_head)
    draw.line([(x_offset + 20, t_y + 35), (W - 60, t_y + 35)], fill=c_border, width=1)

    row_y = t_y + 55
    for item in tabla_esc:
        is_medio = item["esc"] == "Medio"
        c_fill = c_accent if is_medio else c_text_primary
        cpm_val = (inversion_total / item["tot"] * 1000) if item["tot"] > 0 else 0
        
        draw.text((x_offset + 20, row_y), item["esc"], fill=c_fill, font=obtener_fuente(20, bold=is_medio))
        draw.text((x_offset + 300, row_y), f"{int(item['rate']*100)}%", fill=c_text_primary, font=f_table_row)
        draw.text((x_offset + 520, row_y), f"{int(item['dia']):,}".replace(",", "."), fill=c_text_primary, font=f_table_row)
        draw.text((x_offset + 750, row_y), f"{int(item['tot']):,}".replace(",", "."), fill=c_text_primary, font=f_table_row)
        draw.text((x_offset + 990, row_y), f"${int(round(cpm_val)):,}".replace(",", "."), fill=c_text_primary, font=f_table_row)
        row_y += 45

    # 3 Tarjetas Inferiores
    b_y = 510
    draw.rounded_rectangle([(x_offset, b_y), (x_offset + card_w, b_y + card_h)], radius=12, fill=c_card, outline=c_border, width=1)
    draw.text((x_offset + 25, b_y + 20), "Universo activo diario", fill=c_text_muted, font=f_label)
    draw.text((x_offset + 25, b_y + 55), f"{universo:,.0f}".replace(",", "."), fill=c_accent, font=f_num_big)

    draw.rounded_rectangle([(x_offset + card_w + 30, b_y), (x_offset + card_w*2 + 30, b_y + card_h)], radius=12, fill=c_card, outline=c_border, width=1)
    draw.text((x_offset + card_w + 55, b_y + 20), "Costo x impacto (medio)", fill=c_text_muted, font=f_label)
    draw.text((x_offset + card_w + 55, b_y + 55), f"${costo_impacto_m:.1f} CLP", fill=c_accent, font=f_num_big)

    draw.rounded_rectangle([(x_offset + card_w*2 + 60, b_y), (x_offset + card_w*3 + 60, b_y + card_h)], radius=12, fill=c_card, outline=c_border, width=1)
    draw.text((x_offset + card_w*2 + 85, b_y + 20), "Naturaleza del formato", fill=c_text_muted, font=f_label)
    draw.text((x_offset + card_w*2 + 85, b_y + 55), info_f["tipo"], fill=c_accent, font=f_num_big)

    # Contenedor de Comentarios Estratégicos
    com_y = 680
    draw.rounded_rectangle([(x_offset, com_y), (W - 60, 960)], radius=12, fill=c_card, outline=c_border, width=1)
    draw.line([(x_offset, com_y), (x_offset, 960)], fill=c_accent, width=6)
    
    draw.text((x_offset + 30, com_y + 25), f"Universo activo diario: {info_p['res']:,} habitantes + {info_p['flot']:,} flotante = {universo:,}".replace(",", "."), fill=c_text_primary, font=f_label)
    draw.text((x_offset + 30, com_y + 68), "VENTAJA ESTRATÉGICA DEL FORMATO", fill=c_accent, font=f_comment_title)
    
    # Multilínea
    words = comentario_custom.split()
    lines, current_line = [], ""
    for w in words:
        if len(current_line + " " + w) < 90:
            current_line += " " + w
        else:
            lines.append(current_line.strip())
            current_line = w
    if current_line:
        lines.append(current_line.strip())
        
    line_y = com_y + 110
    for l in lines[:4]:
        draw.text((x_offset + 30, line_y), l, fill=c_text_muted, font=f_comment_body)
        line_y += 30

    # Pie de página
    draw.text((60, 1010), f"Inversión mensual total: ${inversion_total:,.0f} CLP · Flota: {cant_unidades} unidades · Valores en CLP neto.".replace(",", "."), fill=c_text_muted, font=f_label)

    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=95)
    return buf.getvalue()

# --- VISTA PRINCIPAL ---
st.title("🎯 Generador de Láminas de Propuesta OOH")
st.markdown("Visualiza la lámina ejecutiva con estilo adaptable (Fondo Claro u Oscuro) y descárgala en JPG.")

img_bytes = render_lamina_jpg()

st.image(img_bytes, caption=f"Vista previa - {plaza_sel} ({modo_fondo} / {color_acento_nombre})", use_container_width=True)

st.download_button(
    label="📥 Descargar Lámina en JPG (Alta Calidad)",
    data=img_bytes,
    file_name=f"propuesta_{plaza_sel.lower().replace(' ', '_')}_{formato_sel.lower().replace(' ', '_')}.jpg",
    mime="image/jpeg",
    type="primary"
)
