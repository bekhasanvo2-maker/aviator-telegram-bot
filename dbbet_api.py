import requests
import re
import json

DBBET_URL = "https://db-bet-20397.pro"

def get_game_page():
    try:
        response = requests.get(
            f"{DBBET_URL}/ru/my-casino?game=52358",
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        response.raise_for_status()
        return response.text
    except requests.RequestException as error:
        print(f"DBBet ulanish xatosi: {error}")
        return None

if __name__ == "__main__":
    page = get_game_page()
    if page:
        print("Sahifa olindi. Hajmi:", len(page))
        print("Aviator matni mavjud:", "Aviator" in page)
