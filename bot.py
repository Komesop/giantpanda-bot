import os
import logging
import sqlite3
import requests
from datetime import datetime

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
GOOGLE_AI_API_KEY = os.environ.get("GOOGLE_AI_API_KEY", "")
DB_PATH = "storage.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        task TEXT,
        done BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS preferences (
        user_id INTEGER PRIMARY KEY,
        work_start TEXT,
        work_end TEXT,
        training_days TEXT,
        goal TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS stats (
        user_id INTEGER PRIMARY KEY,
        weight REAL,
        date_logged TEXT
    )
    """)

    conn.commit()
    conn.close()


def get_user_prefs(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT work_start, work_end, training_days, goal FROM preferences WHERE user_id = ?",
        (user_id,),
    )
    row = c.fetchone()
    conn.close()

    if row:
        return {
            "work_start": row[0],
            "work_end": row[1],
            "training_days": row[2],
            "goal": row[3],
        }

    return {
        "work_start": "08:30",
        "work_end": "17:00",
        "training_days": "ma,woe,vrij,zon",
        "goal": "spieropbouw + licht afvallen",
    }


def get_user_stats(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT weight, date_logged FROM stats WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()

    if row:
        return {"weight": row[0], "date_logged": row[1]}

    return None


def set_user_weight(user_id, weight):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        INSERT OR REPLACE INTO stats (user_id, weight, date_logged)
        VALUES (?, ?, ?)
        """,
        (user_id, weight, datetime.now().strftime("%Y-%m-%d")),
    )
    conn.commit()
    conn.close()


def ask_google_ai(prompt: str) -> str:
    if not GOOGLE_AI_API_KEY:
        return "Google AI API key is niet ingesteld in Render."

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/gemini-2.5-flash:generateContent?key={GOOGLE_AI_API_KEY}"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 800,
        },
    }

    try:
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        logging.exception("Google AI fout")
        return f"Er ging iets mis met de AI: {e}"

async def send_text(target, text, reply_markup=None):
    text = text or "Geen antwoord."
    chunks = [text[i:i + 3900] for i in range(0, len(text), 3900)]

    for i, chunk in enumerate(chunks):
        if hasattr(target, "edit_text") and i == 0:
            await target.edit_text(chunk, reply_markup=reply_markup)
        elif hasattr(target, "reply_text"):
            await target.reply_text(chunk, reply_markup=reply_markup)
        else:
            await target.message.reply_text(chunk, reply_markup=reply_markup)


