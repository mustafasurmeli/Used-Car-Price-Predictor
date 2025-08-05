import os
import torch
import joblib
import numpy as np
from models.fusion_ann import FusionANN
from app.bert_embedder import embed_text
from app.preprocessing import preprocess_features
from dotenv import load_dotenv

load_dotenv()

# Cihaz
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# XGBoost modeli
XGB_MODEL_PATH = os.getenv("XGB_MODEL_PATH", "models/best_xgboost_model.pkl")
xgb_model = joblib.load(XGB_MODEL_PATH)

# ANN modeli ve konfigürasyonu
ANN_MODEL_PATH = os.getenv("ANN_MODEL_PATH", "models/best_ann_model.pth")
ann_checkpoint = torch.load(ANN_MODEL_PATH, map_location=device, weights_only=False)
ann_config = ann_checkpoint["model_config"]

ann_model = FusionANN(
    text_input_dim=768,
    numeric_input_dim=4,
    ekspertiz_input_dim=13,
    cat_embedding_input_dim=12,
    hidden_sizes=(512, 384, 256, 192, 128, 64),
    dropout_rates=(0.1, 0.1, 0.1, 0.2)
).to(device)
ann_model.load_state_dict(ann_checkpoint["model_state_dict"])
ann_model.eval()

# === TAHMİN ===

def predict_price_with_ensemble(
    text_vec: np.ndarray,
    numeric_vec: np.ndarray,
    categorical_vec: np.ndarray,
    ekspertiz_vec: np.ndarray
) -> dict:
    """
    Önceden embed edilmiş ve preprocess edilmiş 4 vektörü al,
    ANN ve XGBoost ile tahmin yap, ensemble sonucu döndür.
    """
    xgb_input = np.concatenate([text_vec, numeric_vec, categorical_vec, ekspertiz_vec]).reshape(1, -1)
    xgb_pred = xgb_model.predict(xgb_input)[0] * 1_000_000

    text_tensor = torch.tensor(text_vec, dtype=torch.float32).unsqueeze(0).to(device)
    numeric_tensor = torch.tensor(numeric_vec, dtype=torch.float32).unsqueeze(0).to(device)
    categorical_tensor = torch.tensor(categorical_vec, dtype=torch.float32).unsqueeze(0).to(device)
    ekspertiz_tensor = torch.tensor(ekspertiz_vec, dtype=torch.float32).unsqueeze(0).to(device)

    with torch.no_grad():
        ann_pred = ann_model(text_tensor, numeric_tensor, ekspertiz_tensor, categorical_tensor)
        ann_pred = ann_pred.item() * 1_000_000

    print("text_vec shape", text_vec.shape)
    print("numeric_vec", numeric_vec)
    print("categorical_vec", categorical_vec)
    print("ekspertiz_vec", ekspertiz_vec)
    print("ANN raw output:", ann_pred)
    print("XGB raw output:", xgb_pred)


    # if ann_pred / xgb_pred > 3 or xgb_pred / ann_pred > 3:
    #     ensemble_price = xgb_pred
    # else:
    ensemble_price = 0.7 * ann_pred + 0.3 * xgb_pred

    mae = 97904
    lower = int(ensemble_price - mae * 0.95)
    upper = int(ensemble_price + mae * 1.05)

    return {
        "modelTahmin": f"{int(ensemble_price):,} TL".replace(",", "."),
        "fiyatAralik": f"{lower:,} - {upper:,} TL".replace(",", ".")
    }
