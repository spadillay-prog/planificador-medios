import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Planificador de Medios: Mix OOH & Metro",
    page_icon="🎯",
    layout="wide"
)

# Inicializar sesión del plan de medios (carrito)
if "plan_items" not in st.session_state:
    st.session_state.plan_items = []

# --- BASE DE DATOS METRO DE SANTIAGO (OFICIAL IPSOS) ---
METRO_DATA = {
    "Línea 1": {
        "Alberto Hurtado": {"flujo_mes": 5146950, "alcance_dia": 171565},
        "Alcantara": {"flujo_mes": 4125420, "alcance_dia": 137514},
        "Baquedano": {"flujo_mes": 11084610, "alcance_dia": 369487},
        "Central": {"flujo_mes": 6083070, "alcance_dia": 202769},
        "Ecuador": {"flujo_mes": 5290230, "alcance_dia": 176341},
        "El Golf": {"flujo_mes": 4568130, "alcance_dia": 152271},
        "Escuela Militar": {"flujo_mes": 3730200, "alcance_dia": 124340},
        "Hernando De Magallanes": {"flujo_mes": 2252940, "alcance_dia": 75098},
        "La Moneda": {"flujo_mes": 6435480, "alcance_dia": 214516},
        "Las Rejas": {"flujo_mes": 4796760, "alcance_dia": 159892},
        "Los Dominicos": {"flujo_mes": 1840920, "alcance_dia": 61364},
        "Los Heroes": {"flujo_mes": 9190050, "alcance_dia": 306335},
        "Los Leones": {"flujo_mes": 8199240, "alcance_dia": 273308},
        "Manquehue": {"flujo_mes": 3751140, "alcance_dia": 125038},
        "Manuel Montt": {"flujo_mes": 4545000, "alcance_dia": 151500},
        "Neptuno": {"flujo_mes": 4353210, "alcance_dia": 145107},
        "Pajaritos": {"flujo_mes": 4272180, "alcance_dia": 142406},
        "Pedro De Valdivia": {"flujo_mes": 4181790, "alcance_dia": 139393},
        "Republica": {"flujo_mes": 5831550, "alcance_dia": 194385},
        "Salvador": {"flujo_mes": 4141680, "alcance_dia": 138056},
        "San Alberto Hurtado": {"flujo_mes": 5146950, "alcance_dia": 171565},
        "San Pablo": {"flujo_mes": 5306610, "alcance_dia": 176887},
        "Santa Lucia": {"flujo_mes": 5918340, "alcance_dia": 197278},
        "Tobalaba": {"flujo_mes": 8866500, "alcance_dia": 295550},
        "U.L.A.": {"flujo_mes": 5797350, "alcance_dia": 193245},
        "Universidad Catolica": {"flujo_mes": 5462820, "alcance_dia": 182094},
        "Universidad De Chile": {"flujo_mes": 8058030, "alcance_dia": 268601}
    },
    "Línea 2": {
        "Cementerios": {"flujo_mes": 1696200, "alcance_dia": 56540},
        "Cerro Blanco": {"flujo_mes": 2221650, "alcance_dia": 74055},
        "Ciudad Del Niño": {"flujo_mes": 2235960, "alcance_dia": 74532},
        "Departamental": {"flujo_mes": 2740380, "alcance_dia": 91346},
        "Dorsal": {"flujo_mes": 2420070, "alcance_dia": 80669},
        "Einstein": {"flujo_mes": 2188440, "alcance_dia": 72948},
        "El Llano": {"flujo_mes": 2977530, "alcance_dia": 99251},
        "El Parrón": {"flujo_mes": 2049000, "alcance_dia": 68300},
        "Franklin": {"flujo_mes": 6393960, "alcance_dia": 213132},
        "La Cisterna": {"flujo_mes": 4272180, "alcance_dia": 142406},
        "Lo Ovalle": {"flujo_mes": 2235960, "alcance_dia": 74532},
        "Lo Vial": {"flujo_mes": 2687550, "alcance_dia": 89585},
        "Los Heroes": {"flujo_mes": 9190050, "alcance_dia": 306335},
        "Parque O'Higgins": {"flujo_mes": 2664090, "alcance_dia": 88803},
        "Patronato": {"flujo_mes": 3290610, "alcance_dia": 109687},
        "Puente Cal Y Canto": {"flujo_mes": 8058030, "alcance_dia": 268601},
        "Rondizzoni": {"flujo_mes": 2348550, "alcance_dia": 78285},
        "San Miguel": {"flujo_mes": 2740380, "alcance_dia": 91346},
        "Santa Ana": {"flujo_mes": 7378950, "alcance_dia": 245965},
        "Toesca": {"flujo_mes": 2664090, "alcance_dia": 88803},
        "Vespucio Norte": {"flujo_mes": 3816750, "alcance_dia": 127225},
        "Zapadores": {"flujo_mes": 2951160, "alcance_dia": 98372}
    },
    "Línea 3": {
        "Chile España": {"flujo_mes": 2378880, "alcance_dia": 79296},
        "Conchali": {"flujo_mes": 2446830, "alcance_dia": 81561},
        "Hospitales": {"flujo_mes": 3816750, "alcance_dia": 127225},
        "Irarrazaval": {"flujo_mes": 5290230, "alcance_dia": 176341},
        "Ñuñoa": {"flujo_mes": 4545000, "alcance_dia": 151500},
        "Plaza De Armas": {"flujo_mes": 8058030, "alcance_dia": 268601},
        "Plaza Egaña": {"flujo_mes": 5462820, "alcance_dia": 182094},
        "Universidad De Chile": {"flujo_mes": 8058030, "alcance_dia": 268601}
    },
    "Línea 4": {
        "Cristobal Colon": {"flujo_mes": 2235960, "alcance_dia": 74532},
        "Francisco Bilbao": {"flujo_mes": 2687550, "alcance_dia": 89585},
        "Macul": {"flujo_mes": 2977530, "alcance_dia": 99251},
        "Plaza De Puente Alto": {"flujo_mes": 3816750, "alcance_dia": 127225},
        "Plaza Egaña": {"flujo_mes": 5462820, "alcance_dia": 182094},
        "Principe De Gales": {"flujo_mes": 2687550, "alcance_dia": 89585},
        "Quilin": {"flujo_mes": 4192650, "alcance_dia": 139755},
        "Tobalaba": {"flujo_mes": 8866500, "alcance_dia": 295550},
        "Vicente Valdes": {"flujo_mes": 6393960, "alcance_dia": 213132}
    },
    "Línea 5": {
        "Baquedano": {"flujo_mes": 11084610, "alcance_dia": 369487},
        "Bellas Artes": {"flujo_mes": 3816750, "alcance_dia": 127225},
        "Bellavista De La Florida": {"flujo_mes": 5462820, "alcance_dia": 182094},
        "Carlos Valdovinos": {"flujo_mes": 2446830, "alcance_dia": 81561},
        "Irarrazaval": {"flujo_mes": 5290230, "alcance_dia": 176341},
        "Ñuble": {"flujo_mes": 4272180, "alcance_dia": 142406},
        "Pedrero": {"flujo_mes": 2446830, "alcance_dia": 81561},
        "Plaza De Armas": {"flujo_mes": 8058030, "alcance_dia": 268601},
        "Plaza De Maipu": {"flujo_mes": 4796760, "alcance_dia": 159892},
        "San Joaquin": {"flujo_mes": 2736360, "alcance_dia": 91212},
        "Santa Ana": {"flujo_mes": 7378950, "alcance_dia": 245965}
    },
    "Línea 6": {
        "Cerrillos": {"flujo_mes": 2378880, "alcance_dia": 79296},
        "Estadio Nacional": {"flujo_mes": 2687550, "alcance_dia": 89585},
        "Franklin": {"flujo_mes": 6393960, "alcance_dia": 213132},
        "Inés De Suárez": {"flujo_mes": 2687550, "alcance_dia": 89585},
        "Los Leones": {"flujo_mes": 8199240, "alcance_dia": 273308},
        "Ñuñoa": {"flujo_mes": 4545000, "alcance_dia": 151500}
    }
}

