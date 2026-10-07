import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

def render_smartfit_advisor():
    st.markdown("## 🏋️‍♂️ Smart Fit — Asesor Estratégico de Vía Pública")
    st.caption("Motor de optimización de mix OOH multiescenario: análisis de cuenca, movilidad y pertinencia de soportes.")

    st.markdown("---")

    col1, col2 = st.columns([1, 1], gap="medium")

    # Catálogo de sedes referenciales (se puede expandir o usar modo manual)
    SEDES_PRECARGADAS = {
        "--- Ingresar sucursal manualmente ---": None,
        "Mallplaza Arica (Arica)": {"plaza": "Regiones (Conurbación / Flota Intercomunal)", "tipo": "Centro Comercial / Mall", "mov": "Mixta (Bus + Auto)", "pob": "Ciudad Intermedia (100k - 300k hab)", "fase": "Mantención / Conversión Continua"},
        "Mallplaza Antofagasta (Antofagasta)": {"plaza": "Regiones (Conurbación / Flota Intercomunal)", "tipo": "Centro Comercial / Mall", "mov": "Mixta (Bus + Auto)", "pob": "Gran Capital Regional (>300k hab)", "fase": "Mantención / Conversión Continua"},
        "Rancagua Centro (Rancagua)": {"plaza": "Regiones (Flota Urbana Local)", "tipo": "A pie de calle / Centro urbano", "mov": "Alta densidad Peatonal", "pob": "Ciudad Intermedia (100k - 300k hab)", "fase": "Mantención / Conversión Continua"},
        "Parque Titanium (Las Condes)": {"plaza": "Gran Santiago (Eje Urbano / Corporativo)", "tipo": "Polo Corporativo / Oficinas", "mov": "Flujo Peatonal / Metro / Vehicular Privado", "pob": "Gran Capital Regional (>300k hab)", "fase": "Mantención / Conversión Continua"},
        "Estación Central (Santiago)": {"plaza": "Gran Santiago (Eje Urbano / Conectado)", "tipo": "A pie de calle / Centro urbano", "mov": "Nodo Intermodal Masivo (Metro + Caminata)", "pob": "Gran Capital Regional (>300k hab)", "fase": "Mantención / Conversión Continua"},
        "Mallplaza Oeste (Cerrillos)": {"plaza": "Gran Santiago (Eje Urbano / Conectado)", "tipo": "Centro Comercial / Mall", "mov": "Mixta (Bus + Auto)", "pob": "Gran Capital Regional (>300k hab)", "fase": "Apertura / Pre-venta (Gran Cobertura)"},
        "Espacio Urbano Melipilla (Melipilla)": {"plaza": "RM Provincial / Entorno Rural-Urbano", "tipo": "Centro Comercial / Mall", "mov": "Mixta (Bus + Auto)", "pob": "Ciudad Intermedia (100k - 300k hab)", "fase": "Mantención / Conversión Continua"},
        "Cenco Costanera (Providencia)": {"plaza": "Gran Santiago (Eje Urbano / Corporativo)", "tipo": "Megapolo Comercial / Hito", "mov": "Nodo Intermodal Masivo (Metro + Caminata)", "pob": "Gran Capital Regional (>300k hab)", "fase": "Apertura / Pre-venta (Gran Cobertura)"}
    }

    with col1:
        st.markdown("#### 1. Perfil Territorial y Entorno")
        seleccion = st.selectbox("Cargar sede de referencia (opcional):", list(SEDES_PRECARGADAS.keys()))
        data_pre = SEDES_PRECARGADAS[seleccion]

        if data_pre:
            default_nombre = seleccion.split("(")[0].strip()
            idx_plaza = 0 if "Regiones" in data_pre["plaza"] else (1 if "Gran Santiago" in data_pre["plaza"] else 2)
            idx_tipo = 0 if "Centro Comercial" in data_pre["tipo"] else (1 if "calle" in data_pre["tipo"] else 2)
            idx_mov = 0 if "Mixta" in data_pre["mov"] else (1 if "Peatonal" in data_pre["mov"] else 2)
        else:
            default_nombre = "Nueva Sucursal Smart Fit"
            idx_plaza, idx_tipo, idx_mov = 0, 0, 0

        nombre_sucursal = st.text_input("Nombre de la sucursal", value=default_nombre)
        
        plaza = st.selectbox(
            "Territorio / Entorno Regional",
            [
                "Regiones (Capital Regional / Conurbación)",
                "Gran Santiago (Urbano / Red Metro)",
                "RM Provincial / Periferia Autónoma (Melipilla, Talagante, Peñaflor, etc.)"
            ],
            index=idx_plaza
        )

        tipo_local = st.selectbox(
            "Emplazamiento del Local",
            [
                "Dentro de Mall / Strip Center / Gran Superficie",
                "A pie de calle (Paseo peatonal / Centro comercial abierto)",
                "Eje Vial / Corredor Vehicular Residencial",
                "Polo Corporativo / Centro Financiero"
            ],
            index=idx_tipo
        )

        movilidad = st.selectbox(
            "Dinámica de Movilidad en el Catchment",
            [
                "Alta dependencia de Transporte Público (Micros / Colectivos)",
                "Predominio Peatonal (Caminabilidad comercial / Oficinas)",
                "Tránsito Mixto estructurado (Autopistas / Vehicular particular)",
                "Nodo de Conectividad Masiva (Estación Metro / Terminal de buses)"
            ],
            index=idx_mov
        )

        duracion_campana = st.radio(
            "Horizonte / Tipo de Campaña",
            [
                "Continuidad / Trimestral (30+ días)",
                "Táctica Flash / Conversión (7 a 15 días - Ej. Cyber, Halloween, Black Friday)"
            ],
            horizontal=True
        )

    # --- MOTOR DE DECISIÓN TÁCTICO ---
    # Evaluar pertinencia de Lunetas
    es_flash = "Flash" in duracion_campana
    es_corporativo = "Corporativo" in tipo_local
    es_peatonal_puro = "Peatonal" in movilidad
    es_metro_hub = "Nodo" in movilidad and "Santiago" in plaza

    if es_flash:
        # En campañas flash, las lunetas quedan DESCARTADAS por tiempos de producción
        usa_luneta = False
        razon_luneta = "Descartadas por tiempos operativos de producción/instalación (5-7 días). Se prioriza DOOH digital."
        mix_movil_pct = 0
        mix_fijo_pct = 100
        formato_movil = "Sin soporte móvil (No aplica para táctica flash)"
        formato_fijo = "Circuitos DOOH Digitales (Pantallas LED y Metro en ráfagas horarias)"
        estrategia_texto = (
            f"Al tratarse de una campaña táctica de corta duración ({duracion_campana.split('(')[0].strip()}), el vinilo estático en buses no es eficiente por costo de producción y tiempo de montaje. "
            "Se destina el 100% de la inversión a soportes digitales DOOH (pantallas viales y circuitos de Metro) para concentrar ráfagas de alta frecuencia en horas peak y permitir activación inmediata sin costo de imprenta."
        )

    elif es_corporativo or es_peatonal_puro:
        # En ejes peatonales o corporativos premium, la luneta dispersa
        usa_luneta = False
        razon_luneta = "Descartadas por dispersión de audiencia. El público se concentra a pie o en accesos cerrados."
        mix_movil_pct = 0
        mix_fijo_pct = 100
        formato_movil = "Sin soporte móvil (Baja afinidad con el target de la zona)"
        formato_fijo = "MUPIS Peatonales (<300m) / Tótems de Acceso / DOOH Corporativo"
        estrategia_texto = (
            "Para una sucursal en entorno peatonal consolidado o corporativo, el transporte público en bus genera dispersión y bajo retorno. "
            "La masa crítica se captura a pie en el radio inmediato. Se privilegia la proximidad con MUPIS, pantallas peatonales y señalética de cercanía ('a pasos de ti') para reducir fricción."
        )

    elif es_metro_hub:
        # En centros intermodales con Metro, Metro absorbe la masa
        usa_luneta = True
        razon_luneta = "Complementaria de baja escala. Metro absorbe el gran volumen."
        mix_movil_pct = 25
        mix_fijo_pct = 75
        formato_movil = "Lunetas RED Troncales de apoyo"
        formato_fijo = "Dominación de Estación de Metro (Andenes / Túneles) + Pantallas Digitales"
        estrategia_texto = (
            "En nodos intermodales con Metro, el subterráneo es el canal hegemónico de tráfico. Las lunetas cumplen solo un rol perimetral secundario (25%), concentrando la inversión en la dominación visual de accesos y andenes de Metro (75%)."
        )

    else:
        # Casos donde la LUNETA ES RECOMENDADA (Regiones conurbadas, malls, barrios comerciales)
        usa_luneta = True
        if "Mall" in tipo_local:
            mix_movil_pct = 60 if "Regiones" in plaza else 50
            mix_fijo_pct = 100 - mix_movil_pct
            formato_movil = "Lunetas de Buses (Flota Intercomunal / Red Conurbada)" if "Regiones" in plaza else "Lunetas RED Corredores hacia el Mall"
            formato_fijo = "Pantallas Digitales y Tótems en Accesos al Centro Comercial"
            razon_luneta = "Altamente recomendada: cubre la cuenca residencial que se traslada hacia el centro comercial."
            estrategia_texto = (
                "La sucursal opera dentro de un polo comercial que atrae público de toda la comuna o conurbación. "
                "Las lunetas de microbuses son el medio más rentable para capturar la cuenca de atracción completa (15 a 20 min de viaje), mientras que los elementos fijos en los accesos al mall cierran la conversión en el punto de destino."
            )
        else: # Eje vial o residencial
            mix_movil_pct = 50
            mix_fijo_pct = 50
            formato_movil = "Lunetas de Buses Flota Comunal / Local"
            formato_fijo = "MUPIS / Pantallas LED en Nudos Viales Cercanos"
            razon_luneta = "Recomendada: genera masa crítica de impactos en el corredor vial estructurante."
            estrategia_texto = (
                "Entorno de movilidad mixta. Las lunetas proporcionan cobertura y frecuencia continua en el corredor vehicular principal, complementadas equitativamente con presencia fija en cruces de alta visibilidad."
            )

    with col2:
        st.markdown(f"#### 2. Diagnóstico y Recomendación: **{nombre_sucursal}**")
        
        # Alerta visual sobre la pertinencia de buses
        if usa_luneta:
            st.success(f"🚌 **Uso de Lunetas de Bus:** RECOMENDADO ({mix_movil_pct}% del mix)\n\n*{razon_luneta}*")
        else:
            st.warning(f"🚫 **Uso de Lunetas de Bus:** NO RECOMENDADO (0% del mix)\n\n*{razon_luneta}*")

        st.info(estrategia_texto)

        sub_c1, sub_c2 = st.columns(2)
        with sub_c1:
            st.metric("Mix Móvil (Buses)", f"{mix_movil_pct}%")
            st.caption(f"**Formato:** {formato_movil}")
        with sub_c2:
            st.metric("Mix Fijo / Proximidad / DOOH", f"{mix_fijo_pct}%")
            st.caption(f"**Formato:** {formato_fijo}")

        st.markdown("---")

        # Generación de Lámina Ejecutiva
        slide_bytes = generar_lamina_estrategica(
            nombre=nombre_sucursal,
            plaza=plaza,
            entorno=tipo_local,
            movilidad=movilidad,
            duracion=duracion_campana,
            mix_movil=mix_movil_pct,
            mix_fijo=mix_fijo_pct,
            fmt_movil=formato_movil,
            fmt_fijo=formato_fijo,
            estrategia=estrategia_texto,
            usa_luneta=usa_luneta
        )

        st.image(slide_bytes, caption="Lámina ejecutiva lista para exportar a deck", use_container_width=True)

        st.download_button(
            label="🖼️ Descargar Lámina en JPG (1920x1080)",
            data=slide_bytes,
            file_name=f"smartfit_{nombre_sucursal.lower().replace(' ', '_').replace('/', '_')}.jpg",
            mime="image/jpeg",
            type="primary",
            use_container_width=True
        )


