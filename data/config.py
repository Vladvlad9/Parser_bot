import os
from dotenv import load_dotenv

load_dotenv(".env")
BOT_TOKEN = os.environ["BOT_TOKEN"]

admins = [
	381252111,
]