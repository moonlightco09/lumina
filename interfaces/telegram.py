# Lumina by Moonlight Co
# interfaces/telegram.py - Telegram bot interface

import os
import sys
import asyncio
import logging
sys.path.insert(0, os.path.expanduser("~/lumina"))
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config.settings import NAME, MAKER, API_KEY, ALLOWED_TELEGRAM_USERS
from core.agent import respond, approve_command, deny_command, clear_session

logging.basicConfig(level=logging.WARNING)

pending = {}

def is_allowed(update: Update):
    user_id = str(update.effective_user.id)
    return user_id in ALLOWED_TELEGRAM_USERS

async def blocked(update: Update):
    await update.message.reply_text("⛔ Unauthorized.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return await blocked(update)
    await update.message.reply_text(
        f"🌙 Hello! I'm {NAME} by {MAKER}.\n\n"
        f"I'm your personal AI assistant.\n"
        f"Brain: {'Online (Claude API)' if API_KEY else 'Offline (Local Model)'}\n\n"
        f"Send me any message to get started!\n\n"
        f"Commands:\n"
        f"/new — start fresh conversation\n"
        f"/approve — approve pending command\n"
        f"/deny — deny pending command\n"
        f"/mode — check current brain mode"
    )

async def mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return await blocked(update)
    brain = "Online (Claude API)" if API_KEY else "Offline (Local Model)"
    await update.message.reply_text(f"🧠 Current brain: {brain}")

async def new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return await blocked(update)
    user_id = str(update.effective_user.id)
    clear_session(f"telegram:{user_id}")
    await update.message.reply_text("🌙 Session cleared! Starting fresh.")

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return await blocked(update)
    user_id = str(update.effective_user.id)
    if user_id in pending:
        cmd = pending.pop(user_id)
        result = await approve_command(cmd, f"telegram:{user_id}")
        await update.message.reply_text(f"✅ Approved and executed:\n`{result}`")
    else:
        await update.message.reply_text("No pending command to approve.")

async def deny(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return await blocked(update)
    user_id = str(update.effective_user.id)
    if user_id in pending:
        cmd = pending.pop(user_id)
        await deny_command(cmd, f"telegram:{user_id}")
        await update.message.reply_text("❌ Command denied and blocked.")
    else:
        await update.message.reply_text("No pending command to deny.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return await blocked(update)
    user_id = str(update.effective_user.id)
    user_input = update.message.text
    session_id = f"telegram:{user_id}"

    await update.message.reply_text("🌙 Thinking...")

    async def on_tool_use(tool_name, tool_input):
        await update.message.reply_text(f"🔧 Using: {tool_name}")

    result = await respond(user_input, session_id, on_tool_use)

    if result["type"] == "needs_approval":
        pending[user_id] = result["command"]
        await update.message.reply_text(result["message"])
    else:
        await update.message.reply_text(result["message"])

def run(token):
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("new", new))
    app.add_handler(CommandHandler("mode", mode))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CommandHandler("deny", deny))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print(f"🌙 Lumina Telegram Bot is running...")
    app.run_polling()
