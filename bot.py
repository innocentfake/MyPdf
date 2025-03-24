import os
import fitz  # PyMuPDF
import asyncio
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN
from fastapi import FastAPI
import uvicorn

# Initialize Telegram bot
app = Client("pdf_compressor_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Create FastAPI instance (dummy server for Render)
web_server = FastAPI()

@web_server.get("/")
async def home():
    return {"status": "Bot is running!"}

# Ensure downloads folder exists
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# Function to compress PDFs
def compress_pdf(input_path, output_path, quality):
    doc = fitz.open(input_path)
    doc.save(output_path, garbage=4, deflate=True, clean=True, compress=9 if quality == "low" else 5)
    doc.close()

# Handle PDF uploads
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

# Start both Telegram bot and FastAPI server
async def main():
    await app.start()
    print("Bot started!")
    config = uvicorn.Config(web_server, host="0.0.0.0", port=10000)
    server = uvicorn.Server(config)
    await server.serve()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
