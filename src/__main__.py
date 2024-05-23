from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
import sys
import logging
from WeatherFactory import WeatherFactory
# puoi scegliere in base al provider


logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class TelegramBotManager():
    def __init__(self, token: str) -> None:  # generalizza il weather_class
        self.token = token

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "3BMeteo Bot: il bot che ti dice che tempo fa."
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Non avrai aiuto")

    async def meteo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if len(context.args) != 3:
            logger.error(f"Not enought arguments for weather command")
            await update.message.reply_text('Per favore fornisci sito_meteo città giorno ')
            return

        site, city, day = [arg.lower() for arg in context.args[:3]]

        weather_getter = WeatherFactory.create_weather_getter(site)

        if not (weather_getter):
            await update.message.reply_text(f'{site} attualmente non supportato o non disponibile')
            logger.error(f"{site} doesn't supported")
            return

        weather = weather_getter.get_weather(city, day)
        await update.message.reply_text(f"Città: {weather['city'].capitalize()}\n"
                                        f"Giorno: {weather['day']}\n"
                                        f"Temperatura minima: {weather['temp1']}\n"
                                        f"Temperatura massima: {weather['temp2']}\n"
                                        f"Informazioni: {weather['info']}")

    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            f"Il comando {update.message.text} non è valido"
        )

    def run(self):
        application = Application.builder().token(
            self.token).build()

        application.add_handler(CommandHandler('start', self.start))
        application.add_handler(CommandHandler('help', self.help_command))
        application.add_handler(CommandHandler('meteo', self.meteo))
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, self.unknown))  # testo senza comandi
        application.add_handler(MessageHandler(filters.COMMAND, self.unknown))

        application.run_polling()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        logger.error(f"Telegram token richiesto")
        exit(1)

    token = sys.argv[1]

    tg_manager = TelegramBotManager(token)
    tg_manager.run()
