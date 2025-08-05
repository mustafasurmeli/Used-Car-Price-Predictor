import os
import pickle
import numpy as np
import joblib

NUMERIC_SCALER_PATH = os.getenv("NUMERIC_SCALER_PATH", "models/preprocessing/numeric_scaler.pkl")
CATEGORICAL_ENCODER_PATH = os.getenv("CATEGORICAL_ENCODER_PATH", "models/preprocessing/categorical_encoders.pkl")

EKSPERTIZ_PARTS = [
    "Tavan", "Ön Tampon", "Arka Tampon", "Motor Kaputu",
    "Sağ Ön Kapı", "Sol Ön Kapı", "Sağ Arka Kapı", "Sol Arka Kapı",
    "Sağ Ön Çamurluk", "Sol Ön Çamurluk", "Sağ Arka Çamurluk", "Sol Arka Çamurluk", "Arka Kaput"
]
ALLOWED_NUMERIC = {"Yıl", "Kilometre", "Motor Hacmi", "Ağırlık"}
ALLOWED_CATEGORICAL = {"Marka", "Seri", "Model", "Yakıt Tipi", "Vites Tipi", "Kasa Tipi", "Renk", "Çekiş", "Kimden", "Araç Türü", "İlk Sahibi Değilim", "Araç Durumu"}


with open(NUMERIC_SCALER_PATH, "rb") as f:
    numeric_scaler = joblib.load("models/preprocessing/numeric_scaler.pkl")

with open(CATEGORICAL_ENCODER_PATH, "rb") as f:
    cat_encoders = joblib.load("models/preprocessing/categorical_encoders.pkl")
    print("[✓] Yüklenen encoder sınıfları:")
    for col, le in cat_encoders.items():
        print(f"  - {col}: {list(le.classes_[:50])} ...")


def preprocess_features(data: dict):
    numeric_raw = [
        int(data["ozellikler"].get("Yıl", 0)),
        int(data["ozellikler"].get("Kilometre", "0").replace(".", "").replace(" km", "")),
        int(data["arac_bilgileri"].get("Motor Hacmi", "0").split()[0]),  # Örn: "1200 cm3"
        int(data["arac_bilgileri"].get("Ağırlık", "0").replace(" kg", "").strip() or 0)
    ]
    numeric_scaled = numeric_scaler.transform([numeric_raw])[0]

    cat_values = {
        key: data["ozellikler"].get(key, "") or data["arac_bilgileri"].get(key, "")
        for key in ALLOWED_CATEGORICAL
    }

    encoded = []
    for col, enc in cat_encoders.items():
        val = cat_values.get(col, "").strip()

        if val in enc.classes_:
            encoded_val = enc.transform([val])[0]
        elif val.capitalize() in enc.classes_:
            encoded_val = enc.transform([val.capitalize()])[0]
        elif val.lower() in enc.classes_:
            encoded_val = enc.transform([val.lower()])[0]
        else:
            print(f"[!] {col} değeri '{val}' encode edilemedi, 0 atanıyor.")
            encoded_val = 0

        encoded.append(encoded_val)

    ekspertiz_dict = {item["label"]: item["durum"].lower() for item in data["ekspertiz"]}
    ekspertiz_mapped = []
    for part in EKSPERTIZ_PARTS:
        durum = ekspertiz_dict.get(part, "")
        if "değişen" in durum:
            ekspertiz_mapped.append(2)
        elif "boyalı" in durum:
            ekspertiz_mapped.append(1)
        else:
            ekspertiz_mapped.append(0)

    return np.array(numeric_scaled), np.array(encoded), np.array(ekspertiz_mapped)


def get_val(scraped_data, col):
    def normalize(text):
        return text.lower().replace(" ", "").replace("_", "").replace("-", "").replace("ı", "i")

    col_norm = normalize(col)

    for source in [scraped_data, scraped_data.get("ozellikler", {}), scraped_data.get("arac_bilgileri", {})]:
        for key in source:
            key_norm = normalize(str(key))
            if col_norm == key_norm:
                return source[key]

    if col == "ilk_sahiplik":
        val = scraped_data.get("arac_bilgileri", {}).get("Aracın ilk sahibiyim", "")
        return val

    return ""
def clean_motor_hacmi(text):
    if "-" in text:
        parts = text.replace("cm3", "").replace(" cc", "").split("-")
        try:
            return (float(parts[0]) + float(parts[1])) / 2
        except:
            return 0.0
    try:
        return float(text)
    except:
        return 0.0


