import os
import sys
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

sys.path.append(os.path.dirname(__file__))

from marketing_content import get_marketing_content
import storage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_MODE = os.environ.get("BOT_MODE", "combined").lower()


def get_mode():
    if BOT_MODE not in ("marketing", "personal", "combined"):
        return "combined"
    return BOT_MODE


def marketing_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Judith (ZZP)", callback_data="m_persona_judith")],
        [InlineKeyboardButton("Rick (ZZP Plus)", callback_data="m_persona_rick")],
        [InlineKeyboardButton("Alex (Scale-up)", callback_data="m_persona_alex")],
        [InlineKeyboardButton("Victor (Enterprise)", callback_data="m_persona_victor")],
        [InlineKeyboardButton("Brand overzicht", callback_data="m_brand")],
        [InlineKeyboardButton("FAQ", callback_data="m_faq")],
    ])


def personal_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Mijn doelen", callback_data="p_goals")],
        [InlineKeyboardButton("Dagelijkse check-in", callback_data="p_checkin")],
        [InlineKeyboardButton("Mijn voortgang", callback_data="p_progress")],
        [InlineKeyboardButton("Nieuw doel", callback_data="p_new_goal")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = get_mode()

    if mode == "marketing":
        await update.message.reply_text(
            "Welkom bij Giantpanda Marketing Bot.\n\nKies een persona of onderdeel:",
            reply_markup=marketing_menu(),
        )
    elif mode == "personal":
        await update.message.reply_text(
            "Welkom bij je persoonlijke helper.\n\nWat wil je doen?",
            reply_markup=personal_menu(),
        )
    else:
        await update.message.reply_text(
            "Welkom! Kies een modus:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Marketing", callback_data="mode_marketing_enter")],
                [InlineKeyboardButton("Personal", callback_data="mode_personal_enter")],
            ]),
        )


async def mode_enter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "mode_marketing_enter":
        await query.edit_message_text(
            "Je bent nu in Marketing mode.\n\nKies een persona of onderdeel:",
            reply_markup=marketing_menu(),
        )
    elif query.data == "mode_personal_enter":
        await query.edit_message_text(
            "Je bent nu in Personal mode.\n\nWat wil je doen?",
            reply_markup=personal_menu(),
        )


async def marketing_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "m_brand":
        brand = get_marketing_content("brand")
        txt = (
            f"BRAND: {brand['naam']}\n"
            f"Positionering: {brand['positionering']}\n"
            f"Headline: {brand['headline']}\n"
            f"Trefwoorden: {', '.join(brand['trefwoorden'])}\n"
            f"Tonality: {brand['tonality']}"
        )
        await query.edit_message_text(txt, reply_markup=marketing_menu())

    elif data == "m_faq":
        faqs = get_marketing_content("faq_generiek")
        txt = "FAQ\n\n"
        for i, faq in enumerate(faqs, 1):
            txt += f"V{i}: {faq['vraag']}\nA: {faq['antwoord']}\n\n"
        await query.edit_message_text(txt, reply_markup=marketing_menu())

    elif data.startswith("m_persona_"):
        persona_key = data.replace("m_persona_", "")
        personas = get_marketing_content("personas")

        if persona_key not in personas:
            await query.edit_message_text("Persona niet gevonden.", reply_markup=marketing_menu())
            return

        p = personas[persona_key]
        txt = (
            f"{persona_key.upper()} — {p['naam']}\n\n"
            f"Verkoopstraal: {p['verkoopstraal']}\n"
            f"Branche: {p['branche']}\n"
            f"Grootte: {p['bedrijfsgrootte']} | Omzet: {p['omzet']}\n"
            f"Technisch: {p['technisch']}\n\n"
            f"Pijnpunten: {', '.join(p['pijnpunten'])}\n"
            f"Verlangens: {', '.join(p['verlangens'])}\n"
            f"False beliefs: {', '.join(p['false_beliefs'])}\n"
            f"CTA-stijl: {p['cta_stijl']}\n"
        )

        lps = get_marketing_content("lp_teksten")

        if persona_key in lps:
            lp = lps[persona_key]
            hooks = get_marketing_content("hooks")

            if persona_key in hooks:
                txt += "\nHooks:\n"
                txt += "\n".join([f"- {h}" for h in hooks[persona_key]])

            if "hero" in lp:
                h = lp["hero"]
                txt += f"\n\nHERO:\nKop: {h['kop']}\nSubkop: {h['subkop']}\n"

                if "voordelen" in h:
                    txt += "\n".join([f"- {v}" for v in h["voordelen"]]) + "\n"

                if "ctas" in h:
                    txt += f"CTAs: {', '.join(h['ctas'])}\n"
                elif "cta" in h:
                    txt += f"CTA: {h['cta']}\n"

            if "social_proof" in lp:
                txt += "\nSocial proof:\n"
                for sp in lp["social_proof"]:
                    metric = sp.get("metric") or sp.get("metrics") or ""
                    txt += f"- {sp['naam']}: {sp['quote']} [{metric}]\n"

            if "faq" in lp:
                txt += "\nFAQ:\n"
                for faq in lp["faq"]:
                    txt += f"V: {faq['vraag']}\nA: {faq['antwoord']}\n\n"

        await query.edit_message_text(txt[:4000], reply_markup=marketing_menu())


