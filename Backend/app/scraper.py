import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.arabam.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_detail_page(url):
    ilan = {
        "url": url,
        "ilan_id": None,
        "ilan_tarihi": None,
        "marka": None,
        "seri": None,
        "model": None,
        "fiyat": None,
        "aciklama": "",
        "ekspertiz": [],
        "ozellikler": {},
        "arac_bilgileri": {}
    }

    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Açıklama
    aciklama_div = soup.select_one('#tab-description')
    if aciklama_div:
        ilan["aciklama"] = aciklama_div.get_text(separator="\n", strip=True)

    # Fiyat
    price_div = soup.select_one("div.desktop-information-price")
    if price_div:
        try:
            price_text = price_div.get_text(strip=True)
            price_clean = price_text.replace(".", "").replace("TL", "").replace("₺", "").replace(" ", "")
            ilan["fiyat"] = int(price_clean)
        except ValueError:
            ilan["fiyat"] = None

    # Ekspertiz
    damage_script = soup.find("script", text=lambda t: "window.damage" in t if t else False)
    if damage_script:
        start = damage_script.string.find("window.damage =") + len("window.damage =")
        end = damage_script.string.find("];", start) + 1
        damage_json = damage_script.string[start:end]
        try:
            damage_data = json.loads(damage_json)
            for item in damage_data:
                ilan["ekspertiz"].append({
                    "id": item['PartNumber'],
                    "label": item['Name'],
                    "durum": item['ValueDescription']
                })
        except json.JSONDecodeError:
            pass

    # Üst özellikler
    properties = soup.select('.product-properties-details.linear-gradient .property-item')
    for prop in properties:
        key = prop.select_one('.property-key')
        value = prop.select_one('.property-value')
        if key and value:
            k = key.get_text(strip=True)
            v = value.get_text(strip=True)
            ilan["ozellikler"][k] = v
            if k == "İlan No":
                ilan["ilan_id"] = v
            elif k == "İlan Tarihi":
                ilan["ilan_tarihi"] = v
            elif k == "Marka":
                ilan["marka"] = v
            elif k == "Seri":
                ilan["seri"] = v
            elif k == "Model":
                ilan["model"] = v

    # Araç bilgileri sekmesi
    car_info_blocks = soup.select('#tab-car-information .tab-content-car-information-container ul')
    for ul in car_info_blocks:
        for li in ul.find_all("li"):
            key = li.find("span", class_="property-key")
            value = li.find("span", class_="property-value")
            if key and value:
                ilan["arac_bilgileri"][key.get_text(strip=True)] = value.get_text(strip=True)
    print(ilan)
    return ilan