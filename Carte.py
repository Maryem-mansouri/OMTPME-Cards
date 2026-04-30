import dash
from dash import dcc, html, Input, Output, State
from plotly import data
import plotly.graph_objects as go
import json
import pandas as pd
import base64
import io
import base64
import os

# ================= SVG FLECHES EN BASE64 =================  ← ICI
def make_arrow_b64(color_hex, direction="up"):
    if direction == "up":
        points = "15,2 28,26 2,26"
    else:
        points = "15,28 2,4 28,4"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30">
  <polygon points="{points}" fill="{color_hex}" />
</svg>'''
    b64 = base64.b64encode(svg.encode()).decode()
    return f"data:image/svg+xml;base64,{b64}"

ARROW_UP_GREEN = make_arrow_b64("#1a9641", "up")
ARROW_DOWN_RED = make_arrow_b64("#d7191c", "down")

# ================= GEOJSON =================
with open("morocco_Province_level_2.geojson", encoding="utf-8") as f:
    geo_provinces = json.load(f)
with open("morocco_Region_level_1.geojson", encoding="utf-8") as f:
    geo_regions = json.load(f)
print([f["properties"]["shape1"] for f in geo_regions["features"]])


regions = [
    "Maroc", "Tanger-Tétouan-Al Hoceima", "Casablanca-Settat", "Rabat-Salé-Kénitra",
    "Béni Mellal-Khénifra", "Oriental", "Fès-Meknès",
    "Marrakech-Safi", "Drâa-Tafilalet", "Souss-Massa",
    "Laâyoune-Sakia El Hamra", "Dakhla-Oued Ed-Dahab",
    "Guelmim-Oued Noun", "Régions du Sud"
]

REGIONS_GROUPES = {
    "Régions du Sud": [
        "Laâyoune-Sakia El Hamra",
        "Dakhla-Oued Ed-Dahab",
        "Guelmim-Oued Noun"
    ]
}

# Mapping pour récupérer les noms shape1 des régions
REGIONS_LEVEL1 = [f["properties"]["shape1"] for f in geo_regions["features"]]

# ================= CONFIG LABEL =================
MAP_LABEL_CONFIG = {
    "Maroc": {
        "default_length": 0.5,
        "zoom": 3.8,
        "text_size": 15,
        "evo_size": 13,
        "provinces": {
            "Tanger-Tétouan-Al Hoceima": {"length": 3.5, "side": "left", "anchor_offset": {"lon": -0.5,  "lat": 0.1}},
            "Oriental":                  {"length": 2, "side": "right", "anchor_offset": {"lon": 0.1,  "lat": 0.0}},
            "Fès-Meknès":                {"length": 5, "side": "right", "anchor_offset": {"lon": 0.0,  "lat": -0.1}},
            "Rabat-Salé-Kénitra":        {"length": 2.5, "side": "left",  "anchor_offset": {"lon": -0.1, "lat": 0.1}},
            "Béni Mellal-Khénifra":      {"length": 7, "side": "right", "anchor_offset": {"lon": 0.1,  "lat": 0.0}},
            "Casablanca-Settat":         {"length": 2.5, "side": "left",  "anchor_offset": {"lon": -0.1, "lat": 0.1}},
            "Marrakech-Safi":            {"length": 2.5, "side": "left",  "anchor_offset": {"lon": -0.1, "lat": 0.0}},
            "Drâa-Tafilalet":            {"length": 3.5, "side": "right", "anchor_offset": {"lon": 0.1,  "lat": 0.0}},
            "Souss-Massa":               {"length": 2, "side": "left",  "anchor_offset": {"lon": -0.1, "lat": 0.0}},
            "Guelmim-Oued Noun":         {"length": 2.5, "side": "left",  "anchor_offset": {"lon": -0.1, "lat": 0.0}},
            "Laâyoune-Sakia El Hamra":   {"length": 3, "side": "left",  "anchor_offset": {"lon": -0.1, "lat": 0.0}},
            "Dakhla-Oued Ed-Dahab":      {"length": 3, "side": "left", "anchor_offset": {"lon": 0.2,  "lat": 0.5}},
        }
    },
    



    "Tanger-Tétouan-Al Hoceima": {
        "default_length": 0.45,
        "provinces": {
            "Tanger-Assilah": {"length": 0.40, "side": "left"},
            "M'diq-Fnideq": {"length": 0.50, "side": "right"},
            "Tétouan": {"length": 0.45, "side": "right","anchor_offset": {"lon": 0.07} },
            "Fahs-Anjra": {"length": 0.4, "side": "left","anchor_offset": {"lon": 0.05,"lat": 0.05}  },
            "Larache": {"length": 0.45, "side": "left","anchor_offset": {"lon": -0.06, "lat": 0.0}},
            "Chefchaouen": {"length": 0.45, "side": "right",
                            "anchor_offset": {"lon": -0.09, "lat": 0.15}  
                            },
            "Al Hoceima": {"length": 0.5, "side": "right","anchor_offset": {"lon": 0.07, "lat": 0.0}},
            "Ouezzane": {"length": 0.5, "side": "left", "anchor_offset": {"lon": -0.09, "lat": 0.0}}
        }
    },
     "Casablanca-Settat": {
        "default_length": 0.45,
        "provinces": {
            "Casablanca": {"length": 0.5, "side": "left"},
            "Mohammedia": {"length": 0.9, "side": "right","anchor_offset": {"lon": 0.0, "lat": 0.0}},
            "Nouaceur": {"length": 0.75, "side": "left","anchor_offset": {"lon": 0.0, "lat": -0.05}},
            "Médiouna": {"length": 1, "side": "right","anchor_offset": {"lon": 0.0, "lat": -0.03}},
            "El Jadida": {"length": 0.6, "side": "left","anchor_offset": {"lon": -0.08, "lat": 0.0}},
            "Sidi Bennour": {"length": 0.50, "side": "left","anchor_offset": {"lon": 0.0, "lat": -0.12}},
            "Settat": {"length": 0.50, "side": "right","anchor_offset": {"lon": 0.5, "lat": 0.0}},
            "Berrechid": {"length": 0.9, "side": "left","anchor_offset": {"lon": -0.03, "lat": 0.06}},
            "Benslimane": {"length": 0.50, "side": "left","anchor_offset": {"lon": -0.08, "lat": 0.05}}
        }
    },

    "Rabat-Salé-Kénitra": {
    "default_length": 0.50,
    "provinces": {
        "Rabat": {
            "length": 0.50, "side": "left",
            "anchor_offset": {"lon": 0.0, "lat": -0.05}   
        },
        "Salé": {
            "length": 0.40, "side": "left",
            "anchor_offset": {"lon": 0.05, "lat": 0.10}  
        },
        "Skhirate-Témara": {"length": 0.60, "side": "left","anchor_offset": {"lon": 0.1, "lat": -0.2}},
        "Kénitra": {"length": 0.5, "side": "left"},
        "Sidi Slimane": {"length": 0.90, "side": "right","anchor_offset": {"lon": 0.0, "lat": -0.08}},
        "Sidi Kacem": {"length": 0.60, "side": "right","anchor_offset": {"lon": 0.2, "lat": 0.05}},
        "Khemisset": {"length": 0.45, "side": "right","anchor_offset": {"lon": 0.35, "lat": 0.0}}
    }
},
    "Béni Mellal-Khénifra": {
        "default_length": 0.45,
        "provinces": {
            "Khouribga": {"length": 0.65, "side": "left","anchor_offset": {"lon": -0.2, "lat": 0.0}},
            "Fquih Ben Saleh": {"length": 0.65, "side": "left","anchor_offset": {"lon": -0.1, "lat": 0.0}},
            "Beni Mellal": {"length": 0.50, "side": "right","anchor_offset": {"lon": 0.5, "lat": -0.1}},
            "Azilal": {"length": 0.7, "side": "left","anchor_offset": {"lon": 0.06, "lat": 0.0}},
            "Khénifra": {"length": 0.6, "side": "right","anchor_offset": {"lon": 0.2, "lat": 0.0}},
        }
    },

    "Fès-Meknès": {
        "default_length": 0.45,
        "provinces": {
            "Taza": {"length": 0.5, "side": "right","anchor_offset": {"lon": 0.2, "lat": 0.0}},
            "Sefrou": {"length": 1.2, "side": "right","anchor_offset": {"lon": 0.4, "lat": 0.0}},
            "Boulemane": {"length": 0.50, "side": "right","anchor_offset": {"lon": 0.8, "lat": 0.0}},
            "Ifrane": {"length": 0.7, "side": "left","anchor_offset": {"lon": 0.0, "lat": -0.03}},
            "El Hajeb": {"length": 0.6, "side": "left","anchor_offset": {"lon": 0.0, "lat": -0.03}},
            "Taounate": {"length": 0.70, "side": "left","anchor_offset": {"lon": 0.0, "lat": 0.4}},
            "Fès": {"length": 1.02, "side": "left","anchor_offset": {"lon": 0.0, "lat": -0.04}},
            "Moulay Yacoub": {"length": 0.9, "side": "left","anchor_offset": {"lon": -0.08, "lat": 0.06}},
            "Meknès": {"length": 0.6, "side": "left","anchor_offset": {"lon": -0.4, "lat": 0.05}}
        }
    },
      "Oriental": {
        "default_length": 0.45,
        "zoom": 5.4,
        "text_size": 18,
        "evo_size": 17,
        "provinces": {
            "Figuig": {"length": 1.5, "side": "left","anchor_offset": {"lon": -0.8, "lat": 0.4}},
            "Guercif": {"length": 0.8, "side": "left","anchor_offset": {"lon": 0.0, "lat": 0.0}},
            "Taourirt": {"length": 1.5, "side": "right","anchor_offset": {"lon": 0.0, "lat": 0.0}},
            "Berkane": {"length": 0.7, "side": "right","anchor_offset": {"lon": 0.0, "lat": 0.0}},
            "Driouch": {"length": 0.7, "side": "left","anchor_offset": {"lon": 0.0, "lat": 0.0}},
            "Oujda-Angad": {"length": 0.70, "side": "right","anchor_offset": {"lon": 0.0, "lat": 0.0}},
            "Jerada": {"length": 0.5, "side": "right","anchor_offset": {"lon": 0.05, "lat": -0.6}},
            "Nador": {"length": 0.9, "side": "right","anchor_offset": {"lon": -0.03, "lat": 0.0}},
        }
    },
    "Marrakech-Safi": {
        "default_length": 0.45,
        "text_size": 18,
        "evo_size": 17,
        
        "provinces": {
            "Al Haouz": {"length": 0.9, "side": "right","anchor_offset": {"lon": 0.0, "lat": 0.0}},
            "Youssoufia": {"length": 1.2, "side": "left","anchor_offset": {"lon": -0.08, "lat": 0.0}},
            "El Kelâa des Sraghna": {"length": 0.6, "side": "right","anchor_offset": {"lon": 0.05, "lat": 0.0}},
            "Chichaoua": {"length": 1.5, "side": "left","anchor_offset": {"lon": 0.0, "lat": -0.06}},
            "Marrakech": {"length": 1.2, "side": "right","anchor_offset": {"lon": 0.0, "lat": 0.0}},
            "Rhamna": {"length": 0.70, "side": "right","anchor_offset": {"lon": 0.1, "lat": 0.0}},
            "Safi": {"length": 0.5, "side": "left","anchor_offset": {"lon": 0.0, "lat": 0.0}},
            "Essaouira": {"length": 0.5, "side": "left","anchor_offset": {"lon": 0.0, "lat": -0.1}},
            
        }
    },
    "Drâa-Tafilalet": {
        "default_length": 0.45,
        "zoom": 5,
        "text_size": 20,
        "evo_size": 20,
        "provinces": {
            "Midelt": {"length": 0.5, "side": "right","anchor_offset": {"lon": 0.9, "lat": 0.1}},
            "Tinghir": {"length": 1.2, "side": "left","anchor_offset": {"lon": -0.4, "lat": 0.1}},
            "Zagora": {"length": 0.9, "side": "left","anchor_offset": {"lon": -0.05, "lat": 0.0}},
            "Errachidia": {"length": 1, "side": "right","anchor_offset": {"lon": 0.0, "lat": -0.0}},
            "Ouarzazate": {"length": 1, "side": "left","anchor_offset": {"lon": -0.09, "lat": 0.0}},
            
        }
    },

    "Souss-Massa": {
        "default_length": 0.45,
        "zoom": 4.5,
        "text_size": 17,
        "evo_size": 17,
        "provinces": {
            "Chtouka-Aït Baha": {"length": 0.7, "side": "left","anchor_offset": {"lon": 0.0, "lat": -0.09}},
            "Inezgane-Ait Melloul": {"length": 0.5, "side": "left","anchor_offset": {"lon": 0.0, "lat": -0.04}},
            "Tiznit": {"length": 0.7, "side": "left","anchor_offset": {"lon": -0.1, "lat": -0.03}},
            "Agadir Ida-Outanane": {"length": 0.7, "side": "left","anchor_offset": {"lon": 0.0, "lat": 0.1}},
            "Taroudant": {"length": 0.7, "side": "right","anchor_offset": {"lon": 0.4, "lat": 0.1}},
            "Tata": {"length": 0.8, "side": "right","anchor_offset": {"lon": -0.2, "lat": -0.2}},

        }
    },
    "Laâyoune-Sakia El Hamra": {
        "default_length": 0.45,
        "zoom": 4.5,
        "text_size": 19,
        "evo_size": 19,
        "provinces": {
            "Boujdour": {"length": 0.6, "side": "left","anchor_offset": {"lon": 0.0, "lat": 0.0}},
            "Tarfaya": {"length": 0.65, "side": "left","anchor_offset": {"lon": 0.0, "lat": 0.0}},
            "Es-Semara": {"length": 1.5, "side": "right","anchor_offset": {"lon": 0.0, "lat": 0.8}},
            "Laâyoune": {"length": 0.6, "side": "left","anchor_offset": {"lon": 0.0, "lat": 0.0}},
        }
    },
    "Dakhla-Oued Ed-Dahab": {
        "default_length": 0.45,
        "zoom": 5.5,
        "text_size": 20,
        "evo_size": 20,
        "provinces": {
            "Oued Ed-Dahab": {"length": 0.7, "side": "left","anchor_offset": {"lon": 0.9, "lat": 1.6}},
            "Aousserd": {"length": 0.7, "side": "left","anchor_offset": {"lon": 0.0, "lat": 0.5}},

        }
    },
    "Guelmim-Oued Noun": {
        "default_length": 0.45,
        "zoom": 7,
        "provinces": {
            "Guelmim": {"length": 0.7, "side": "left","anchor_offset": {"lon": -0.05, "lat": 0.0}},
            "Assa-Zag": {"length": 0.7, "side": "right","anchor_offset": {"lon": 0.7, "lat": 0.0}},
            "Tan-Tan": {"length": 0.6, "side": "left","anchor_offset": {"lon": 0.0, "lat": 0.0}},
            "Sidi Ifni": {"length": 0.6, "side": "left","anchor_offset": {"lon": 0.0, "lat": 0.0}},
        }
    },
    "Régions du Sud": {
        "default_length": 0.45,
        "zoom": 2,
        "text_size": 20,
        "evo_size": 20,
        "provinces": {
            "Guelmim": {"length": 1.5, "side": "right","anchor_offset": {"lon": 0.7, "lat": 0.0}},
            "Assa-Zag": {"length": 1.2, "side": "right","anchor_offset": {"lon": 0.7, "lat": 0.0}},
            "Tan-Tan": {"length": 1.1, "side": "left","anchor_offset": {"lon": 0.0, "lat": 0.0}},
            "Sidi Ifni": {"length": 1.2, "side": "left","anchor_offset": {"lon": 0.0, "lat": 0.0}},
            "Oued Ed-Dahab": {"length": 1.2, "side": "left","anchor_offset": {"lon": 1.1, "lat": 2.19}},
            "Aousserd": {"length": 1.2, "side": "left","anchor_offset": {"lon": 0.0, "lat": 0.2}},
            "Boujdour": {"length": 1, "side": "left","anchor_offset": {"lon": 0.0, "lat": 0.0}},
            "Tarfaya": {"length": 1.2, "side": "left","anchor_offset": {"lon": 0.0, "lat": 0.0}},
            "Es-Semara": {"length": 1.2, "side": "right","anchor_offset": {"lon": 1.9, "lat": 0.2}},
            "Laâyoune": {"length": 1.2, "side": "left","anchor_offset": {"lon": 0.0, "lat": 0.0}},
        }
    },
}

# ================= APP =================
app = dash.Dash(__name__,
    assets_folder=os.path.join(os.path.dirname(__file__), "assets"))
app.title = "Carte interactive des régions du Maroc"

#stored_values = {region: {} for region in regions}


# ================= UTILS =================
def province_center(feature):
    geometry = feature["geometry"]

    if geometry["type"] == "Polygon":
        coords = geometry["coordinates"][0]
    else:
        coords = geometry["coordinates"][0][0]

    lon = sum(pt[0] for pt in coords) / len(coords)
    lat = sum(pt[1] for pt in coords) / len(coords)

    return lon, lat


def parse_excel(contents):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    df = pd.read_excel(io.BytesIO(decoded))
    df.columns = [c.lower().strip() for c in df.columns]

    # Accepter avec ou sans colonne province
    required_with = {"region", "province", "part", "evolution"}
    required_without = {"region", "part", "evolution"}

    if required_with.issubset(df.columns):
        return df, "province"
    elif required_without.issubset(df.columns):
        return df, "region"   # ← clé = region pour Maroc
    else:
        raise ValueError("Le fichier doit contenir : region, part, evolution (+ province optionnel)")

def geo_to_paper(lon, lat, lon_min, lon_max, lat_min, lat_max):
    """Convertit coordonnées géo → coordonnées paper (0-1) pour add_layout_image"""
    x = (lon - lon_min) / (lon_max - lon_min) if lon_max != lon_min else 0.5
    y = (lat - lat_min) / (lat_max - lat_min) if lat_max != lat_min else 0.5
    return x, y


# ================= LAYOUT =================
app.layout = html.Div([
    # ===== SESSION STORE =====
    dcc.Store(id="stored-values", storage_type="session", data={}),
    dcc.Store(id="excel-contents-store", storage_type="session", data=None),

    # ===== HEADER =====
    html.Div([

    html.Div([

        # ===== LOGO =====
        html.Img(
            src="/assets/Logo.png",
            style={
                "height": "50px",
                "marginRight": "15px"
            }
        ),

        # ===== TITRES =====
        html.Div([
            html.H2(
                "Tableau de Bord des Régions",
                style={"marginBottom": "2px","color": "#3F82AD"}
            ),
            html.P(
                "Analyse interactive des indicateurs par province",
                style={"color": "#3F82AD", "marginTop": "0px"}
            )
        ])

    ], style={
        "display": "flex",
        "alignItems": "center"
    }),
        html.Div([
            html.Div([
                html.Div("12", style={"fontSize": "20px", "fontWeight": "bold", "color": "#2c7fb8"}),
                html.Div("Régions", style={"fontSize": "11px", "color": "#888"})
            ], style={
                "textAlign": "center", "padding": "8px 16px",
                "background": "#f5f8fc", "borderRadius": "8px",
                "border": "0.5px solid #dce8f5"
            }),
            html.Div([
                html.Div("75", style={"fontSize": "20px", "fontWeight": "bold", "color": "#27ae60"}),
                html.Div("Provinces", style={"fontSize": "11px", "color": "#888"})
            ], style={
                "textAlign": "center", "padding": "8px 16px",
                "background": "#f5fcf8", "borderRadius": "8px",
                "border": "0.5px solid #d5f0e2"
            }),
        ], style={"display": "flex", "gap": "10px", "marginLeft": "auto", "alignItems": "center"})

], style={
    "padding": "15px 25px",
    "backgroundColor": "#FFFFFF",
    "boxShadow": "0px 2px 6px rgba(0,0,0,0.05)",
    "display": "flex",                        # ← AJOUTER
    "alignItems": "center",                   # ← AJOUTER
    "justifyContent": "space-between"
}),


    # ===== MAIN CONTAINER =====
    html.Div([

        # ===== LEFT PANEL =====
        html.Div([

            html.H4("Configuration"),

            html.Label("Région cible"),
            dcc.Dropdown(
                id="filter-region",
                options=[{"label": r, "value": r} for r in regions],
                placeholder="Sélectionner une région",
                style={"marginBottom": "15px"}
            ),

            html.H5("Données manuelles", style={"marginTop": "20px"}),

            dcc.Dropdown(
                id="dropdown-province",
                placeholder="Province",
                style={"marginBottom": "10px"}
            ),

            dcc.Input(
                id="input-value",
                type="number",
                placeholder="Part %",
                style={"width": "100%", "marginBottom": "10px"}
            ),

            dcc.Input(
                id="input-evolution",
                type="number",
                placeholder="Evolution %",
                style={"width": "100%", "marginBottom": "15px"}
            ),

            html.Button(
                "Mettre à jour la carte",
                id="btn-update",
                n_clicks=0,
                style={
                    "width": "100%",
                    "backgroundColor": "#2E63D3",
                    "color": "white",
                    "border": "none",
                    "padding": "10px",
                    "borderRadius": "6px",
                    "fontWeight": "bold"
                }
            ),
            html.Button(
                "🗑️ Effacer la carte",
                id="btn-clear",
                n_clicks=0,
                style={
                    "width": "100%",
                    "backgroundColor": "#e74c3c",
                    "color": "white",
                    "border": "none",
                    "padding": "10px",
                    "borderRadius": "6px",
                    "fontWeight": "bold",
                    "marginTop": "8px"
                }
            ),
            dcc.Download(id="download-template"),

            html.Button(
                "📥 Télécharger le modèle Excel",
                id="btn-download-template",
                n_clicks=0,
                style={
                    "width": "100%",
                    "backgroundColor": "#27ae60",
                    "color": "white",
                    "border": "none",
                    "padding": "10px",
                    "borderRadius": "6px",
                    "fontWeight": "bold",
                    "marginTop": "8px"
                }
            ),
            
            html.Hr(style={"marginTop": "25px"}),

            html.H5("Import de masse"),

            dcc.Upload(
                id="upload-excel",
                children=html.Div(["📂 Excel (Drag & Drop)"]),
                style={
                    "width": "100%",
                    "height": "70px",
                    "lineHeight": "70px",
                    "borderWidth": "2px",
                    "borderStyle": "dashed",
                    "borderRadius": "8px",
                    "textAlign": "center",
                    "backgroundColor": "#F8FAFC"
                },
                multiple=False
            ),

            html.Div(
                id="upload-message",
                style={
                    "marginTop": "10px",
                    "color": "green",
                    "fontSize": "14px"
                }
            )

        ], style={
            "width": "300px",
            "backgroundColor": "white",
            "padding": "20px",
            "borderRadius": "10px",
            "boxShadow": "0px 3px 10px rgba(0,0,0,0.08)"
        }),

        # ===== RIGHT PANEL (MAP) =====
        html.Div([
            dcc.Graph(
                id="graph-region",
                style={"height": "100%","minHeight": "85vh"},
                config={
                    "displayModeBar": True,
                    "toImageButtonOptions": {"format": "png", "scale": 6},
                    "scrollZoom": False,    # ← désactive zoom souris
                    "doubleClick": False, 
                }
            )
        ], style={
            "flex": "1",
            "marginLeft": "20px",
            "backgroundColor": "white",
            "borderRadius": "10px",
            "padding": "10px",
            "boxShadow": "0px 3px 10px rgba(0,0,0,0.08)"
        })

    ], style={
        "display": "flex",
        "padding": "20px",
        "backgroundColor": "#EDF6F7",
        "minHeight": "90vh"
    }),
    # ===== FOOTER =====
    html.Div([
        html.P([
            "Réalisé par ",
            html.Span("Maryem El Mansouri | DA", style={
                "fontWeight": "bold",
                "color": "#3F82AD"
            }),
            " — OMTPME © 2026"
        ], style={
            "margin": "0",
            "fontSize": "12px",
            "color": "#3F82AD"
        })
    ], style={
        "padding": "12px 25px",
        "backgroundColor": "#FFFFFF",
        "borderTop": "0.5px solid #e0e0e0",
        "textAlign": "center",
        "boxShadow": "0px -2px 6px rgba(0,0,0,0.03)"
    })

])


# ================= UPDATE PROVINCES =================
@app.callback(
    Output("dropdown-province", "options"),
    Input("filter-region", "value")
)
def update_provinces(region_name):

    if not region_name:
        return []
    
    # ← CAS MAROC : le 2ème dropdown affiche les régions
    if region_name == "Maroc":
        return [{"label": r, "value": r} for r in REGIONS_LEVEL1]

    if region_name in REGIONS_GROUPES:
        provinces = [
            f for f in geo_provinces["features"]
            if f["properties"]["shape1"] in REGIONS_GROUPES[region_name]
        ]
    else:
        provinces = [
            f for f in geo_provinces["features"]
            if f["properties"]["shape1"] == region_name
        ]

    return [{"label": f["properties"]["shape2"], "value": f["properties"]["shape2"]}
            for f in provinces]

@app.callback(
    Output("download-template", "data"),
    Input("btn-download-template", "n_clicks"),
    State("filter-region", "value"),
    prevent_initial_call=True
)
def download_template(n_clicks, region_name):
    if not region_name or not n_clicks:
        return dash.no_update

    # ===== CAS MAROC : 3 colonnes avec les régions =====
    if region_name == "Maroc":
        df_template = pd.DataFrame({
            "region":    REGIONS_LEVEL1,
            "part":      [""] * len(REGIONS_LEVEL1),
            "evolution": [""] * len(REGIONS_LEVEL1)
        })
    elif region_name in REGIONS_GROUPES:
        provinces = [
            f["properties"]["shape2"]
            for f in geo_provinces["features"]
            if f["properties"]["shape1"] in REGIONS_GROUPES[region_name]
        ]
        df_template = pd.DataFrame({
            "region":    [region_name] * len(provinces),
            "province":  provinces,
            "part":      [""] * len(provinces),
            "evolution": [""] * len(provinces)
        })
    else:
        provinces = [
            f["properties"]["shape2"]
            for f in geo_provinces["features"]
            if f["properties"]["shape1"] == region_name
        ]
        df_template = pd.DataFrame({
            "region":    [region_name] * len(provinces),
            "province":  provinces,
            "part":      [""] * len(provinces),
            "evolution": [""] * len(provinces)
        })

    # Exporter en Excel en mémoire
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_template.to_excel(writer, index=False, sheet_name="Template")

        # Mise en forme basique
        ws = writer.sheets["Template"]
        for col in ws.columns:
            max_len = max(len(str(cell.value or "")) for cell in col) + 4
            ws.column_dimensions[col[0].column_letter].width = max_len

    output.seek(0)
    b64 = base64.b64encode(output.read()).decode()

    filename = f"template_{region_name.replace(' ', '_')}.xlsx"

    return dict(
        content=b64,
        filename=filename,
        base64=True
    )
# ================= HANDLE EXCEL UPLOAD =================
@app.callback(
    Output("excel-contents-store", "data"),
    Input("upload-excel", "contents"),
    prevent_initial_call=True
)
def store_excel(contents):
    return contents


@app.callback(
    Output("graph-region", "figure"),
    Output("stored-values", "data"),
    Input("btn-update", "n_clicks"),
    Input("btn-clear", "n_clicks"), 
    Input("upload-excel", "contents"),
    State("excel-contents-store", "data"),
    State("stored-values", "data"),
    State("filter-region", "value"),
    State("dropdown-province", "value"),
    State("input-value", "value"),
    State("input-evolution", "value"),
)


def update_figure(n_clicks, n_clear,excel_trigger, excel_contents,stored_values, region_name,
                  selected_province, val, evo):
    # Initialiser si vide
    if not stored_values:
        stored_values = {region: {} for region in regions}

    for region in regions:
        if region not in stored_values:
            stored_values[region] = {}

    # ===== Detect which button triggered =====
    ctx = dash.callback_context
    triggered = ctx.triggered[0]["prop_id"] if ctx.triggered else ""

    if "btn-clear" in triggered and region_name:
        stored_values[region_name] = {}

    # ===== Remplissage depuis Excel =====
    
    if "upload-excel" in triggered and excel_trigger:
        try:
            df, key_col = parse_excel(excel_trigger)
            for _, row in df.iterrows():
                r = str(row["region"]).strip()
                if key_col == "province":
                    p = str(row["province"]).strip()
                    if r in stored_values:
                        stored_values[r][p] = {
                            "part": row["part"],
                            "evolution": row["evolution"]
                        }
                else:
                    stored_values["Maroc"][r] = {
                        "part": row["part"],
                        "evolution": row["evolution"]
                    }
        except Exception as e:
            print(f"Erreur: {e}")

    if not region_name:

        # ===== Carte complète Maroc =====
        fig = go.Figure()
    
        fig.add_trace(go.Choroplethmapbox(
            geojson=geo_provinces,
            locations=[f["properties"]["shape2"] for f in geo_provinces["features"]],
            z=[1]*len(geo_provinces["features"]),
            featureidkey="properties.shape2",
            colorscale=[[0, "#E6EEF5"], [1, "#E6EEF5"]],
            showscale=False,
            marker_line_color="white"
        ))
    
        # ===== Texte central =====
        fig.add_annotation(
            text="""
    <b>Plateforme des cartes régionaux </b><br><br>
    Cette application permet de visualiser les parts (%) et les évolutions (%) 
    par province à l’échelle régionale et national.<br><br>
    
    <b>Étapes d’utilisation :</b><br>
    1️⃣ Sélectionner une région cible<br>
    2️⃣ Ajouter les données manuellement<br>
    ou<br>
    3️⃣ Importer un fichier Excel (region, province, part, evolution)<br>
    4️⃣ Cliquer sur "Mettre à jour la carte"
            """,
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            align="center",
            font=dict(size=16, color="#3F82AD")
        )
    
        # Centrage Maroc
        centers = [province_center(f) for f in geo_provinces["features"]]
    
        fig.update_layout(
            mapbox=dict(
                style="white-bg",
                zoom=4.8,
                center={
                    "lat": sum(c[1] for c in centers)/len(centers),
                    "lon": sum(c[0] for c in centers)/len(centers)
                }
            ),
            margin=dict(r=0, t=0, l=0, b=0),
            height=950,
            uirevision="Maroc",
        )
    
        return fig, stored_values


    # ===== Ajout manuel =====
    if selected_province and (val is not None or evo is not None):
        existing = stored_values[region_name].get(selected_province, {})
        stored_values[region_name][selected_province] = {
            "part": val if val is not None else existing.get("part"),
            "evolution": evo if evo is not None else existing.get("evolution")
        }

# ===== Provinces région ou Régions Maroc =====
    if region_name == "Maroc":
        features = geo_regions["features"]
        geojson_data = geo_regions
        featureidkey = "properties.shape1"
        name_key = "shape1"
    elif region_name in REGIONS_GROUPES:
        features = [f for f in geo_provinces["features"]
                    if f["properties"]["shape1"] in REGIONS_GROUPES[region_name]]
        geojson_data = {"type": "FeatureCollection", "features": features}
        featureidkey = "properties.shape2"
        name_key = "shape2"
    else:
        features = [f for f in geo_provinces["features"]
                    if f["properties"]["shape1"] == region_name]
        geojson_data = {"type": "FeatureCollection", "features": features}
        featureidkey = "properties.shape2"
        name_key = "shape2"

    fig = go.Figure()

    fig.add_trace(go.Choroplethmapbox(
        geojson=geojson_data,
        locations=[f["properties"][name_key] for f in features],
        z=[1] * len(features),
        featureidkey=featureidkey,
        colorscale=[[0, "#2c7fb8"], [1, "#2c7fb8"]],
        showscale=False,
        marker_line_color="white",
        marker_line_width=2
    ))

    centers = [province_center(f) for f in features]
    region_mid_lon = sum(c[0] for c in centers) / len(centers)
    lon_values = [c[0] for c in centers]
    lat_values = [c[1] for c in centers]
    auto_length = (max(lon_values) - min(lon_values)) * 0.25

    region_zoom  = MAP_LABEL_CONFIG.get(region_name, {}).get("zoom", 7.5)
    text_size    = MAP_LABEL_CONFIG.get(region_name, {}).get("text_size") or max(15, int(region_zoom * 2.5))
    evo_size     = MAP_LABEL_CONFIG.get(region_name, {}).get("evo_size")  or max(10, int(region_zoom * 2.2))
    diamond_size = max(10, int(region_zoom * 1.8))
    if region_name == "Maroc":
        lat_offset_text = 0.22
        lat_offset_evo  = 0.28
    else:
        lat_offset_text = 0.04 * (7.5 / region_zoom)
        lat_offset_evo  = 0.05 * (7.5 / region_zoom)

    for feature in features:
        name = feature["properties"][name_key]   # ← utilise name_key dynamique

        region_cfg   = MAP_LABEL_CONFIG.get(region_name, {})
        province_cfg = region_cfg.get("provinces", {}).get(name, {})

        lon_base, lat_base = province_center(feature)
        anchor_offset = province_cfg.get("anchor_offset", {})
        lon = lon_base + anchor_offset.get("lon", 0.0)
        lat = lat_base + anchor_offset.get("lat", 0.0)

        data = stored_values[region_name].get(name, {})
        part = data.get("part")
        evo  = data.get("evolution")

        if part is None and evo is None:
            continue

        # ... reste de la boucle labels inchangé (ligne, point, texte, évolution)

        auto_side = 1 if lon >= region_mid_lon else -1

        region_cfg = MAP_LABEL_CONFIG.get(region_name, {})
        province_cfg = region_cfg.get("provinces", {}).get(name, {})

        line_length = (
            province_cfg.get("length")
            or region_cfg.get("default_length")
            or auto_length
        )

        side = -1 if province_cfg.get("side") == "left" else \
               1 if province_cfg.get("side") == "right" else auto_side

        gap = 0.17

        line_end_lon = lon + side * (line_length - gap)
        label_lon    = lon + side * line_length
        label_lat    = lat
        
        # ligne
        fig.add_trace(go.Scattermapbox(
            lon=[lon, line_end_lon], lat=[label_lat, label_lat],
            mode="lines", line=dict(color="black", width=2),
            showlegend=False
        ))

        # ===== Point d'ancrage =====
        fig.add_trace(go.Scattermapbox(
            lon=[lon], lat=[lat],
            mode="markers", marker=dict(size=6, color="black"),
            showlegend=False
        ))

        # ===== Nom + Part % =====
        # Nom + Part %
        if region_name == "Maroc":
            label_text = name.replace("-", " ").replace(" ", "\u00A0")
        else:
            label_text = name.replace(" ", "\u00A0")
            
        if part is not None and str(part).strip() != "":
            part_float = float(part)
            part_display = int(part_float) if part_float == int(part_float) else part_float
            label_text += f"\u00A0{part_display}%"


        # ===== Nom + Part % =====
        if region_name == "Maroc":
            # Trace invisible pour positionner, puis trace gras séparé
            fig.add_trace(go.Scattermapbox(
                lon=[label_lon], lat=[label_lat + lat_offset_text],
                mode="text",
                text=[label_text],
                textfont=dict(size=text_size, color="black", weight="bold"),
                showlegend=False
            ))
        else:
            fig.add_trace(go.Scattermapbox(
                lon=[label_lon], lat=[label_lat + lat_offset_text],
                mode="text",
                text=[label_text],
                textfont=dict(size=text_size, color="black"),
                showlegend=False
            ))

        # ===== Évolution (seulement si renseignée) =====
        if evo is not None and str(evo).strip() != "":
            evo_float = float(evo)
            sign  = "+" if evo_float >= 0 else "-"
            color = "#1a9641" if evo_float >= 0 else "#d7191c"
            evo_display = int(evo_float) if evo_float == int(evo_float) else evo_float
            fig.add_trace(go.Scattermapbox(
                lon=[label_lon],
                lat=[label_lat - lat_offset_evo],
                mode="markers+text",
                marker=dict(
                    size=diamond_size,
                    color=color,
                    symbol="diamond",
                    allowoverlap=True,
                    opacity=1
                ),
                
                text=[f"  {sign}{abs(evo_display)}%"],
                textposition="middle right",
                textfont=dict(size=evo_size, color=color),
                showlegend=False,
                hoverinfo="skip"
            ))

    fig.update_layout(
        mapbox=dict(
            style="white-bg",
            zoom=region_zoom,
            center={"lat": sum(c[1] for c in centers) / len(centers),
                    "lon": sum(c[0] for c in centers) / len(centers)}
        ),
        margin=dict(r=0, t=0, l=0, b=0),
        height=950
    )

    return fig, stored_values


# ================= RUN =================
#if __name__ == "__main__":
#    app.run(debug=False, host="0.0.0.0", port=8050)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))