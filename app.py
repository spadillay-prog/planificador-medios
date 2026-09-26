import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io
import os

st.set_page_config(
    page_title="Planificador de Medios Chile / Vía pública",
    page_icon="🎯",
    layout="wide"
)

# Inicializar sesión para el Plan de Medios Multi-Formato (Carrito)
if "plan_items" not in st.session_state:
    st.session_state.plan_items = []

# --- 1. GESTIÓN DE FUENTES UNICODE ---
def obtener_fuente(size=24, bold=False):
    rutas = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        "arialbd.ttf" if bold else "arial.ttf"
    ]
    for ruta in rutas:
        if os.path.exists(ruta):
            try:
                return ImageFont.truetype(ruta, size)
            except Exception:
                pass
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except Exception:
        return ImageFont.load_default()

# --- 2. GENERADOR VECTORIAL DEL LOGO MADCOM ---
def generar_logo_madcom(fondo_oscuro=True):
    W, H = 220, 60
    color_trazo = (255, 255, 255, 255) if fondo_oscuro else (20, 20, 20, 255)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    # Isotipo geométrico M
    d.line([(10, 48), (10, 20), (22, 12), (32, 22), (42, 12), (54, 20), (54, 48), (10, 48)], fill=color_trazo, width=4)
    
    # Tipografía MADCOM
    f_logo = obtener_fuente(25, bold=True)
    d.text((68, 16), "MADCOM", fill=color_trazo, font=f_logo)
    return im

# --- 3. COLORES CORPORATIVOS ---
COLORES_BASE = {
    "Naranjo Enérgico": "#FF5630",
    "Amarillo (Smart Fit)": "#FFB800",
    "Negro Corporativo": "#1A1A1A",
    "Azul Intenso": "#0052CC",
    "Rojo Retail": "#D9383A",
    "Verde Esmeralda": "#00875A",
    "Azul Marino": "#091E42"
}

# --- 4. BASE DE DATOS METRO DE SANTIAGO (OFICIAL IPSOS) ---
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

