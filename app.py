import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Simulador de Medios Vía Pública & DOOH",
    page_icon="🎯",
    layout="wide"
)

# Estructura Jerárquica: Región -> Sector -> Comunas y Puntos Específicos
DATA_JERARQUICA = {
    "Región Metropolitana": {
        "Sector Sur": {
            "res_sector": 1400000, "flot_sector": 300000,
            "comunas": {
                "San Joaquín": {
                    "res": 103000, "flot": 65000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Vicuña Mackenna con Departamental (Eje Metro Pedrero / Mall Florida Center)": {"flujo": 95000},
                        "Santa Rosa con Departamental": {"flujo": 75000},
                        "Vicuña Mackenna con Carlos Valdovinos (Eje Universidades)": {"flujo": 60000}
                    }
                },
                "San Miguel": {
                    "res": 140000, "flot": 70000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Gran Avenida con Departamental (Nudo Comercial / Metro)": {"flujo": 85000},
                        "Gran Avenida con Salesianos / San Nicolás": {"flujo": 65000}
                    }
                },
                "La Cisterna": {
                    "res": 100000, "flot": 120000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Intermodal La Cisterna (Américo Vespucio Sur con Gran Avenida)": {"flujo": 140000}
                    }
                },
                "San Bernardo": {
                    "res": 335000, "flot": 50000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Plaza de Armas / Estación Tren Central": {"flujo": 55000}
                    }
                }
            }
        },
        "Sector Oriente": {
            "res_sector": 1060000, "flot_sector": 800000,
            "comunas": {
                "Las Condes": {
                    "res": 330000, "flot": 450000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Apoquindo con Manquehue (Eje Apumanque)": {"flujo": 140000},
                        "El Golf / Sanhattan (Apoquindo con El Bosque)": {"flujo": 160000},
                        "Rotonda Atenas (Av. Cristóbal Colón con Cuarto Centenario)": {"flujo": 70000}
                    }
                },
                "Providencia": {
                    "res": 155000, "flot": 350000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Providencia con Tobalaba (Nudo Costanera Center)": {"flujo": 180000},
                        "Providencia con Pedro de Valdivia": {"flujo": 110000},
                        "Plaza Baquedano / Vicuña Mackenna": {"flujo": 150000}
                    }
                },
                "Ñuñoa": {
                    "res": 255000, "flot": 80000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Plaza Egaña (Larraín con Av. Ossa)": {"flujo": 120000},
                        "Irarrázaval con Pedro de Valdivia (Eje Metro)": {"flujo": 85000}
                    }
                },
                "Vitacura": {
                    "res": 95000, "flot": 110000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. Vitacura con Américo Vespucio": {"flujo": 95000}
                    }
                }
            }
        },
        "Sector Sur-Oriente": {
            "res_sector": 1420000, "flot_sector": 250000,
            "comunas": {
                "Peñalolén / Macul (Eje Quilín)": {
                    "res": 280000, "flot": 90000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Rotonda Quilín / Américo Vespucio (Mall Paseo Quilín)": {"flujo": 130000},
                        "Av. Macul con Quilín": {"flujo": 60000}
                    }
                },
                "La Florida": {
                    "res": 400000, "flot": 110000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Vicuña Mackenna con Américo Vespucio (Mall Plaza Vespucio / Metro Bellavista)": {"flujo": 170000},
                        "Vicuña Mackenna con Trinidad": {"flujo": 75000}
                    }
                },
                "Puente Alto": {
                    "res": 650000, "flot": 60000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Plaza de Puente Alto (Concha y Toro)": {"flujo": 85000}
                    }
                }
            }
        },
        "Sector Centro": {
            "res_sector": 500000, "flot_sector": 1000000,
            "comunas": {
                "Santiago Centro": {
                    "res": 500000, "flot": 1000000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Alameda con Paseo Ahumada / Metro U. de Chile": {"flujo": 220000},
                        "Alameda con Santa Rosa": {"flujo": 140000},
                        "Barrio Meiggs / Estación Central Alameda": {"flujo": 190000}
                    }
                }
            }
        },
        "Sector Poniente": {
            "res_sector": 1600000, "flot_sector": 550000,
            "comunas": {
                "Maipú": {
                    "res": 580000, "flot": 80000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Plaza de Maipú (Pajaritos con 5 de Abril)": {"flujo": 130000},
                        "Pajaritos con Américo Vespucio (Mall Arauco Maipú)": {"flujo": 120000}
                    }
                },
                "Estación Central": {
                    "res": 210000, "flot": 350000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Alameda frente a Terminales de Buses (Sur / San Borja)": {"flujo": 180000}
                    }
                },
                "Pudahuel": {
                    "res": 255000, "flot": 120000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "San Pablo con Teniente Cruz": {"flujo": 70000}
                    }
                }
            }
        },
        "Sector Norte": {
            "res_sector": 1250000, "flot_sector": 450000,
            "comunas": {
                "Huechuraba": {
                    "res": 110000, "flot": 130000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Ciudad Empresarial (Av. del Parque con Américo Vespucio)": {"flujo": 110000}
                    }
                },
                "Quilicura": {
                    "res": 260000, "flot": 90000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Américo Vespucio Norte con Panamericana Norte": {"flujo": 115000}
                    }
                },
                "Independencia / Recoleta": {
                    "res": 310000, "flot": 180000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. Independencia con Santos Dumont (Sector Hospitales)": {"flujo": 95000},
                        "Av. Recoleta con Av. La Paz (La Vega Central / Tirso de Molina)": {"flujo": 130000}
                    }
                }
            }
        }
    },
    "Región de Coquimbo": {
        "Conurbación La Serena - Coquimbo": {
            "res_sector": 530000, "flot_sector": 60000,
            "comunas": {
                "La Serena": {
                    "res": 260000, "flot": 40000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Ruta 5 con Francisco de Aguirre": {"flujo": 80000},
                        "Av. Balmaceda con Cuatro Esquinas": {"flujo": 65000}
                    }
                },
                "Coquimbo": {
                    "res": 270000, "flot": 35000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Ruta 5 con La Cantera": {"flujo": 75000},
                        "Av. Videla con Hospital de Coquimbo": {"flujo": 55000}
                    }
                }
            }
        }
    },
    "Región de Antofagasta": {
        "Gran Antofagasta": {
            "res_sector": 440000, "flot_sector": 50000,
            "comunas": {
                "Antofagasta": {
                    "res": 440000, "flot": 50000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. Costanera con Balmaceda (Sector Mall Plaza)": {"flujo": 110000},
                        "Pedro Aguirre Cerda con Av. Pérez Zujovic (Sector Norte)": {"flujo": 90000}
                    }
                }
            }
        }
    },
    "Región de Valparaíso": {
        "Gran Valparaíso": {
            "res_sector": 750000, "flot_sector": 150000,
            "comunas": {
                "Viña del Mar": {
                    "res": 360000, "flot": 120000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "1 Norte con Libertad / Mall Marina": {"flujo": 130000},
                        "Av. Benidorm (15 Norte) con San Martín": {"flujo": 85000}
                    }
                },
                "Valparaíso": {
                    "res": 315000, "flot": 90000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. Argentina con Pedro Montt (Congreso / Terminal)": {"flujo": 110000}
                    }
                }
            }
        }
    }
}

