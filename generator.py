import os
import requests
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from groq import Groq

app = FastAPI()

# Map voor gegenereerde previews
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

TELEGRAM_BOT_TOKEN = "8639869806:AAElec-a0x28qDwGFqMRaEkFaWYek9b_2OQ"
TELEGRAM_CHAT_ID = "8414903602"
GROQ_API_KEY = "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"

groq_client = Groq(api_key=GROQ_API_KEY)

# 1. Contactformulier pagina (bezoeker ziet dit)
@app.get("/", response_class=HTMLResponse)
async def show_form():
    return """
    <!DOCTYPE html>
    <html lang="nl">
    <head>
        <meta charset="UTF-8">
        <title>Aanvraag Webdesign</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-950 text-slate-100 font-sans min-h-screen flex items-center justify-center p-4">
        <div class="max-w-md w-full bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
            <h1 class="text-2xl font-bold text-indigo-400 mb-2">Gratis Concept Ontwerp</h1>
            <p class="text-slate-400 text-sm mb-6">Vul je gegevens in en de AI genereert direct een eerste opzet.</p>
            
            <form action="/api/contact" method="POST" class="space-y-4">
                <div>
                    <label class="block text-xs text-slate-400 mb-1">Naam / Bedrijfsnaam</label>
                    <input type="text" name="naam" required class="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-white focus:outline-none focus:border-indigo-500">
                </div>
                <div>
                    <label class="block text-xs text-slate-400 mb-1">E-mail of Telefoonnummer</label>
                    <input type="text" name="contact_info" required class="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-white focus:outline-none focus:border-indigo-500">
                </div>
                <div>
                    <label class="block text-xs text-slate-400 mb-1">Wensen / Branche</label>
                    <textarea name="wensen" rows="3" placeholder="Bijv. Hoveniersbedrijf met een moderne, groene uitstraling..." class="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-white focus:outline-none focus:border-indigo-500"></textarea>
                </div>
                <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-3 rounded-lg transition">
                    Genereer Mijn Website
                </button>
            </form>
        </div>
    </body>
    </html>
    """

# 2. Verwerking van het formulier
@app.post("/api/contact")
async def handle_contact(
    naam: str = Form(...),
    contact_info: str = Form(...),
    wensen: str = Form("")
):
    print(f"📥 Nieuwe aanvraag van: {naam}")

    # AI opdracht
    prompt = f"""
    Je bent een top webdesigner. Maak een complete, schitterende, moderne landingpage met Tailwind CSS voor de klant '{naam}'.
    Wensen/branche: {wensen if wensen else 'Snel, modern en conversiegericht'}.
    Geef ENKEL en ALLEEN de geldige HTML code terug. Geen uitleg, geen markdown fences (geen ```html).
    """

    completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    generated_html = completion.choices[0].message.content

    # Preview opslaan als HTML-bestand
    clean_name = "".join(c for c in naam if c.isalnum() or c in (' ', '_')).rstrip().lower().replace(' ', '_')
    preview_filename = f"preview_{clean_name}.html"
    file_path = os.path.join("static", preview_filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(generated_html)

    # Stuur een simpele melding naar jou via Telegram
    telegram_text = (
        f"🚨 *Nieuwe Lead Binnengekomen!*\n\n"
        f"👤 *Naam:* {naam}\n"
        f"📞 *Contact:* {contact_info}\n"
        f"💬 *Wensen:* {wensen if wensen else 'Geen'}\n\n"
        f"🔗 *Preview gemaakt!*"
    )
    
    try:
        endpoint = f"[https://api.telegram.org/bot](https://api.telegram.org/bot){TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(endpoint, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": telegram_text,
            "parse_mode": "Markdown"
        })
    except Exception as e:
        print(f"Telegram melding mislukt: {e}")

    # Bedankpagina die direct de gemaakte preview toont
    return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html lang="nl">
        <head>
            <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
        </head>
        <body class="bg-slate-950 text-slate-100 font-sans flex flex-col items-center justify-center min-h-screen p-6">
            <div class="text-center max-w-md mx-auto mb-8">
                <div class="w-16 h-16 bg-indigo-600/20 text-indigo-400 rounded-full flex items-center justify-center text-3xl mx-auto mb-4">🚀</div>
                <h1 class="text-2xl font-bold text-indigo-400 mb-2">Bedankt, {naam}!</h1>
                <p class="text-slate-400 text-sm">Je conceptontwerp is succesvol gegenereerd.</p>
                <a href="/static/{preview_filename}" target="_blank" class="inline-block mt-4 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold px-6 py-2 rounded-lg transition">
                    Bekijk Je Preview Live ↗
                </a>
            </div>
        </body>
        </html>
    """)