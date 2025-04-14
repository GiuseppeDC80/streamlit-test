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
    
    print("\n=== Risultato: Posizione della Boa ===")
    print(f"Lat barca: {round(lat_barca, 3)} | Lon barca: {round(lon_barca, 3)}")
    print(f"→ Distanza: {round(distanza, 2)} NM | Angolo: {round(angolo_bb, 2)}°")
    print(f"Lat boa: {round(lat_boa, 3)} | Lon boa: {round(lon_boa, 3)}")

def calcola_corrente(dati):
    vp = dati["vp"].valore
    bussola = dati["bussola"].valore
    ve = dati["ve"].valore
    sog = dati["sog"].valore

    bx = vp * math.cos(gradi2radianti(bussola))
    by = vp * math.sin(gradi2radianti(bussola))
    vx = ve * math.cos(gradi2radianti(sog)) - bx
    vy = ve * math.sin(gradi2radianti(sog)) - by

    vc = math.sqrt(vx**2 + vy**2)
    dc = angolo_360(radianti2gradi(math.atan2(vy, vx)))

    dati["vc"].valore =  round(vc, 1)
    dati["dc"].valore = round(dc, 1)
    print("\n=== Risultato: Corrente Calcolata ===")
    print(f"VP: {round(vp, 2)} nodi a {round(bussola, 1)}°")
    print(f"VE: {round(ve, 2)} nodi a {round(sog, 1)}°")
    print(f"→ Corrente stimata: {round(vc, 2)} nodi da {round(dc, 1)}°")

def studio_campo(dati):
    lat_barca = dati["lat_barca"].valore
    lon_barca = dati["lon_barca"].valore
    lat_boa = dati["lat_boa"].valore
    lon_boa = dati["lon_boa"].valore
    ve_sx = dati["ve_sx"].valore
    ve_dx = dati["ve_dx"].valore
    rotta_vera_sx = dati["rotta_vera_sx"].valore
    rotta_vera_dx = dati["rotta_vera_dx"].valore

    distanza,angolo_bb=calc_distanza(lat_barca, lon_barca, lat_boa,lon_boa)

    print("===== RISULTATI COMPLETI =====")
    print(f"Barca: lat {round(lat_barca,3)}, lon {round(lon_barca,3)}|Boa:lat {round(lat_boa,3)},long {round(lon_boa,3)}")
    print(f"Distanza: {round(distanza, 2)}NM| Angolo: {round(angolo_bb, 2)}°")
  
 
    if in_range(rotta_vera_sx, rotta_vera_dx, angolo_bb):
        navigazione = "bordi"
    else:
        navigazione = "dritto in boa"

    if navigazione == "bordi":
        beta = angolo_360(angolo_bb - rotta_vera_sx)
        alpha = angolo_360(rotta_vera_dx - angolo_bb)

        vmg_sx = ve_sx * math.cos(gradi2radianti(beta))
        vmg_dx = ve_dx * math.cos(gradi2radianti(alpha))

        angolo_intermedio = gradi2radianti(180 - alpha - beta)
        dist_layline_sx = distanza / math.sin(angolo_intermedio) * math.sin(gradi2radianti(alpha))
        dist_layline_dx = distanza / math.sin(angolo_intermedio) * math.sin(gradi2radianti(beta))

        tempo_sx = dist_layline_sx / ve_sx
        tempo_dx = dist_layline_dx / ve_dx
        tempo_totale = tempo_sx + tempo_dx
        ore, minuti = ore_minuti(tempo_totale)
        ore_sx, minuti_sx = ore_minuti(tempo_sx)
        ore_dx, minuti_dx = ore_minuti(tempo_dx)

        intercetto_sx_lat = lat_barca + (dist_layline_sx * math.cos(gradi2radianti(rotta_vera_sx))) / 60
        intercetto_sx_lon = lon_barca + (dist_layline_sx * math.sin(gradi2radianti(rotta_vera_sx))) / (60 * math.cos(gradi2radianti(lat_barca)))
        intercetto_dx_lat = lat_barca + (dist_layline_dx * math.cos(gradi2radianti(rotta_vera_dx))) / 60
        intercetto_dx_lon = lon_boa + (dist_layline_dx * math.sin(gradi2radianti(rotta_vera_dx))) / (60 * math.cos(gradi2radianti(lat_barca)))

        print(f"Lato sinistro →  Rotta:{round(rotta_vera_sx, 2)}°, Ve: {round(ve_sx, 2)} nodi, VMG: {round(vmg_sx, 2)} nodi, → layline: {round(dist_layline_sx, 2)} NM,{ore_sx} ore e {minuti_sx} minuti ")
        print(f"Lato destro →  Rotta:{round(rotta_vera_dx, 2)}°, Ve: {round(ve_dx, 2)} nodi, VMG: {round(vmg_dx, 2)} nodi, → layline: {round(dist_layline_dx, 2)} NM,{ore_dx} ore e {minuti_dx} minuti ")
        print(f"Tempo totale stimato: {ore} ore e {minuti} minuti, Distanza: {round((dist_layline_sx+dist_layline_dx), 2)} NM")
        print(f"Intercetto layline sx: lat {round(intercetto_sx_lat, 5)}, lon {round(intercetto_sx_lon, 5)}")
        print(f"Intercetto layline dx: lat {round(intercetto_dx_lat, 5)}, lon {round(intercetto_dx_lon, 5)}")

    else:
        diff_sx = angolo_360(angolo_bb - rotta_vera_sx)
        diff_dx = angolo_360(rotta_vera_dx - angolo_bb)
        ve = ve_sx if diff_sx < diff_dx else ve_dx
        rotta_vera = angolo_bb
        distanza_totale = distanza
        tempo_ore = distanza_totale / ve
        ore, minuti = ore_minuti(tempo_ore)

        print(f" Rotta:{round(angolo_bb, 2)}° ")
        print(f"Ve: {round(ve, 2)} nodi ")
        print(f"Distanza Totale: {round(distanza_totale, 2)} NM|Tempo stimato: {ore} ore e {minuti} minuti")