# --- 5. BASE DE DATOS NACIONAL (16 REGIONES DE CHILE) ---
DATA_JERARQUICA = {
    "Región de Arica y Parinacota": {
        "Arica Urbano": {
            "res_sector": 250000, "flot_sector": 35000,
            "comunas": {
                "Arica": {
                    "res": 245000, "flot": 35000,
                    "contexto": "Eje fronterizo y comercial costero, con flujo constante en torno a Av. Diego Portales y el puerto.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. Diego Portales con Santa María": {"flujo": 65000},
                        "Av. 21 de Mayo (Centro Peatonal)": {"flujo": 50000}
                    }
                }
            }
        }
    },
    "Región de Tarapacá": {
        "Conurbación Iquique - Alto Hospicio": {
            "res_sector": 360000, "flot_sector": 65000,
            "comunas": {
                "Iquique": {
                    "res": 225000, "flot": 50000,
                    "contexto": "Alta concentración vehicular entre el puerto, el polo comercial ZOFRI y la costanera de Cavancha.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Rotonda El Pampino (Acceso Iquique)": {"flujo": 85000},
                        "Av. Arturo Prat frente a Cavancha": {"flujo": 70000}
                    }
                },
                "Alto Hospicio": {
                    "res": 135000, "flot": 15000,
                    "contexto": "Conexión obligada por Ruta A-16 con tráfico pendular diario hacia Iquique.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. Ramón Pérez Opazo (Eje Central)": {"flujo": 45000}
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
                    "contexto": "Ciudad lineal encajonada entre cerro y mar; la concentración vehicular en Av. Costanera y Pedro Aguirre Cerda eleva los OTS diarios.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. Costanera con Balmaceda (Mall Plaza)": {"flujo": 110000},
                        "Pedro Aguirre Cerda con Av. Pérez Zujovic": {"flujo": 90000}
                    }
                },
                "Calama": {
                    "res": 190000, "flot": 35000,
                    "contexto": "Centro neurálgico de la minería con gran flujo corporativo y de transporte de turnos por Av. Balmaceda.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. Balmaceda con Mall Plaza Calama": {"flujo": 65000}
                    }
                }
            }
        }
    },
    "Región de Atacama": {
        "Copiapó - Vallenar": {
            "res_sector": 290000, "flot_sector": 35000,
            "comunas": {
                "Copiapó": {
                    "res": 175000, "flot": 25000,
                    "contexto": "Eje minero y comercial centrado en Av. Copayapu y el centro cívico de la plaza de armas.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. Copayapu con Los Carrera": {"flujo": 60000}
                    }
                },
                "Vallenar": {
                    "res": 60000, "flot": 10000,
                    "contexto": "Paso obligado del Valle del Huasco con tránsito por Ruta 5 Norte.",
                    "puntos": {
                        "Toda la comuna (General)": None
                    }
                }
            }
        }
    },
    "Región de Coquimbo": {
        "Conurbación La Serena - Coquimbo": {
            "res_sector": 530000, "flot_sector": 60000,
            "comunas": {
                "Coquimbo": {
                    "res": 240000, "flot": 40000,
                    "contexto": "Coquimbo concentra su movimiento en pocos ejes que todas las rutas cruzan, generando repetición diaria de alto impacto sobre el puerto, el centro y los barrios altos.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Ruta 5 con La Cantera": {"flujo": 75000},
                        "Av. Videla con Hospital": {"flujo": 55000}
                    }
                },
                "La Serena": {
                    "res": 240000, "flot": 40000,
                    "contexto": "Ejes Balmaceda y Ruta 5 conectan el flujo intercomunal con alta retención en semáforos y centros comerciales.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Ruta 5 con Francisco de Aguirre": {"flujo": 80000},
                        "Av. Balmaceda con Cuatro Esquinas": {"flujo": 65000}
                    }
                },
                "Ovalle": {
                    "res": 125000, "flot": 15000,
                    "contexto": "Cabecera del Limarí con fuerte circulación comercial en torno a la Alameda de Ovalle.",
                    "puntos": {
                        "Toda la comuna (General)": None
                    }
                }
            }
        }
    },
    "Región de Valparaíso": {
        "Gran Valparaíso": {
            "res_sector": 1000000, "flot_sector": 180000,
            "comunas": {
                "Viña del Mar": {
                    "res": 360000, "flot": 120000,
                    "contexto": "Alta densidad turística, comercial y gastronómica concentrada en ejes 1 Norte, Libertad y borde costero.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "1 Norte con Libertad / Mall Marina": {"flujo": 130000},
                        "Av. Benidorm (15 Norte) con San Martín": {"flujo": 85000}
                    }
                },
                "Valparaíso": {
                    "res": 315000, "flot": 90000,
                    "contexto": "Centro administrativo y universitario regional con flujo masivo en torno a Av. Argentina y Pedro Montt.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. Argentina con Pedro Montt (Congreso / Terminal)": {"flujo": 110000}
                    }
                },
                "Quilpué": {
                    "res": 160000, "flot": 30000,
                    "contexto": "Polo residencial del Marga Marga con fuerte tránsito diario por el troncal urbano hacia Viña y Valparaíso.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. Los Carrera (Troncal Urbano)": {"flujo": 65000}
                    }
                },
                "Villa Alemana": {
                    "res": 130000, "flot": 20000,
                    "contexto": "Acceso interior con alto tráfico residencial por el troncal y estación de tren.",
                    "puntos": {
                        "Toda la comuna (General)": None
                    }
                },
                "Concón": {
                    "res": 65000, "flot": 35000,
                    "contexto": "Zona gastronómica y residencial de alta plusvalía en el eje costero de Borgoño.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Rotonda de Concón": {"flujo": 50000}
                    }
                }
            }
        }
    },
    "Región Metropolitana": {
        "Sector Oriente": {
            "res_sector": 1060000, "flot_sector": 800000,
            "comunas": {
                "Las Condes": {
                    "res": 330000, "flot": 450000,
                    "contexto": "Polo corporativo y financiero de máxima afluencia flotante de la capital, ideal para campañas de cobertura y frecuencia masiva.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Apoquindo con Manquehue (Apumanque)": {"flujo": 140000},
                        "El Golf / Sanhattan (Apoquindo con El Bosque)": {"flujo": 160000},
                        "Rotonda Atenas": {"flujo": 70000}
                    }
                },
                "Providencia": {
                    "res": 155000, "flot": 350000,
                    "contexto": "Eje comercial y de oficinas de mayor flujo peatonal continuo y conectividad oriente-centro.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Providencia con Tobalaba (Costanera Center)": {"flujo": 180000},
                        "Plaza Baquedano": {"flujo": 150000}
                    }
                },
                "Ñuñoa": {
                    "res": 255000, "flot": 80000,
                    "contexto": "Sector residencial y de servicios con importantes nudos de detención vehicular y gastronómicos.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Plaza Egaña (Larraín con Av. Ossa)": {"flujo": 120000},
                        "Irarrázaval con Pedro de Valdivia": {"flujo": 85000}
                    }
                },
                "Vitacura": {
                    "res": 95000, "flot": 110000,
                    "contexto": "Polo de alta renta con vitrina premium en Av. Vitacura y Américo Vespucio.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. Vitacura con Américo Vespucio": {"flujo": 95000}
                    }
                }
            }
        },
        "Sector Sur": {
            "res_sector": 1400000, "flot_sector": 300000,
            "comunas": {
                "San Joaquín": {
                    "res": 103000, "flot": 65000,
                    "contexto": "Nudo estratégico con alta densidad comercial (Mall Florida Center) y conectividad con Metro Línea 5.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Vicuña Mackenna con Departamental (Eje Metro Pedrero / Mall Florida Center)": {"flujo": 95000},
                        "Santa Rosa con Departamental": {"flujo": 75000},
                        "Vicuña Mackenna con Carlos Valdovinos": {"flujo": 60000}
                    }
                },
                "San Miguel": {
                    "res": 140000, "flot": 70000,
                    "contexto": "Eje comercial estructurante de Gran Avenida con alto tráfico vehicular, hospitales y comercio comunal.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Gran Avenida con Departamental": {"flujo": 85000},
                        "Gran Avenida con Salesianos": {"flujo": 65000}
                    }
                },
                "La Cisterna": {
                    "res": 100000, "flot": 120000,
                    "contexto": "Principal polo de trasbordo del sector sur que conecta Gran Avenida con Américo Vespucio.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Intermodal La Cisterna (Américo Vespucio con Gran Avenida)": {"flujo": 140000}
                    }
                },
                "San Bernardo": {
                    "res": 335000, "flot": 50000,
                    "contexto": "Polo sur de gran tamaño con alto tráfico en torno a la Plaza de Armas y estación Tren Central.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Plaza de Armas / Estación Tren Central": {"flujo": 55000}
                    }
                }
            }
        },
        "Sector Sur-Oriente": {
            "res_sector": 1420000, "flot_sector": 250000,
            "comunas": {
                "Peñalolén / Macul (Eje Quilín)": {
                    "res": 280000, "flot": 90000,
                    "contexto": "Punto neurálgico de Vespucio Sur con gran afluencia hacia centros médicos y Mall Paseo Quilín.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Rotonda Quilín / Américo Vespucio (Mall Paseo Quilín)": {"flujo": 130000}
                    }
                },
                "La Florida": {
                    "res": 400000, "flot": 110000,
                    "contexto": "Gran polo comercial del suroriente con concurrencia masiva en torno a malls y estaciones de metro.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Vicuña Mackenna con Américo Vespucio (Mall Plaza Vespucio)": {"flujo": 170000}
                    }
                },
                "Puente Alto": {
                    "res": 650000, "flot": 60000,
                    "contexto": "La comuna más poblada del país con flujo masivo diario por el eje Concha y Toro.",
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
                    "contexto": "El epicentro financiero, comercial y de servicios del país, con la mayor concentración flotante diaria de Chile.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Alameda con Paseo Ahumada / Metro U. de Chile": {"flujo": 220000},
                        "Alameda con Santa Rosa": {"flujo": 140000}
                    }
                }
            }
        },
        "Sector Poniente": {
            "res_sector": 1600000, "flot_sector": 550000,
            "comunas": {
                "Maipú": {
                    "res": 580000, "flot": 80000,
                    "contexto": "Gran polo del poniente con concentración en Plaza de Maipú y el eje comercial Pajaritos.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Plaza de Maipú (Pajaritos con 5 de Abril)": {"flujo": 130000},
                        "Pajaritos con Américo Vespucio (Mall Arauco Maipú)": {"flujo": 120000}
                    }
                },
                "Estación Central": {
                    "res": 210000, "flot": 350000,
                    "contexto": "Nodo de transporte interurbano con terminales de buses y estación de trenes sobre eje Alameda.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Alameda frente a Terminales de Buses": {"flujo": 180000}
                    }
                },
                "Pudahuel": {
                    "res": 255000, "flot": 120000,
                    "contexto": "Puerta de entrada logística e internacional por conectividad con el Aeropuerto de Santiago.",
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
                    "contexto": "Polo empresarial y tecnológico con alto tráfico corporativo en Ciudad Empresarial.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Ciudad Empresarial (Av. del Parque)": {"flujo": 110000}
                    }
                },
                "Quilicura": {
                    "res": 260000, "flot": 90000,
                    "contexto": "Gran polo industrial y logístico con conexión hacia Panamericana Norte.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Américo Vespucio Norte con Panamericana": {"flujo": 115000}
                    }
                },
                "Independencia / Recoleta": {
                    "res": 310000, "flot": 180000,
                    "contexto": "Sector de alta concurrencia por el polo hospitalario, Vega Central y Patronato.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. Independencia con Santos Dumont": {"flujo": 95000},
                        "Av. Recoleta con Av. La Paz (La Vega)": {"flujo": 130000}
                    }
                }
            }
        }
    },
    "Región de O'Higgins": {
        "Rancagua y Alrededores": {
            "res_sector": 400000, "flot_sector": 70000,
            "comunas": {
                "Rancagua": {
                    "res": 260000, "flot": 50000,
                    "contexto": "Capital regional con intensa actividad minera, agrícola y comercial en torno al eje Alameda.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. Bernardo O'Higgins (Alameda) con Freire": {"flujo": 75000}
                    }
                },
                "Machalí": {
                    "res": 60000, "flot": 15000,
                    "contexto": "Zona residencial de alto crecimiento con flujo pendular diario por Av. San Juan hacia Rancagua.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. San Juan": {"flujo": 40000}
                    }
                },
                "San Fernando": {
                    "res": 80000, "flot": 15000,
                    "contexto": "Centro comercial y de distribución del Valle de Colchagua.",
                    "puntos": {
                        "Toda la comuna (General)": None
                    }
                }
            }
        }
    },
    "Región del Maule": {
        "Talca - Curicó - Linares": {
            "res_sector": 650000, "flot_sector": 90000,
            "comunas": {
                "Talca": {
                    "res": 235000, "flot": 45000,
                    "contexto": "Capital regional y universitaria con alto flujo comercial por 1 Sur y Av. San Miguel.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. San Miguel con Mall Plaza Maule": {"flujo": 70000},
                        "1 Sur con 5 Oriente (Paseo Peatonal)": {"flujo": 55000}
                    }
                },
                "Curicó": {
                    "res": 165000, "flot": 25000,
                    "contexto": "Polo agroindustrial con alta concurrencia en eje Camilo Henríquez.",
                    "puntos": {
                        "Toda la comuna (General)": None
                    }
                },
                "Linares": {
                    "res": 100000, "flot": 15000,
                    "contexto": "Centro de servicios agrícolas de la cuenca sur del Maule.",
                    "puntos": {
                        "Toda la comuna (General)": None
                    }
                }
            }
        }
    },
    "Región de Ñuble": {
        "Chillán Urbano": {
            "res_sector": 250000, "flot_sector": 40000,
            "comunas": {
                "Chillán": {
                    "res": 195000, "flot": 35000,
                    "contexto": "Capital regional con flujo continuo en torno a la plaza de armas, mercado y Av. O'Higgins.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. O'Higgins con Av. Ecuador": {"flujo": 60000}
                    }
                },
                "Chillán Viejo": {
                    "res": 35000, "flot": 8000,
                    "contexto": "Acceso sur de la conurbación con fuerte movimiento vehicular e histórico.",
                    "puntos": {
                        "Toda la comuna (General)": None
                    }
                }
            }
        }
    },
    "Región del Biobío": {
        "Gran Concepción": {
            "res_sector": 1050000, "flot_sector": 220000,
            "comunas": {
                "Concepción": {
                    "res": 240000, "flot": 160000,
                    "contexto": "Segundo polo económico y universitario del país, con flujo intenso en el eje O'Higgins, Carrera y Mall del Centro.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. O'Higgins con Aníbal Pinto (Plaza Independencia)": {"flujo": 120000},
                        "Av. Los Carrera con Paicaví": {"flujo": 95000}
                    }
                },
                "Talcahuano": {
                    "res": 160000, "flot": 50000,
                    "contexto": "Polo portuario e industrial con tránsito masivo en torno a Mall Plaza Trébol y autopista.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Autopista Concepción-Talcahuano frente a Mall Plaza": {"flujo": 110000}
                    }
                },
                "San Pedro de la Paz": {
                    "res": 145000, "flot": 30000,
                    "contexto": "Paso obligado del tránsito hacia la costa sur y ruta de la madera.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Ruta 160 con Puente Llacolén": {"flujo": 80000}
                    }
                },
                "Los Ángeles": {
                    "res": 220000, "flot": 40000,
                    "contexto": "Capital del sector forestal e industrial de la provincia con alta actividad en el centro.",
                    "puntos": {
                        "Toda la comuna (General)": None
                    }
                }
            }
        }
    },
    "Región de La Araucanía": {
        "Gran Temuco": {
            "res_sector": 450000, "flot_sector": 75000,
            "comunas": {
                "Temuco": {
                    "res": 310000, "flot": 65000,
                    "contexto": "Principal polo comercial, de salud y universitario del sur con alta densidad en Av. Alemania y Caupolicán.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. Alemania con Mall Portal Temuco": {"flujo": 90000},
                        "Av. Caupolicán con Manuel Montt": {"flujo": 75000}
                    }
                },
                "Padre Las Casas": {
                    "res": 90000, "flot": 15000,
                    "contexto": "Conurbación conectada por los puentes Cautín y Treng Treng Kay Kay.",
                    "puntos": {
                        "Toda la comuna (General)": None
                    }
                },
                "Villarrica / Pucón": {
                    "res": 105000, "flot": 50000,
                    "contexto": "Polo turístico lacustre con altísima saturación y tráfico vehicular durante temporada alta.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Camino Villarrica - Pucón": {"flujo": 45000}
                    }
                }
            }
        }
    },
    "Región de Los Ríos": {
        "Valdivia Urbano": {
            "res_sector": 210000, "flot_sector": 40000,
            "comunas": {
                "Valdivia": {
                    "res": 180000, "flot": 35000,
                    "contexto": "Polo turístico, fluvial y cervecero con paso obligado por los puentes Pedro de Valdivia y Calle-Calle.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. Ramón Picarte con Plaza de la República": {"flujo": 60000},
                        "Acceso Puente Pedro de Valdivia (Isla Teja)": {"flujo": 45000}
                    }
                }
            }
        }
    },
    "Región de Los Lagos": {
        "Puerto Montt - Osorno": {
            "res_sector": 550000, "flot_sector": 85000,
            "comunas": {
                "Puerto Montt": {
                    "res": 260000, "flot": 50000,
                    "contexto": "Capital de la industria acuícola y punto neurálgico de conexión hacia la Carretera Austral.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. Diego Portales (Costanera frente al Mall)": {"flujo": 80000}
                    }
                },
                "Puerto Varas": {
                    "res": 55000, "flot": 25000,
                    "contexto": "Zona residencial y de turismo premium con alta afluencia por costanera Vicente Pérez Rosales.",
                    "puntos": {
                        "Toda la comuna (General)": None
                    }
                },
                "Osorno": {
                    "res": 175000, "flot": 30000,
                    "contexto": "Polo lechero y ganadero con alta actividad en el eje Mackenna y Plaza de Armas.",
                    "puntos": {
                        "Toda la comuna (General)": None
                    }
                },
                "Castro (Chiloé)": {
                    "res": 55000, "flot": 20000,
                    "contexto": "Cabecera del archipiélago con circulación en torno a la plaza y el bypass.",
                    "puntos": {
                        "Toda la comuna (General)": None
                    }
                }
            }
        }
    },
    "Región de Aysén": {
        "Coyhaique Urbano": {
            "res_sector": 80000, "flot_sector": 15000,
            "comunas": {
                "Coyhaique": {
                    "res": 65000, "flot": 15000,
                    "contexto": "Centro de servicios de la Patagonia chilena centrado en torno a su plaza pentagonal y Av. Baquedano.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. Baquedano con Plaza de Armas": {"flujo": 30000}
                    }
                }
            }
        }
    },
    "Región de Magallanes y de la Antártica Chilena": {
        "Punta Arenas Urbano": {
            "res_sector": 150000, "flot_sector": 25000,
            "comunas": {
                "Punta Arenas": {
                    "res": 140000, "flot": 25000,
                    "contexto": "Polo austral del país con tráfico comercial en torno a la Costanera del Estrecho y Zona Franca.",
                    "puntos": {
                        "Toda la comuna (General)": None,
                        "Av. Costanera con Av. Colón": {"flujo": 45000},
                        "Acceso Zona Franca": {"flujo": 40000}
                    }
                }
            }
        }
    }
}

