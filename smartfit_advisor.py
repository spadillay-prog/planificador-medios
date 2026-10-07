import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

def render_smartfit_advisor():
    st.markdown("## 🏋️‍♂️ Smart Fit — Recomendador Táctico OOH")
    st.caption("Módulo exclusivo para optimización de cobertura, proximidad y mix de medios en vía pública.")

    st.markdown("---")

    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown("#### 1. Datos de la Sucursal")
        nombre_sucursal = st.text_input(
            "Nombre / Referencia de la sucursal", 
            value="Smart Fit - Mallplaza El Trébol (Talcahuano / Concepción)"
        )
        
        plaza = st.selectbox(
            "Territorio / Plaza",
            [
                "Regiones (Flota Intercomunal / Capital Regional)",
                "Gran Santiago (Región Metropolitana)"
            ],
            index=0
        )
        
        tipo_local = st.selectbox(
            "Tipología de Emplazamiento",
            [
                "En Centro Comercial / Mall / Strip Center",
                "A pie de calle (Eje comercial abierto / Centro urbano)",
                "Polo residencial / Mixto suburbano"
            ],
            index=0
        )
        
        objetivo_campana = st.radio(
            "Fase / Objetivo de Campaña",
            [
                "Apertura / Pre-venta (Máximo Reach & Recordación)",
                "Mantención / Campaña Estacional (Frecuencia & Conversión)"
            ],
            index=0
        )

    # Lógica táctica adaptada a la realidad operativa de regiones
    es_region = "Regiones" in plaza

    if objetivo_campana.startswith("Apertura"):
        if "Centro Comercial" in tipo_local:
            mix_movil_pct = 70 if es_region else 60
            mix_fijo_pct = 100 - mix_movil_pct
            formato_movil = "Lunetas de Buses (Flota Intercomunal / Red Conurbación)" if es_region else "Lunetas Troncales RED con destino al Centro Comercial"
            formato_fijo = "Pantallas Digitales en Accesos / Tótems de Estacionamiento Mall"
            estrategia_texto = (
                "Para preventa o apertura en centro comercial, la prioridad es generar masa crítica en toda la cuenca "
                "de atracción intercomunal (radio de 15 a 20 min). En regiones, las lunetas se operan a nivel de flota "
                "conurbada para garantizar cobertura distribuida sin dispersión operativa, mientras que los soportes fijos "
                "en accesos validan la llegada y cierran el call-to-action."
            )
        elif "calle" in tipo_local:
            mix_movil_pct = 60
            mix_fijo_pct = 40
            formato_movil = "Lunetas de Buses (Parque Central de la Ciudad)" if es_region else "Lunetas de Buses Troncales RED"
            formato_fijo = "MUPIS Peatonales / Refugios de Paradero (Radio < 500m)"
            estrategia_texto = (
                "Combina impacto masivo móvil en los ejes estructurantes de la ciudad con soportes peatonales fijos "
                "cercanos que resuelven la orientación física del local ('A pasos de ti'), reduciendo fricción de búsqueda."
            )
        else: # Residencial
            mix_movil_pct = 65
            mix_fijo_pct = 35
            formato_movil = "Lunetas de Buses (Flota Local Comunal)"
            formato_fijo = "Valla / Pantalla LED en Acceso Vial Principal"
            estrategia_texto = (
                "En enclaves suburbanos o residenciales se privilegia la cobertura móvil comunal y un elemento fijo "
                "de alta visibilidad en el principal nudo de ingreso vehicular."
            )
    else:  # Mantención
        if "Centro Comercial" in tipo_local:
            mix_movil_pct = 40
            mix_fijo_pct = 60
            formato_movil = "Lunetas de Buses (Flota Principal de la Plaza)"
            formato_fijo = "Circuitos MUPIS Digitales en Mall y Paraderos Adyacentes"
            estrategia_texto = (
                "En régimen regular, el objetivo es capturar al flujo flotante cautivo que ya visita el centro comercial "
                "para convertir visitas en suscripciones, manteniendo una presencia móvil de recordación de marca."
            )
        elif "calle" in tipo_local:
            mix_movil_pct = 45
            mix_fijo_pct = 55
            formato_movil = "Lunetas de Buses"
            formato_fijo = "MUPIS / Relojes de Proximidad Peatonal Inmediata"
            estrategia_texto = (
                "Prioriza la frecuencia sobre la masa trabajadora y residente local en los horarios peak de tránsito "
                "alrededor de la sede."
            )
        else:
            mix_movil_pct = 50
            mix_fijo_pct = 50
            formato_movil = "Lunetas de Buses Locales"
            formato_fijo = "Pantallas DOOH Viales de Retorno Laboral"
            estrategia_texto = (
                "Equilibrio entre presencia móvil de ruta y soporte fijo en los trayectos de retorno laboral."
            )

    with col2:
        st.markdown(f"#### 2. Propuesta Estratégica: **{nombre_sucursal}**")
        st.info(estrategia_texto)

        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            st.metric(
                label="Mix Móvil (Alcance / Cobertura)",
                value=f"{mix_movil_pct}% Presupuesto",
                help="Genera volumen de impactos y penetración territorial en toda la cuenca de atracción."
            )
            st.caption(f"**Soporte:** {formato_movil}")
            
        with sub_col2:
            st.metric(
                label="Mix Fijo (Proximidad / CTA)",
                value=f"{mix_fijo_pct}% Presupuesto",
                help="Direccionamiento inmediato, señalética de acceso y cierre de decisión."
            )
            st.caption(f"**Soporte:** {formato_fijo}")

        st.markdown("---")
        
        # Generación de Lámina Ejecutiva en JPG
        slide_bytes = generar_lamina_smartfit(
            nombre_sucursal=nombre_sucursal,
            plaza=plaza,
            tipo_local=tipo_local,
            fase=objetivo_campana,
            mix_movil=mix_movil_pct,
            mix_fijo=mix_fijo_pct,
            formato_movil=formato_movil,
            formato_fijo=formato_fijo,
            estrategia=estrategia_texto
        )

        st.image(slide_bytes, caption="Vista previa de la lámina ejecutiva", use_container_width=True)

        st.download_button(
            label="🖼️ Descargar Lámina Ejecutiva en JPG (Alta Calidad)",
            data=slide_bytes,
            file_name=f"smartfit_{nombre_sucursal.lower().replace(' ', '_').replace('/', '_')}.jpg",
            mime="image/jpeg",
            type="primary",
            use_container_width=True
        )


