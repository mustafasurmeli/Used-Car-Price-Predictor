from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from app.scraper import scrape_detail_page
from app.llm_cleaner import clean_description_with_llm
from app.bert_embedder import embed_text
from app.preprocessing import preprocess_all
from app.price_predictor import predict_price_with_ensemble

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class URLRequest(BaseModel):
    url: str

class EkspertizParca(BaseModel):
    id: str
    label: str
    durum: str

class Kimlik(BaseModel):
    Marka_Model: str
    Yil: str
    KM: str
    Yakit: str
    Vites: str

class PredictionResponse(BaseModel):
    modelTahmin: str
    fiyatAralik: str
    etiket: str
    temizlenmisAciklama: str
    kimlik: Kimlik
    ekspertizSvg: List[EkspertizParca]

@app.post("/tahmin", response_model=PredictionResponse)
def tahmin_et(req: URLRequest):
    scraped = scrape_detail_page(req.url)

    temizlenmis = clean_description_with_llm(scraped["aciklama"])

    # metin = scraped['ozellikler'].get('Yıl', '') + ' MODEL ' + scraped['marka'] + ' ' + scraped['model'] + ' ' + temizlenmis
    ilan_basligi = scraped.get('ilan_basligi', '').strip()
    # metin = (
    #         str(scraped.get('ozellikler', {}).get('Yıl', '')).strip() + ' MODEL ' +
    #         str(scraped.get('marka', '')).strip() + ' ' +
    #         str(scraped.get('model') or '').strip() + ' ' +
    #         temizlenmis.strip()
    # )
    metin = (
             ilan_basligi + ' ' + temizlenmis.strip()
     )
    text_vec = embed_text(metin)

    numeric_vec, categorical_vec, ekspertiz_vec = preprocess_all(scraped)

    fiyat_dict = predict_price_with_ensemble(text_vec, numeric_vec, categorical_vec, ekspertiz_vec)



    try:
        ilan_fiyati = float(scraped.get("fiyat", 0))
        tahmin_fiyati = float(
            str(fiyat_dict["modelTahmin"]).replace(".", "").replace(",", "").replace(" TL", "").strip())

        fark_orani = abs(tahmin_fiyati - ilan_fiyati) / ilan_fiyati

        if fark_orani <= 0.05:
            etiket = "İYİ FIRSAT"
        elif fark_orani <= 0.10:
            etiket = "ORTALAMA"
        else:
            etiket = "RİSKLİ"
    except Exception as e:
        print(f"[!] Etiket hesaplama hatası: {e}")
        etiket = "BİLİNMİYOR"
    kimlik = Kimlik(
        Marka_Model=f"{scraped['marka']} {scraped['model']}",
        Yil=scraped['ozellikler'].get("Yıl", ""),
        KM=scraped['ozellikler'].get("Kilometre", ""),
        Yakit=scraped['ozellikler'].get("Yakıt Tipi", ""),
        Vites=scraped['ozellikler'].get("Vites Tipi", "")
    )

    ekspertiz_svg = [
        EkspertizParca(
            id=str(item["id"]),
            label=item["label"],
            durum=item["durum"]
        )
        for item in scraped["ekspertiz"]
    ]

    return PredictionResponse(
        modelTahmin=fiyat_dict["modelTahmin"],
        fiyatAralik=fiyat_dict["fiyatAralik"],
        etiket=etiket,
        temizlenmisAciklama=temizlenmis,
        kimlik=kimlik,
        ekspertizSvg=ekspertiz_svg
    )