# --- 6. FORMATOS COMERCIALES (OOH & METRO) ---
FORMATOS_OOH = {
    "Building Wrap (Edificio)": {
        "base": 1, "c": 0.25, "m": 0.30, "o": 0.35, "tipo": "Gran impacto edificio", "unidad": "edificios",
        "es_wrap": True,
        "contexto": "Gigantografía de escala monumental sobre fachada de edificio (>400-500 m²), con visualización a larga distancia y cono visual abierto sobre avenidas estructurantes."
    },
    "Pantalla Digital (DOOH)": {"base": 1, "c": 0.20, "m": 0.25, "o": 0.30, "tipo": "Gran impacto LED", "unidad": "pantallas", "es_wrap": False},
    "Lunetas Buses": {"base": 30, "c": 0.20, "m": 0.25, "o": 0.30, "tipo": "Cobertura móvil", "unidad": "lunetas", "es_wrap": False},
    "Buses Troncales": {"base": 70, "c": 0.30, "m": 0.35, "o": 0.40, "tipo": "Troncal móvil", "unidad": "buses", "es_wrap": False},
    "Valla Estática": {"base": 1, "c": 0.15, "m": 0.20, "o": 0.25, "tipo": "Soporte fijo", "unidad": "soportes", "es_wrap": False}
}