FORMATOS = {
    "Pantalla Digital Gran Formato (DOOH)": {
        "c": 0.20, "m": 0.25, "o": 0.30,
        "base_unidades": 1,
        "unidad_nombre": "pantallas",
        "desc": "Impacto dinámico en nudos de tráfico y detención vehicular/peatonal."
    },
    "Buses Troncales / Gran Impacto": {
        "c": 0.30, "m": 0.35, "o": 0.40,
        "base_unidades": 70,
        "unidad_nombre": "buses",
        "desc": "Cobertura masiva en avenidas troncales y estructurantes."
    },
    "Lunetas en Microbuses": {
        "c": 0.25, "m": 0.30, "o": 0.35,
        "base_unidades": 40,
        "unidad_nombre": "lunetas",
        "desc": "Alta saturación visual vehicular, tacos y semáforos."
    },
    "Valla / Monoposte Estático": {
        "c": 0.15, "m": 0.20, "o": 0.25,
        "base_unidades": 1,
        "unidad_nombre": "soportes",
        "desc": "Exposición continua en puntos estratégicos fijos."
    }
}

st.title("🎯 Planificador & Simulador de Medios OOH / DOOH")
st.markdown("Herramienta para estimar impactos brutos, alcance y CPM por sector, comuna y georreferencia en Chile.")

st.sidebar.header("⚙️ Configuración Territorial")

# 1. Región
region_sel = st.sidebar.selectbox("1. Selecciona Región:", list(DATA_JERARQUICA.keys()))

# 2. Sector / Macrozona
sectores_dict = DATA_JERARQUICA[region_sel]
sector_sel = st.sidebar.selectbox("2. Selecciona Sector / Zona:", list(sectores_dict.keys()))

datos_sector = sectores_dict[sector_sel]
comunas_disponibles = list(datos_sector["comunas"].keys())

# 3. Comuna (con opción de evaluar todo el sector completo)
opciones_comuna = ["Todo el Sector en conjunto"] + comunas_disponibles
comuna_sel = st.sidebar.selectbox("3. Selecciona Comuna:", opciones_comuna)

# 4. Georreferencia / Punto Específico
if comuna_sel == "Todo el Sector en conjunto":
    punto_sel = "Evaluación Macrozona Completa"
    pop_res_default = datos_sector["res_sector"]
    pop_flot_default = datos_sector["flot_sector"]
    universo_default = pop_res_default + pop_flot_default
    es_punto_fijo = False
else:
    datos_comuna = datos_sector["comunas"][comuna_sel]
    puntos_disponibles = list(datos_comuna["puntos"].keys()) + ["Otro punto específico (Personalizado)"]
    punto_sel = st.sidebar.selectbox("4. Georreferencia / Punto Específico:", puntos_disponibles)
    
    if punto_sel == "Toda la comuna (General)":
        pop_res_default = datos_comuna["res"]
        pop_flot_default = datos_comuna["flot"]
        universo_default = pop_res_default + pop_flot_default
        es_punto_fijo = False
    elif punto_sel == "Otro punto específico (Personalizado)":
        nombre_personalizado = st.sidebar.text_input("Ingresa nombre de la intersección / calle:", "Ej: Vicuña Mackenna con...")
        universo_default = 80000
        es_punto_fijo = True
    else:
        universo_default = datos_comuna["puntos"][punto_sel]["flujo"]
        es_punto_fijo = True

# Panel de Audiencia
st.sidebar.markdown("---")
st.sidebar.subheader("Población y Flujo Diario")

if es_punto_fijo:
    universo_total = st.sidebar.number_input(
        "Flujo Diario Estimado en el Punto (Vehículos + Peatones):",
        value=universo_default,
        step=5000
    )
    st.sidebar.info(f"📍 **Punto evaluado:** {punto_sel}\n\n**Flujo activo diario:** {universo_total:,.0f} personas".replace(",", "."))
else:
    pop_residente = st.sidebar.number_input("Población Residente:", value=pop_res_default, step=10000)
    pop_flotante = st.sidebar.number_input("Población Flotante Estimada:", value=pop_flot_default, step=10000)
    universo_total = pop_residente + pop_flotante
    st.sidebar.info(f"**Universo Total Activo Diario:** {universo_total:,.0f} personas".replace(",", "."))

# 5. Formato y Soportes
st.sidebar.markdown("---")
st.sidebar.subheader("Soporte Publicitario")
formato_sel = st.sidebar.selectbox("5. Formato de Vía Pública:", list(FORMATOS.keys()))
info_formato = FORMATOS[formato_sel]

cant_elementos = st.sidebar.number_input(
    f"Cantidad de {info_formato['unidad_nombre'].capitalize()} contratadas:",
    min_value=1,
    max_value=500,
    value=info_formato["base_unidades"],
    step=1
)

dias_campana = st.sidebar.slider("Días de Campaña (Exhibición):", min_value=1, max_value=90, value=10 if "Pantalla" in formato_sel else 30)
inversion_neta = st.sidebar.number_input("Inversión Neta ($ CLP):", value=500000 if "Pantalla" in formato_sel else 4500000, step=250000)

factor_elementos = cant_elementos / info_formato["base_unidades"]

castigo_pct = st.sidebar.slider("Castigo Técnico / Descuento Duplicidad (%):", min_value=0, max_value=25, value=0, step=5)
factor_castigo = (100 - castigo_pct) / 100

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
ubicacion_label = f"{comuna_sel} - {punto_sel}" if es_punto_fijo else comuna_sel

col1, col2, col3, col4 = st.columns(4)
col1.metric("Universo / Flujo Diario", f"{universo_total:,.0f}".replace(",", "."))
col2.metric("Soportes Contratados", f"{cant_elementos} {info_formato['unidad_nombre']}")
col3.metric("Duración Campaña", f"{dias_campana} días")
col4.metric("Inversión Neta", f"${inversion_neta:,.0f}".replace(",", "."))

st.markdown("---")
st.subheader(f"📊 Proyección: {cant_elementos} {info_formato['unidad_nombre'].capitalize()} en {ubicacion_label}")
st.caption(f"{info_formato['desc']} | Sector: {sector_sel} ({region_sel})" + (f" | Castigo técnico: {castigo_pct}%" if castigo_pct > 0 else ""))

st.table(df_res)

# Resumen tipo propuesta para copiar
st.markdown("---")
st.subheader("📋 Resumen Ejecutivo para Propuesta")
esc_medio = resultados[1]
texto_propuesta = f"""**Resumen de Propuesta Comercial:**
- **Territorio:** {region_sel} - {sector_sel}
- **Comuna / Ubicación:** {ubicacion_label}
- **Flujo Activo Diario:** {universo_total:,.0f} personas
- **Soporte:** {formato_sel} ({cant_elementos} {info_formato['unidad_nombre']})
- **Duración:** {dias_campana} días
- **Inversión Neta:** ${inversion_neta:,.0f} CLP
- **Contactos Diarios Estimados (Escenario Medio):** {esc_medio['Contactos Diarios']}
- **Impactos Brutos Totales (OTS):** {esc_medio[f'Impactos Totales ({dias_campana} días)']}
- **Costo por Impacto:** {esc_medio['Costo x Impacto']} CLP
- **CPM Estimado:** {esc_medio['CPM ($ CLP)']} CLP
"""
st.code(texto_propuesta, language="markdown")
