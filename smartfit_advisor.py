import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

def render_smartfit_advisor():
    st.markdown("## 🏋️‍♂️ Smart Fit — Asesor Táctico OOH")
    st.caption("Motor de selección multivariable: formatos de alto impacto, gran formato estático y circuitos digitales.")

    st.markdown("---")

    col1, col2 = st.columns([1, 1], gap="medium")

    # Catálogo referencial de sedes
    SEDES_PRECARGADAS = {
        "--- Ingresar sucursal manualmente ---": None,
        
        # --- SEDES REGIONALES ---
        "Mallplaza Arica [SOS] (Arica)": {
            "plaza": "Arica y Parinacota (Escala Compacta)",
            "tipo": "Dentro de Mall / Strip Center / Gran Superficie",
            "vial": "Avenida / Eje Estructurante (Diego Portales / Costanera)",
            "presupuesto": "Presupuesto Ajustado / Medio ($1.5M - $3.5M)",
            "escala": "Ciudad Compacta (<250k hab)",
            "duracion": "Continuidad / Trimestral (30+ días)"
        },
        "Mallplaza Antofagasta [SOS] (Antofagasta)": {
            "plaza": "Regiones (Capital Regional / Conurbación Mayor)",
            "tipo": "Dentro de Mall / Strip Center / Gran Superficie",
            "vial": "Avenida / Eje Estructurante (Balmaceda / Costanera)",
            "presupuesto": "Presupuesto Óptimo (> $4M)",
            "escala": "Gran Conurbación Regional (>400k hab)",
            "duracion": "Continuidad / Trimestral (30+ días)"
        },
        "Rancagua Centro [SOS] (Rancagua)": {
            "plaza": "Regiones (Capital Regional / Conurbación Mayor)",
            "tipo": "A pie de calle (Paseo peatonal / Centro comercial abierto)",
            "vial": "Paseo Peatonal / Centro Histórico Comercial",
            "presupuesto": "Presupuesto Ajustado / Medio ($1.5M - $3.5M)",
            "escala": "Ciudad Intermedia (250k - 400k hab)",
            "duracion": "Continuidad / Trimestral (30+ días)"
        },
        "Acuenta Azaleas [SOS] (Los Ángeles)": {
            "plaza": "Regiones (Capital Regional / Conurbación Mayor)",
            "tipo": "Dentro de Mall / Strip Center / Gran Superficie",
            "vial": "Corredor Mixto Vecinal / Acceso Residencial",
            "presupuesto": "Presupuesto Ajustado / Medio ($1.5M - $3.5M)",
            "escala": "Ciudad Compacta (<250k hab)",
            "duracion": "Continuidad / Trimestral (30+ días)"
        },

        # --- SANTIAGO URBANO ---
        "Cenco Costanera [Hito Marca] (Providencia)": {
            "plaza": "Gran Santiago (Urbano / Red Metro)",
            "tipo": "Dentro de Mall / Strip Center / Gran Superficie",
            "vial": "Nodo Metropolitano / Eje Financiero (Andrés Bello)",
            "presupuesto": "Presupuesto Óptimo (> $4M)",
            "escala": "Metrópoli Nacional (Gran Santiago)",
            "duracion": "Continuidad / Trimestral (30+ días)"
        },
        "Mallplaza Oeste [URGENTE] (Cerrillos)": {
            "plaza": "Gran Santiago (Urbano / Red Metro)",
            "tipo": "Dentro de Mall / Strip Center / Gran Superficie",
            "vial": "Autopista / Vía Expresa (Vespucio Sur / Gral. Velásquez)",
            "presupuesto": "Presupuesto Óptimo (> $4M)",
            "escala": "Metrópoli Nacional (Gran Santiago)",
            "duracion": "Continuidad / Trimestral (30+ días)"
        },
        "Parque Titanium [SOS] (Las Condes)": {
            "plaza": "Gran Santiago (Urbano / Red Metro)",
            "tipo": "Polo Corporativo / Centro Financiero",
            "vial": "Corredor Empresarial / El Golf",
            "presupuesto": "Presupuesto Óptimo (> $4M)",
            "escala": "Metrópoli Nacional (Gran Santiago)",
            "duracion": "Continuidad / Trimestral (30+ días)"
        },

        # --- RM PROVINCIAL / PERIFERIA ---
        "Melipilla / Espacio Urbano [SOS] (Melipilla)": {
            "plaza": "RM Provincial / Periferia Autónoma (Melipilla, Talagante, etc.)",
            "tipo": "Dentro de Mall / Strip Center / Gran Superficie",
            "vial": "Avenida / Eje Estructurante (Ruta 78 / Autopista del Sol)",
            "presupuesto": "Presupuesto Ajustado / Medio ($1.5M - $3.5M)",
            "escala": "Ciudad Compacta (<250k hab)",
            "duracion": "Continuidad / Trimestral (30+ días)"
        }
    }

    with col1:
        st.markdown("#### 1. Parámetros de la Sede y Entorno")
        seleccion = st.selectbox("Cargar sede de referencia (opcional):", list(SEDES_PRECARGADAS.keys()))
        data_pre = SEDES_PRECARGADAS[seleccion]

        if data_pre:
            default_nombre = seleccion.split("(")[0].strip()
            idx_plaza = 0 if "Arica" in data_pre["plaza"] else (2 if "Gran Santiago" in data_pre["plaza"] else (3 if "RM Provincial" in data_pre["plaza"] else 1))
            idx_tipo = 0 if "Mall" in data_pre["tipo"] else (1 if "calle" in data_pre["tipo"] else 2)
            idx_vial = 0 if "Autopista" in data_pre["vial"] else (1 if "Avenida" in data_pre["vial"] else (2 if "Peatonal" in data_pre["vial"] else 3))
            idx_pres = 0 if "Ajustado" in data_pre["presupuesto"] else 1
            idx_dur = 0 if "Continuidad" in data_pre["duracion"] else 1
        else:
            default_nombre = "Nueva Sucursal Smart Fit"
            idx_plaza, idx_tipo, idx_vial, idx_pres, idx_dur = 1, 0, 1, 0, 0

        nombre_sucursal = st.text_input("Nombre de la sucursal", value=default_nombre)

        plaza = st.selectbox(
            "Territorio / Entorno Regional",
            [
                "Arica y Parinacota (Escala Compacta)",
                "Regiones (Capital Regional / Conurbación Mayor)",
                "Gran Santiago (Urbano / Red Metro)",
                "RM Provincial / Periferia Autónoma (Melipilla, Talagante, etc.)"
            ],
            index=idx_plaza
        )

        tipo_local = st.selectbox(
            "Emplazamiento del Local",
            [
                "Dentro de Mall / Strip Center / Gran Superficie",
                "A pie de calle (Paseo peatonal / Centro comercial abierto)",
                "Polo Corporativo / Centro Financiero"
            ],
            index=idx_tipo
        )

        entorno_vial = st.selectbox(
            "Entorno Vial / Tráfico Circundante",
            [
                "Autopista / Vía Expresa de Alto Flujo (Vespucio, Ruta 5, Autopista del Sol)",
                "Avenida / Eje Estructurante Principal (Diego Portales, Av. Alemania, Los Carrera)",
                "Paseo Peatonal / Centro Histórico Comercial",
                "Nodo Corporativo / Metro Subterráneo"
            ],
            index=idx_vial
        )

        nivel_presupuesto = st.selectbox(
            "Nivel Presupuestario por Sede",
            [
                "Presupuesto Ajustado / Medio (Priorizar eficiencia y evitar mínimos de producción)",
                "Presupuesto Óptimo / Amplio (Permite combinación y formatos de alto volumen)"
            ],
            index=idx_pres
        )

        duracion_campana = st.radio(
            "Horizonte de Campaña",
            [
                "Continuidad / Trimestral (30+ días)",
                "Táctica Flash / Conversión (7 a 15 días)"
            ],
            index=idx_dur,
            horizontal=True
        )

    # --- MOTOR DE ASIGNACIÓN DINÁMICA POR ROL DE MEDIO ---
    es_flash = "Flash" in duracion_campana
    es_arica = "Arica" in plaza or "Arica" in nombre_sucursal
    es_autopista = "Autopista" in entorno_vial
    es_avenida = "Avenida" in entorno_vial
    es_peatonal = "Peatonal" in entorno_vial or "calle" in tipo_local
    es_corporativo = "Corporativo" in tipo_local or "Corporativo" in entorno_vial
    es_metro_santiago = "Gran Santiago" in plaza and not es_autopista
    presupuesto_ajustado = "Ajustado" in nivel_presupuesto

    # Regla 1: Campañas Flash (Siempre 100% Digital / Cero Producción Física)
    if es_flash:
        soporte_primario_titulo = "DOOH GRAN FORMATO (PANTALLAS LED)"
        soporte_primario_desc = "Pantallas LED Viales de Alto Tráfico"
        soporte_secundario_titulo = "PANTALLAS DIGITALES EN ACCESO"
        soporte_secundario_desc = "Circuito DOOH en Mall / Metro Andenes"
        estrategia_texto = (
            f"Al ser una campaña táctica de corta duración ({duracion_campana.split('(')[0].strip()}), no se justifica producción gráfica en papel ni vinilos. "
            "Se destina la inversión a soportes digitales DOOH sincronizados en horarios peak para generar alta frecuencia y permitir salida al aire inmediata sin costo de imprenta."
        )

    # Regla 2: Arica o Ciudades donde el Formato Estático o DOOH supera al Bus
    elif es_arica or (es_avenida and presupuesto_ajustado):
        soporte_primario_titulo = "GRAN FORMATO ESTÁTICO (ALTO IMPACTO)"
        soporte_primario_desc = "Valla Monumental / Letrero Estático en Eje Principal"
        soporte_secundario_titulo = "CIRCUITO PANTALLAS DIGITALES (DOOH)"
        soporte_secundario_desc = "Pantallas en Accesos Mall / Tótems de Proximidad"
        estrategia_texto = (
            f"Para {nombre_sucursal}, no se contemplan buses debido al costo mínimo de entrada y la dispersión de recorridos en la plaza. "
            "La recomendación más costo-eficiente es un elemento estático de alto impacto (valla monumental o unipolar vial) sobre el eje estructurante de aproximación, "
            "complementado con un mix de pantallas digitales (DOOH) en los accesos del centro comercial para validar la llegada del usuario."
        )

    # Regla 3: Autopistas y Vías Expresas (Vallas Monumentales o Pantallas Digitales de Autopista)
    elif es_autopista:
        soporte_primario_titulo = "GRAN FORMATO ESTÁTICO DE AUTOPISTA"
        soporte_primario_desc = "Valla Monumental / Prisma Unipolar de Alto Flujo"
        soporte_secundario_titulo = "PROXIMIDAD DIGITAL (DOOH MALL)"
        soporte_secundario_desc = "Pantallas Digitales en Accesos y Estacionamientos"
        estrategia_texto = (
            "En entornos de autopista y alta velocidad vehicular, los formatos de menor tamaño pierden visibilidad. "
            "El medio más efectivo es un soporte estático de gran escala o unipolar con 100% de Share of Voice permanente, "
            "cerrando el trayecto con señalética digital en los accesos del recinto."
        )

    # Regla 4: Entornos Peatonales o Corporativos (Cero Buses / Foco Vereda y Proximidad)
    elif es_peatonal or es_corporativo:
        soporte_primario_titulo = "MUPIS PEATONALES / VEREDA (<300 METROS)"
        soporte_primario_desc = "Circuito de Caras Peatonales en Radio Inmediato"
        soporte_secundario_titulo = "DOOH INTERIOR / ACCESOS CORPORATIVOS"
        soporte_secundario_desc = "Pantallas Digitales de Entrada y Tótems de Paso"
        estrategia_texto = (
            "La audiencia se mueve caminando o llega en transporte menor directamente al polo comercial/oficinas. "
            "No se justifican buses ni vallas de autopista. La mayor tasa de conversión se logra con MUPIS peatonales a pasos de la sucursal "
            "que guían el ingreso físico y reducen la fricción de búsqueda."
        )

    # Regla 5: Gran Santiago Metro Hub (Dominación Metro)
    elif es_metro_santiago and "Cenco" in nombre_sucursal:
        soporte_primario_titulo = "DOMINACIÓN ESTACIÓN DE METRO (TOBALABA)"
        soporte_primario_desc = "Branding Integral en Andenes y Túneles Peatonales"
        soporte_secundario_titulo = "MEGA PANTALLAS DIGITALES (DOOH)"
        soporte_secundario_desc = "Pantallas Gran Formato en Accesos Costanera Center"
        estrategia_texto = (
            "Para el hito de marca en Cenco Costanera, la estrategia descarta formatos móviles y se enfoca en dominación fija: "
            "presencia estelar en los túneles y andenes de Metro Tobalaba combinada con pantallas digitales de gran impacto en los accesos del centro comercial."
        )

    # Regla 6: Conurbaciones con Presupuesto Óptimo donde las Lunetas SÍ son eficientes
    else:
        soporte_primario_titulo = "LUNETAS DE BUSES (FLOTA CONURBADA)"
        soporte_primario_desc = "Cobertura en Red de Microbuses Intercomunales"
        soporte_secundario_titulo = "DOOH / SOPORTES FIJOS EN ACCESOS"
        soporte_secundario_desc = "Pantallas Digitales en Accesos y Cruces Nodales"
        estrategia_texto = (
            "En esta conurbación con presupuesto adecuado, las lunetas de buses en flota completa proporcionan el alcance intercomunal necesario "
            "para cubrir el radio de 15 a 20 minutos de viaje, complementándose con pantallas fijas en el centro comercial de destino."
        )

    with col2:
        st.markdown(f"#### 2. Recomendación Estratégica: **{nombre_sucursal}**")
        st.info(estrategia_texto)

        sub_c1, sub_c2 = st.columns(2)
        with sub_c1:
            st.markdown(f"**🎯 Soporte Primario (Impacto/Eje):**")
            st.success(f"**{soporte_primario_titulo}**\n\n*{soporte_primario_desc}*")
        with sub_c2:
            st.markdown(f"**📍 Soporte Secundario (Proximidad):**")
            st.warning(f"**{soporte_secundario_titulo}**\n\n*{soporte_secundario_desc}*")

        st.markdown("---")

        # Generar lámina dinámica
        slide_bytes = generar_lamina_roles(
            nombre=nombre_sucursal,
            plaza=plaza,
            entorno=tipo_local,
            vial=entorno_vial,
            presupuesto=nivel_presupuesto,
            tit1=soporte_primario_titulo,
            desc1=soporte_primario_desc,
            tit2=soporte_secundario_titulo,
            desc2=soporte_secundario_desc,
            estrategia=estrategia_texto
        )

        st.image(slide_bytes, caption="Lámina ejecutiva lista para exportar a deck (1920x1080)", use_container_width=True)

        st.download_button(
            label="🖼️ Descargar Lámina en JPG (Alta Calidad)",
            data=slide_bytes,
            file_name=f"smartfit_{nombre_sucursal.lower().replace(' ', '_').replace('/', '_')}.jpg",
            mime="image/jpeg",
            type="primary",
            use_container_width=True
        )