FORMATOS_METRO = {
    "Muro Estación (Gran Formato)": {
        "base": 1, "c": 0.35, "m": 0.45, "o": 0.55, "tipo": "Dominación muro", "unidad": "muros", "es_tren": False,
        "contexto": "Brandeo de muro completo en andén o pasillo de trasbordo con cobertura total de superficie, alto impacto visual y máxima permanencia en espera."
    },
    "Brandeo Tren Integral (Línea 1 - 27 Estaciones)": {
        "base": 1, "c": 0.22, "m": 0.27, "o": 0.32, "tipo": "Tren completo", "unidad": "trenes", "es_tren": True, "flujo_red_dia": 850000,
        "contexto": "Tren completo en circulación continua de San Pablo a Los Dominicos impactando andenes de 27 estaciones más usuarios en viaje."
    },
    "Circuito Pantallas Digitales Andén (DOOH)": {
        "base": 1, "c": 0.30, "m": 0.40, "o": 0.50, "tipo": "DOOH Andén", "unidad": "circuitos", "es_tren": False,
        "contexto": "Pantallas frente a los usuarios en tiempo de espera cautiva en andén, con alto recuerdo de marca."
    },
    "Valla / Panel Andén Estático": {
        "base": 1, "c": 0.25, "m": 0.35, "o": 0.45, "tipo": "Panel Andén", "unidad": "paneles", "es_tren": False,
        "contexto": "Panel publicitario de gran formato ubicado frente a las vías de abordaje."
    },
    "Panel Acceso / Torniquetes": {
        "base": 1, "c": 0.35, "m": 0.45, "o": 0.55, "tipo": "Panel Mesanina", "unidad": "paneles", "es_tren": False,
        "contexto": "Impacto forzado al paso en torniquetes y accesos principales a la estación."
    }
}

# --- 7. BARRA LATERAL: LOGO MADCOM Y CONFIGURACIÓN ---
st.sidebar.markdown("### 🏢 Agencia")
logo_preview = generar_logo_madcom(fondo_oscuro=True)
st.sidebar.image(logo_preview, width=170)

st.sidebar.markdown("---")
st.sidebar.header("🎨 Diseño de la Lámina")
modo_fondo = st.sidebar.radio("Estilo de Fondo:", ["Fondo Claro (Blanco)", "Fondo Oscuro"])
color_acento_nombre = st.sidebar.selectbox("Color de Acento / Cliente:", list(COLORES_BASE.keys()))
color_acento = COLORES_BASE[color_acento_nombre]

if modo_fondo == "Fondo Claro (Blanco)":
    c_bg = "#FFFFFF"
    c_card = "#F8F9FA"
    c_border = "#E2E8F0"
    c_text_primary = "#1A202C"
    c_text_muted = "#64748B"
    c_accent = color_acento
    c_card_highlight_bg = color_acento
    c_card_highlight_text = "#FFFFFF" if color_acento_nombre in ["Negro Corporativo", "Azul Intenso", "Rojo Retail", "Azul Marino"] else "#000000"
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
st.sidebar.header("⚙️ Configuración Territorial & Medios")
medio_tipo = st.sidebar.radio("Selecciona Entorno:", ["Vía Pública Tradicional (Calles)", "Metro de Santiago (Estaciones y Trenes)"])

ancho_wrap = 0
alto_wrap = 0
superficie_wrap = 0

if medio_tipo == "Metro de Santiago (Estaciones y Trenes)":
    formato_dict = FORMATOS_METRO
    formato_sel = st.sidebar.selectbox("Formato en Metro:", list(formato_dict.keys()))
    info_f = formato_dict[formato_sel]
    fuente_medicion_pie = "Medición Oficial de Audiencias: Metro de Santiago e Ipsos."
    
    if info_f.get("es_tren", False):
        universo_calculo = info_f["flujo_red_dia"]
        nombre_territorio = "Línea 1 Completa"
        nombre_titulo_lamina = "LÍNEA 1"
        texto_estrategico_default = info_f["contexto"]
    else:
        linea_sel = st.sidebar.selectbox("Línea de Metro:", list(METRO_DATA.keys()))
        estacion_sel = st.sidebar.selectbox("Estación:", list(METRO_DATA[linea_sel].keys()))
        datos_estacion = METRO_DATA[linea_sel][estacion_sel]
        universo_calculo = datos_estacion["alcance_dia"]
        nombre_territorio = f"Metro {linea_sel} - {estacion_sel}"
        nombre_titulo_lamina = f"ESTACIÓN {estacion_sel.upper()}"
        if "Muro" in formato_sel:
            texto_estrategico_default = f"Muro completo en Estación {estacion_sel} ({datos_estacion['flujo_mes']:,.0f} pasajeros mensuales Ipsos), entregando máxima superficie y dominación de andén.".replace(",", ".")
        else:
            texto_estrategico_default = f"Estación {estacion_sel} registra {datos_estacion['flujo_mes']:,.0f} pasajeros mensuales (Ipsos), con tiempo de espera cautivo de alta exposición.".replace(",", ".")
else:
    fuente_medicion_pie = "Medición Oficial de Audiencias: INE Chile · EOD / SECTRA / MTT · UOCT / MOP."
    reg_sel = st.sidebar.selectbox("1. Región:", list(DATA_JERARQUICA.keys()))
    sec_sel = st.sidebar.selectbox("2. Sector / Zona:", list(DATA_JERARQUICA[reg_sel].keys()))
    datos_sec = DATA_JERARQUICA[reg_sel][sec_sel]
    
    opciones_comuna = ["Todo el Sector en conjunto"] + list(datos_sec["comunas"].keys())
    com_sel = st.sidebar.selectbox("3. Comuna:", opciones_comuna)
    
    if com_sel == "Todo el Sector en conjunto":
        universo_calculo = datos_sec["res_sector"] + datos_sec["flot_sector"]
        nombre_territorio = f"{sec_sel}"
        nombre_titulo_lamina = sec_sel.split("(")[0].strip().upper()
        texto_estrategico_default = f"Macrozona con un flujo activo superior a {universo_calculo:,.0f} personas al día.".replace(",", ".")
    else:
        com_data = datos_sec["comunas"][com_sel]
        puntos_comuna = list(com_data.get("puntos", {}).keys())
        if not puntos_comuna:
            puntos_comuna = ["Toda la comuna (General)"]
            
        puntos_disponibles = puntos_comuna + ["➕ Otro punto específico (Personalizado)"]
        pto_sel = st.sidebar.selectbox("4. Georreferencia / Punto:", puntos_disponibles)
        nombre_titulo_lamina = com_sel.split("/")[0].strip().upper()
        
        if pto_sel == "Toda la comuna (General)":
            universo_calculo = com_data["res"] + com_data["flot"]
            nombre_territorio = com_sel
            texto_estrategico_default = com_data.get("contexto", "Cobertura continua sobre residentes y población flotante.")
        elif pto_sel == "➕ Otro punto específico (Personalizado)":
            punto_custom_nombre = st.sidebar.text_input("Nombre del Punto / Intersección:", "Ej: Vicuña Mackenna con Departamental")
            universo_calculo = st.sidebar.number_input("Flujo Activo Diario Estimado (Vehículos + Peatones):", min_value=5000, value=85000, step=5000)
            nombre_territorio = f"{com_sel} - {punto_custom_nombre}"
            texto_estrategico_default = f"Punto comercial y vial de alta afluencia con un flujo estimado de {universo_calculo:,.0f} personas al día.".replace(",", ".")
        else:
            universo_calculo = com_data["puntos"][pto_sel]["flujo"]
            nombre_territorio = f"{com_sel} - {pto_sel}"
            texto_estrategico_default = f"Punto de alta concentración vial y comercial con un flujo auditado de {universo_calculo:,.0f} personas diarias.".replace(",", ".")

    formato_dict = FORMATOS_OOH
    formato_sel = st.sidebar.selectbox("Formato Publicitario:", list(formato_dict.keys()))
    info_f = formato_dict[formato_sel]

    # Cuadros de dimensiones para Building Wrap
    if info_f.get("es_wrap", False):
        st.sidebar.markdown("📐 **Dimensiones de la Gigantografía:**")
        col_w, col_h = st.sidebar.columns(2)
        ancho_wrap = col_w.number_input("Ancho (metros):", min_value=5.0, max_value=60.0, value=20.0, step=1.0)
        alto_wrap = col_h.number_input("Alto (metros):", min_value=5.0, max_value=80.0, value=25.0, step=1.0)
        superficie_wrap = ancho_wrap * alto_wrap
        st.sidebar.success(f"Superficie total: **{superficie_wrap:,.0f} m²** ({ancho_wrap:.0f}×{alto_wrap:.0f} m)")
        texto_estrategico_default = f"Elemento monumental de {superficie_wrap:,.0f} m² sobre edificio ({ancho_wrap:.0f}×{alto_wrap:.0f}m), con cono de visibilidad a más de 400 metros de distancia sobre arteria principal."

