import torch
from transformers import AutoTokenizer, AutoModel

# BERT modeli ve tokenizer
MODEL_NAME = "xlm-roberta-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
bert_model = AutoModel.from_pretrained(MODEL_NAME)
bert_model.eval()  # dropout vs. kapalı

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
bert_model.to(device)

def embed_text(text: str) -> torch.Tensor:
    """Bir metni (ilan başlığı + temiz açıklama) BERT ile 768 boyutlu vektöre çevirir"""
    with torch.no_grad():
        encoded = tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=128,
            return_tensors="pt"
        )
        input_ids = encoded["input_ids"].to(device)
        attention_mask = encoded["attention_mask"].to(device)

        outputs = bert_model(input_ids=input_ids, attention_mask=attention_mask)
        cls_embedding = outputs.last_hidden_state[:, 0, :]  # [CLS] token
        return cls_embedding.squeeze(0).cpu()  # shape: (768,)