# --- BASE VÍA PÚBLICA TRADICIONAL ---
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
                        "Vicuña Mackenna con Carlos Valdovinos": {"flujo": 60000}
                    }
                },
                "San Miguel": {
                    "res": 140000, "flot": 70000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Gran Avenida con Departamental": {"flujo": 85000},
                        "Gran Avenida con Salesianos": {"flujo": 65000}
                    }
                },
                "La Cisterna": {
                    "res": 100000, "flot": 120000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Intermodal La Cisterna (Américo Vespucio con Gran Avenida)": {"flujo": 140000}
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
                        "Apoquindo con Manquehue (Apumanque)": {"flujo": 140000},
                        "El Golf / Sanhattan (Apoquindo con El Bosque)": {"flujo": 160000},
                        "Rotonda Atenas": {"flujo": 70000}
                    }
                },
                "Providencia": {
                    "res": 155000, "flot": 350000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Providencia con Tobalaba (Costanera Center)": {"flujo": 180000},
                        "Plaza Baquedano": {"flujo": 150000}
                    }
                },
                "Ñuñoa": {
                    "res": 255000, "flot": 80000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Plaza Egaña (Larraín con Av. Ossa)": {"flujo": 120000},
                        "Irarrázaval con Pedro de Valdivia": {"flujo": 85000}
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
                        "Rotonda Quilín / Américo Vespucio (Mall Paseo Quilín)": {"flujo": 130000}
                    }
                },
                "La Florida": {
                    "res": 400000, "flot": 110000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Vicuña Mackenna con Américo Vespucio (Mall Plaza Vespucio)": {"flujo": 170000}
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
                        "Ruta 5 con Francisco de Aguirre": {"flujo": 80000}
                    }
                },
                "Coquimbo": {
                    "res": 270000, "flot": 35000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Ruta 5 con La Cantera": {"flujo": 75000}
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
                        "Av. Costanera con Balmaceda (Mall Plaza)": {"flujo": 110000}
                    }
                }
            }
        }
    }
}