cant_unidades = st.sidebar.number_input(f"Cantidad de {info_f['unidad']}:", min_value=1, value=info_f["base"], step=1)
dias_campana = st.sidebar.number_input("Días de Campaña:", min_value=1, value=30, step=1)
inversion_total = st.sidebar.number_input("Inversión Total ($ CLP):", min_value=100000, value=3500000 if info_f.get("es_wrap", False) else 2500000, step=250000)

foto_soporte = st.sidebar.file_uploader("Subir foto del soporte (opcional):", type=["jpg", "png", "jpeg"])

comentario_custom = st.sidebar.text_area(
    "Ventaja Estratégica / Comentarios:",
    value=texto_estrategico_default,
    height=100
)

# Cálculos del soporte actual
factor_escala = cant_unidades / info_f["base"]
costo_unitario = inversion_total / cant_unidades if cant_unidades > 0 else 0
imp_diarios_c = universo_calculo * info_f["c"] * factor_escala
imp_diarios_m = universo_calculo * info_f["m"] * factor_escala
imp_diarios_o = universo_calculo * info_f["o"] * factor_escala

imp_totales_c = imp_diarios_c * dias_campana
imp_totales_m = imp_diarios_m * dias_campana
imp_totales_o = imp_diarios_o * dias_campana

costo_impacto_m = inversion_total / imp_totales_m if imp_totales_m > 0 else 0
cpm_m = (inversion_total / imp_totales_m * 1000) if imp_totales_m > 0 else 0

tabla_esc = [
    {"esc": "Conservador", "rate": info_f["c"], "dia": imp_diarios_c, "tot": imp_totales_c},
    {"esc": "Medio", "rate": info_f["m"], "dia": imp_diarios_m, "tot": imp_totales_m},
    {"esc": "Optimista", "rate": info_f["o"], "dia": imp_diarios_o, "tot": imp_totales_o}
]

# Etiqueta para el mix
if info_f.get("es_wrap", False):
    soporte_mix_nombre = f"Building Wrap ({superficie_wrap:,.0f} m²)"
else:
    soporte_mix_nombre = f"{formato_sel} ({cant_unidades} {info_f['unidad']})"

# Botones de agregar al plan
st.sidebar.markdown("---")
if st.sidebar.button("➕ Agregar este elemento al Plan de Medios", use_container_width=True, type="primary"):
    st.session_state.plan_items.append({
        "Soporte": soporte_mix_nombre,
        "Ubicación": nombre_territorio,
        "Días": dias_campana,
        "Inversión Neta": inversion_total,
        "Impactos Conservador": int(imp_totales_c),
        "Impactos Medio": int(imp_totales_m),
        "Impactos Optimista": int(imp_totales_o),
        "CPM Medio": cpm_m,
        "Entorno": medio_tipo
    })
    st.sidebar.success("¡Elemento agregado al Plan de Medios!")

if st.sidebar.button("🗑️ Limpiar Plan de Medios", use_container_width=True):
    st.session_state.plan_items = []
    st.rerun()

# --- 8. RENDERIZADOR PIL: LÁMINA INDIVIDUAL (CON FOTO) ---
def render_lamina_jpg():
    W, H = 1920, 1080
    im = Image.new("RGB", (W, H), c_bg)
    draw = ImageDraw.Draw(im)

    f_sub = obtener_fuente(24, bold=False)
    f_num_big = obtener_fuente(42, bold=True)
    f_label = obtener_fuente(22, bold=False)
    f_table_head = obtener_fuente(20, bold=True)
    f_table_row = obtener_fuente(22, bold=False)
    f_comment_title = obtener_fuente(22, bold=True)
    f_comment_body = obtener_fuente(20, bold=False)
    f_footer = obtener_fuente(18, bold=False)

    # 1. Cabecera (Título conciso con auto-escalado anti-solapamiento)
    title_text = f"{nombre_titulo_lamina} - {formato_sel.upper()}"
    
    if info_f.get("es_wrap", False):
        subtitle_text = f"{superficie_wrap:,.0f} m² ({ancho_wrap:.0f}×{alto_wrap:.0f}m) · {dias_campana} días"
    else:
        subtitle_text = f"{cant_unidades} {info_f['unidad']} · {dias_campana} días"
    
    max_title_w = W - 520
    t_size = 42
    f_title = obtener_fuente(t_size, bold=True)
    
    while t_size > 22:
        bbox_t = draw.textbbox((0, 0), title_text, font=f_title)
        if (bbox_t[2] - bbox_t[0]) <= max_title_w:
            break
        t_size -= 2
        f_title = obtener_fuente(t_size, bold=True)

    draw.text((60, 48), title_text, fill=c_accent, font=f_title)
    draw.text((W - 440, 58), subtitle_text, fill=c_text_muted, font=f_sub)
    draw.line([(60, 115), (W - 60, 115)], fill=c_accent, width=3)

    # 2. Recuadro Foto Soporte
    foto_box = [(60, 145), (710, 960)]
    if foto_soporte is not None:
        try:
            uploaded_img = Image.open(foto_soporte).convert("RGB")
            uploaded_img = uploaded_img.resize((650, 815))
            im.paste(uploaded_img, (60, 145))
        except Exception:
            draw.rectangle(foto_box, fill=c_card, outline=c_border, width=2)
    else:
        draw.rectangle(foto_box, fill=c_card, outline=c_border, width=2)
        draw.text((230, 530), "[ FOTO SOPORTE ]", fill=c_text_muted, font=f_sub)

    # 3. Tarjetas Superiores
    card_w, card_h = 360, 130
    x_offset = 750
    
    # Inversión
    draw.rounded_rectangle([(x_offset, 145), (x_offset + card_w, 145 + card_h)], radius=12, fill=c_card, outline=c_border, width=1)
    draw.text((x_offset + 25, 165), "Inversión mensual", fill=c_text_muted, font=f_label)
    draw.text((x_offset + 25, 202), f"${inversion_total:,.0f}".replace(",", "."), fill=c_text_primary, font=f_num_big)

    # Costo Unitario / m2
    draw.rounded_rectangle([(x_offset + card_w + 30, 145), (x_offset + card_w*2 + 30, 145 + card_h)], radius=12, fill=c_card, outline=c_border, width=1)
    if info_f.get("es_wrap", False):
        costo_m2 = inversion_total / superficie_wrap if superficie_wrap > 0 else 0
        draw.text((x_offset + card_w + 55, 165), "Costo por m² / mes", fill=c_text_muted, font=f_label)
        draw.text((x_offset + card_w + 55, 202), f"${costo_m2:,.0f}".replace(",", "."), fill=c_text_primary, font=f_num_big)
    else:
        draw.text((x_offset + card_w + 55, 165), f"Costo por {info_f['unidad'][:-1]} / mes", fill=c_text_muted, font=f_label)
        draw.text((x_offset + card_w + 55, 202), f"${costo_unitario:,.0f}".replace(",", "."), fill=c_text_primary, font=f_num_big)

    # Impactos Totales
    draw.rounded_rectangle([(x_offset + card_w*2 + 60, 145), (x_offset + card_w*3 + 60, 145 + card_h)], radius=12, fill=c_card_highlight_bg)
    draw.text((x_offset + card_w*2 + 85, 165), f"Impactos {dias_campana} días (caso medio)", fill=c_card_highlight_text, font=f_label)
    draw.text((x_offset + card_w*2 + 85, 202), f"{imp_totales_m:,.0f}".replace(",", "."), fill=c_card_highlight_text, font=f_num_big)

    # 4. Tabla de Escenarios
    t_y = 315
    draw.text((x_offset + 20, t_y), "Escenario", fill=c_text_muted, font=f_table_head)
    draw.text((x_offset + 270, t_y), "% Exposición diaria", fill=c_text_muted, font=f_table_head)
    draw.text((x_offset + 520, t_y), "Contactos diarios", fill=c_text_muted, font=f_table_head)
    draw.text((x_offset + 750, t_y), f"Impactos {dias_campana} días", fill=c_text_muted, font=f_table_head)
    draw.text((x_offset + 980, t_y), "CPM Efectivo", fill=c_text_muted, font=f_table_head)
    draw.line([(x_offset + 20, t_y + 35), (W - 60, t_y + 35)], fill=c_border, width=2)

    row_y = t_y + 55
    for item in tabla_esc:
        is_medio = item["esc"] == "Medio"
        c_fill = c_accent if is_medio else c_text_primary
        cpm_val = (inversion_total / item["tot"] * 1000) if item["tot"] > 0 else 0
        
        draw.text((x_offset + 20, row_y), item["esc"], fill=c_fill, font=obtener_fuente(22, bold=is_medio))
        draw.text((x_offset + 300, row_y), f"{int(item['rate']*100)}%", fill=c_text_primary, font=f_table_row)
        draw.text((x_offset + 520, row_y), f"{int(item['dia']):,}".replace(",", "."), fill=c_text_primary, font=f_table_row)
        draw.text((x_offset + 750, row_y), f"{int(item['tot']):,}".replace(",", "."), fill=c_text_primary, font=f_table_row)
        draw.text((x_offset + 980, row_y), f"${int(round(cpm_val)):,}".replace(",", "."), fill=c_text_primary, font=f_table_row)
        row_y += 45

    # 5. Tarjetas Inferiores
    b_y = 505
    # Universo activo
    draw.rounded_rectangle([(x_offset, b_y), (x_offset + card_w, b_y + card_h)], radius=12, fill=c_card, outline=c_border, width=1)
    draw.text((x_offset + 25, b_y + 20), "Universo activo diario", fill=c_text_muted, font=f_label)
    draw.text((x_offset + 25, b_y + 55), f"{universo_calculo:,.0f}".replace(",", "."), fill=c_accent, font=f_num_big)

    # Costo x impacto
    draw.rounded_rectangle([(x_offset + card_w + 30, b_y), (x_offset + card_w*2 + 30, b_y + card_h)], radius=12, fill=c_card, outline=c_border, width=1)
    draw.text((x_offset + card_w + 55, b_y + 20), "Costo x impacto (medio)", fill=c_text_muted, font=f_label)
    draw.text((x_offset + card_w + 55, b_y + 55), f"${costo_impacto_m:.1f} CLP", fill=c_accent, font=f_num_big)

    # Naturaleza del formato con ajuste en dos líneas
    card3_x = x_offset + card_w*2 + 60
    draw.rounded_rectangle([(card3_x, b_y), (card3_x + card_w, b_y + card_h)], radius=12, fill=c_card, outline=c_border, width=1)
    draw.text((card3_x + 25, b_y + 20), "Naturaleza del formato", fill=c_text_muted, font=f_label)
    
    texto_naturaleza = info_f["tipo"]
    f_nat_test = obtener_fuente(32, bold=True)
    bbox_nat = draw.textbbox((0, 0), texto_naturaleza, font=f_nat_test)
    ancho_nat = bbox_nat[2] - bbox_nat[0]
    
    if ancho_nat <= 300:
        draw.text((card3_x + 25, b_y + 55), texto_naturaleza, fill=c_accent, font=f_nat_test)
    else:
        partes = texto_naturaleza.split()
        if len(partes) >= 2:
            linea1 = partes[0]
            linea2 = " ".join(partes[1:])
        else:
            linea1 = texto_naturaleza
            linea2 = ""
        f_nat_dos_lineas = obtener_fuente(26, bold=True)
        draw.text((card3_x + 25, b_y + 50), linea1, fill=c_accent, font=f_nat_dos_lineas)
        if linea2:
            draw.text((card3_x + 25, b_y + 82), linea2, fill=c_accent, font=f_nat_dos_lineas)

    # 6. Comentarios Estratégicos
    com_y = 675
    draw.rounded_rectangle([(x_offset, com_y), (W - 60, 960)], radius=12, fill=c_card, outline=c_border, width=1)
    draw.line([(x_offset, com_y), (x_offset, 960)], fill=c_accent, width=6)
    
    draw.text((x_offset + 30, com_y + 22), f"Universo / Flujo diario base: {universo_calculo:,.0f} personas activas".replace(",", "."), fill=c_text_primary, font=f_label)
    draw.text((x_offset + 30, com_y + 65), "VENTAJA ESTRATÉGICA DEL FORMATO", fill=c_accent, font=f_comment_title)
    
    words = comentario_custom.split()
    lines, current_line = [], ""
    for w in words:
        if len(current_line + " " + w) < 85:
            current_line += " " + w
        else:
            lines.append(current_line.strip())
            current_line = w
    if current_line:
        lines.append(current_line.strip())
        
    line_y = com_y + 105
    for l in lines[:4]:
        draw.text((x_offset + 30, line_y), l, fill=c_text_muted, font=f_comment_body)
        line_y += 32

    # 7. Pie de Página: Acreditación de Fuentes Técnicas en la Esquina Inferior Izquierda
    draw.text((60, 1005), fuente_medicion_pie, fill=c_text_muted, font=f_footer)

    # Estampar el logo MADCOM exclusivamente en la esquina inferior derecha
    try:
        logo_to_stamp = generar_logo_madcom(fondo_oscuro=(modo_fondo == "Fondo Oscuro"))
        logo_to_stamp.thumbnail((190, 48), Image.Resampling.LANCZOS)
        im.paste(logo_to_stamp, (W - 60 - logo_to_stamp.width, 995), logo_to_stamp)
    except Exception:
        pass

    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=95)
    return buf.getvalue()


