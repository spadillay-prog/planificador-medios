import streamlit as st

def render_smartfit_advisor():
    st.markdown("## 🏋️‍♂️ Smart Fit — Recomendador Táctico OOH")
    st.caption("Módulo exclusivo para optimización de cobertura, proximidad y mix de medios en vía pública.")

    st.markdown("---")

    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown("#### 1. Datos de la Sucursal")
        nombre_sucursal = st.text_input("Nombre / Referencia de la sucursal", value="Smart Fit - Mallplaza El Trébol (Talcahuano / Concepción)")
        
        plaza = st.selectbox(
            "Territorio / Plaza",
            [
                "Regiones (Ciudades intermedias / Capital regional)",
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

    # Lógica de recomendación táctica
    if objetivo_campana.startswith("Apertura"):
        if "Centro Comercial" in tipo_local:
            mix_movil_pct = 70 if "Regiones" in plaza else 60
            mix_fijo_pct = 100 - mix_movil_pct
            formato_movil = "Lunetas de Buses Locales (Líneas con destino al Centro Comercial)"
            formato_fijo = "Pantallas Digitales en Accesos / Tótems de Estacionamiento Mall"
            estrategia_texto = (
                "Para la preventa o inauguración en un centro comercial, la prioridad es sembrar la marca en los barrios "
                "residenciales de donde provienen los usuarios (radio de viaje de 10 a 20 min). Las lunetas de microbuses "
                "garantizan cobertura comunal amplia y continua, mientras que los soportes fijos en el acceso al mall "
                "validan la entrada y rematan el call-to-action."
            )
        elif "calle" in tipo_local:
            mix_movil_pct = 60
            mix_fijo_pct = 40
            formato_movil = "Lunetas de Buses Troncales de la Ciudad"
            formato_fijo = "MUPIS Peatonales / Refugios de Paradero (Radio < 500m)"
            estrategia_texto = (
                "Combina impacto masivo móvil en los recorridos que cruzan la avenida principal con soportes peatonales fijos "
                "cercanos que resuelven la orientación física del local ('A pasos de aquí', 'Inscríbete hoy'), reduciendo la "
                "fricción de búsqueda."
            )
        else:
            mix_movil_pct = 65
            mix_fijo_pct = 35
            formato_movil = "Lunetas de Buses de Flota Comunal / Alimentadora"
            formato_fijo = "Valla / Pantalla LED en Acceso Vial Principal"
            estrategia_texto = (
                "En enclaves suburbanos, el público transita en automóvil y locomoción colectiva. Se privilegia la cobertura móvil "
                "comunal y un elemento fijo de alta visibilidad en el nudo de acceso vehicular de mayor flujo."
            )
    else:  # Mantención
        if "Centro Comercial" in tipo_local:
            mix_movil_pct = 40
            mix_fijo_pct = 60
            formato_movil = "Lunetas de Buses (Recorridos directos seleccionados)"
            formato_fijo = "Circuitos MUPIS Digitales en Mall y Paraderos Adyacentes"
            estrategia_texto = (
                "En régimen regular, el objetivo es capturar al flujo flotante recurrente que ya visita el mall para convertir visitas "
                "semanales en suscripciones, manteniendo un piso móvil de recordación de marca."
            )
        elif "calle" in tipo_local:
            mix_movil_pct = 45
            mix_fijo_pct = 55
            formato_movil = "Lunetas de Buses"
            formato_fijo = "MUPIS / Relojes de Proximidad Peatonal Inmediata"
            estrategia_texto = (
                "Prioriza la frecuencia sobre la masa trabajadora y residente local en los horarios peak matutino y de salida laboral "
                "en torno a la sucursal."
            )
        else:
            mix_movil_pct = 50
            mix_fijo_pct = 50
            formato_movil = "Lunetas de Buses Locales"
            formato_fijo = "Pantallas DOOH Viales de Retorno Laboral"
            estrategia_texto = (
                "Equilibrio entre presencia móvil de ruta y soporte fijo en los trayectos de regreso a casa tras la jornada laboral."
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
        resumen_pitch = (
            f"RECOMENDACIÓN TÁCTICA OOH — SMART FIT\n"
            f"Sucursal: {nombre_sucursal}\n"
            f"Plaza: {plaza}\n"
            f"Emplazamiento: {tipo_local}\n\n"
            f"• Cobertura Móvil ({mix_movil_pct}%): {formato_movil}\n"
            f"• Proximidad Fija ({mix_fijo_pct}%): {formato_fijo}\n\n"
            f"Racional Estratégico:\n{estrategia_texto}"
        )
        st.text_area("📋 Resumen ejecutivo (copiar para propuesta / deck):", value=resumen_pitch, height=140)
        
        st.download_button(
            label="📥 Descargar Resumen Ejecutivo (.txt)",
            data=resumen_pitch,
            file_name=f"estrategia_ooh_{nombre_sucursal.lower().replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )
