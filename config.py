import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "SIZNING_SUPPORT_BOT_TOKEN_BU_YERGA")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
DB_PATH = "support.db"
