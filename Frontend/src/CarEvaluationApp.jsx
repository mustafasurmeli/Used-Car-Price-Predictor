import React, { useState } from "react";
import InputURL from "./InputURL";
import PriceBox from "./PriceBox";
import CarIdentity from "./CarIdentity";
import ExplanationBox from "./ExplanationBox";
import CarDiagram from "./CarDiagram";
import EvaluationLegend from "./EvaluationLegend";

//demo
const DEMO_DATA = {
    fiyatAralik: "735.000 - 865.000 TL",
    modelTahmin: "800.000 TL",
    etiket: "İYİ FIRSAT",
    temizlenmisAciklama: "Düşük kilometre, yetkili servis bakımlı, hasar kaydı yok. Küçük lokal boya, 2. sahip.",
    kimlik: {
        "Marka/Model": "Renault Clio 1.0 TCe Joy",
        "Yıl": "2021",
        "KM": "23.500",
        "Yakıt": "Benzin",
        "Vites": "Manuel"
    },
    ekspertizSvg: "", // SVG burada (CarDiagram bileşeni içinde oluşturulacak)
    parcaListesi: [
        { ad: "Motor Kaputu", durum: "Boyalı" },
        { ad: "Sol Ön Çamurluk", durum: "Değişmiş" },
        { ad: "Sağ Arka Çamurluk", durum: "Orijinal" },
        { ad: "Arka Kaput", durum: "Orijinal" },
        { ad: "Sol Arka Çamurluk", durum: "Orijinal" },
        { ad: "Sağ Arka Kapı", durum: "Orijinal" },
        { ad: "Sağ Ön Kapı", durum: "Orijinal" },
        { ad: "Tavan", durum: "Orijinal" },
        { ad: "Sol Arka Kapı", durum: "Orijinal" },
        { ad: "Sol Ön Kapı", durum: "Orijinal" },
        { ad: "Sağ Ön Çamurluk", durum: "Orijinal" },
        { ad: "Ön Tampon", durum: "Orijinal" },
        { ad: "Arka Tampon", durum: "Orijinal" }
    ]
};

const CarEvaluationApp = () => {
    const [data, setData] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleEvaluate = async (url) => {
        setIsLoading(true);
        setData(null);

        try {
            const response = await fetch("http://localhost:8000/tahmin", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ url })
            });

            if (!response.ok) throw new Error("Backend hatası");

            let result = await response.json();

            const kimlik = {};
            kimlik["Marka/Model"] = result.kimlik["Marka_Model"] || result.kimlik["Marka/Model"] || "-";
            kimlik["Yıl"] = result.kimlik["Yil"] || result.kimlik["Yıl"] || "-";
            kimlik["KM"] = result.kimlik["KM"] || result.kimlik["Km"] || result.kimlik["km"] || "-";
            kimlik["Yakıt"] = result.kimlik["Yakit"] || result.kimlik["Yakıt"] || "-";
            kimlik["Vites"] = result.kimlik["Vites"] || "-";
            const parcaListesi = (result.ekspertizSvg || []).map(e => ({
                ad: e.label,
                durum: e.durum
            }));

            setData({
                fiyatAralik: result.fiyatAralik,
                modelTahmin: result.modelTahmin,
                etiket: result.etiket,
                temizlenmisAciklama: result.temizlenmisAciklama,
                kimlik,
                parcaListesi
            });
        } catch (e) {
            alert("Bir hata oluştu: " + e.message);
        }

        setIsLoading(false);
    };


    return (
        <div className="main-bg">
            <div className="container">
                <InputURL onEvaluate={handleEvaluate} isLoading={isLoading} />
                {data && (
                    <div className="result-area fade-in">
                        <PriceBox
                            fiyatAralik={data.fiyatAralik}
                            modelTahmin={data.modelTahmin}
                            etiket={data.etiket}
                        />
                        <div className="grid-area">
                            <ExplanationBox aciklama={data.temizlenmisAciklama} />
                            <CarIdentity kimlik={data.kimlik} />
                            <div className="expertise-area">
                                <CarDiagram parcaListesi={data.parcaListesi} />
                                <EvaluationLegend parcaListesi={data.parcaListesi} />
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default CarEvaluationApp;
