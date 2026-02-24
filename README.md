<div align="center">

# ✦ DataLens AI

### An end-to-end AI-powered data analysis web app
**Upload any CSV → Get instant visualizations → Chat with your data in plain English**

<br>

![Python](https://img.shields.io/badge/Python-3.10+-4B8BBE?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.54+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=for-the-badge&logo=groq&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive_Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-2ecc71?style=for-the-badge)

<br>

> 🌐 **[Live Demo → Coming Soon](#)** &nbsp;|&nbsp; ⭐ Star this repo if you find it useful!

</div>

---

## 📖 About

**DataLens AI** is a fully functional, end-to-end data analysis tool built by **Anuj Vishwakarma** that brings together the power of **Groq's ultra-fast AI inference** and **Streamlit's interactive UI** — making data analysis accessible to everyone, not just data scientists.

No code needed. Just upload a CSV, and DataLens AI does the rest — auto-generates charts, computes statistics, and lets you have a natural conversation with your data using **LLaMA 3.3 70B**, one of the most capable open-source AI models available today.

Built as a complete project from scratch — UI design, AI integration, data visualization, and cloud deployment — all in one clean, professional package.

---

## ✨ Features

| | Feature | What it does |
|---|---|---|
| 📋 | **Data Preview** | Browse your raw data, inspect column types, nulls, unique counts, and full summary statistics |
| 📊 | **Auto Visualizations** | Instantly generates correlation heatmaps, distributions, bar charts, scatter plots, and box plots |
| 🛠 | **Custom Chart Builder** | Pick any columns, choose your chart type, and build your own interactive visualization |
| 🤖 | **AI Analysis** | 5 intelligent analysis modes — General, Statistical, Business Intelligence, Anomaly Detection, Predictive Patterns |
| 💬 | **Chat with Data** | Ask any question in plain English and get data-backed answers from the AI |
| ⬇️ | **Export** | Download summary statistics as CSV or your full AI chat log as TXT |
| 🔒 | **Secure by Design** | API key entered via sidebar — never hardcoded, never stored permanently |

---

## 🖥 App Walkthrough

```
┌─────────────────────────────────────────────────────────┐
│  ✦ DataLens AI                          sidebar: config  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Upload your CSV file   [  Drop file here  ]           │
│                                                         │
│   📦 1,500 Rows  │ 12 Cols  │ 8 Numeric  │ 0 Missing   │
│                                                         │
│  ┌──────────┬──────────┬──────────┬──────────┐         │
│  │📋 Preview│📊 Charts │🤖 AI     │💬 Chat   │         │
│  └──────────┴──────────┴──────────┴──────────┘         │
│                                                         │
│   [Auto-generated charts appear here]                   │
│   [AI insights appear here]                             │
│   [Chat conversation appears here]                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- A free Groq API key → [console.groq.com](https://console.groq.com)

---

### 1. Clone the repository

```bash
git clone https://github.com/anujvish005/datalens-ai.git
cd datalens-ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get your free Groq API key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for free (takes 30 seconds)
3. Click **API Keys** → **Create API Key**
4. Copy the key — it starts with `gsk_...`

> ⚠️ You only see the key once — save it somewhere safe immediately.

### 4. Run the app

```bash
python -m streamlit run app.py
```

Your browser opens at `http://localhost:8501` automatically.

### 5. Enter your API key

Paste your `gsk_...` key into the **API Key** field in the left sidebar. It's stored only for the current session — never saved to disk.

---

## 🤖 AI Models Available

All models run free via [Groq](https://groq.com) — the fastest AI inference platform:

| Model | Speed | Best For |
|---|---|---|
| `llama-3.3-70b-versatile` | Fast | Best quality, recommended for all tasks |
| `llama-3.1-8b-instant` | Fastest | Quick questions, large datasets |
| `mixtral-8x7b-32768` | Fast | Long context, detailed analysis |
| `gemma2-9b-it` | Fast | Alternative perspective, concise answers |

---

## 🧠 Analysis Modes

| Mode | What the AI focuses on |
|---|---|
| **General Insights** | Patterns, trends, notable findings, and recommendations |
| **Statistical Deep Dive** | Distributions, outliers, correlations, and statistical significance |
| **Business Intelligence** | KPIs, opportunities, risks, and business recommendations |
| **Anomaly Detection** | Unusual values, outliers, and what might be causing them |
| **Predictive Patterns** | Trends, important variables, and what could be forecast |

---

## 🌐 Deploy to Streamlit Cloud (Free)

Share your app with anyone — no server needed.

**Step 1** — Push your code to GitHub:
```bash
git init
git add .
git commit -m "feat: DataLens AI - end to end data analyzer"
git remote add origin https://github.com/anujvish005/datalens-ai.git
git push -u origin main
```

**Step 2** — Deploy on Streamlit Cloud:
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub → click **New app**
3. Select your repo → set main file to `app.py`
4. Click **Advanced settings → Secrets** and add:

```toml
GROQ_API_KEY = "gsk_your_actual_key_here"
```

5. Click **Deploy** → get your live public URL 🎉

---

## 🗂 Project Structure

```
datalens-ai/
│
├── app.py                        # Main Streamlit application
├── requirements.txt              # Python dependencies
├── .env.example                  # Template for local environment variables
├── .gitignore                    # Keeps secrets and cache out of Git
├── .streamlit/
│   └── secrets.toml.example      # Streamlit secrets template
└── README.md                     # You are here
```

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | [Streamlit 1.54](https://streamlit.io) | Web app framework, UI components |
| **AI Inference** | [Groq API](https://groq.com) | Ultra-fast LLM inference |
| **Language Model** | [LLaMA 3.3 70B](https://ai.meta.com/llama/) | Natural language understanding |
| **Data Processing** | [Pandas](https://pandas.pydata.org) | CSV parsing and data manipulation |
| **Visualizations** | [Plotly Express](https://plotly.com/python/plotly-express/) | Interactive charts |
| **Styling** | Custom CSS + Google Fonts | DM Serif Display, DM Sans, DM Mono |

---

## 🔒 Security & Privacy

- Your CSV data is processed **locally in your browser session** — never sent to any external server except when you click "Analyze" (only a text summary is sent to Groq, not the raw file)
- Your Groq API key is stored **only in session memory** — cleared when you close the tab
- **Never hardcode** your API key in `app.py` — use the sidebar input or `.env` file
- The `.gitignore` already protects `.env` and `secrets.toml` from being committed

---

## 📦 Dependencies

```txt
streamlit>=1.54.0
pandas>=2.0.0
groq>=0.4.0
plotly>=5.18.0
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 🙋 FAQ

**Q: Do I need to pay for anything?**
No. Groq offers a generous free tier. Streamlit Cloud deployment is also free.

**Q: What file types are supported?**
Currently CSV only. Excel (.xlsx) support can be added with `openpyxl`.

**Q: Is my data safe?**
Yes. Your file never leaves your machine. Only a text summary (first 30 rows + stats) is sent to the Groq API for AI analysis.

**Q: The app shows a blank page — what do I do?**
Run `python -m streamlit run app.py` instead of clicking the VS Code play button. Make sure all dependencies are installed with `pip install -r requirements.txt`.

**Q: Can I use OpenAI instead of Groq?**
The app is built for Groq, but can be adapted for OpenAI by replacing the `groq` client with `openai`.

---

## 🗺 Roadmap

- [ ] Excel (.xlsx) file support
- [ ] PDF export of full analysis report
- [ ] Multi-file comparison mode
- [ ] Natural language to SQL query generator
- [ ] Saved analysis history
- [ ] Dark / light theme toggle

---

## 👨‍💻 Author

**Anuj Vishwakarma**

[![GitHub](https://img.shields.io/badge/GitHub-anujvish005-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/anujvish005)

---

## 📄 License

MIT License — free to use, modify, and share with attribution.

---

## 🙌 Acknowledgements

- [Groq](https://groq.com) for blazing-fast free AI inference
- [Streamlit](https://streamlit.io) for making Python web apps effortless
- [Meta AI](https://ai.meta.com) for open-sourcing LLaMA 3.3
- [Plotly](https://plotly.com) for beautiful interactive charts

---

<div align="center">

Built with care by **[Anuj Vishwakarma](https://github.com/anujvish005)** using **Streamlit** + **Groq AI** + **Python**

*If this project helped you, give it a ⭐ on GitHub!*

**[🐛 Report a Bug](https://github.com/anujvish005/datalens-ai/issues)** &nbsp;·&nbsp; **[💡 Request a Feature](https://github.com/anujvish005/datalens-ai/issues)**

</div>
