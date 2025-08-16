# 🔍🔗 Excel Formula Dependency Tracer

**Professional-grade formula lineage, hop-depth analytics, and cross-sheet mapping for Excel models.**

This Streamlit application lets you upload an Excel workbook (`.xlsx`) and interactively explore its formula dependencies. It parses formulas, maps their relationships, and highlights potential risks — all in a clear, visual interface.

---

## 💡 Features

- **Formula Lineage & Dependency Graphs** – Trace precedents and dependents across sheets.
- **Hop Depth Analysis** – See the longest calculation chains from inputs to outputs.
- **Cross-Sheet Matrix** – Visualize how formulas reference data across sheets.
- **Circular & Risky Formula Detection** – Identify loops and high-risk functions.
- **KPI Tracer** – Inspect key performance indicator calculation flows.

---

## 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
```

---

## ▶️ Running the App Locally

```bash
streamlit run app.py
```

Then open the URL provided in the terminal (usually `http://localhost:8501`).

---

## 🌐 Deploying Online

You can deploy this app for free on **Streamlit Community Cloud**:

1. Push your code to a **public GitHub repo**.
2. Go to [share.streamlit.io](https://share.streamlit.io/) → “Deploy an app”.
3. Select your repo, branch, and `app.py` file.
4. Deploy.

---

## 📂 Project Structure

```
.
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
└── modules/                # Supporting Python scripts
    ├── loader.py
    ├── tracer.py
    ├── summaries.py
    ├── views_overview.py
    ├── views_inspector.py
    ├── views_matrix.py
    ├── views_risks.py
    └── views_kpi.py
```

---

## 📄 License

This project is licensed under the MIT License — feel free to modify and share.
