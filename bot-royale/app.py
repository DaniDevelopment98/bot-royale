import requests
from flask import Flask, jsonify

app = Flask(__name__)

# --- CONFIGURA AQUI ---
TOKEN_ROYALE = "AQUI_VA_TU_TOKEN_DE_CLASH_ROYALE"  # de developer.clashroyale.com
MI_TAG = "8Q9GPQQYP"  # el tuyo sin #
# ----------------------

@app.route("/")
def home():
    return f"Bot Royale Online! Prueba /perfil/{MI_TAG} o /myip"

@app.route("/myip")
def myip():
    # Este endpoint es para saber la IP que Render usa para salir a internet
    try:
        ip = requests.get("https://ifconfig.me", timeout=5).text
        return jsonify({"tu_ip_de_render_es": ip, "copia_esta_ip_y_ponla_en_supercell": ip})
    except:
        return jsonify({"error": "no pude sacar ip"})

@app.route("/perfil/<tag>")
def perfil(tag):
    clean_tag = tag.replace("#", "").strip().upper()
    url = f"https://api.clashroyale.com/v1/players/%23{clean_tag}"
    headers = {"Authorization": f"Bearer {TOKEN_ROYALE}"}
    
    r = requests.get(url, headers=headers)
    
    if r.status_code == 403:
        return jsonify({
            "error": "IP no autorizada",
            "solucion": "Ve a /myip, copia la IP y ponla en developer.clashroyale.com",
            "status": r.status_code
        }), 403
    
    if r.status_code != 200:
        return jsonify({"error": r.text}), r.status_code
    
    data = r.json()
    
    # Mensaje bonito que usará WhatsApp después
    mensaje = {
        "name": data.get('name'),
        "tag": data.get('tag'),
        "trophies": data.get('trophies'),
        "bestTrophies": data.get('bestTrophies'),
        "level": data.get('expLevel'),
        "wins": data.get('wins'),
        "clan": data.get('clan', {}).get('name', 'Sin clan'),
        "whatsapp_message": f"👑 {data.get('name')} ({data.get('tag')})\n🏆 {data.get('trophies')} copas | Record: {data.get('bestTrophies')}\n🛡️ Clan: {data.get('clan', {}).get('name', 'Sin clan')}"
    }
    return jsonify(mensaje)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)