FORMATOS_OOH = {
    "Pantalla Digital Gran Formato (DOOH)": {"c": 0.20, "m": 0.25, "o": 0.30, "base": 1, "unidad": "pantallas"},
    "Valla / Monoposte Estático": {"c": 0.15, "m": 0.20, "o": 0.25, "base": 1, "unidad": "soportes"},
    "Buses Troncales / Gran Impacto": {"c": 0.30, "m": 0.35, "o": 0.40, "base": 70, "unidad": "buses"},
    "Lunetas en Microbuses": {"c": 0.25, "m": 0.30, "o": 0.35, "base": 40, "unidad": "lunetas"}
}

FORMATOS_METRO = {
    "Brandeo Tren Integral (Línea 1 - 27 Estaciones)": {
        "c": 0.22, "m": 0.27, "o": 0.32, "base": 1, "unidad": "trenes", "es_tren": True, "flujo_red_dia": 850000
    },
    "Circuito Pantallas Digitales Andén (DOOH)": {
        "c": 0.30, "m": 0.40, "o": 0.50, "base": 1, "unidad": "circuitos", "es_tren": False
    },
    "Valla / Panel Andén Estático": {
        "c": 0.25, "m": 0.35, "o": 0.45, "base": 1, "unidad": "paneles", "es_tren": False
    },
    "Panel Acceso / Torniquetes": {
        "c": 0.35, "m": 0.45, "o": 0.55, "base": 1, "unidad": "paneles", "es_tren": False
    },
    "Brandeo Integral de Estación / Muro": {
        "c": 0.50, "m": 0.65, "o": 0.75, "base": 1, "unidad": "estaciones", "es_tren": False
    }
}

st.title("🎯 Planificador de Medios Multi-Formato (OOH & Metro)")
st.markdown("Arma un mix con múltiples soportes, calcula el rendimiento por ítem y el consolidado total de campaña.")

# --- SIDEBAR: CONFIGURADOR DE ELEMENTO ---
st.sidebar.header("🛠️ Configurar Soporte")
medio_tipo = st.sidebar.radio("Entorno:", ["Vía Pública Tradicional / Calles", "Metro de Santiago (Estaciones y Trenes)"])

if medio_tipo == "Metro de Santiago (Estaciones y Trenes)":
    formato_dict = FORMATOS_METRO
    formato_sel = st.sidebar.selectbox("Formato en Metro:", list(formato_dict.keys()))
    info_formato = formato_dict[formato_sel]
    
    if info_formato.get("es_tren", False):
        universo_calculo = info_formato["flujo_red_dia"]
        nombre_territorio = "Línea 1 Completa (27 Estaciones)"
    else:
        linea_sel = st.sidebar.selectbox("Línea de Metro:", list(METRO_DATA.keys()))
        estacion_sel = st.sidebar.selectbox("Estación:", list(METRO_DATA[linea_sel].keys()))
        universo_calculo = METRO_DATA[linea_sel][estacion_sel]["alcance_dia"]
        nombre_territorio = f"Metro {linea_sel} - Estación {estacion_sel}"