# --- 9. RENDERIZADOR PIL: LÁMINA CONSOLIDADA (MIX COMPLETO - PANORÁMICA SIN FOTO) ---
def render_lamina_consolidada_jpg():
    W, H = 1920, 1080
    im = Image.new("RGB", (W, H), c_bg)
    draw = ImageDraw.Draw(im)

    f_title = obtener_fuente(42, bold=True)
    f_sub = obtener_fuente(24, bold=False)
    f_label = obtener_fuente(22, bold=False)
    f_table_head = obtener_fuente(20, bold=True)
    f_table_row = obtener_fuente(20, bold=False)
    f_sec_title = obtener_fuente(24, bold=True)
    f_footer = obtener_fuente(18, bold=False)

    num_items = len(st.session_state.plan_items)
    total_inversion = sum(item["Inversión Neta"] for item in st.session_state.plan_items)
    total_imp_c = sum(item["Impactos Conservador"] for item in st.session_state.plan_items)
    total_imp_m = sum(item["Impactos Medio"] for item in st.session_state.plan_items)
    total_imp_o = sum(item["Impactos Optimista"] for item in st.session_state.plan_items)
    cpm_global_m = (total_inversion / total_imp_m * 1000) if total_imp_m > 0 else 0
    cpm_global_c = (total_inversion / total_imp_c * 1000) if total_imp_c > 0 else 0
    cpm_global_o = (total_inversion / total_imp_o * 1000) if total_imp_o > 0 else 0

    # Fuentes técnicas presentes en el plan
    tiene_metro = any(item.get("Entorno") == "Metro de Santiago (Estaciones y Trenes)" for item in st.session_state.plan_items)
    tiene_ooh = any(item.get("Entorno") != "Metro de Santiago (Estaciones y Trenes)" for item in st.session_state.plan_items)
    if tiene_metro and tiene_ooh:
        fuente_plan_pie = "Medición Oficial: Metro de Santiago e Ipsos · INE Chile · EOD / SECTRA / MTT · UOCT / MOP."
    elif tiene_metro:
        fuente_plan_pie = "Medición Oficial de Audiencias: Metro de Santiago e Ipsos."
    else:
        fuente_plan_pie = "Medición Oficial de Audiencias: INE Chile · EOD / SECTRA / MTT · UOCT / MOP."

    # 1. Cabecera Panorámica
    draw.text((60, 48), "PLAN DE MEDIOS - RESUMEN CONSOLIDADO", fill=c_accent, font=f_title)
    draw.text((W - 520, 58), f"{num_items} soportes en el Mix · Campaña Integral", fill=c_text_muted, font=f_sub)
    draw.line([(60, 115), (W - 60, 115)], fill=c_accent, width=3)

    # 2. 4 Tarjetas Superiores Panorámicas (x=60 a 1860, ancho 1800 px)
    card_w = 425
    card_h = 130
    gap = (1800 - (card_w * 4)) // 3
    x_pos = 60

    # Tarjeta 1: Total Soportes en Mix (Ajuste conciso y auto-escalado)
    draw.rounded_rectangle([(x_pos, 145), (x_pos + card_w, 145 + card_h)], radius=12, fill=c_card, outline=c_border, width=1)
    draw.text((x_pos + 25, 165), "Total Soportes en Mix", fill=c_text_muted, font=f_label)
    
    txt_soportes = f"{num_items} soportes" if num_items != 1 else "1 soporte"
    t1_size = 42
    f_t1 = obtener_fuente(t1_size, bold=True)
    while t1_size > 26:
        bbox_t1 = draw.textbbox((0, 0), txt_soportes, font=f_t1)
        if (bbox_t1[2] - bbox_t1[0]) <= (card_w - 50):
            break
        t1_size -= 2
        f_t1 = obtener_fuente(t1_size, bold=True)
    draw.text((x_pos + 25, 202), txt_soportes, fill=c_text_primary, font=f_t1)

    # Tarjeta 2: Inversión Total Neta
    x_pos += card_w + gap
    draw.rounded_rectangle([(x_pos, 145), (x_pos + card_w, 145 + card_h)], radius=12, fill=c_card, outline=c_border, width=1)
    draw.text((x_pos + 25, 165), "Inversión Total Neta", fill=c_text_muted, font=f_label)
    draw.text((x_pos + 25, 202), f"${total_inversion:,.0f}".replace(",", "."), fill=c_text_primary, font=obtener_fuente(42, bold=True))

    # Tarjeta 3: Impactos Totales (Destacada)
    x_pos += card_w + gap
    draw.rounded_rectangle([(x_pos, 145), (x_pos + card_w, 145 + card_h)], radius=12, fill=c_card_highlight_bg)
    draw.text((x_pos + 25, 165), "Impactos Brutos (Caso Medio)", fill=c_card_highlight_text, font=f_label)
    draw.text((x_pos + 25, 202), f"{total_imp_m:,.0f}".replace(",", "."), fill=c_card_highlight_text, font=obtener_fuente(42, bold=True))

    # Tarjeta 4: CPM Ponderado Global
    x_pos += card_w + gap
    draw.rounded_rectangle([(x_pos, 145), (x_pos + card_w, 145 + card_h)], radius=12, fill=c_card, outline=c_border, width=1)
    draw.text((x_pos + 25, 165), "CPM Ponderado Global", fill=c_text_muted, font=f_label)
    draw.text((x_pos + 25, 202), f"${int(round(cpm_global_m)):,}".replace(",", "."), fill=c_accent, font=obtener_fuente(42, bold=True))

    # 3. Contenedor Tabla Desglose del Mix
    t_box_y = 305
    draw.rounded_rectangle([(60, t_box_y), (W - 60, 680)], radius=12, fill=c_card, outline=c_border, width=1)
    draw.text((85, t_box_y + 20), "DESGLOSE DE SOPORTES EN EL MIX", fill=c_accent, font=f_sec_title)

    # Encabezados de la tabla de desglose
    th_y = t_box_y + 65
    draw.text((85, th_y), "Soporte", fill=c_text_muted, font=f_table_head)
    draw.text((540, th_y), "Ubicación / Territorio", fill=c_text_muted, font=f_table_head)
    draw.text((1060, th_y), "Días", fill=c_text_muted, font=f_table_head)
    draw.text((1180, th_y), "Inversión Neta", fill=c_text_muted, font=f_table_head)
    draw.text((1440, th_y), "Impactos (Medio)", fill=c_text_muted, font=f_table_head)
    draw.text((1700, th_y), "CPM Efectivo", fill=c_text_muted, font=f_table_head)
    draw.line([(85, th_y + 32), (W - 85, th_y + 32)], fill=c_border, width=1)

    # Filas de la tabla de desglose
    row_y = th_y + 45
    for item in st.session_state.plan_items[:6]:
        soporte_txt = item["Soporte"][:32] + "..." if len(item["Soporte"]) > 32 else item["Soporte"]
        ubica_txt = item["Ubicación"][:38] + "..." if len(item["Ubicación"]) > 38 else item["Ubicación"]
        inv_txt = f"${int(item['Inversión Neta']):,}".replace(",", ".")
        imp_txt = f"{int(item['Impactos Medio']):,}".replace(",", ".")
        cpm_txt = f"${int(round(item['CPM Medio'])):,}".replace(",", ".")

        draw.text((85, row_y), soporte_txt, fill=c_text_primary, font=f_table_row)
        draw.text((540, row_y), ubica_txt, fill=c_text_muted, font=f_table_row)
        draw.text((1060, row_y), f"{item['Días']}d", fill=c_text_primary, font=f_table_row)
        draw.text((1180, row_y), inv_txt, fill=c_text_primary, font=f_table_row)
        draw.text((1440, row_y), imp_txt, fill=c_text_primary, font=f_table_row)
        draw.text((1700, row_y), cpm_txt, fill=c_accent, font=f_table_row)
        row_y += 42

    # 4. Contenedor Tabla Consolidada de Escenarios Totales
    e_box_y = 705
    draw.rounded_rectangle([(60, e_box_y), (W - 60, 960)], radius=12, fill=c_card, outline=c_border, width=1)
    draw.text((85, e_box_y + 20), "CONSOLIDADO DE RENDIMIENTO GLOBAL (TODA LA CAMPAÑA)", fill=c_accent, font=f_sec_title)

    eth_y = e_box_y + 65
    draw.text((85, eth_y), "Escenario Global", fill=c_text_muted, font=f_table_head)
    draw.text((540, eth_y), "Inversión Total", fill=c_text_muted, font=f_table_head)
    draw.text((950, eth_y), "Impactos Brutos Totales", fill=c_text_muted, font=f_table_head)
    draw.text((1350, eth_y), "Costo Promedio x Impacto", fill=c_text_muted, font=f_table_head)
    draw.text((1680, eth_y), "CPM Global", fill=c_text_muted, font=f_table_head)
    draw.line([(85, eth_y + 32), (W - 85, eth_y + 32)], fill=c_border, width=1)

    esc_datos = [
        {"esc": "Conservador", "imp": total_imp_c, "cpm": cpm_global_c},
        {"esc": "Medio (Recomendado)", "imp": total_imp_m, "cpm": cpm_global_m},
        {"esc": "Optimista", "imp": total_imp_o, "cpm": cpm_global_o}
    ]

    erow_y = eth_y + 45
    for e in esc_datos:
        is_m = "Medio" in e["esc"]
        c_name = c_accent if is_m else c_text_primary
        costo_unit = (total_inversion / e["imp"]) if e["imp"] > 0 else 0
        
        draw.text((85, erow_y), e["esc"], fill=c_name, font=obtener_fuente(20, bold=is_m))
        draw.text((540, erow_y), f"${total_inversion:,.0f}".replace(",", "."), fill=c_text_primary, font=f_table_row)
        draw.text((950, erow_y), f"{e['imp']:,.0f}".replace(",", "."), fill=c_name, font=f_table_row)
        draw.text((1350, erow_y), f"${costo_unit:.2f}".replace(".", ","), fill=c_text_primary, font=f_table_row)
        draw.text((1680, erow_y), f"${int(round(e['cpm'])):,}".replace(",", "."), fill=c_name, font=f_table_row)
        erow_y += 42

    # 5. Pie de Página: Acreditación de Fuentes Técnicas e Isotipo MADCOM
    draw.text((60, 1005), fuente_plan_pie, fill=c_text_muted, font=f_footer)

    try:
        logo_to_stamp = generar_logo_madcom(fondo_oscuro=(modo_fondo == "Fondo Oscuro"))
        logo_to_stamp.thumbnail((190, 48), Image.Resampling.LANCZOS)
        im.paste(logo_to_stamp, (W - 60 - logo_to_stamp.width, 995), logo_to_stamp)
    except Exception:
        pass

    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=95)
    return buf.getvalue()


