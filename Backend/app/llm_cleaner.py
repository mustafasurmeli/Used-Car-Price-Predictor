import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_description_with_llm(text: str) -> str:
    """Bir araç açıklamasını GPT-4.1-mini ile temizler"""
    try:
        prompt = f"""
Aşağıda bir araç ilan açıklaması bulunmaktadır. Lütfen:

- Anlamı bozmadan düzelt,
- Spam ve yazım hatalarını çıkar,
- Donanım bilgilerini koru,
- Özellikleri tek cümlede ve virgüllerle yaz,
- Yeni bilgi üretme, kişisel bilgi ekleme.
- Araç Sahibi, Fiyat, İletişim Bilgileri gibi kişisel bilgileri çıkar.
- Gereksiz ifadeleri ve tekrarları kaldır.

Sadece temizlenmiş haliyle aşağıya yaz:

{text.strip()}
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini-2025-04-14",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=600
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ OpenAI Hatası:", e)
        return ""
