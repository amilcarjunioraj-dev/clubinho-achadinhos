import requests
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import os

# ============ CONFIGURAÇÕES ============
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "SEU_TOKEN_AQUI")
TELEGRAM_CANAL = os.environ.get("TELEGRAM_CANAL", "@clubinhodeachados")
AFILIO_TOKEN = os.environ.get("AFILIO_TOKEN", "SEU_TOKEN_AFILIO")
AFILIO_ID = os.environ.get("AFILIO_ID", "SEU_ID_AFILIO")
INTERVALO_HORAS = 1

logging.basicConfig(level=logging.INFO)

# ============ OFERTAS SIMULADAS (substitui pela Afilio quando aprovar) ============
OFERTAS_SIMULADAS = [
    {"nome": "Airfryer Mondial 4L 1500W", "preco": "R$ 189,90", "preco_old": "R$ 299,90", "desconto": 37, "link": "https://amazon.com.br", "emoji": "🍟"},
    {"nome": "Fone Bluetooth JBL Tune 510BT", "preco": "R$ 179,00", "preco_old": "R$ 259,00", "desconto": 31, "link": "https://amazon.com.br", "emoji": "🎧"},
    {"nome": "Perfume 212 Men NYC 100ml", "preco": "R$ 219,00", "preco_old": "R$ 380,00", "desconto": 42, "link": "https://amazon.com.br", "emoji": "🌸"},
    {"nome": "Smartwatch Samsung Galaxy Watch 6", "preco": "R$ 899,00", "preco_old": "R$ 1.299,00", "desconto": 31, "link": "https://amazon.com.br", "emoji": "⌚"},
    {"nome": "Kit Skincare Vitamina C Neutrogena", "preco": "R$ 89,90", "preco_old": "R$ 139,90", "desconto": 36, "link": "https://amazon.com.br", "emoji": "✨"},
]

indice_oferta = 0

def buscar_oferta():
    global indice_oferta
    # Quando a Afilio aprovar, substitui essa função pela busca real
    oferta = OFERTAS_SIMULADAS[indice_oferta % len(OFERTAS_SIMULADAS)]
    indice_oferta += 1
    return oferta

def montar_mensagem(oferta):
    texto = (
        f"🚨 *OFERTA DO DIA* 🚨\n\n"
        f"{oferta['emoji']} *{oferta['nome']}*\n\n"
        f"❌ De: ~{oferta['preco_old']}~\n"
        f"✅ Por: *{oferta['preco']}*\n"
        f"💥 *{oferta['desconto']}% de desconto!*\n\n"
        f"⚠️ Estoque limitado — aproveite agora!"
    )
    teclado = [[InlineKeyboardButton("🛒 GARANTIR OFERTA", url=oferta['link'])]]
    return texto, InlineKeyboardMarkup(teclado)

async def postar_oferta(app):
    try:
        oferta = buscar_oferta()
        texto, markup = montar_mensagem(oferta)
        await app.bot.send_message(
            chat_id=TELEGRAM_CANAL,
            text=texto,
            parse_mode="Markdown",
            reply_markup=markup
        )
        logging.info(f"✅ Postado: {oferta['nome']}")
    except Exception as e:
        logging.error(f"❌ Erro ao postar: {e}")

async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(postar_oferta, 'interval', hours=INTERVALO_HORAS, args=[app])
    scheduler.start()
    logging.info("🚀 Bot iniciado!")
    await app.initialize()
    await app.start()
    # Posta imediatamente ao iniciar
    await postar_oferta(app)
    # Mantém rodando
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    asyncio.run(main())