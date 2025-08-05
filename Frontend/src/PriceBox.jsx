import React from "react";

const getEtiketClass = (etiket) => {
    switch (etiket) {
        case "İYİ FIRSAT":
            return "etiket yesil";
        case "ORTALAMA":
            return "etiket turuncu";
        case "RİSKLİ":
            return "etiket kirmizi";
        default:
            return "etiket";
    }
};

const PriceBox = ({ fiyatAralik, modelTahmin, etiket }) => (
    <div className="price-box">
        <span className="price-range">{fiyatAralik}</span>
        <span className="model-estimate">Model Tahmini: {modelTahmin}</span>
        <span className={getEtiketClass(etiket)}>{etiket}</span>
    </div>
);

export default PriceBox;

