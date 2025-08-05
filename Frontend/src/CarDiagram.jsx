import React from "react";

// Parça adı - SVG koordinat eşleşmesi
const PARTS = [
    { ad: "Ön Tampon", x: 130, y: 325, w: 240, h: 24, rx: 8 },
    { ad: "Arka Tampon", x: 130, y: 50, w: 240, h: 24, rx: 8 },
    { ad: "Arka Kaput", x: 180, y: 90, w: 120, h: 32, rx: 10 },
    { ad: "Sol Ön Çamurluk", x: 60, y: 235, w: 38, h: 55, rx: 12 },
    { ad: "Sağ Ön Çamurluk", x: 402, y: 235, w: 38, h: 55, rx: 12 },
    { ad: "Sol Ön Kapı", x: 60, y: 170, w: 38, h: 55, rx: 12 },
    { ad: "Sağ Ön Kapı", x: 402, y: 170, w: 38, h: 55, rx: 12 },
    { ad: "Sol Arka Kapı", x: 60, y: 100, w: 38, h: 55, rx: 12 },
    { ad: "Sağ Arka Kapı", x: 402, y: 100, w: 38, h: 55, rx: 12 },
    { ad: "Sol Arka Çamurluk", x: 60, y: 45, w: 38, h: 47, rx: 14 },
    { ad: "Sağ Arka Çamurluk", x: 402, y: 45, w: 38, h: 47, rx: 14 },
    { ad: "Tavan", x: 160, y: 130, w: 180, h: 100, rx: 22 },
    { ad: "Motor Kaputu", x: 110, y: 280, w: 280, h: 34, rx: 10 }
];

const DURUM_RENK = {
    "Orijinal": "#a5d6a7",
    "Boyalı": "#ffeb3b",
    "Lokal Boyalı": "#e3d28d",
    "Değişmiş": "#ef5350",
    "Belirtilmemiş": "#e0e0e0"
};

const DURUM_STROKE = {
    "Orijinal": "#388e3c",
    "Boyalı": "#bfa60a",
    "Lokal Boyalı": "#e3d28d",
    "Değişmiş": "#b71c1c",
    "Belirtilmemiş": "#aaa"
};

function normalizeDurum(durumRaw) {
    const d = durumRaw.toLowerCase();

    if (d.includes("değiş")) return "Değişmiş";
    if (d.includes("lokal")) return "Lokal Boyalı";
    if (d.includes("boya")) return "Boyalı";
    if (d.includes("orijinal")) return "Orijinal";
    return "Belirtilmemiş";
}

function getDurum(parcaListesi, ad) {
    const found = parcaListesi.find(p => p.label === ad || p.ad === ad);
    return found ? normalizeDurum(found.durum || "") : "Belirtilmemiş";
}


const CarDiagram = ({ parcaListesi }) => (
    <div className="car-diagram">
        <svg viewBox="0 0 500 400" width="320" height="240" className="svg-car">
            {/* Gövde ana hat */}
            <rect x="110" y="90" width="280" height="180" rx="38" fill="#e8f5e9" stroke="#bdbdbd" strokeWidth="5"/>
            {/* Parçalar */}
            {PARTS.map((part, i) => {
                const durum = getDurum(parcaListesi, part.ad);
                return (
                    <rect
                        key={part.ad}
                        x={part.x}
                        y={part.y}
                        width={part.w}
                        height={part.h}
                        rx={part.rx}
                        fill={DURUM_RENK[durum] || "#e0e0e0"}
                        stroke={DURUM_STROKE[durum] || "#aaa"}
                        strokeWidth="2"
                        className="car-part"
                    >
                        <title>{part.ad}: {durum}</title>
                    </rect>
                );
            })}
        </svg>
    </div>
);

export default CarDiagram;