else:
    reg_sel = st.sidebar.selectbox("Región:", list(DATA_JERARQUICA.keys()))
    sec_sel = st.sidebar.selectbox("Sector / Zona:", list(DATA_JERARQUICA[reg_sel].keys()))
    datos_sec = DATA_JERARQUICA[reg_sel][sec_sel]
    com_sel = st.sidebar.selectbox("Comuna:", ["Todo el Sector en conjunto"] + list(datos_sec["comunas"].keys()))
    
    if com_sel == "Todo el Sector en conjunto":
        universo_calculo = datos_sec["res_sector"] + datos_sec["flot_sector"]
        nombre_territorio = f"{sec_sel} (Macrozona)"
    else:
        com_data = datos_sec["comunas"][com_sel]
        pto_sel = st.sidebar.selectbox("Georreferencia / Punto:", list(com_data["puntos"].keys()))
        if pto_sel == "Toda la comuna (General)":
            universo_calculo = com_data["res"] + com_data["flot"]
            nombre_territorio = com_sel
        else:
            universo_calculo = com_data["puntos"][pto_sel]["flujo"]
            nombre_territorio = f"{com_sel} - {pto_sel}"

    formato_dict = FORMATOS_OOH
    formato_sel = st.sidebar.selectbox("Formato Vía Pública:", list(formato_dict.keys()))
    info_formato = formato_dict[formato_sel]

cant_elementos = st.sidebar.number_input(
    f"Cantidad de {info_formato['unidad'].capitalize()}:",
    min_value=1, max_value=200, value=info_formato["base"], step=1
)
dias_campana = st.sidebar.slider("Días de Exhibición:", min_value=1, max_value=60, value=10 if "Pantalla" in formato_sel else 30)
inversion_neta = st.sidebar.number_input("Inversión Neta ($ CLP):", value=500000 if "Pantalla" in formato_sel else 2500000, step=250000)

castigo_pct = st.sidebar.slider("Castigo Técnico (%):", min_value=0, max_value=25, value=10, step=5)
factor_castigo = (100 - castigo_pct) / 100
factor_elementos = cant_elementos / info_formato["base"]

# Cálculo de impactos del ítem actual
imp_c = (universo_calculo * info_formato["c"] * factor_elementos * factor_castigo) * dias_campana
imp_m = (universo_calculo * info_formato["m"] * factor_elementos * factor_castigo) * dias_campana
imp_o = (universo_calculo * info_formato["o"] * factor_elementos * factor_castigo) * dias_campana

st.sidebar.markdown("---")
if st.sidebar.button("➕ Agregar este elemento al Plan de Medios", use_container_width=True, type="primary"):
    st.session_state.plan_items.append({
        "Soporte": f"{formato_sel} ({cant_elementos} {info_formato['unidad']})",
        "Ubicación": nombre_territorio,
        "Días": dias_campana,
        "Inversión Neta": inversion_neta,
        "Impactos Conservador": int(imp_c),
        "Impactos Medio": int(imp_m),
        "Impactos Optimista": int(imp_o),
        "CPM Medio": (inversion_neta / imp_m * 1000) if imp_m > 0 else 0
    })
    st.sidebar.success("¡Elemento agregado al mix!")

if st.sidebar.button("🗑️ Limpiar Plan de Medios", use_container_width=True):
    st.session_state.plan_items = []
    st.rerun()

# --- VISTA PRINCIPAL: DASHBOARD MULTI-FORMATO ---
if len(st.session_state.plan_items) == 0:
    st.info("👈 Configura los parámetros en el menú lateral y haz clic en **'➕ Agregar este elemento al Plan de Medios'** para armar tu propuesta combinada.")
