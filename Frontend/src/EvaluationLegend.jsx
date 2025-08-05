import React from "react";

const RENKLER = {
    "Orijinal": "green",
    "Lokal Boyalı": "#e3d28d",
    "Boyalı": "#ffeb3b",
    "Değişmiş": "crimson",
    "Belirtilmemiş": "#aaa"
};

const GRUPLAR = ["Orijinal", "Lokal Boyalı", "Boyalı", "Değişmiş", "Belirtilmemiş"];

function normalizeDurum(durumRaw) {
    const d = durumRaw.toLowerCase();
    if (d.includes("değiş")) return "Değişmiş";
    if (d.includes("lokal")) return "Lokal Boyalı";
    if (d.includes("boya")) return "Boyalı";
    if (d.includes("orijinal")) return "Orijinal";
    return "Belirtilmemiş";
}

function parcalariGrupla(parcaListesi) {
    const gruplar = {};
    GRUPLAR.forEach(d => { gruplar[d] = []; });

    parcaListesi.forEach(p => {
        const durum = normalizeDurum(p.durum || "");
        const ad = p.label || p.ad || "Bilinmeyen Parça";
        gruplar[durum].push(ad);
    });

    return gruplar;
}


const EvaluationLegend = ({ parcaListesi }) => {
    const gruplar = parcalariGrupla(parcaListesi);

    return (
        <div className="legend-box">
            {GRUPLAR.map(grup => (
                <div key={grup} className="legend-row">
          <span
              className="legend-dot"
              style={{
                  background: RENKLER[grup] || "#aaa",
                  border: grup === "Orijinal" ? "1.5px solid #388e3c" : "1.5px solid #888"
              }}
          ></span>
                    <span className="legend-label">{grup}</span>
                    <span className="legend-parcalar">
            {gruplar[grup].length > 0
                ? gruplar[grup].join(" • ")
                : "-"}
          </span>
                </div>
            ))}
        </div>
    );
};

export default EvaluationLegend;