def generar_lamina_estrategica(nombre, plaza, entorno, movilidad, duracion, mix_movil, mix_fijo, fmt_movil, fmt_fijo, estrategia, usa_luneta):
    ancho, alto = 1920, 1080
    img = Image.new("RGB", (ancho, alto), color="#121316")
    draw = ImageDraw.Draw(img)

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
    f_tit = cargar(rutas_fuentes, 46)
    f_sub = cargar(rutas_regular, 24)
    f_num = cargar(rutas_fuentes, 70)
    f_card_tit = cargar(rutas_fuentes, 24)
    f_body = cargar(rutas_regular, 22)
    f_bold = cargar(rutas_fuentes, 22)

    amarillo_sf = "#FFB703"

    # Barra superior de acento corporativo
    draw.rectangle([(0, 0), (ancho, 14)], fill=amarillo_sf)

    # Encabezado
    draw.text((100, 60), "SMART FIT | ANÁLISIS DE PERTINENCIA & MIX OOH", font=f_tag, fill=amarillo_sf)
    draw.text((100, 100), nombre[:55], font=f_tit, fill="#FFFFFF")
    
    # Metadatos limpios en 2 líneas
    plaza_corta = plaza.split("(")[0].strip()
    draw.text((100, 168), f"Plaza: {plaza_corta}   •   Entorno: {entorno}   •   Campaña: {duracion.split('(')[0].strip()}", font=f_sub, fill="#A6B0BF")
    draw.text((100, 204), f"Movilidad Dominante: {movilidad}", font=f_sub, fill="#7A828E")

    # Card 1: Cobertura Móvil (Lunetas)
    draw.rounded_rectangle([(100, 270), (930, 560)], radius=18, fill="#1C1E24", outline="#2D3139", width=2)
    color_num_movil = amarillo_sf if usa_luneta else "#6C757D"
    draw.text((140, 300), "COBERTURA MÓVIL (LUNETAS)", font=f_card_tit, fill="#A6B0BF")
    draw.text((140, 345), f"{mix_movil}%", font=f_num, fill=color_num_movil)
    draw.text((140, 440), "Diagnóstico técnico:", font=f_tag, fill="#6C757D")
    
    palabras_sm = fmt_movil.split()
    l1, l2 = "", ""
    for p in palabras_sm:
        if len(l1 + " " + p) < 42:
            l1 += " " + p
        else:
            l2 += " " + p
    draw.text((140, 475), l1.strip(), font=f_bold, fill="#FFFFFF" if usa_luneta else "#888888")
    if l2:
        draw.text((140, 510), l2.strip(), font=f_bold, fill="#FFFFFF" if usa_luneta else "#888888")

    # Card 2: Proximidad / DOOH Fijo
    draw.rounded_rectangle([(990, 270), (1820, 560)], radius=18, fill="#1C1E24", outline="#2D3139", width=2)
    draw.text((1030, 300), "PROXIMIDAD & DOOH (PUNTOS FIJOS)", font=f_card_tit, fill="#A6B0BF")
    draw.text((1030, 345), f"{mix_fijo}%", font=f_num, fill="#FFFFFF")
    draw.text((1030, 440), "Soporte recomendado:", font=f_tag, fill="#6C757D")
    
    palabras_sf = fmt_fijo.split()
    l1f, l2f = "", ""
    for p in palabras_sf:
        if len(l1f + " " + p) < 42:
            l1f += " " + p
        else:
            l2f += " " + p
    draw.text((1030, 475), l1f.strip(), font=f_bold, fill="#FFFFFF")
    if l2f:
        draw.text((1030, 510), l2f.strip(), font=f_bold, fill="#FFFFFF")

    # Card 3: Racional Estratégico y Cuenca de Atracción
    draw.rounded_rectangle([(100, 605), (1820, 960)], radius=18, fill="#181A20", outline="#303540", width=2)
    draw.rectangle([(100, 605), (115, 960)], fill=amarillo_sf)
    draw.text((150, 645), "RACIONAL ESTRATÉGICO: MOVILIDAD Y CATCHMENT", font=f_card_tit, fill=amarillo_sf)

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

    y_txt = 705
    for linea in lineas[:6]:
        draw.text((150, y_txt), linea, font=f_body, fill="#D8DCE3")
        y_txt += 38

    draw.text((100, 1010), "Generado con Planificador Táctico OOH • Herramienta de Modelación Estratégica", font=f_body, fill="#555B66")

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    return buf.getvalue()
