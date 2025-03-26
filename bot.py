import requests
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = "7866619287:AAE6VHhgm8zJPBKjFjFTelo5pJIJEnudmx8"

# API Function
def fetch_compatibility(rasi1, natchathiram1, rasi2, natchathiram2):
    api_url = "https://astroapi.com/match"
    params = {
        "bride_rasi": rasi1,
        "bride_natchathiram": natchathiram1,
        "groom_rasi": rasi2,
        "groom_natchathiram": natchathiram2
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["match_score"], data["description"]
    else:
        return None, "மன்னிக்கவும், API-ல் இருந்து தகவல் பெற முடியவில்லை."

# PDF Function
from fpdf import FPDF
def generate_pdf(rasi1, natchathiram1, rasi2, natchathiram2, match_score, description):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Thirumana Porutham Report", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"மணமகன்: {rasi1} - {natchathiram1}", ln=True)
    pdf.cell(200, 10, txt=f"மணமகள்: {rasi2} - {natchathiram2}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"🔢 Matching Score: {match_score}/10", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=f"🔍 Detailed Analysis:\n{description}")
    filename = "thirumana_porutham.pdf"
    pdf.output(filename)
    return filename

# Command Handlers
async def start(update: Update, context):
    await update.message.reply_text("🙏 வணக்கம்! ராசி மற்றும் நட்சத்திரம் உள்ளீடு செய்து திருமண பொருத்தம் பெறலாம்.")

async def match(update: Update, context):
    text = update.message.text.split()
    if len(text) < 5:
        await update.message.reply_text("உதாரணம்: /match Mesham Aswini Rishabam Rohini")
        return
    r1, n1, r2, n2 = text[1], text[2], text[3], text[4]
    score, desc = fetch_compatibility(r1, n1, r2, n2)
    if score:
        await update.message.reply_text(f"🔢 Matching Score: {score}/10\n🔍 {desc}")
    else:
        await update.message.reply_text(desc)

async def pdf_report(update: Update, context):
    text = update.message.text.split()
    if len(text) < 5:
        await update.message.reply_text("உதாரணம்: /pdf Mesham Aswini Rishabam Rohini")
        return
    r1, n1, r2, n2 = text[1], text[2], text[3], text[4]
    score, desc = fetch_compatibility(r1, n1, r2, n2)
    if score:
        file_path = generate_pdf(r1, n1, r2, n2, score, desc)
        await update.message.reply_document(document=open(file_path, "rb"))
    else:
        await update.message.reply_text(desc)

# Bot Setup
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("match", match))
app.add_handler(CommandHandler("pdf", pdf_report))

print("Bot is running...")
app.run_polling()