else:
    st.subheader(f"📋 1. Desglose por Elemento ({len(st.session_state.plan_items)} soportes en el Mix)")
    
    df_items = pd.DataFrame(st.session_state.plan_items)
    
    # Formateo visual de la tabla individual
    df_display = df_items.copy()
    df_display["Inversión Neta"] = df_display["Inversión Neta"].apply(lambda x: f"${int(x):,}".replace(",", "."))
    df_display["Impactos Conservador"] = df_display["Impactos Conservador"].apply(lambda x: f"{int(x):,}".replace(",", "."))
    df_display["Impactos Medio"] = df_display["Impactos Medio"].apply(lambda x: f"{int(x):,}".replace(",", "."))
    df_display["Impactos Optimista"] = df_display["Impactos Optimista"].apply(lambda x: f"{int(x):,}".replace(",", "."))
    df_display["CPM Medio"] = df_display["CPM Medio"].apply(lambda x: f"${int(round(x)):,}".replace(",", "."))
    
    st.dataframe(df_display, use_container_width=True)
    
    # --- CONSOLIDADO GLOBAL ---
    total_inversion = sum(item["Inversión Neta"] for item in st.session_state.plan_items)
    total_imp_c = sum(item["Impactos Conservador"] for item in st.session_state.plan_items)
    total_imp_m = sum(item["Impactos Medio"] for item in st.session_state.plan_items)
    total_imp_o = sum(item["Impactos Optimista"] for item in st.session_state.plan_items)
    
    cpm_global_c = (total_inversion / total_imp_c * 1000) if total_imp_c > 0 else 0
    cpm_global_m = (total_inversion / total_imp_m * 1000) if total_imp_m > 0 else 0
    cpm_global_o = (total_inversion / total_imp_o * 1000) if total_imp_o > 0 else 0

    st.markdown("---")
    st.subheader("📊 2. Consolidado Total de la Campaña (Mix Integrado)")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Soportes en Mix", f"{len(st.session_state.plan_items)} líneas")
    m2.metric("Inversión Total Neta", f"${total_inversion:,.0f}".replace(",", "."))
    m3.metric("Impactos Totales (Medio)", f"{total_imp_m:,.0f}".replace(",", "."))
    m4.metric("CPM Ponderado Global", f"${int(round(cpm_global_m)):,}".replace(",", "."))
    
    # Tabla consolidada de escenarios totales
    tabla_consolidada = [
        {
            "Escenario Global": "Conservador",
            "Impactos Totales Campaña": f"{total_imp_c:,.0f}".replace(",", "."),
            "Costo por Impacto Promedio": f"${(total_inversion / total_imp_c):.2f}" if total_imp_c > 0 else "$0",
            "CPM Global": f"${int(round(cpm_global_c)):,}".replace(",", ".")
        },
        {
            "Escenario Global": "Medio (Recomendado)",
            "Impactos Totales Campaña": f"{total_imp_m:,.0f}".replace(",", "."),
            "Costo por Impacto Promedio": f"${(total_inversion / total_imp_m):.2f}" if total_imp_m > 0 else "$0",
            "CPM Global": f"${int(round(cpm_global_m)):,}".replace(",", ".")
        },
        {
            "Escenario Global": "Optimista",
            "Impactos Totales Campaña": f"{total_imp_o:,.0f}".replace(",", "."),
            "Costo por Impacto Promedio": f"${(total_inversion / total_imp_o):.2f}" if total_imp_o > 0 else "$0",
            "CPM Global": f"${int(round(cpm_global_o)):,}".replace(",", ".")
        }
    ]
    st.table(pd.DataFrame(tabla_consolidada))
    
    # --- RESUMEN EJECUTIVO PARA COPIAR ---
    st.markdown("---")
    st.subheader("📋 3. Resumen Ejecutivo para Propuesta al Cliente")
    
    lineas_resumen = ""
    for idx, item in enumerate(st.session_state.plan_items, 1):
        lineas_resumen += f"  {idx}. **{item['Soporte']}** en {item['Ubicación']} | {item['Días']} días | Inversión: \({item['Inversión Neta']:,.0f} | Impactos (Medio): {item['Impactos Medio']:,} | CPM:\){int(round(item['CPM Medio'])):,}\n".replace(",", ".")
        
    texto_resumen = f"""**PROPUESTA DE MEDIOS INTEGRADA (MIX OOH & METRO)**
**Inversión Total Neta:** ${total_inversion:,.0f} CLP
**Impactos Brutos Totales (Escenario Medio):** {total_imp_m:,.0f} impactos
**CPM Ponderado Global:** ${int(round(cpm_global_m)):,}.00 CLP

**Detalle del Mix de Medios:**
{lineas_resumen}
*Todos los valores son netos y aplican castigo técnico por dispersión.*
"""
    st.code(texto_resumen, language="markdown")