# --- 10. VISTA PRINCIPAL ---
st.title("🎯 Planificador de Medios & Exportador de Propuestas")
st.markdown("Calcula el rendimiento por soporte, diseña la lámina ejecutiva y consolida el mix total de la campaña.")

tab1, tab2 = st.tabs(["🖼️ Lámina Ejecutiva (Soporte Actual)", "📊 Plan de Medios Consolidado (Mix Completo)"])

with tab1:
    img_bytes = render_lamina_jpg()
    st.image(img_bytes, caption=f"Vista previa — {nombre_territorio} ({modo_fondo} / {color_acento_nombre})", use_container_width=True)
    
    col_d1, col_d2 = st.columns([1, 3])
    with col_d1:
        st.download_button(
            label="📥 Descargar Lámina en JPG (Alta Calidad)",
            data=img_bytes,
            file_name=f"propuesta_{nombre_titulo_lamina.lower()}_{formato_sel.lower().replace(' ', '_')}.jpg",
            mime="image/jpeg",
            type="primary",
            use_container_width=True
        )

with tab2:
    if len(st.session_state.plan_items) == 0:
        st.info("👈 Configura los parámetros en el menú lateral y haz clic en **'➕ Agregar este elemento al Plan de Medios'** para sumar soportes a la campaña consolidada.")
    else:
        st.subheader("🖼️ Vista Previa de la Lámina Resumen Consolidada (Mix Completo)")
        
        img_consolidada_bytes = render_lamina_consolidada_jpg()
        st.image(img_consolidada_bytes, caption=f"Lámina Consolidada — Campaña Multi-Soporte ({len(st.session_state.plan_items)} elementos)", use_container_width=True)
        
        col_c1, col_c2 = st.columns([1, 3])
        with col_c1:
            st.download_button(
                label="📥 Descargar Lámina Consolidada en JPG",
                data=img_consolidada_bytes,
                file_name="propuesta_consolidada_plan_de_medios.jpg",
                mime="image/jpeg",
                type="primary",
                use_container_width=True
            )

        st.markdown("---")
        st.subheader(f"📋 1. Desglose del Mix ({len(st.session_state.plan_items)} soportes contratados)")
        
        df_items = pd.DataFrame(st.session_state.plan_items)
        df_display = df_items.copy()
        df_display["Inversión Neta"] = df_display["Inversión Neta"].apply(lambda x: f"${int(x):,}".replace(",", "."))
        df_display["Impactos Conservador"] = df_display["Impactos Conservador"].apply(lambda x: f"{int(x):,}".replace(",", "."))
        df_display["Impactos Medio"] = df_display["Impactos Medio"].apply(lambda x: f"{int(x):,}".replace(",", "."))
        df_display["Impactos Optimista"] = df_display["Impactos Optimista"].apply(lambda x: f"{int(x):,}".replace(",", "."))
        df_display["CPM Medio"] = df_display["CPM Medio"].apply(lambda x: f"${int(round(x)):,}".replace(",", "."))
        
        st.dataframe(df_display[["Soporte", "Ubicación", "Días", "Inversión Neta", "Impactos Medio", "CPM Medio"]], use_container_width=True)
        
        total_inversion = sum(item["Inversión Neta"] for item in st.session_state.plan_items)
        total_imp_c = sum(item["Impactos Conservador"] for item in st.session_state.plan_items)
        total_imp_m = sum(item["Impactos Medio"] for item in st.session_state.plan_items)
        total_imp_o = sum(item["Impactos Optimista"] for item in st.session_state.plan_items)
        
        cpm_global_c = (total_inversion / total_imp_c * 1000) if total_imp_c > 0 else 0
        cpm_global_m = (total_inversion / total_imp_m * 1000) if total_imp_m > 0 else 0
        cpm_global_o = (total_inversion / total_imp_o * 1000) if total_imp_o > 0 else 0

        st.markdown("---")
        st.subheader("📊 2. Totales Acumulados de la Campaña")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Líneas en Mix", f"{len(st.session_state.plan_items)} soportes")
        m2.metric("Inversión Total Neta", f"${total_inversion:,.0f}".replace(",", "."))
        m3.metric("Impactos Totales (Medio)", f"{total_imp_m:,.0f}".replace(",", "."))
        m4.metric("CPM Ponderado Global", f"${int(round(cpm_global_m)):,}".replace(",", "."))
        
        tabla_consolidada = [
            {
                "Escenario Global": "Conservador",
                "Impactos Totales Campaña": f"{total_imp_c:,.0f}".replace(",", "."),
                "Costo x Impacto Promedio": f"${(total_inversion / total_imp_c):.2f}" if total_imp_c > 0 else "$0",
                "CPM Ponderado Global": f"${int(round(cpm_global_c)):,}".replace(",", ".")
            },
            {
                "Escenario Global": "Medio (Recomendado)",
                "Impactos Totales Campaña": f"{total_imp_m:,.0f}".replace(",", "."),
                "Costo x Impacto Promedio": f"${(total_inversion / total_imp_m):.2f}" if total_imp_m > 0 else "$0",
                "CPM Ponderado Global": f"${int(round(cpm_global_m)):,}".replace(",", ".")
            },
            {
                "Escenario Global": "Optimista",
                "Impactos Totales Campaña": f"{total_imp_o:,.0f}".replace(",", "."),
                "Costo x Impacto Promedio": f"${(total_inversion / total_imp_o):.2f}" if total_imp_o > 0 else "$0",
                "CPM Ponderado Global": f"${int(round(cpm_global_o)):,}".replace(",", ".")
            }
        ]
        st.table(pd.DataFrame(tabla_consolidada))
        
        st.markdown("---")
        st.subheader("📋 3. Resumen Ejecutivo Integrado para Propuesta")
        
        lineas_resumen = ""
        for idx, item in enumerate(st.session_state.plan_items, 1):
            lineas_resumen += f"  {idx}. **{item['Soporte']}** en {item['Ubicación']} | {item['Días']} días | Inversión: \({item['Inversión Neta']:,.0f} | Impactos: {item['Impactos Medio']:,} | CPM:\){int(round(item['CPM Medio'])):,}\n".replace(",", ".")
            
        texto_resumen = f"""**PROPUESTA DE MEDIOS INTEGRADA (MIX OOH & METRO)**
**Agencia Responsable:** MADCOM
**Inversión Total Neta:** ${total_inversion:,.0f} CLP
**Impactos Brutos Totales (Escenario Medio):** {total_imp_m:,.0f} impactos
**CPM Ponderado Global:** ${int(round(cpm_global_m)):,}.00 CLP

**Detalle de Soportes Contratados:**
{lineas_resumen}
*Valores netos calculados en pesos chilenos.*
"""
        st.code(texto_resumen, language="markdown")
