import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Simulador de Medios Vía Pública & Metro",
    page_icon="🎯",
    layout="wide"
)

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
        "Cardenal Caro": {"flujo_mes": 2188440, "alcance_dia": 72948},
        "Fernando Castillo Velasco": {"flujo_mes": 2049000, "alcance_dia": 68300},
        "Hospitales": {"flujo_mes": 3816750, "alcance_dia": 127225},
        "Irarrazaval": {"flujo_mes": 5290230, "alcance_dia": 176341},
        "Los Libertadores": {"flujo_mes": 2977530, "alcance_dia": 99251},
        "Matta": {"flujo_mes": 3140550, "alcance_dia": 104685},
        "Monseñor Eyzaguirre": {"flujo_mes": 2188440, "alcance_dia": 72948},
        "Ñuble": {"flujo_mes": 4272180, "alcance_dia": 142406},
        "Ñuñoa": {"flujo_mes": 4545000, "alcance_dia": 151500},
        "Parque Almagro": {"flujo_mes": 3433650, "alcance_dia": 114455},
        "Plaza Chacabuco": {"flujo_mes": 3290610, "alcance_dia": 109687},
        "Plaza De Armas": {"flujo_mes": 8058030, "alcance_dia": 268601},
        "Plaza Egaña": {"flujo_mes": 5462820, "alcance_dia": 182094},
        "Puente Cal Y Canto": {"flujo_mes": 8058030, "alcance_dia": 268601},
        "Universidad De Chile": {"flujo_mes": 8058030, "alcance_dia": 268601},
        "Vivar": {"flujo_mes": 2420070, "alcance_dia": 80669}
    },
    "Línea 4": {
        "Cristobal Colon": {"flujo_mes": 2235960, "alcance_dia": 74532},
        "Elisa Correa": {"flujo_mes": 2049000, "alcance_dia": 68300},
        "Francisco Bilbao": {"flujo_mes": 2687550, "alcance_dia": 89585},
        "Hospital Sotero Del Rio": {"flujo_mes": 2664090, "alcance_dia": 88803},
        "Las Torres": {"flujo_mes": 2348550, "alcance_dia": 78285},
        "Los Presidentes": {"flujo_mes": 2221650, "alcance_dia": 74055},
        "Los Quillayes": {"flujo_mes": 2049000, "alcance_dia": 68300},
        "Macul": {"flujo_mes": 2977530, "alcance_dia": 99251},
        "Mercedes": {"flujo_mes": 2188440, "alcance_dia": 72948},
        "Plaza De Puente Alto": {"flujo_mes": 3816750, "alcance_dia": 127225},
        "Plaza Egaña": {"flujo_mes": 5462820, "alcance_dia": 182094},
        "Principe De Gales": {"flujo_mes": 2687550, "alcance_dia": 89585},
        "Protectora De La Infancia": {"flujo_mes": 2049000, "alcance_dia": 68300},
        "Quilin": {"flujo_mes": 4192650, "alcance_dia": 139755},
        "Rojas Magallanes": {"flujo_mes": 2188440, "alcance_dia": 72948},
        "San Jose De La Estrella": {"flujo_mes": 2049000, "alcance_dia": 68300},
        "Simon Bolivar": {"flujo_mes": 2378880, "alcance_dia": 79296},
        "Tobalaba": {"flujo_mes": 8866500, "alcance_dia": 295550},
        "Trinidad": {"flujo_mes": 2188440, "alcance_dia": 72948},
        "Vicente Valdes": {"flujo_mes": 6393960, "alcance_dia": 213132},
        "Vicuña Mackenna": {"flujo_mes": 6083070, "alcance_dia": 202769}
    },
    "Línea 4A": {
        "La Cisterna": {"flujo_mes": 4272180, "alcance_dia": 142406},
        "San Ramon": {"flujo_mes": 1696200, "alcance_dia": 56540},
        "Santa Julia": {"flujo_mes": 1696200, "alcance_dia": 56540},
        "Santa Rosa": {"flujo_mes": 2977530, "alcance_dia": 99251},
        "Vicuña Mackenna": {"flujo_mes": 6083070, "alcance_dia": 202769}
    },
    "Línea 5": {
        "Baquedano": {"flujo_mes": 11084610, "alcance_dia": 369487},
        "Bellas Artes": {"flujo_mes": 3816750, "alcance_dia": 127225},
        "Bellavista De La Florida": {"flujo_mes": 5462820, "alcance_dia": 182094},
        "Blinking / Del Sol": {"flujo_mes": 3290610, "alcance_dia": 109687},
        "Carlos Valdovinos": {"flujo_mes": 2446830, "alcance_dia": 81561},
        "Cumming": {"flujo_mes": 2740380, "alcance_dia": 91346},
        "Gruta De Lourdes": {"flujo_mes": 2740380, "alcance_dia": 91346},
        "Irarrazaval": {"flujo_mes": 5290230, "alcance_dia": 176341},
        "Mirador": {"flujo_mes": 3816750, "alcance_dia": 127225},
        "Monte Tabor": {"flujo_mes": 2188440, "alcance_dia": 72948},
        "Ñuble": {"flujo_mes": 4272180, "alcance_dia": 142406},
        "Parque Bustamante": {"flujo_mes": 2687550, "alcance_dia": 89585},
        "Pedrero": {"flujo_mes": 2446830, "alcance_dia": 81561},
        "Plaza De Armas": {"flujo_mes": 8058030, "alcance_dia": 268601},
        "Plaza De Maipu": {"flujo_mes": 4796760, "alcance_dia": 159892},
        "Rodrigo De Araya": {"flujo_mes": 2348550, "alcance_dia": 78285},
        "San Joaquin": {"flujo_mes": 2736360, "alcance_dia": 91212},
        "Santa Ana": {"flujo_mes": 7378950, "alcance_dia": 245965},
        "Santa Isabel": {"flujo_mes": 3290610, "alcance_dia": 109687},
        "Santiago Bueras": {"flujo_mes": 2235960, "alcance_dia": 74532},
        "Vicente Valdes": {"flujo_mes": 6393960, "alcance_dia": 213132}
    },
    "Línea 6": {
        "Bío Bío": {"flujo_mes": 2446830, "alcance_dia": 81561},
        "Cerrillos": {"flujo_mes": 2378880, "alcance_dia": 79296},
        "Estadio Nacional": {"flujo_mes": 2687550, "alcance_dia": 89585},
        "Franklin": {"flujo_mes": 6393960, "alcance_dia": 213132},
        "Inés De Suárez": {"flujo_mes": 2687550, "alcance_dia": 89585},
        "Lo Valledor": {"flujo_mes": 3816750, "alcance_dia": 127225},
        "Los Leones": {"flujo_mes": 8199240, "alcance_dia": 273308},
        "Ñuble": {"flujo_mes": 4272180, "alcance_dia": 142406},
        "Ñuñoa": {"flujo_mes": 4545000, "alcance_dia": 151500},
        "Pedro Aguirre Cerda": {"flujo_mes": 2188440, "alcance_dia": 72948}
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
                        "Rotonda Atenas": {"flujo": 70000}
                    }
                },
                "Providencia": {
                    "res": 155000, "flot": 350000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Providencia con Tobalaba (Nudo Costanera Center)": {"flujo": 180000},
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
                },
                "Puente Alto": {
                    "res": 650000, "flot": 60000,
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Plaza de Puente Alto": {"flujo": 85000}
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

# Formatos Vía Pública tradicional
FORMATOS_OOH = {
    "Pantalla Digital Gran Formato (DOOH)": {"c": 0.20, "m": 0.25, "o": 0.30, "base": 1, "unidad": "pantallas"},
    "Buses Troncales / Gran Impacto": {"c": 0.30, "m": 0.35, "o": 0.40, "base": 70, "unidad": "buses"},
    "Lunetas en Microbuses": {"c": 0.25, "m": 0.30, "o": 0.35, "base": 40, "unidad": "lunetas"},
    "Valla / Monoposte Estático": {"c": 0.15, "m": 0.20, "o": 0.25, "base": 1, "unidad": "soportes"}
}

# Formatos Metro de Santiago (incluyendo Brandeo Tren)
FORMATOS_METRO = {
    "Brandeo Tren Integral (Línea 1 - 27 Estaciones)": {
        "c": 0.22, "m": 0.27, "o": 0.32,
        "base": 1,
        "unidad": "trenes",
        "es_tren": True,
        "flujo_red_dia": 850000, # Afluencia activa promedio de toda la Línea 1
        "desc": "Tren completo brandeado en circulación continua entre San Pablo y Los Dominicos (27 estaciones)."
    },
    "Circuito Pantallas Digitales Andén (DOOH)": {
        "c": 0.30, "m": 0.40, "o": 0.50,
        "base": 1,
        "unidad": "circuitos",
        "es_tren": False,
        "desc": "Impacto visual dinámico frente a usuarios en espera de andén."
    },
    "Valla / Panel Andén Estático": {
        "c": 0.25, "m": 0.35, "o": 0.45,
        "base": 1,
        "unidad": "paneles",
        "es_tren": False,
        "desc": "Panel publicitario fijo en vías de andén."
    },
    "Panel Acceso / Torniquetes": {
        "c": 0.35, "m": 0.45, "o": 0.55,
        "base": 1,
        "unidad": "paneles",
        "es_tren": False,
        "desc": "Impacto forzado al ingreso y salida de pasajeros en mesanina."
    },
    "Brandeo Integral de Estación / Muro": {
        "c": 0.50, "m": 0.65, "o": 0.75,
        "base": 1,
        "unidad": "estaciones",
        "es_tren": False,
        "desc": "Dominación total de espacios publicitarios dentro de una estación."
    }
}

st.title("🎯 Planificador & Simulador: Vía Pública & Metro de Santiago")
st.markdown("Herramienta para estimar impactos brutos, alcance y CPM con datos auditados de calles, estaciones y trenes.")

st.sidebar.header("⚙️ Modo de Planificación")
medio_tipo = st.sidebar.radio("Selecciona Entorno:", ["Vía Pública Tradicional / Calles", "Metro de Santiago (Estaciones y Trenes)"])

if medio_tipo == "Metro de Santiago (Estaciones y Trenes)":
    st.sidebar.markdown("---")
    st.sidebar.subheader("Soporte Publicitario en Metro")
    formato_dict = FORMATOS_METRO
    formato_sel = st.sidebar.selectbox("1. Formato Comercial en Metro:", list(formato_dict.keys()))
    info_formato = formato_dict[formato_sel]
    
    if info_formato.get("es_tren", False):
        # Brandeo Tren Línea 1
        st.sidebar.info(
            "🚆 **Brandeo Tren Integral:**\n\n"
            "• **Recorrido:** Línea 1 completa (27 estaciones entre San Pablo y Los Dominicos).\n\n"
            "• **Afluencia Diaria Total Línea 1:** ~850.000 pasajeros/día.\n\n"
            "• **Exposición:** Doble sentido de circulación durante toda la jornada operativa."
        )
        universo_calculo = info_formato["flujo_red_dia"]
        nombre_territorio = "Línea 1 Completa (27 Estaciones)"
    else:
        # Soportes en estación individual
        st.sidebar.markdown("---")
        st.sidebar.subheader("Selección de Estación (Datos Ipsos)")
        linea_sel = st.sidebar.selectbox("2. Selecciona Línea de Metro:", list(METRO_DATA.keys()))
        estaciones_linea = METRO_DATA[linea_sel]
        estacion_sel = st.sidebar.selectbox("3. Selecciona Estación:", list(estaciones_linea.keys()))
        
        datos_estacion = estaciones_linea[estacion_sel]
        flujo_mes_oficial = datos_estacion["flujo_mes"]
        alcance_dia_oficial = datos_estacion["alcance_dia"]
        
        st.sidebar.info(
            f"🚇 **Estación:** {estacion_sel} ({linea_sel})\n\n"
            f"• **Alcance Día:** {alcance_dia_oficial:,.0f} pasajeros\n\n"
            f"• **Flujo Mes:** {flujo_mes_oficial:,.0f} pasajeros\n\n"
            f"*(Fuente oficial: Ipsos / Metro)*".replace(",", ".")
        )
        universo_calculo = alcance_dia_oficial
        nombre_territorio = f"Metro {linea_sel} - Estación {estacion_sel}"

else:
    # Vía Pública tradicional
    st.sidebar.markdown("---")
    st.sidebar.subheader("Configuración Territorial")
    reg_sel = st.sidebar.selectbox("1. Selecciona Región:", list(DATA_JERARQUICA.keys()))
    sec_sel = st.sidebar.selectbox("2. Selecciona Sector / Zona:", list(DATA_JERARQUICA[reg_sel].keys()))
    
    datos_sec = DATA_JERARQUICA[reg_sel][sec_sel]
    opciones_comuna = ["Todo el Sector en conjunto"] + list(datos_sec["comunas"].keys())
    com_sel = st.sidebar.selectbox("3. Selecciona Comuna:", opciones_comuna)
    
    if com_sel == "Todo el Sector en conjunto":
        universo_calculo = datos_sec["res_sector"] + datos_sec["flot_sector"]
        nombre_territorio = f"{sec_sel} (Macrozona)"
    else:
        com_data = datos_sec["comunas"][com_sel]
        pto_sel = st.sidebar.selectbox("4. Georreferencia / Punto:", list(com_data["puntos"].keys()))
        if pto_sel == "Toda la comuna (General)":
            universo_calculo = com_data["res"] + com_data["flot"]
            nombre_territorio = com_sel
        else:
            universo_calculo = com_data["puntos"][pto_sel]["flujo"]
            nombre_territorio = f"{com_sel} - {pto_sel}"

    st.sidebar.info(f"📍 **Ubicación:** {nombre_territorio}\n\n**Flujo diario:** {universo_calculo:,.0f} personas".replace(",", "."))
    formato_dict = FORMATOS_OOH
    formato_sel = st.sidebar.selectbox("Formato Comercial:", list(formato_dict.keys()))
    info_formato = formato_dict[formato_sel]

# Cantidad, duración e inversión
st.sidebar.markdown("---")
st.sidebar.subheader("Parámetros de Compra")

cant_elementos = st.sidebar.number_input(
    f"Cantidad de {info_formato['unidad'].capitalize()} contratados:",
    min_value=1,
    max_value=100,
    value=info_formato["base"],
    step=1
)

dias_campana = st.sidebar.slider("Días de Campaña:", min_value=1, max_value=60, value=30)
inversion_neta = st.sidebar.number_input("Inversión Neta ($ CLP):", value=12000000 if info_formato.get("es_tren", False) else 3500000, step=500000)

castigo_pct = st.sidebar.slider("Castigo Técnico / Descuento Duplicidad (%):", min_value=0, max_value=25, value=10, step=5)
factor_castigo = (100 - castigo_pct) / 100
factor_elementos = cant_elementos / info_formato["base"]

# Tasas
escenarios = [
    {"nombre": "Conservador", "tasa": info_formato["c"]},
    {"nombre": "Medio (Recomendado)", "tasa": info_formato["m"]},
    {"nombre": "Optimista", "tasa": info_formato["o"]}
]

resultados = []
for esc in escenarios:
    contactos_dia = universo_calculo * esc["tasa"] * factor_elementos * factor_castigo
    impactos_totales = contactos_dia * dias_campana
    costo_impacto = (inversion_neta / impactos_totales) if impactos_totales > 0 else 0
    cpm = costo_impacto * 1000
    
    resultados.append({
        "Escenario": esc["nombre"],
        "Tasa Contacto": f"{int(esc['tasa'] * 100)}%",
        "Contactos Diarios": f"{int(contactos_dia):,}".replace(",", "."),
        f"Impactos Totales ({dias_campana} días)": f"{int(impactos_totales):,}".replace(",", "."),
        "Costo x Impacto": f"${costo_impacto:.2f}",
        "CPM ($ CLP)": f"${int(round(cpm)):,}".replace(",", ".")
    })

df_res = pd.DataFrame(resultados)

# --- VISTA PRINCIPAL ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Universo / Flujo Día", f"{universo_calculo:,.0f}".replace(",", "."))
col2.metric("Soportes", f"{cant_elementos} {info_formato['unidad']}")
col3.metric("Duración", f"{dias_campana} días")
col4.metric("Inversión Neta", f"${inversion_neta:,.0f}".replace(",", "."))

st.markdown("---")
st.subheader(f"📊 Proyección: {cant_elementos} {info_formato['unidad'].capitalize()} en {nombre_territorio}")
st.caption(f"Soporte: {formato_sel} | {info_formato.get('desc', '')} | Descuento duplicidad: {castigo_pct}%")

st.table(df_res)

# Resumen propuesta
st.markdown("---")
st.subheader("📋 Resumen Ejecutivo para Propuesta")
esc_medio = resultados[1]
texto_propuesta = f"""**Resumen de Propuesta de Medios:**
- **Entorno / Soporte:** {formato_sel}
- **Ubicación / Recorrido:** {nombre_territorio}
- **Afluencia Diaria Base:** {universo_calculo:,.0f} personas
- **Flota Contratada:** {cant_elementos} {info_formato['unidad']}
- **Duración de Campaña:** {dias_campana} días
- **Inversión Neta Negociada:** ${inversion_neta:,.0f} CLP
- **Contactos Diarios Estimados (Escenario Medio):** {esc_medio['Contactos Diarios']}
- **Impactos Brutos Totales (OTS a {dias_campana} días):** {esc_medio[f'Impactos Totales ({dias_campana} días)']}
- **Costo por Impacto:** {esc_medio['Costo x Impacto']} CLP
- **CPM Estimado:** {esc_medio['CPM ($ CLP)']} CLP
"""
st.code(texto_propuesta, language="markdown")
