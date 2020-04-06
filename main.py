import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

import tg, parse, graph


def main():
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    tg.launch_bot(TELEGRAM_TOKEN)

if __name__ == '__main__':
    load_dotenv()
    main()