def generar_lamina_roles(nombre, plaza, entorno, vial, presupuesto, tit1, desc1, tit2, desc2, estrategia):
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
    f_card_label = cargar(rutas_fuentes, 20)
    f_card_tit = cargar(rutas_fuentes, 26)
    f_card_desc = cargar(rutas_regular, 22)
    f_body = cargar(rutas_regular, 22)

    amarillo_sf = "#FFB703"

    # Barra superior de acento corporativo
    draw.rectangle([(0, 0), (ancho, 14)], fill=amarillo_sf)

    # Encabezado
    draw.text((100, 60), "SMART FIT | RECOMENDACIÓN TÁCTICA DE FORMATOS OOH", font=f_tag, fill=amarillo_sf)
    draw.text((100, 100), nombre[:55], font=f_tit, fill="#FFFFFF")
    
    # Metadatos en 2 líneas limpias
    plaza_corta = plaza.split("(")[0].strip()
    draw.text((100, 168), f"Plaza: {plaza_corta}   •   Entorno: {entorno}", font=f_sub, fill="#A6B0BF")
    draw.text((100, 204), f"Flujo Dominante: {vial[:45]}   •   Perfil Presupuestario: {presupuesto.split('(')[0].strip()}", font=f_sub, fill="#7A828E")

    # Card 1: Soporte Primario (Impacto / Cobertura de Eje)
    draw.rounded_rectangle([(100, 270), (930, 560)], radius=18, fill="#1C1E24", outline="#2D3139", width=2)
    draw.text((140, 305), "SOPORTE PRIMARIO (ALTO IMPACTO / EJE)", font=f_card_label, fill=amarillo_sf)
    
    palabras_t1 = tit1.split()
    l1, l2 = "", ""
    for p in palabras_t1:
        if len(l1 + " " + p) < 28:
            l1 += " " + p
        else:
            l2 += " " + p
    draw.text((140, 350), l1.strip(), font=f_card_tit, fill="#FFFFFF")
    if l2:
        draw.text((140, 390), l2.strip(), font=f_card_tit, fill="#FFFFFF")
    
    draw.text((140, 455), "Detalle operativo:", font=f_card_label, fill="#6C757D")
    draw.text((140, 490), desc1[:45], font=f_card_desc, fill="#D8DCE3")

    # Card 2: Soporte Secundario (Proximidad / Cierre)
    draw.rounded_rectangle([(990, 270), (1820, 560)], radius=18, fill="#1C1E24", outline="#2D3139", width=2)
    draw.text((1030, 305), "SOPORTE SECUNDARIO (PROXIMIDAD / CIERRE)", font=f_card_label, fill="#60A5FA")
    
    palabras_t2 = tit2.split()
    l1f, l2f = "", ""
    for p in palabras_t2:
        if len(l1f + " " + p) < 28:
            l1f += " " + p
        else:
            l2f += " " + p
    draw.text((1030, 350), l1f.strip(), font=f_card_tit, fill="#FFFFFF")
    if l2f:
        draw.text((1030, 390), l2f.strip(), font=f_card_tit, fill="#FFFFFF")

    draw.text((1030, 455), "Detalle operativo:", font=f_card_label, fill="#6C757D")
    draw.text((1030, 490), desc2[:45], font=f_card_desc, fill="#D8DCE3")

    # Card 3: Racional Estratégico
    draw.rounded_rectangle([(100, 605), (1820, 960)], radius=18, fill="#181A20", outline="#303540", width=2)
    draw.rectangle([(100, 605), (115, 960)], fill=amarillo_sf)
    draw.text((150, 645), "RACIONAL TÁCTICO Y JUSTIFICACIÓN DE FORMATOS", font=f_tag, fill=amarillo_sf)

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

    draw.text((100, 1010), "Generado con Planificador Táctico OOH • Optimización de Medios y Retorno de Inversión", font=f_body, fill="#555B66")

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    return buf.getvalue()