def generar_lamina_smartfit(nombre_sucursal, plaza, tipo_local, fase, mix_movil, mix_fijo, formato_movil, formato_fijo, estrategia):
    """
    Genera un canvas ejecutivo 16:9 (1920x1080) alineado a la estética del planificador.
    """
    ancho, alto = 1920, 1080
    img = Image.new("RGB", (ancho, alto), color="#121316")
    draw = ImageDraw.Draw(img)

    # Intentar cargar fuentes del sistema compatibles con Linux/Debian
    rutas_fuentes = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "arialbd.ttf"
    ]
    rutas_regular = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "arial.ttf"
    ]

    def cargar(rutas, tam):
        for r in rutas:
            if os.path.exists(r):
                try:
                    return ImageFont.truetype(r, tam)
                except Exception:
                    pass
        return ImageFont.load_default()

    f_tag = cargar(rutas_fuentes, 22)
    f_tit = cargar(rutas_fuentes, 48)
    f_sub = cargar(rutas_regular, 26)
    f_num = cargar(rutas_fuentes, 72)
    f_card_tit = cargar(rutas_fuentes, 24)
    f_body = cargar(rutas_regular, 22)
    f_bold = cargar(rutas_fuentes, 22)

    amarillo_sf = "#FFB703"

    # Barra superior de acento
    draw.rectangle([(0, 0), (ancho, 14)], fill=amarillo_sf)

    # Header / Branding
    draw.text((100, 70), "SMART FIT | ESTRATEGIA TÁCTICA DE VÍA PÚBLICA", font=f_tag, fill=amarillo_sf)
    draw.text((100, 110), nombre_sucursal[:60], font=f_tit, fill="#FFFFFF")
    draw.text((100, 180), f"Plaza: {plaza}   •   Entorno: {tipo_local}   •   Fase: {fase.split('(')[0].strip()}", font=f_sub, fill="#9E9E9E")

    # Card 1: Cobertura Móvil
    draw.rounded_rectangle([(100, 260), (930, 560)], radius=18, fill="#1C1E24", outline="#2D3139", width=2)
    draw.text((140, 295), "COBERTURA TERRITORIAL (MÓVIL)", font=f_card_tit, fill="#A6B0BF")
    draw.text((140, 345), f"{mix_movil}%", font=f_num, fill=amarillo_sf)
    draw.text((140, 445), "Soporte recomendado:", font=f_tag, fill="#6C757D")
    
    # Texto del soporte móvil (con salto de línea si es largo)
    palabras_sm = formato_movil.split()
    l1, l2 = "", ""
    for p in palabras_sm:
        if len(l1 + " " + p) < 42:
            l1 += " " + p
        else:
            l2 += " " + p
    draw.text((140, 480), l1.strip(), font=f_bold, fill="#FFFFFF")
    if l2:
        draw.text((140, 510), l2.strip(), font=f_bold, fill="#FFFFFF")

    # Card 2: Proximidad Fija
    draw.rounded_rectangle([(990, 260), (1820, 560)], radius=18, fill="#1C1E24", outline="#2D3139", width=2)
    draw.text((1030, 295), "PROXIMIDAD & CALL-TO-ACTION (FIJO)", font=f_card_tit, fill="#A6B0BF")
    draw.text((1030, 345), f"{mix_fijo}%", font=f_num, fill="#FFFFFF")
    draw.text((1030, 445), "Soporte recomendado:", font=f_tag, fill="#6C757D")
    
    palabras_sf = formato_fijo.split()
    l1f, l2f = "", ""
    for p in palabras_sf:
        if len(l1f + " " + p) < 42:
            l1f += " " + p
        else:
            l2f += " " + p
    draw.text((1030, 480), l1f.strip(), font=f_bold, fill="#FFFFFF")
    if l2f:
        draw.text((1030, 510), l2f.strip(), font=f_bold, fill="#FFFFFF")

    # Card 3: Racional Estratégico y Operativo
    draw.rounded_rectangle([(100, 600), (1820, 960)], radius=18, fill="#181A20", outline="#303540", width=2)
    draw.rectangle([(100, 600), (115, 960)], fill=amarillo_sf) # Acento vertical
    draw.text((150, 640), "RACIONAL ESTRATÉGICO Y OPERATIVO EN TERRITORIO", font=f_card_tit, fill=amarillo_sf)

    # Word wrap del texto del racional
    palabras = estrategia.split()
    lineas, linea_actual = [], ""
    for p in palabras:
        if len(linea_actual + " " + p) < 95:
            linea_actual += " " + p
        else:
            lineas.append(linea_actual.strip())
            linea_actual = p
    if linea_actual:
        lineas.append(linea_actual.strip())

    y_txt = 700
    for linea in lineas[:6]:
        draw.text((150, y_txt), linea, font=f_body, fill="#D8DCE3")
        y_txt += 38

    # Footer
    draw.text((100, 1010), "Generado con Planificador Táctico OOH • Confidencial Smart Fit", font=f_body, fill="#555B66")

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    return buf.getvalue()