async def personal_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == "p_goals":
        goals = storage.get_goals(user_id)

        if not goals:
            await query.edit_message_text(
                "Je hebt nog geen doelen. Gebruik 'Nieuw doel' om er een toe te voegen.",
                reply_markup=personal_menu(),
            )
            return

        txt = "Mijn doelen:\n\n"
        for goal_id, title, status in goals:
            txt += f"- [{status}] {title}\n"

        await query.edit_message_text(txt, reply_markup=personal_menu())

    elif data == "p_checkin":
        await query.edit_message_text(
            "Hoe gaat het?\n\nKies je mood:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Goed 🔥", callback_data="checkin_goed")],
                [InlineKeyboardButton("Matig 😐", callback_data="checkin_matig")],
                [InlineKeyboardButton("Slecht 😔", callback_data="checkin_slecht")],
                [InlineKeyboardButton("Terug", callback_data="mode_personal_enter")],
            ]),
        )

    elif data == "p_progress":
        checkins = storage.get_recent_checkins(user_id, limit=7)

        if not checkins:
            await query.edit_message_text(
                "Nog geen check-ins. Start met een dagelijkse check-in.",
                reply_markup=personal_menu(),
            )
            return

        txt = "Laatste 7 check-ins:\n\n"
        for mood, note, date in checkins:
            txt += f"[{date}] {mood}: {note}\n"

        await query.edit_message_text(txt, reply_markup=personal_menu())

    elif data == "p_new_goal":
        await query.edit_message_text(
            "Stuur je doel in dit format:\n\nTitel | Beschrijving\n\nVoorbeeld: 10 nieuwe klanten | Door Giantpanda leads op te laten volgen",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Terug", callback_data="mode_personal_enter")]
            ]),
        )
        context.user_data["awaiting_goal"] = True


async def checkin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    mood = query.data.replace("checkin_", "")
    mood_label = {
        "goed": "Goed 🔥",
        "matig": "Matig 😐",
        "slecht": "Slecht 😔",
    }.get(mood, mood)

    await query.edit_message_text(
        f"Mood: {mood_label}\n\nStuur een korte notitie:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Terug", callback_data="mode_personal_enter")]
        ]),
    )

    context.user_data["awaiting_checkin"] = True
    context.user_data["checkin_mood"] = mood_label


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if context.user_data.get("awaiting_goal"):
        text = update.message.text.strip()

        if "|" in text:
            title, desc = text.split("|", 1)
            title = title.strip()
            desc = desc.strip()
        else:
            title = text
            desc = ""

        storage.add_goal(user_id, title, desc)
        context.user_data["awaiting_goal"] = False

        await update.message.reply_text(f"Doel toegevoegd: {title}")
        return

    if context.user_data.get("awaiting_checkin"):
        mood = context.user_data.get("checkin_mood", "Onbekend")
        note = update.message.text.strip()

        storage.add_checkin(user_id, mood, note)
        context.user_data["awaiting_checkin"] = False

        await update.message.reply_text("Check-in opgeslagen. Tot morgen!")
        return

    await update.message.reply_text("Gebruik /start om te beginnen of kies een optie uit het menu.")


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")

    if not token:
        print("ERROR: Zet je bot-token in TELEGRAM_BOT_TOKEN")
        sys.exit(1)

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(mode_enter, pattern=r"^mode_"))
    application.add_handler(CallbackQueryHandler(marketing_callback, pattern=r"^m_"))
    application.add_handler(CallbackQueryHandler(personal_callback, pattern=r"^p_"))
    application.add_handler(CallbackQueryHandler(checkin_handler, pattern=r"^checkin_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot gestart...")
    application.run_polling()


if __name__ == "__main__":
    main()