# Programma 4 (con logica simile)
def studio_campo_con_vento_e_corrente(dati):
    lat_barca = dati["lat_barca"].valore
    lon_barca = dati["lon_barca"].valore
    lat_boa = dati["lat_boa"].valore
    lon_boa = dati["lon_boa"].valore
    angolo_vento = dati["angolo_vento"].valore
    angolo_bolina_sx = dati["angolo_bolina_sx"].valore
    angolo_bolina_dx = dati["angolo_bolina_dx"].valore
    angolo_poppa_sx = dati["angolo_poppa_sx"].valore
    angolo_poppa_dx = dati["angolo_poppa_dx"].valore
    vp_sx = dati["vp_sx"].valore
    vp_dx = dati["vp_dx"].valore
    vc = dati["vc"].valore
    dc = dati["dc"].valore
    vp=(vp_dx+vp_sx)/2    # da aggiornare

    # Calcolo distanza e angolo BB
    distanza,angolo_bb=calc_distanza(lat_barca, lon_barca, lat_boa,lon_boa)
    
    # Settori
    bolina_sx = angolo_360(angolo_vento - angolo_bolina_sx)
    bolina_dx = angolo_360(angolo_vento + angolo_bolina_dx)
    poppa_sx = angolo_360(angolo_vento + 180 - angolo_poppa_sx)
    poppa_dx = angolo_360(angolo_vento + 180 + angolo_poppa_dx)

    if in_range(bolina_sx, bolina_dx, angolo_bb): settore = "Bolina" 
    elif in_range(bolina_dx, poppa_sx, angolo_bb): settore = "Dx - Mura a Sinistra"
    elif in_range(poppa_sx, poppa_dx, angolo_bb): settore = "Poppa"
    elif in_range(poppa_dx, bolina_sx, angolo_bb): settore = "Sx - Mura a Dritta"
 
    print("===== RISULTATI COMPLETI =====")
    print(f"Barca: lat {round(lat_barca,3)}, lon {round(lon_barca,3)}|Boa:lat {round(lat_boa,3)},long {round(lon_boa,3)}")
    print(f"Distanza: {round(distanza, 2)}NM| Angolo: {round(angolo_bb, 2)}°")
    print(f"Angolo Vento: {angolo_vento}° | Corrente: {vc} nodi da {dc}° ")

    if settore in ["Bolina", "Poppa"]:
        prora_sx = bolina_sx if settore == "Bolina" else poppa_sx
        prora_dx = bolina_dx if settore == "Bolina" else poppa_dx

        x_sx = vp_sx * math.cos(gradi2radianti(prora_sx)) + vc * math.cos(gradi2radianti(dc))
        y_sx = vp_sx * math.sin(gradi2radianti(prora_sx)) + vc * math.sin(gradi2radianti(dc))
        rotta_vera_sx = angolo_360(radianti2gradi(math.atan2(y_sx, x_sx)))

        x_dx = vp_dx * math.cos(gradi2radianti(prora_dx)) + vc * math.cos(gradi2radianti(dc))
        y_dx = vp_dx * math.sin(gradi2radianti(prora_dx)) + vc * math.sin(gradi2radianti(dc))
        rotta_vera_dx = angolo_360(radianti2gradi(math.atan2(y_dx, x_dx)))

        if in_range(rotta_vera_sx, rotta_vera_dx, angolo_bb):
            beta = angolo_360(angolo_bb - rotta_vera_sx)
            alpha = angolo_360(rotta_vera_dx - angolo_bb)

            ve_sx = math.sqrt(x_sx**2 + y_sx**2)
            ve_dx = math.sqrt(x_dx**2 + y_dx**2)

            vmg_sx = ve_sx * math.cos(gradi2radianti(beta))
            vmg_dx = ve_dx * math.cos(gradi2radianti(alpha))

            angolo_intermedio = gradi2radianti(180 - alpha - beta)
            dist_layline_sx = distanza / math.sin(angolo_intermedio) * math.sin(gradi2radianti(alpha))
            dist_layline_dx = distanza / math.sin(angolo_intermedio) * math.sin(gradi2radianti(beta))

            tempo_sx = dist_layline_sx / ve_sx
            tempo_dx = dist_layline_dx / ve_dx
            tempo_totale = tempo_sx + tempo_dx
            ore, minuti = ore_minuti(tempo_totale)
            ore_sx, minuti_sx = ore_minuti(tempo_sx)
            ore_dx, minuti_dx = ore_minuti(tempo_dx)

            intercetto_sx_lat = lat_barca + (dist_layline_sx * math.cos(gradi2radianti(rotta_vera_sx))) / 60
            intercetto_sx_lon = lon_barca + (dist_layline_sx * math.sin(gradi2radianti(rotta_vera_sx))) / (60 * math.cos(gradi2radianti(lat_barca)))
            intercetto_dx_lat = lat_barca + (dist_layline_dx * math.cos(gradi2radianti(rotta_vera_dx))) / 60
            intercetto_dx_lon = lon_boa + (dist_layline_dx * math.sin(gradi2radianti(rotta_vera_dx))) / (60 * math.cos(gradi2radianti(lat_barca)))

            print(f"Vai di: {settore}")
            print(f"Lato sinistro → Prora:{round(prora_sx, 2)}°, Rotta:{round(rotta_vera_sx, 2)}°, Ve: {round(ve_sx, 2)} nodi, VMG: {round(vmg_sx, 2)} nodi, → layline: {round(dist_layline_sx, 2)} NM,{ore_sx} ore e {minuti_sx} minuti ")
            print(f"Lato destro → Prora:{round(prora_dx, 2)}°, Rotta:{round(rotta_vera_dx, 2)}°, Ve: {round(ve_dx, 2)} nodi, VMG: {round(vmg_dx, 2)} nodi, → layline: {round(dist_layline_dx, 2)} NM,{ore_dx} ore e {minuti_dx} minuti ")
            print(f"Tempo totale stimato: {ore} ore e {minuti} minuti, Distanza bordi: {round((dist_layline_sx+dist_layline_dx), 2)} NM")
            print(f"Intercetto layline sx: lat {round(intercetto_sx_lat, 3)}, lon {round(intercetto_sx_lon, 3)}")
            print(f"Intercetto layline dx: lat {round(intercetto_dx_lat, 3)}, lon {round(intercetto_dx_lon, 3)}")

        else: settore = "Dx - Mura a Sinistra", "Sx - Mura a Dritta"

    if settore in ["Dx - Mura a Sinistra", "Sx - Mura a Dritta"]:

       
        numeratore = vc * math.sin(gradi2radianti(dc - angolo_bb))
        denominatore = vp - vc * math.cos(gradi2radianti(dc - angolo_bb))
        prora_vera = angolo_360(angolo_bb + radianti2gradi(math.atan2(numeratore, denominatore)))
        x_ve = vp * math.cos(gradi2radianti(prora_vera)) + vc * math.cos(gradi2radianti(dc))
        y_ve = vp * math.sin(gradi2radianti(prora_vera)) + vc * math.sin(gradi2radianti(dc))
        ve = math.sqrt(x_ve**2 + y_ve**2)
        distanza_totale = distanza
        tempo_ore = distanza_totale / ve
        ore, minuti = ore_minuti(tempo_ore)

        print(f"Vai di: {settore}")
        print(f"Prora: {round(prora_vera, 2)}°, Rotta:{round(angolo_bb, 2)}° ")
        print(f"Ve: {round(ve, 2)} nodi| Vp: {round(vp, 2)} nodi ")
        print(f"Distanza Totale: {round(distanza_totale, 2)} NM|Tempo stimato: {ore} ore e {minuti} minuti")

    

