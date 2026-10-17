import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID", "0"))  # ID вашей группы (со знаком минус)
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your-domain.github.io/avatar-gatekeeper-bot/webapp/")

# Шаблон анкеты (замените текст внутри на свой формат)
ANKETA_TEMPLATE = """
🌿 **АНКЕТА НОВОПРИБЫВШЕГО** 🌿

1. Имя / Позывной:
2. Возраст:
3. Чем занимаешься / Чем полезен клану:
4. Цель вступления:
5. О себе в двух предложениях:
""".strip()