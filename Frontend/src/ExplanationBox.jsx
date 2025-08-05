import React from "react";

const ExplanationBox = ({ aciklama }) => (
    <div className="explanation-box">
        <div className="explanation-title">İlan Öne Çıkanları</div>
        <div className="explanation-content">
            {aciklama
                ? aciklama.split("\n").map((line, i) => (
                    <div key={i}>{line}</div>
                ))
                : <span>Veri bulunamadı.</span>
            }
        </div>
    </div>
);

export default ExplanationBox;
