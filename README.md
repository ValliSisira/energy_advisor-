# ⚡ Energy Advisor — AI App

**Energy Advisor** is a modern, interactive **Streamlit** app that analyzes **time-series energy data**, visualizes **usage KPIs**, and generates **AI-powered recommendations** using GPT models integrated via **LangChain** and **LangGraph**.  
In addition, the app includes a built-in **AI chatbot** that can answer general energy-related questions — and even interpret uploaded images (using GPT-4o).

---

## 🧠 What It Does

- Upload any **time-series CSV** (energy, or similar)
- Automatically detect **time/value columns**
- Compute and visualize **key KPIs**
- Generate **smart, data-driven tips** via GPT (LangChain + LangGraph)
- Ask the **chatbot** energy-related questions or upload images for analysis
- Enjoy a **dark, modern UI** with color-coded cards

---

## 🧱 Tech Stack

| Layer | Tools |
|-------|-------|
| **Frontend** | Streamlit ( responsive layout, sidebar controls, HTML/CSS styling) |
| **Backend / Data Processing** | Python 3.10+, Pandas, NumPy, Matplotlib, Pathlib, Argparse |
| **AI/LLM Layer** | LangChain, LangGraph, OpenAI GPT-4o / GPT-4o-mini |
| **Environment & Config** | python-dotenv, os, pathlib |
| **Utilities** | Base64 (image encoding for GPT-4o), Datetime utilities (via Pandas) |
| **Optional / Future Enhancements** | Seaborn / Plotly (interactive charts), ReportLab / Pandas-Profiling (export reports) |

---

## 📂 Project Structure

```
.
├── energy_advisor.py          # Core pipeline (data, KPIs, LLM tips)
├── energy_advisor_app.py      # Streamlit UI + chatbot interface
├── requirements.txt
├── samples/
│   └── demo_energy.csv        # Optional sample dataset
├── .streamlit/
│   └── config.toml            # Theme customization (optional)
└── README.md
```

---

## ⚙️ Key Features

### 🔍 Analysis Pipeline (LangGraph)
```
load_data → compute_kpis → visualize → llm_recommend
```
Each node updates a shared **EnergyState** dictionary that holds CSV path, columns, zone, KPIs, plot path, and LLM output.

### 🧾 KPIs
- Number of rows  
- Date range  
- Peak usage  
- Average usage  
- Load factor (avg ÷ peak)

### 💡 Recommendations
- Uses **LangChain + OpenAI GPT** for contextual energy tips  


### 💬 Chatbot
- Ask any energy question  
- Optional **image upload** (GPT-4o vision)  
- Context-aware: uses your KPIs to give better answers  
- Chat history stored in session state  
- Styled message bubbles (Bot vs You)

---

## 🧪 Example CSV Format

```
timestamp,load_mw,zone
2024-07-01 00:00,72,Houston
2024-07-01 01:00,70,Houston
2024-07-01 02:00,63,Houston
```

---

## 🚀 Quick Start (Local)

### 1️⃣ Clone Repo
```bash
git clone https://github.com/yourusername/energy-advisor.git
cd energy-advisor
```

### 2️⃣ Create Virtual Environment
```bash
python3 -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
.\.venv\Scripts\Activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ (Optional) Set OpenAI API Key
```bash
export OPENAI_API_KEY=sk-...
```

### 5️⃣ Run App
```bash
streamlit run energy_advisor_app.py
```

---

## 🧰 CLI Mode

You can also run analysis directly via CLI:

```bash
python energy_advisor.py --csv samples/demo_energy.csv

```

Output:
```
=== KPIs ===
{'rows': 48, 'start': '2024-07-01T00:00:00', ...}

Plot: output/energy_plot.png

=== Tips ===
• Shift flexible loads to off-peak hours.
• Use smart thermostats for demand flattening.
```

---

## ☁️ Streamlit Cloud Deployment

1. Push repo to GitHub.  
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud).  
3. Select your repo → set **Main file path** to `energy_advisor_app.py`.  
4. Add environment secret `OPENAI_API_KEY`.  
5. Deploy! 🌍  

---

## 📦 requirements.txt

```
python-dotenv>=1.0.1
pandas>=2.1
numpy>=1.26
matplotlib>=3.8
streamlit>=1.36
openai>=1.40.0
langchain>=0.2.10
langchain-openai>=0.1.14
langgraph>=0.2.20
```

---

## 💡 Troubleshooting

| Issue | Fix |
|--------|-----|
| **OpenAI API error / 401** | Verify `OPENAI_API_KEY` is set |
| **Time parsing fails** | Ensure timestamps are ISO / parseable |
| **Matplotlib errors** | Reinstall with `pip install matplotlib --upgrade` |
| **Streamlit Cloud fails** | Add your OpenAI key under app secrets |

---

## 🧩 Roadmap

- [ ] Multi-zone energy comparison  
- [ ] Emission factor overlay  
- [ ] Downloadable PDF reports (KPIs + tips + plots)  
- [ ] Anomaly detection via seasonal decomposition  
- [ ] RAG-based chatbot memory for previous uploads  

---
## Outputs of the streamlit app

<img src="/Users/vallisisirasista/Screenshots/app-1.png" alt="Website-Overview" width="800"/>
<img src="/Users/vallisisirasista/Screenshots/app-2.png" alt="Website-Overview" width="800"/>
<img src="/Users/vallisisirasista/Screenshots/app-3.png" alt="Website-Overview" width="800"/>
<img src="/Users/vallisisirasista/Screenshots/app-4.png" alt="Website-Overview" width="800"/>
<img src="/Users/vallisisirasista/Screenshots/app-5.png" alt="Website-Overview" width="800"/>
<img src="/Users/vallisisirasista/Screenshots/app-6.png" alt="Website-Overview" width="800"/>


## 📄 License

MIT License © 2025 Valli Sisira Sista 

---