def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🍽 Voeding", callback_data="voeding")],
        [InlineKeyboardButton("💪 Sport", callback_data="sport")],
        [InlineKeyboardButton("📅 Dagplan", callback_data="dagplan")],
        [InlineKeyboardButton("🧠 Mindset", callback_data="mindset")],
        [InlineKeyboardButton("🤝 Social", callback_data="social")],
        [InlineKeyboardButton("✅ Taken", callback_data="todo_menu")],
        [InlineKeyboardButton("💬 Chat met coach", callback_data="chat_mode")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    prefs = get_user_prefs(user_id)
    stats = get_user_stats(user_id)

    weight_text = f"Gewicht: {stats['weight']} kg" if stats else "Gewicht: nog niet ingevuld"

    await update.message.reply_text(
        f"Hey {update.effective_user.first_name}, ik ben je persoonlijke coach.\n\n"
        f"Werkdag: {prefs['work_start']}–{prefs['work_end']}\n"
        f"Training: {prefs['training_days']}\n"
        f"Doel: {prefs['goal']}\n"
        f"{weight_text}\n\n"
        f"Kies een onderwerp of stuur een bericht om te chatten.",
        reply_markup=main_menu(),
    )


async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    stats = get_user_stats(user_id)

    if stats:
        text = f"📊 Jouw stats:\n\nGewicht: {stats['weight']} kg\nLaatst bijgewerkt: {stats['date_logged']}"
    else:
        text = "Je hebt nog geen stats ingevuld.\n\nGebruik: /gewicht 85"

    await update.message.reply_text(text)


async def set_weight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Gebruik: /gewicht 85")
        return

    try:
        weight = float(context.args[0])

        if weight < 30 or weight > 300:
            await update.message.reply_text("Vul een realistisch gewicht in tussen 30 en 300 kg.")
            return

        set_user_weight(update.effective_user.id, weight)
        await update.message.reply_text(f"✅ Gewicht opgeslagen: {weight} kg")
    except ValueError:
        await update.message.reply_text("Vul alleen een getal in. Voorbeeld: /gewicht 85")


async def voeding(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    prefs = get_user_prefs(user_id)
    stats = get_user_stats(user_id)

    weight = stats["weight"] if stats else 80
    protein_goal = round(weight * 2)

    prompt = f"""
Je bent een Nederlandse voedingscoach.
Doel: spieropbouw met licht afvallen.
Werkdag: {prefs['work_start']} tot {prefs['work_end']}.
Gewicht: {weight} kg.
Eiwitdoel: {protein_goal}g per dag.

Maak een praktisch voedingsschema met:
- ontbijt
- lunch
- tussendoortje
- diner

Geef per maaltijd:
- wat eten
- calorieën
- eiwitten

Houd het kort en concreet.
"""

    answer = ask_google_ai(prompt)
    target = update.callback_query.message if update.callback_query else update.message
    await send_text(target, f"🍽 Voedingsschema:\n\n{answer}")


async def sport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    prefs = get_user_prefs(user_id)

    prompt = f"""
Je bent een Nederlandse sportcoach.
Doel: {prefs['goal']}.
Trainingsdagen: {prefs['training_days']}.
Werkdag: {prefs['work_start']} tot {prefs['work_end']}.

Maak een 4-daags fitnessschema van 60-75 minuten.
Focus op compound oefeningen.
Geef per dag spiergroepen, oefeningen, sets en reps.
Houd het praktisch.
"""

    answer = ask_google_ai(prompt)
    target = update.callback_query.message if update.callback_query else update.message
    await send_text(target, f"💪 Workout schema:\n\n{answer}")


async def dagplan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    prefs = get_user_prefs(user_id)
    stats = get_user_stats(user_id)
    weight = stats["weight"] if stats else 80

    prompt = f"""
Je bent een Nederlandse productiviteitscoach.

Maak een realistisch dagplan voor:
- Werkdag: {prefs['work_start']} tot {prefs['work_end']}
- Doel: {prefs['goal']}
- Gewicht: {weight} kg
- Training: {prefs['training_days']}

Gebruik tijden.
Neem werkblokken, pauzes, maaltijden, training en afsluiting mee.
"""

    answer = ask_google_ai(prompt)
    target = update.callback_query.message if update.callback_query else update.message
    await send_text(target, f"📅 Dagplan:\n\n{answer}")


async def mindset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = """
Geef een korte Nederlandse mindset-tip voor vandaag.
Focus op consistentie, discipline en zelfvertrouwen.
Maximaal 4 zinnen.
Geen fluff.
"""

    answer = ask_google_ai(prompt)
    target = update.callback_query.message if update.callback_query else update.message
    await send_text(target, f"🧠 Mindset tip:\n\n{answer}")


async def social(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = """
Geef een concrete Nederlandse tip om sociale vaardigheden, netwerken of relaties te verbeteren.
Focus op één kleine actie die vandaag gedaan kan worden.
Maximaal 4 zinnen.
"""

    answer = ask_google_ai(prompt)
    target = update.callback_query.message if update.callback_query else update.message
    await send_text(target, f"🤝 Social tip:\n\n{answer}")


async def todo_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Nieuwe taak", callback_data="todo_add")],
        [InlineKeyboardButton("📋 Mijn taken", callback_data="todo_list")],
        [InlineKeyboardButton("⬅️ Terug", callback_data="back_main")],
    ])

    target = update.callback_query.message if update.callback_query else update.message
    await send_text(target, "✅ Takenlijst:", reply_markup=keyboard)


async def todo_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.edit_text(
        "Typ je taak met:\n\n/add Taakomschrijving"
    )


async def todo_add_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Gebruik: /add Taakomschrijving")
        return

    user_id = update.effective_user.id
    task = " ".join(context.args)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO todos (user_id, task) VALUES (?, ?)", (user_id, task))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"✅ Toegevoegd: {task}")


async def todo_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT id, task, done FROM todos WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,),
    )
    rows = c.fetchall()
    conn.close()

    if not rows:
        text = "Je hebt nog geen taken."
    else:
        text = "\n".join([
            f"{'✅' if done else '⬜'} {task} (id: {task_id})"
            for task_id, task, done in rows
        ])

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Terug", callback_data="todo_menu")]
    ])

    target = update.callback_query.message if update.callback_query else update.message
    await send_text(target, f"📋 Jouw taken:\n\n{text}", reply_markup=keyboard)


