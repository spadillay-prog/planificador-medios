import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

def render_smartfit_advisor():
    st.markdown("## 🏋️‍♂️ Smart Fit — Asesor Estratégico de Vía Pública")
    st.caption("Motor de optimización de mix OOH: análisis de cuenca, pertinencia de soportes y escala urbana territorial.")

    st.markdown("---")

    col1, col2 = st.columns([1, 1], gap="medium")

    # Catálogo de sedes referenciales con perfiles territoriales reales
    SEDES_PRECARGADAS = {
        "--- Ingresar sucursal manualmente ---": None,
        
        # --- BUDGET PRE-OPERACIONAL (APERTURAS / RAMP UP) ---
        "Mallplaza Oeste [URGENTE] (Cerrillos)": {
            "plaza": "Gran Santiago (Urbano / Red Metro)", 
            "tipo": "Dentro de Mall / Strip Center / Gran Superficie", 
            "mov": "Alta dependencia de Transporte Público (Micros / Colectivos)", 
            "escala": "Metrópoli Nacional (Gran Santiago)", 
            "fase": "Apertura / Pre-venta (Máximo Reach & Recordación)"
        },
        "Cenco Costanera [Hito Marca] (Providencia)": {
            "plaza": "Gran Santiago (Urbano / Red Metro)", 
            "tipo": "Dentro de Mall / Strip Center / Gran Superficie", 
            "mov": "Nodo de Conectividad Masiva (Estación Metro / Terminal de buses)", 
            "escala": "Metrópoli Nacional (Gran Santiago)", 
            "fase": "Apertura / Pre-venta (Máximo Reach & Recordación)"
        },
        "Lo Prado (San Pablo 6602)": {
            "plaza": "Gran Santiago (Urbano / Red Metro)", 
            "tipo": "A pie de calle (Paseo peatonal / Centro comercial abierto)", 
            "mov": "Nodo de Conectividad Masiva (Estación Metro / Terminal de buses)", 
            "escala": "Metrópoli Nacional (Gran Santiago)", 
            "fase": "Apertura / Pre-venta (Máximo Reach & Recordación)"
        },
        "Líder Quilín (Peñalolén / Macul)": {
            "plaza": "Gran Santiago (Urbano / Red Metro)", 
            "tipo": "Dentro de Mall / Strip Center / Gran Superficie", 
            "mov": "Tránsito Mixto estructurado (Autopistas / Vehicular particular)", 
            "escala": "Metrópoli Nacional (Gran Santiago)", 
            "fase": "Apertura / Pre-venta (Máximo Reach & Recordación)"
        },
        "Mondrian (Quilpué - Los Carrera 1250)": {
            "plaza": "Regiones (Capital Regional / Conurbación Mayor)", 
            "tipo": "A pie de calle (Paseo peatonal / Centro comercial abierto)", 
            "mov": "Alta dependencia de Transporte Público (Micros / Colectivos)", 
            "escala": "Gran Conurbación Regional (>400k hab / Concepción, Valparaíso, Antofagasta)", 
            "fase": "Apertura / Pre-venta (Máximo Reach & Recordación)"
        },
        "Open Macul (La Florida - Av. La Florida 6400)": {
            "plaza": "Gran Santiago (Urbano / Red Metro)", 
            "tipo": "Dentro de Mall / Strip Center / Gran Superficie", 
            "mov": "Alta dependencia de Transporte Público (Micros / Colectivos)", 
            "escala": "Metrópoli Nacional (Gran Santiago)", 
            "fase": "Apertura / Pre-venta (Máximo Reach & Recordación)"
        },
        "Mallplaza Los Dominicos (Las Condes)": {
            "plaza": "Gran Santiago (Urbano / Red Metro)", 
            "tipo": "Dentro de Mall / Strip Center / Gran Superficie", 
            "mov": "Predominio Peatonal (Caminabilidad comercial / Oficinas)", 
            "escala": "Metrópoli Nacional (Gran Santiago)", 
            "fase": "Apertura / Pre-venta (Máximo Reach & Recordación)"
        },
        "Mallplaza Tobalaba (Puente Alto)": {
            "plaza": "Gran Santiago (Urbano / Red Metro)", 
            "tipo": "Dentro de Mall / Strip Center / Gran Superficie", 
            "mov": "Alta dependencia de Transporte Público (Micros / Colectivos)", 
            "escala": "Metrópoli Nacional (Gran Santiago)", 
            "fase": "Apertura / Pre-venta (Máximo Reach & Recordación)"
        },
        "Go Florida Talca [Próximamente] (Talca)": {
            "plaza": "Regiones (Capital Regional / Conurbación Mayor)", 
            "tipo": "Dentro de Mall / Strip Center / Gran Superficie", 
            "mov": "Tránsito Mixto estructurado (Autopistas / Vehicular particular)", 
            "escala": "Ciudad Intermedia (250k - 400k hab)", 
            "fase": "Apertura / Pre-venta (Máximo Reach & Recordación)"
        },
        "Midmall Maipú [Próximamente] (Maipú)": {
            "plaza": "Gran Santiago (Urbano / Red Metro)", 
            "tipo": "Dentro de Mall / Strip Center / Gran Superficie", 
            "mov": "Tránsito Mixto estructurado (Autopistas / Vehicular particular)", 
            "escala": "Metrópoli Nacional (Gran Santiago)", 
            "fase": "Apertura / Pre-venta (Máximo Reach & Recordación)"
        },

        # --- BUDGET OPERACIONAL (SEDES SOS REGIONES) ---
        "Mallplaza Arica [SOS] (Arica)": {
            "plaza": "Arica y Parinacota (Escala Compacta)", 
            "tipo": "Dentro de Mall / Strip Center / Gran Superficie", 
            "mov": "Predominio Peatonal (Caminabilidad comercial / Oficinas)", 
            "escala": "Ciudad Compacta (<250k hab / Flota microbuses reducida)", 
            "fase": "Mantención / Campaña Estacional (Frecuencia & Conversión)"
        },
        "Mallplaza Antofagasta [SOS] (Antofagasta)": {
            "plaza": "Regiones (Capital Regional / Conurbación Mayor)", 
            "tipo": "Dentro de Mall / Strip Center / Gran Superficie", 
            "mov": "Alta dependencia de Transporte Público (Micros / Colectivos)", 
            "escala": "Gran Conurbación Regional (>400k hab / Concepción, Valparaíso, Antofagasta)", 
            "fase": "Mantención / Campaña Estacional (Frecuencia & Conversión)"
        },
        "Coquimbo [SOS] (Coquimbo)": {
            "plaza": "Regiones (Capital Regional / Conurbación Mayor)", 
            "tipo": "A pie de calle (Paseo peatonal / Centro comercial abierto)", 
            "mov": "Alta dependencia de Transporte Público (Micros / Colectivos)", 
            "escala": "Gran Conurbación Regional (>400k hab / Concepción, Valparaíso, Antofagasta)", 
            "fase": "Mantención / Campaña Estacional (Frecuencia & Conversión)"
        },
        "Rancagua Plaza América [SOS] (Rancagua)": {
            "plaza": "Regiones (Capital Regional / Conurbación Mayor)", 
            "tipo": "Dentro de Mall / Strip Center / Gran Superficie", 
            "mov": "Tránsito Mixto estructurado (Autopistas / Vehicular particular)", 
            "escala": "Ciudad Intermedia (250k - 400k hab)", 
            "fase": "Mantención / Campaña Estacional (Frecuencia & Conversión)"
        },
        "Rancagua Centro [SOS] (Rancagua)": {
            "plaza": "Regiones (Capital Regional / Conurbación Mayor)", 
            "tipo": "A pie de calle (Paseo peatonal / Centro comercial abierto)", 
            "mov": "Predominio Peatonal (Caminabilidad comercial / Oficinas)", 
            "escala": "Ciudad Intermedia (250k - 400k hab)", 
            "fase": "Mantención / Campaña Estacional (Frecuencia & Conversión)"
        },
        "Curicó [SOS] (Curicó)": {
            "plaza": "Regiones (Capital Regional / Conurbación Mayor)", 
            "tipo": "A pie de calle (Paseo peatonal / Centro comercial abierto)", 
            "mov": "Predominio Peatonal (Caminabilidad comercial / Oficinas)", 
            "escala": "Ciudad Compacta (<250k hab / Flota microbuses reducida)", 
            "fase": "Mantención / Campaña Estacional (Frecuencia & Conversión)"
        },
        "Talca Centro [SOS] (Talca)": {
            "plaza": "Regiones (Capital Regional / Conurbación Mayor)", 
            "tipo": "A pie de calle (Paseo peatonal / Centro comercial abierto)", 
            "mov": "Alta dependencia de Transporte Público (Micros / Colectivos)", 
            "escala": "Ciudad Intermedia (250k - 400k hab)", 
            "fase": "Mantención / Campaña Estacional (Frecuencia & Conversión)"
        },
        "Chillán [SOS] (Chillán)": {
            "plaza": "Regiones (Capital Regional / Conurbación Mayor)", 
            "tipo": "A pie de calle (Paseo peatonal / Centro comercial abierto)", 
            "mov": "Alta dependencia de Transporte Público (Micros / Colectivos)", 
            "escala": "Ciudad Intermedia (250k - 400k hab)", 
            "fase": "Mantención / Campaña Estacional (Frecuencia & Conversión)"
        },
        "Acuenta Azaleas [SOS] (Los Ángeles)": {
            "plaza": "Regiones (Capital Regional / Conurbación Mayor)", 
            "tipo": "Dentro de Mall / Strip Center / Gran Superficie", 
            "mov": "Alta dependencia de Transporte Público (Micros / Colectivos)", 
            "escala": "Ciudad Compacta (<250k hab / Flota microbuses reducida)", 
            "fase": "Mantención / Campaña Estacional (Frecuencia & Conversión)"
        },
        "Los Ángeles Alemania [SOS] (Los Ángeles)": {
            "plaza": "Regiones (Capital Regional / Conurbación Mayor)", 
            "tipo": "Eje Vial / Corredor Vehicular Residencial", 
            "mov": "Tránsito Mixto estructurado (Autopistas / Vehicular particular)", 
            "escala": "Ciudad Compacta (<250k hab / Flota microbuses reducida)", 
            "fase": "Mantención / Campaña Estacional (Frecuencia & Conversión)"
        },

        # --- BUDGET OPERACIONAL (SEDES SOS RM: SANTIAGO URBANO) ---
        "Alameda Telecanal [SOS] (Santiago Centro)": {
            "plaza": "Gran Santiago (Urbano / Red Metro)", 
            "tipo": "A pie de calle (Paseo peatonal / Centro comercial abierto)", 
            "mov": "Nodo de Conectividad Masiva (Estación Metro / Terminal de buses)", 
            "escala": "Metrópoli Nacional (Gran Santiago)", 
            "fase": "Mantención / Campaña Estacional (Frecuencia & Conversión)"
        },
        "Estación Central [SOS] (Estación Central)": {
            "plaza": "Gran Santiago (Urbano / Red Metro)", 
            "tipo": "A pie de calle (Paseo peatonal / Centro comercial abierto)", 
            "mov": "Nodo de Conectividad Masiva (Estación Metro / Terminal de buses)", 
            "escala": "Metrópoli Nacional (Gran Santiago)", 
            "fase": "Mantención / Campaña Estacional (Frecuencia & Conversión)"
        },
        "Núcleo San Diego [SOS] (Santiago Centro)": {
            "plaza": "Gran Santiago (Urbano / Red Metro)", 
            "tipo": "A pie de calle (Paseo peatonal / Centro comercial abierto)", 
            "mov": "Predominio Peatonal (Caminabilidad comercial / Oficinas)", 
            "escala": "Metrópoli Nacional (Gran Santiago)", 
            "fase": "Mantención / Campaña Estacional (Frecuencia & Conversión)"
        },
        "Núcleo Recoleta [SOS] (Recoleta)": {
            "plaza": "Gran Santiago (Urbano / Red Metro)", 
            "tipo": "A pie de calle (Paseo peatonal / Centro comercial abierto)", 
            "mov": "Alta dependencia de Transporte Público (Micros / Colectivos)", 
            "escala": "Metrópoli Nacional (Gran Santiago)", 
            "fase": "Mantención / Campaña Estacional (Frecuencia & Conversión)"
        },
        "Parque Titanium [SOS] (Las Condes)": {
            "plaza": "Gran Santiago (Urbano / Red Metro)", 
            "tipo": "Polo Corporativo / Centro Financiero", 
            "mov": "Predominio Peatonal (Caminabilidad comercial / Oficinas)", 
            "escala": "Metrópoli Nacional (Gran Santiago)", 
            "fase": "Mantención / Campaña Estacional (Frecuencia & Conversión)"
        },

        # --- BUDGET OPERACIONAL (SEDES SOS RM: PERIFERIA / PROVINCIAL) ---
        "Quilicura [SOS] (Quilicura)": {
            "plaza": "Gran Santiago (Urbano / Red Metro)", 
            "tipo": "A pie de calle (Paseo peatonal / Centro comercial abierto)", 
            "mov": "Alta dependencia de Transporte Público (Micros / Colectivos)", 
            "escala": "Metrópoli Nacional (Gran Santiago)", 
            "fase": "Mantención / Campaña Estacional (Frecuencia & Conversión)"
        },
        "San Bernardo [SOS] (San Bernardo)": {
            "plaza": "Gran Santiago (Urbano / Red Metro)", 
            "tipo": "A pie de calle (Paseo peatonal / Centro comercial abierto)", 
            "mov": "Alta dependencia de Transporte Público (Micros / Colectivos)", 
            "escala": "Metrópoli Nacional (Gran Santiago)", 
            "fase": "Mantención / Campaña Estacional (Frecuencia & Conversión)"
        },
        "Melipilla Centro [SOS] (Melipilla)": {
            "plaza": "RM Provincial / Periferia Autónoma (Melipilla, Talagante, etc.)", 
            "tipo": "A pie de calle (Paseo peatonal / Centro comercial abierto)", 
            "mov": "Predominio Peatonal (Caminabilidad comercial / Oficinas)", 
            "escala": "Ciudad Compacta (<250k hab / Flota microbuses reducida)", 
            "fase": "Mantención / Campaña Estacional (Frecuencia & Conversión)"
        },
        "Espacio Urbano Melipilla [SOS] (Melipilla)": {
            "plaza": "RM Provincial / Periferia Autónoma (Melipilla, Talagante, etc.)", 
            "tipo": "Dentro de Mall / Strip Center / Gran Superficie", 
            "mov": "Alta dependencia de Transporte Público (Micros / Colectivos)", 
            "escala": "Ciudad Compacta (<250k hab / Flota microbuses reducida)", 
            "fase": "Mantención / Campaña Estacional (Frecuencia & Conversión)"
        },
        "Peñaflor Stripcenter [SOS] (Peñaflor)": {
            "plaza": "RM Provincial / Periferia Autónoma (Melipilla, Talagante, etc.)", 
            "tipo": "Dentro de Mall / Strip Center / Gran Superficie", 
            "mov": "Tránsito Mixto estructurado (Autopistas / Vehicular particular)", 
            "escala": "Ciudad Compacta (<250k hab / Flota microbuses reducida)", 
            "fase": "Mantención / Campaña Estacional (Frecuencia & Conversión)"
        }
    }

    with col1:
        st.markdown("#### 1. Perfil Territorial y Entorno")
        seleccion = st.selectbox("Cargar sede de referencia (opcional):", list(SEDES_PRECARGADAS.keys()))
        data_pre = SEDES_PRECARGADAS[seleccion]

        if data_pre:
            default_nombre = seleccion.split("(")[0].strip()
            # Mapeo de índices automáticos
            if "Arica" in data_pre["plaza"]:
                idx_plaza = 0
            elif "Gran Santiago" in data_pre["plaza"]:
                idx_plaza = 2
            elif "RM Provincial" in data_pre["plaza"]:
                idx_plaza = 3
            else:
                idx_plaza = 1

            idx_tipo = 0 if "Mall" in data_pre["tipo"] else (1 if "calle" in data_pre["tipo"] else (2 if "Vial" in data_pre["tipo"] else 3))
            idx_mov = 0 if "Transporte" in data_pre["mov"] else (1 if "Peatonal" in data_pre["mov"] else (2 if "Mixto" in data_pre["mov"] else 3))
            idx_escala = 0 if "Compacta" in data_pre["escala"] else (1 if "Intermedia" in data_pre["escala"] else (2 if "Gran" in data_pre["escala"] else 3))
            idx_fase = 0 if "Apertura" in data_pre["fase"] else 1
        else:
            default_nombre = "Nueva Sucursal Smart Fit"
            idx_plaza, idx_tipo, idx_mov, idx_escala, idx_fase = 1, 0, 0, 1, 1

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

        escala_urbana = st.selectbox(
            "Escala de Población / Parque Urbano",
            [
                "Ciudad Compacta (<250k hab / Flota microbuses reducida)",
                "Ciudad Intermedia (250k - 400k hab)",
                "Gran Conurbación Regional (>400k hab / Concepción, Valparaíso, Antofagasta)",
                "Metrópoli Nacional (Gran Santiago)"
            ],
            index=idx_escala
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
                "Táctica Flash / Conversión (7 a 15 días - Ej. Halloween, Black Friday)"
            ],
            index=idx_fase,
            horizontal=True
        )

    # --- MOTOR DE DECISIÓN TÁCTICO MULTIVARIABLE ---
    es_arica = "Arica" in nombre_sucursal or "Arica" in plaza
    es_ciudad_compacta = "Compacta" in escala_urbana
    es_flash = "Flash" in duracion_campana
    es_corporativo = "Corporativo" in tipo_local
    es_peatonal_puro = "Peatonal" in movilidad
    es_metro_hub = "Nodo" in movilidad and "Santiago" in plaza

    if es_flash:
        usa_luneta = False
        razon_luneta = "Descartadas por tiempos operativos de producción/instalación (5-7 días). Se prioriza DOOH digital."
        mix_movil_pct = 0
        mix_fijo_pct = 100
        formato_movil = "Sin soporte móvil (No aplica para táctica flash)"
        formato_fijo = "Circuitos DOOH Digitales (Pantallas LED y Metro en ráfagas horarias)"
        estrategia_texto = (
            f"Al tratarse de una campaña táctica de corta duración ({duracion_campana.split('(')[0].strip()}), el vinilo estático en buses no es eficiente por costo de producción y montaje. "
            "Se destina el 100% de la inversión a soportes digitales DOOH (pantallas viales y circuitos de Metro) para concentrar ráfagas de alta frecuencia en horas peak sin costo de imprenta."
        )

    elif es_arica or es_ciudad_compacta:
        # En Arica o ciudades compactas: Flota pequeña, sin supervisión y dispersa.
        usa_luneta = False
        razon_luneta = "No recomendada: escala urbana compacta, parque de micros reducido y baja supervisión en terreno."
        mix_movil_pct = 0
        mix_fijo_pct = 100
        formato_movil = "Sin soporte en buses (Inviable operativamente / Baja tasa de retorno)"
        formato_fijo = "Pantallas Digitales (DOOH) en accesos Mall + MUPIS en Ejes Principales"
        estrategia_texto = (
            f"En {nombre_sucursal}, la trama urbana concentrada y la dispersión del transporte menor no justifican producción de lunetas en buses. "
            "Se destina el 100% del mix OOH a pantallas DOOH de alta frecuencia en el acceso directo al centro comercial y ejes estructurantes de llegada, "
            "reforzando con radio local para cobertura comunal según los lineamientos de Q4."
        )

    elif es_corporativo or es_peatonal_puro:
        usa_luneta = False
        razon_luneta = "Descartadas por dispersión. El público target se concentra a pie en el radio inmediato."
        mix_movil_pct = 0
        mix_fijo_pct = 100
        formato_movil = "Sin soporte móvil (Baja afinidad con el público objetivo)"
        formato_fijo = "MUPIS Peatonales (<300m) / Tótems de Acceso / DOOH Corporativo"
        estrategia_texto = (
            "Para un entorno peatonal consolidado o corporativo, el transporte público genera dispersión. "
            "La masa crítica se captura a pie en el radio inmediato. Se privilegia la proximidad con MUPIS, pantallas peatonales y señalética de cercanía ('a pasos de ti')."
        )

    elif es_metro_hub:
        usa_luneta = True
        razon_luneta = "Complementaria de baja escala. Metro absorbe el gran volumen de masa."
        mix_movil_pct = 25
        mix_fijo_pct = 75
        formato_movil = "Lunetas RED Troncales de apoyo"
        formato_fijo = "Dominación de Estación de Metro (Andenes / Túneles) + Pantallas Digitales"
        estrategia_texto = (
            "En nodos intermodales con Metro, el subterráneo es el canal hegemónico de tráfico. Las lunetas cumplen solo un rol perimetral secundario (25%), concentrando la inversión en la dominación visual de accesos y andenes de Metro (75%)."
        )

    else:
        # Grandes conurbaciones o Malls regionales de gran escala (Concepción, Antofagasta, La Serena)
        usa_luneta = True
        if "Mall" in tipo_local:
            mix_movil_pct = 60 if ("Regiones" in plaza or "Conurbación" in escala_urbana) else 50
            mix_fijo_pct = 100 - mix_movil_pct
            formato_movil = "Lunetas de Buses (Flota Intercomunal / Red Conurbada)" if "Regiones" in plaza else "Lunetas RED Corredores hacia el Mall"
            formato_fijo = "Pantallas Digitales y Tótems en Accesos al Centro Comercial"
            razon_luneta = "Recomendada: cubre la cuenca residencial intercomunal que viaja hacia el centro comercial."
            estrategia_texto = (
                "La sucursal opera dentro de un polo comercial de gran alcance que atrae público de toda la conurbación. "
                "Las lunetas en flota son el medio más costo-eficiente para capturar la cuenca de atracción completa (15 a 20 min de viaje), combinadas con elementos fijos en los accesos al mall para el cierre."
            )
        else:
            mix_movil_pct = 50
            mix_fijo_pct = 50
            formato_movil = "Lunetas de Buses Flota Local / Ejes Troncales"
            formato_fijo = "MUPIS / Pantallas LED en Cruces Viales Cercanos"
            razon_luneta = "Recomendada: genera masa crítica de impactos en el corredor vehicular principal."
            estrategia_texto = (
                "Entorno de movilidad mixta en eje vial. Las lunetas proporcionan cobertura y frecuencia continua en el corredor principal, complementadas equitativamente con presencia fija en cruces de alta visibilidad."
            )

    with col2:
        st.markdown(f"#### 2. Diagnóstico y Recomendación: **{nombre_sucursal}**")
        
        # Alerta visual en Streamlit
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

        # Generación de Lámina Ejecutiva 16:9
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

        st.image(slide_bytes, caption="Lámina ejecutiva generada automáticamente (1920x1080)", use_container_width=True)

        st.download_button(
            label="🖼️ Descargar Lámina en JPG (Alta Calidad)",
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
    f_num = cargar(rutas_fuentes, 72)
    f_card_tit = cargar(rutas_fuentes, 24)
    f_body = cargar(rutas_regular, 22)
    f_bold = cargar(rutas_fuentes, 22)

    amarillo_sf = "#FFB703"

    # Barra superior de acento corporativo
    draw.rectangle([(0, 0), (ancho, 14)], fill=amarillo_sf)

    # Encabezado / Branding
    draw.text((100, 60), "SMART FIT | ANÁLISIS DE PERTINENCIA & MIX OOH", font=f_tag, fill=amarillo_sf)
    draw.text((100, 100), nombre[:55], font=f_tit, fill="#FFFFFF")
    
    # Metadatos limpios en 2 líneas independientes (sin cortes hacia la derecha)
    plaza_corta = plaza.split("(")[0].strip()
    campana_corta = duracion.split("(")[0].strip()
    draw.text((100, 168), f"Plaza: {plaza_corta}   •   Entorno: {entorno}   •   Campaña: {campana_corta}", font=f_sub, fill="#A6B0BF")
    draw.text((100, 204), f"Dinámica de Movilidad: {movilidad}", font=f_sub, fill="#7A828E")

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
