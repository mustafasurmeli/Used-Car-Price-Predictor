import React from "react";

const CarIdentity = ({ kimlik }) => (
    <div className="identity-box">
        <div className="identity-title">Araç Kimliği</div>
        <div className="identity-list">
            {Object.entries(kimlik).map(([label, value]) => (
                <div key={label} className="identity-row">
                    <span className="identity-label">{label}</span>
                    <span className="identity-value">{value}</span>
                </div>
            ))}
        </div>
    </div>
);

export default CarIdentity;
