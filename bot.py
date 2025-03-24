import os
import fitz  # PyMuPDF
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN

# Initialize bot
app = Client("pdf_compressor_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Ensure downloads folder exists
if not os.path.exists("downloads"):
    os.makedirs("downloads")

# Function to compress PDF with different quality levels
def compress_pdf(input_path, output_path, quality):
    doc = fitz.open(input_path)

    if quality == "low":
        doc.save(output_path, garbage=4, deflate=True, clean=True, compress=9)
    elif quality == "medium":
        doc.save(output_path, garbage=3, deflate=True, clean=True, compress=5)
    else:  # high quality (default)
        doc.save(output_path, garbage=2, deflate=True, clean=True, compress=3)

    doc.close()

# Handle PDF files sent by users
@app.on_message(filters.document & filters.file_extension("pdf"))
async def pdf_handler(client, message):
    await message.reply_text(
        "📥 Send a number to choose compression level:\n\n"
        "1️⃣ Low (max compression, lower quality)\n"
        "2️⃣ Medium (balanced compression)\n"
        "3️⃣ High (minimum compression, best quality)\n\n"
        "Reply with 1, 2, or 3."
    )

    # Wait for user reply
    user_reply = await app.listen(message.chat.id, timeout=30)
    quality_choice = user_reply.text.strip()

    quality_map = {"1": "low", "2": "medium", "3": "high"}
    quality = quality_map.get(quality_choice, "medium")  # Default to medium

    await message.reply_text("📥 Downloading your PDF...")

    pdf_path = f"downloads/{message.document.file_id}.pdf"
    compressed_pdf_path = f"downloads/compressed_{message.document.file_id}.pdf"

    await message.download(pdf_path)

    await message.reply_text("🔄 Compressing your PDF...")
    compress_pdf(pdf_path, compressed_pdf_path, quality)

    new_filename = f"compressed_{message.document.file_name}"
    await message.reply_document(compressed_pdf_path, caption="Here is your compressed PDF 📄✨", file_name=new_filename)

    # Clean up files
    os.remove(pdf_path)
    os.remove(compressed_pdf_path)

# Run the bot
app.run()
