# Used Car Price Predictor

A comprehensive machine learning system designed to predict used car prices specifically for the Turkish market. The project leverages an advanced combination of artificial neural networks (ANN), XGBoost, transformer-based NLP embeddings (BERT), and OpenAI LLM integration to provide accurate predictions through an interactive web-based frontend.

---

## 🔍 Project Overview

This application predicts used car prices based on data scraped from Turkish car listing websites. The backend consists of scraping mechanisms, data preprocessing pipelines, NLP cleaning, embedding extraction via transformer models, and ensemble modeling. The frontend offers an intuitive interface built with React for easy interaction and visualization.

---

## ⚙️ Key Features

- **Data Scraping:** Custom scraper to fetch real-time car listings.
- **Transformer-based NLP (BERT):** Embeds car descriptions into high-dimensional vectors.
- **OpenAI LLM Integration:** Cleans and structures raw car description texts.
- **Fusion ANN and XGBoost Ensemble:** Combines neural networks and gradient boosting for enhanced prediction accuracy.
- **Interactive Frontend:** React-based user interface for intuitive vehicle evaluation.

---

## 📂 Project Structure

```
.
├── Backend
│   ├── app
│   │   ├── main.py                   # FastAPI backend endpoints
│   │   ├── preprocessing.py          # Data preprocessing
│   │   ├── price_predictor.py        # Ensemble model predictions
│   │   ├── scraper.py                # Web scraping logic
│   │   ├── llm_cleaner.py            # OpenAI LLM cleaning integration
│   │   └── models
│   │       └── fusion_ann.py         # ANN model definition
│   └── requirements.txt              # Python dependencies
├── Frontend
│   ├── public
│   └── src
│       ├── CarEvaluationApp.jsx      # Main evaluation component
│       ├── CarDiagram.jsx            # Car part diagram visualization
│       ├── CarIdentity.jsx           # Car identity details component
│       ├── EvaluationLegend.jsx      # Evaluation legend for diagram
│       ├── ExplanationBox.jsx        # Description highlights
│       ├── InputURL.jsx              # URL input form
│       └── PriceBox.jsx              # Predicted price display
├── models
│   ├── best_xgboost_model.pkl
│   └── best_ann_model.pth
└── README.md
```

---

## 🚀 Installation and Setup

### Backend Setup

```bash
cd Backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Ensure you have environment variables set for OpenAI API Key (`OPENAI_API_KEY`).

### Frontend Setup

```bash
cd Frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173` and interacts with the backend running at `http://localhost:8000`.

---

## 🔧 Usage

1. Open the frontend application.
2. Paste a URL from a Turkish used-car listing site into the provided form.
3. Click "Değerlendir" (Evaluate).
4. See the predicted price, detailed car features, and a visual representation of evaluated car parts.

---

## 📌 Technology Stack

- **Backend:** FastAPI, PyTorch, XGBoost, OpenAI API, Transformers (XLM-RoBERTa)
- **Frontend:** React, Vite
- **Other:** BeautifulSoup for scraping, Scikit-learn for preprocessing

---

## 📈 Model Pipeline

- **Scraping:** Extract vehicle data and descriptions from listings.
- **Text Cleaning:** OpenAI LLM cleans and standardizes description texts.
- **Embeddings:** Transformer-based embeddings (XLM-RoBERTa) of cleaned texts.
- **Prediction:** ANN and XGBoost ensemble predictions for robust and accurate estimates.

---

## 📝 Contribution

Contributions, improvements, and suggestions are welcome. Feel free to open issues and pull requests.

---

## 📧 Contact

Developed by Mustafa Surmeli – [GitHub Profile](https://github.com/mustafasurmeli)