async def todo_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Gebruik: /done 3")
        return

    user_id = update.effective_user.id
    task_id = context.args[0]

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE todos SET done = 1 WHERE id = ? AND user_id = ?", (task_id, user_id))
    conn.commit()
    affected = c.rowcount
    conn.close()

    if affected:
        await update.message.reply_text(f"✅ Taak {task_id} voltooid.")
    else:
        await update.message.reply_text("❌ Taak niet gevonden.")


async def chat_coach(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    prefs = get_user_prefs(user_id)
    stats = get_user_stats(user_id)

    if not context.args:
        await update.message.reply_text("Gebruik: /chat jouw vraag")
        return

    message = " ".join(context.args)
    weight = stats["weight"] if stats else "onbekend"

    prompt = f"""
Je bent de persoonlijke coach van deze gebruiker.

Doel: {prefs['goal']}
Werkdag: {prefs['work_start']} tot {prefs['work_end']}
Training: {prefs['training_days']}
Gewicht: {weight}

Gebruiker zegt:
{message}

Reageer direct, concreet en ondersteunend.
Maximaal 5 zinnen.
"""

    answer = ask_google_ai(prompt)
    await update.message.reply_text(f"💬 Coach:\n\n{answer}")


async def handle_free_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    prefs = get_user_prefs(user_id)
    stats = get_user_stats(user_id)
    weight = stats["weight"] if stats else "onbekend"

    prompt = f"""
Je bent de persoonlijke coach van deze gebruiker.

Context:
- Doel: {prefs['goal']}
- Werkdag: {prefs['work_start']} tot {prefs['work_end']}
- Training: {prefs['training_days']}
- Gewicht: {weight}

Gebruiker schrijft:
{update.message.text}

Antwoord in het Nederlands.
Wees direct, concreet en praktisch.
Geen fluff.
"""

    answer = ask_google_ai(prompt)
    await update.message.reply_text(f"💬 Coach:\n\n{answer[:3900]}")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "voeding":
        await voeding(update, context)
    elif data == "sport":
        await sport(update, context)
    elif data == "dagplan":
        await dagplan(update, context)
    elif data == "mindset":
        await mindset(update, context)
    elif data == "social":
        await social(update, context)
    elif data == "todo_menu":
        await todo_menu(update, context)
    elif data == "todo_add":
        await todo_add(update, context)
    elif data == "todo_list":
        await todo_list(update, context)
    elif data == "chat_mode":
        await query.message.edit_text(
            "💬 Chat met coach is actief.\n\nStuur gewoon een bericht, of gebruik:\n/chat jouw vraag"
        )
    elif data == "back_main":
        await query.message.edit_text("Kies een onderwerp:", reply_markup=main_menu())


def main():
    if not BOT_TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN ontbreekt.")
        return

    init_db()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("voeding", voeding))
    application.add_handler(CommandHandler("sport", sport))
    application.add_handler(CommandHandler("dagplan", dagplan))
    application.add_handler(CommandHandler("mindset", mindset))
    application.add_handler(CommandHandler("social", social))
    application.add_handler(CommandHandler("todo", todo_menu))
    application.add_handler(CommandHandler("add", todo_add_cmd))
    application.add_handler(CommandHandler("done", todo_done))
    application.add_handler(CommandHandler("chat", chat_coach))
    application.add_handler(CommandHandler("stats", stats_cmd))
    application.add_handler(CommandHandler("gewicht", set_weight))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_free_text))

    print("Coach bot gestart...")
    application.run_polling()


if __name__ == "__main__":
    main()
