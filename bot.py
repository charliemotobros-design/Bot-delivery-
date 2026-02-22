from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN =8519663573:AAEP0dhvxZAeN5gLTNxzsfNakcfikM85q3c

GRUPO_COMERCIO = -1003810499805
GRUPO_ENTREGADORES = -1003899897131

pedidos_aceitos = set()

async def encaminhar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id == GRUPO_COMERCIO:
        mensagem = update.message.text
        
        keyboard = [[InlineKeyboardButton("🚀 ACEITAR CORRIDA", callback_data=str(update.message.message_id))]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(
            chat_id=GRUPO_ENTREGADORES,
            text=f"📦 NOVO PEDIDO\n\n{mensagem}",
            reply_markup=reply_markup
        )

async def aceitar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data in pedidos_aceitos:
        return

    pedidos_aceitos.add(query.data)

    await query.edit_message_text("✅ CORRIDA ACEITA\n\n🛵 Um entregador já está a caminho!")

    await context.bot.send_message(
        chat_id=GRUPO_COMERCIO,
        text="🛵 Um entregador já aceitou o pedido!"
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, encaminhar))
app.add_handler(CallbackQueryHandler(aceitar))

app.run_polling()