# === Dizionario programmi ===
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
    },
    "Studio_campo_con_Ve_e_Rv": {
        "input": ["lat_barca", "lon_barca", "lat_boa", "lon_boa", "ve_sx", "rotta_vera_sx", "ve_dx", "rotta_vera_dx"],
        "output": [],
        "funzione": studio_campo
    },
    "Studio_campo_con_Vento_e_corrente": {
        "input": [
            "lat_barca", "lon_barca", "lat_boa", "lon_boa",
            "angolo_vento", "angolo_bolina_sx", "angolo_bolina_dx",
            "angolo_poppa_sx", "angolo_poppa_dx", "vp_sx","vp_dx", "vc", "dc"
        ],
        "output": [],
        "funzione": studio_campo_con_vento_e_corrente
    }
}

# === Selezione e input ===

if __name__ == "__main__":
    print("\n=== Seleziona un programma di calcolo ===")
    lista_programmi = list(programmi.keys())
    for idx, nome_prog in enumerate(lista_programmi, start=1):
        print(f"[{idx}] {nome_prog}")
    scelta = input("Scegli un numero (default 1): ").strip()

    if scelta == "":
        index = 0
    else:
        try:
            index = int(scelta) - 1
        except ValueError:
            print("❌ Inserisci un numero valido. Esco.")
            exit()

    if index < 0 or index >= len(lista_programmi):
        print("❌ Selezione fuori range. Esco.")
        exit()

    nome_selezionato = lista_programmi[index]
    programma = programmi[nome_selezionato]

    print(f"\n=== Inserisci i dati per '{nome_selezionato}' ===")
    for nome_input in programma["input"]:
        var = defaults[nome_input]
        valore = input(f"{nome_input.replace('_', ' ').capitalize()} [{var.valore}]: ").strip()
        if valore != "":
            try:
                var.valore = float(valore)
            except ValueError:
                print(f"⚠️ Valore non valido per {nome_input}, mantenuto il precedente.")

    # === Esecuzione ===
    print(f"\n⚙️ Eseguo: {nome_selezionato}")
    programma["funzione"](defaults)



    # === Salvataggio ===
    with open(file_input, "w") as f:
        json.dump({k: v.valore for k, v in defaults.items()}, f, indent=4)

    input("\nPremi INVIO per uscire...")



