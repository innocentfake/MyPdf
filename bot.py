import os
import fitz  # PyMuPDF for PDF compression
import asyncio
from pyrogram import Client, filters
from fastapi import FastAPI
import uvicorn
from config import API_ID, API_HASH, BOT_TOKEN

# Initialize Telegram Bot
app = Client("@Pdf_sectbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# FastAPI Web Server (Required for Render Deployment)
web_server = FastAPI()

@web_server.get("/")
async def home():
    return {"status": "Bot is running!"}

# Ensure downloads folder exists
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# Function to compress PDFs
def compress_pdf(input_path, output_path, quality="medium"):
    doc = fitz.open(input_path)
    doc.save(output_path, garbage=4, deflate=True, clean=True, compress=9 if quality == "low" else 5)
    doc.close()

# Start Command
@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        "👋 Hello! I am a PDF Compressor Bot. 📄\n"
        "Just send me a **PDF file**, and I'll compress it for you! 📉\n\n"
        "Use /help for more details."
    )

# Help Command
@app.on_message(filters.command("help"))
async def help_command(client, message):
    await message.reply_text(
        "📌 **How to Use This Bot:**\n"
        "1️⃣ Send me a **PDF file**.\n"
        "2️⃣ I will **compress** the file and send it back.\n"
        "3️⃣ If the file is too large, I may take some time to process.\n\n"
        "🔹 Available Commands:\n"
        "/start - Welcome Message\n"
        "/compress - Upload PDF for compression\n"
        "/about - Info about this bot\n\n"
        "🚀 Send a **PDF now**, and I'll compress it!"
    )

# About Command
@app.on_message(filters.command("about"))
async def about_command(client, message):
    await message.reply_text(
        "🤖 **PDF Compressor Bot**\n"
        "🔹 Compress PDF files with high efficiency.\n"
        "🔹 Supports different compression levels.\n\n"
        "👨‍💻 Developed by: @LetsChatbro\n"
        "🤩 Main Channel: @Manga_Sect\n"
        "⚡ Fast & Free to use!"
    )

# Handle PDF Uploads & Compression
@app.on_message(filters.document)
async def pdf_handler(client, message):
    if not message.document.file_name.endswith(".pdf"):
        await message.reply_text("❌ Please send a valid PDF file.")
        return

    await message.reply_text("📥 Downloading your PDF...")

    pdf_path = f"downloads/{message.document.file_id}.pdf"
    compressed_pdf_path = f"downloads/compressed_{message.document.file_id}.pdf"

    await message.download(pdf_path)

    await message.reply_text("🔄 Compressing your PDF...")
    compress_pdf(pdf_path, compressed_pdf_path, "medium")

    await message.reply_document(compressed_pdf_path, caption="Here is your compressed PDF 📄✨")

    os.remove(pdf_path)
    os.remove(compressed_pdf_path)

# Start Telegram Bot & Web Server for Render
async def main():
    await app.start()
    print("Bot started!")
    import os
PORT = int(os.environ.get("PORT", 8080))  
config = uvicorn.Config(web_server, host="0.0.0.0", port=PORT)

    server = uvicorn.Server(config)
    await server.serve()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
