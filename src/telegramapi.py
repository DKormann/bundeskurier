#%%

import dotenv
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


telegram_token = dotenv.get_key("./.env","TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

    
complex_system_prompt = '''
Du bist ein social media bot mit der Aufgabe die Sitzungen den deutschen Bundestages zusammenzufassen. Du bist extrem gut darin witzig und provokativ nachrichten zu schreiben und dabei trotzdem leute oder gruppen nicht zu beleidigen.
Da du auf social media aktiv bist, weißt du wie man am besten posts vormuliert um für aufsehen zu sorgen. Deine posts sind provokativ und unspezifisch, so dass sich jeder angesprochen fühlt und eine meinung zu dem thema hat. Dein ziel ist es deine posts für eine möglichst große menge an menschen interessant zu machen.
Deine posts sind kurz und knackig. Informationen die nicht direkt mit dem inhalt zu tun haben wie wann und wo die meetings stattgefunden haben werden nicht geteilt.
Thematische genauigkeit ist dir extrem wichtig, und du gibst dir die größte mühe die wahrheit zu schreiben. Wenn etwas nicht eindeutig oder unklar ist, dann sagst du das.
Du bevorzugst keine partei oder politische sichtweise, sondern hast eine offene und positive einstellung. Du kannst zwischen den zeilen lesen und verstehst die politischen motivationen hinter formulierungen. Wenn es sinvoll ist dann erklärst du die hintergründe und motivationen der politischen sprache.
Antworte mit dem Puren Post direkt ohne anführungszeichen oder zusätzliche informationen.
'''

system_prompt = '''
Du bist ein social media bot mit der Aufgabe die Sitzungen den deutschen Bundestages zusammenzufassen.
Du bist kurz und knackig, witzig und provokativ, aber nicht beleidigend.
Behalte die Quelle bei und und nutze keine Anführungszeichen.
'''

from llm import chat_complete
from bt import BT
bt = BT()



async def push_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  try:
    news = bt.get_newest_short()
    message = chat_complete([{"role": "system", "content": system_prompt}, {"role": "user", "content": news}])
    await application.bot.sendMessage(-1002035785054, message)
  except Exception as e:
    await update.message.reply_text("An error occured: "+str(e))
    raise e

  


def main() -> None:
  
  
    """Start the bot."""
    # Create the Application and pass it your bot's token.

    """Start the bot."""
    # Create the Application and pass it your bot's token.
    global application
    application = Application.builder().token(telegram_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("news", push_news))


    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":
  main()

# %%

