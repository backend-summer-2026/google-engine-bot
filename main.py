import os

import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()

TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Search Bot ga xush kelibsiz! nima qidirmoqchisiz?")


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "api_key": API_KEY,
        "q": update.message.text
    }
    response = requests.get(url=url, params=params)

    knowledge_graph = response.json().get("knowledge_graph", {})

    title = knowledge_graph.get("title", "Unknown")
    entity_type = knowledge_graph.get("type", "")
    description = knowledge_graph.get("description", "")
    born = knowledge_graph.get("born", "Unknown")
    died = knowledge_graph.get("died", "Unknown")
    spouse = knowledge_graph.get("spouse")
    parents = knowledge_graph.get("parents")
    children = knowledge_graph.get("children")
    burial = knowledge_graph.get("place_of_burial")

    text = f"""👤 <b>{title}</b>

    🏷 <b>Type:</b> {entity_type}

    📝 <b>Description:</b>
    {description}

    📅 <b>Born:</b> {born}
    ⚰️ <b>Died:</b> {died}
    """

    if spouse:
        text += f"\n💍 <b>Spouse:</b> {spouse}"

    if parents:
        text += f"\n👨‍👩‍👦 <b>Parents:</b> {parents}"

    if children:
        text += f"\n👶 <b>Children:</b> {children}"

    if burial:
        text += f"\n🏛 <b>Burial:</b> {burial}"

    source = knowledge_graph.get("source", {})
    if source.get("link"):
        text += f"\n\n🔗 <a href='{source['link']}'>Read more</a>"

    await update.message.reply_html(text)


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(filters.TEXT, search))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
