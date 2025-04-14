import math
import json
import os

# === Classe Variabile ===
class Variabile:
    def __init__(self, nome, valore):
        self.nome = nome
        self.valore = valore

    def __repr__(self):
        return f"{self.nome}: {self.valore}"

# === Funzioni di utilità ===
def gradi2radianti(gradi): return math.radians(gradi)
def radianti2gradi(radianti): return math.degrees(radianti)
def angolo_360(angolo): return angolo % 360
def ore_minuti(decimal):
    if decimal is None: return None, None
    ore = int(decimal)
    minuti = round((decimal - ore) * 60)
    return ore, minuti

def in_range(start, end, angle):
    if start <= end:
        return start <= angle <= end
    else:
        return angle >= start or angle <= end
def calc_distanza(lat1, long1, lat2,long2):
    R = 3440.065
    lat_diff = gradi2radianti((lat1 - lat2) / 2)
    lon_diff = gradi2radianti((long1 - long2) / 2)
    a = math.sin(lat_diff)**2 + math.cos(gradi2radianti(lat2)) * math.cos(gradi2radianti(lat1)) * math.sin(lon_diff)**2
    c = 2 * math.asin(math.sqrt(a))
    distanza = R * c
    x = (long2 - long1) * math.cos(gradi2radianti((lat2 + lat1) / 2))
    y = lat2 - lat1
    angolo_bb = angolo_360(450 - radianti2gradi(math.atan2(y, x)))
    return distanza,angolo_bb
   
def settore_navigazione(angolo,bolina_sx,bolina_dx,poppa_sx,poppa_dx):
    if in_range(bolina_sx, bolina_dx, angolo): return "Bolina"
    elif in_range(bolina_dx, poppa_sx, angolo): return "Dx - Mura a Sinistra"
    elif in_range(poppa_sx, poppa_dx, angolo): return "Poppa"
    elif in_range(poppa_dx, bolina_sx, angolo): return "Sx - Mura a Dritta"
    return "Errore"

# === Variabili iniziali ===
defaults = {
    "lat_barca": Variabile("lat_barca", 41.2248),
    "lon_barca": Variabile("lon_barca", 13.0971),
    "lat_boa": Variabile("lat_boa", 41.2833),
    "lon_boa": Variabile("lon_boa", 13.0000),
    "angolo_bb": Variabile("angolo_bb", 310),
    "distanza": Variabile("distanza", 4),
    "vp": Variabile("vp", 4.0),
    "vp_sx": Variabile("vp_sx", 4.0),
    "vp_dx": Variabile("vp_dx", 4.0), 
    "bussola": Variabile("bussola", 275),
    "ve": Variabile("ve", 5.0),
    "sog": Variabile("sog", 280),
    "vc": Variabile("vc", 1.0),
    "dc": Variabile("dc", 270),
    "ve_sx": Variabile("ve_sx", 5.0),
    "ve_dx": Variabile("ve_dx", 4.5),
    "rotta_vera_sx": Variabile("rotta_vera_sx", 270),
    "rotta_vera_dx": Variabile("rotta_vera_dx", 330),
    "angolo_vento": Variabile("angolo_vento", 310),
    "angolo_bolina_sx": Variabile("angolo_bolina_sx", 35),
    "angolo_bolina_dx": Variabile("angolo_bolina_dx", 35),
    "angolo_poppa_sx": Variabile("angolo_poppa_sx", 20),
    "angolo_poppa_dx": Variabile("angolo_poppa_dx", 20),
}

file_input = "input_precedente.json"
if os.path.exists(file_input):
    with open(file_input, "r") as f:
        contenuto = f.read().strip()
        if contenuto:
            dati_salvati = json.loads(contenuto)
            for k, v in dati_salvati.items():
                if k in defaults:
                    defaults[k].valore = v

# === Programmi ===
def calcola_boa(dati):
    lat_barca = dati["lat_barca"].valore
    lon_barca = dati["lon_barca"].valore
    distanza = dati["distanza"].valore
    angolo_bb = dati["angolo_bb"].valore

    ang_rad = gradi2radianti(angolo_bb)
    lat_boa = lat_barca + (distanza * math.cos(ang_rad)) / 60
    lon_boa = lon_barca + (distanza * math.sin(ang_rad)) / (60 * math.cos(gradi2radianti(lat_barca)))

    dati["lat_boa"].valore = round(lat_boa, 3)
    dati["lon_boa"].valore = round(lon_boa, 3)
    
