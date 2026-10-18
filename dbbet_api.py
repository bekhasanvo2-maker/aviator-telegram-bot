import requests


DBBET_URL = "https://db-bet-20397.pro"


def get_game_page():
    try:
        response = requests.get(
            DBBET_URL,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        response.raise_for_status()
        return response.text
    except requests.RequestException as error:
        print(f"DBBet bilan ulanish xatosi: {error}")
        return None