def preprocess_all(scraped_data):
    print("Gelen veri örneği:", scraped_data.get("marka"), scraped_data.get("yıl"))

    # === NUMERIC ===
    numeric_cols = ["yıl", "kilometre", "motor_hacmi", "ağırlık"]
    numeric_vec = []
    for col in numeric_cols:
        val = get_val(scraped_data, col)
        if col == "motor_hacmi":
            numeric_vec.append(clean_motor_hacmi(val))
        else:
            val = val.replace(".", "").replace(" km", "").replace(" cc", "").strip()
            try:
                numeric_vec.append(float(val))
            except:
                print(f"[!] {col} değeri '{val}' float'a çevrilemedi, 0 atanıyor.")
                numeric_vec.append(0.0)

    print("Raw numeric vector:", numeric_vec)
    numeric_vec = numeric_scaler.transform([numeric_vec])[0]

    # === CATEGORICAL ===
    categorical_cols = [
        'marka', 'seri', 'model', 'yakıt_tipi', 'vites_tipi', 'kasa_tipi', 'renk',
        'çekiş', 'kimden', 'araç_türü', 'ilk_sahiplik', 'araç_durumu'
    ]
    categorical_vec = []
    for col in categorical_cols:
        val = get_val(scraped_data, col)
        val = str(val).strip()

        encoder = cat_encoders.get(col)
        if encoder:
            found = False
            for option in [val, val.title(), val.upper(), val.lower()]:
                if option in encoder.classes_:
                    encoded_val = encoder.transform([option])[0]
                    found = True
                    break

            if not found:
                print(f"[!] {col} değeri '{val}' encode edilemedi, 0 atanıyor.")
                encoded_val = 0
        else:
            encoded_val = 0

        categorical_vec.append(encoded_val)

        # # === EKSPERTİZ ===
        # ekspertiz_vec = []
        # ekspertiz_parcalar = [
        #     "Tavan", "Ön Tampon", "Arka Tampon", "Motor Kaputu",
        #     "Sağ Ön Kapı", "Sol Ön Kapı", "Sağ Arka Kapı", "Sol Arka Kapı",
        #     "Sağ Ön Çamurluk", "Sol Ön Çamurluk", "Sağ Arka Çamurluk", "Sol Arka Çamurluk", "Arka Kaput"
        # ]
        # for part in ekspertiz_parcalar:
        #     durum = next(
        #         (item["durum"].strip().lower() for item in scraped_data.get("ekspertiz", []) if item["label"] == part),
        #         None
        #     )
        #     if durum is None or "belirtilmemiş" in durum:
        #         ekspertiz_vec.append(1.5)  # Bilgi yoksa cezalandır
        #     elif "değiş" in durum:
        #         ekspertiz_vec.append(2.0)
        #     elif "lokal boyanmış" in durum:
        #         ekspertiz_vec.append(0.6)
        #     elif "boya" in durum:
        #         ekspertiz_vec.append(1.0)
        #     else:
        #         ekspertiz_vec.append(0.0)
        # === EKSPERTİZ (Geliştirilmiş) ===
        ekspertiz_vec = []
        parca_onem_katsayilari = {
            "Tavan": 3.0,
            "Ön Tampon": 1.0,
            "Arka Tampon": 1.0,
            "Motor Kaputu": 2.5,
            "Sağ Ön Kapı": 1.5,
            "Sol Ön Kapı": 1.5,
            "Sağ Arka Kapı": 1.2,
            "Sol Arka Kapı": 1.2,
            "Sağ Ön Çamurluk": 1.0,
            "Sol Ön Çamurluk": 1.0,
            "Sağ Arka Çamurluk": 1.0,
            "Sol Arka Çamurluk": 1.0,
            "Arka Kaput": 1.3
        }

        ekspertiz_parcalar = list(parca_onem_katsayilari.keys())

        for part in ekspertiz_parcalar:
            durum = next(
                (item["durum"].strip().lower() for item in scraped_data.get("ekspertiz", []) if item["label"] == part),
                None
            )

            if durum is None or "belirtilmemiş" in durum:
                base_score = 0.8
            elif "değiş" in durum:
                base_score = 2.0
            elif "lokal boyanmış" in durum:
                base_score = 0.6
            elif "boya" in durum:
                base_score = 1.0
            else:
                base_score = 0.0

            weighted_score = base_score * parca_onem_katsayilari[part]
            ekspertiz_vec.append(weighted_score)

        max_etki = 20.0
        total_score = sum(ekspertiz_vec)
        if total_score > max_etki:
            scale = max_etki / total_score
            ekspertiz_vec = [v * scale for v in ekspertiz_vec]

    return np.array(numeric_vec), np.array(categorical_vec), np.array(ekspertiz_vec)
