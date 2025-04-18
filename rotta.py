import math

# === Classe Variabile ===
class Variabile:
    def __init__(self, nome, valore):
        self.nome = nome
        self.valore = valore

    def __repr__(self):
        return f"{self.nome}: {self.valore}"

# === Utility ===
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

def calc_distanza(lat1, long1, lat2, long2):
    R = 3440.065
    lat_diff = gradi2radianti((lat1 - lat2) / 2)
    lon_diff = gradi2radianti((long1 - long2) / 2)
    a = math.sin(lat_diff)**2 + math.cos(gradi2radianti(lat2)) * math.cos(gradi2radianti(lat1)) * math.sin(lon_diff)**2
    c = 2 * math.asin(math.sqrt(a))
    distanza = R * c
    x = (long2 - long1) * math.cos(gradi2radianti((lat2 + lat1) / 2))
    y = lat2 - lat1
    angolo_bb = angolo_360(450 - radianti2gradi(math.atan2(y, x)))
    return distanza, angolo_bb

def calcola_boa(dati):
    lat, lon = dati["lat_barca"].valore, dati["lon_barca"].valore
    dist, ang = dati["distanza"].valore, dati["angolo_bb"].valore
    ang_rad = gradi2radianti(ang)
    dati["lat_boa"].valore = round(lat + (dist * math.cos(ang_rad)) / 60, 3)
    dati["lon_boa"].valore = round(lon + (dist * math.sin(ang_rad)) / (60 * math.cos(gradi2radianti(lat))), 3)

def calcola_corrente(dati):
    vp, buss, ve, sog = dati["vp"].valore, dati["bussola"].valore, dati["ve"].valore, dati["sog"].valore
    bx = vp * math.cos(gradi2radianti(buss))
    by = vp * math.sin(gradi2radianti(buss))
    vx = ve * math.cos(gradi2radianti(sog)) - bx
    vy = ve * math.sin(gradi2radianti(sog)) - by
    dati["vc"].valore = round(math.sqrt(vx**2 + vy**2), 1)
    dati["dc"].valore = round(angolo_360(radianti2gradi(math.atan2(vy, vx))), 1)

# Variabili e programmi
defaults = {
    "lat_barca": Variabile("lat_barca", 41.2248),
    "lon_barca": Variabile("lon_barca", 13.0971),
    "lat_boa": Variabile("lat_boa", 0),
    "lon_boa": Variabile("lon_boa", 0),
    "angolo_bb": Variabile("angolo_bb", 310),
    "distanza": Variabile("distanza", 4),
    "vp": Variabile("vp", 4.0),
    "bussola": Variabile("bussola", 275),
    "ve": Variabile("ve", 5.0),
    "sog": Variabile("sog", 280),
    "vc": Variabile("vc", 0),
    "dc": Variabile("dc", 0),
}
programmi = {
    "Posizione_boa": {
        "input": ["lat_barca", "lon_barca", "distanza", "angolo_bb"],
        "output": ["lat_boa", "lon_boa"],
        "funzione": calcola_boa
    },
    "Calcolo_corrente": {
        "input": ["vp", "bussola", "ve", "sog"],
        "output": ["vc", "dc"],
        "funzione": calcola_corrente
    }
}
