# HireSense – AI Resume Intelligence Engine

HireSense is an AI-powered resume screening system built on top of the Endee vector database.  
It performs semantic skill matching using sentence embeddings and vector similarity search to evaluate candidate-role alignment.

The system combines embedding-based similarity scoring with structured evaluation logic to generate detailed candidate analysis, skill coverage insights, and executive summaries.

---

## 🚀 Key Features

- 📄 PDF Resume Parsing (pdfplumber)
- 🧠 Semantic Embeddings (SentenceTransformers – all-MiniLM-L6-v2)
- 🔎 Vector Similarity Search using Endee
- 📊 Role-Based Skill Matching
- 📉 Skill Gap Identification
- 📈 Match Percentage & Confidence Scoring
- 🧾 Executive Summary Generation
- 🌐 FastAPI Backend with Clean Web UI

---

## 🏗 System Architecture

Resume (PDF)  
→ Text Extraction  
→ Sentence Embedding  
→ Vector Search (Endee)  
→ Similarity Scoring  
→ Structured Skill Evaluation  
→ Executive Summary + Final Report  

---

## 🛠 Tech Stack

- Python 3.10+
- FastAPI
- SentenceTransformers
- Endee (Vector Database)
- pdfplumber
- Uvicorn
- Jinja2

---

## 📂 Project Structure

```
HireSense/
│
│
├── app/                  # Application logic
│   ├── resume_processor.py
│   ├── role_engine.py
│   ├── ai_summary.py
│
├── data/
│   └── role_profiles.py
│
├── templates/
│   └── index.html
│
├── main.py               # FastAPI entry point
├── insert_roles.py       # Script to index role profiles into Endee
├── requirements.txt

```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Forked Repository

```bash
git clone https://github.com/Ananya-Bala/HireSense.git
cd HireSense
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate     # Mac/Linux
# venv\Scripts\activate      # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Start Endee Server

Ensure Endee is running locally:

```
http://localhost:8080/api/v1
```

If using Docker:

```bash
docker-compose up
```

---

### 5️⃣ Index Role Profiles

```bash
python insert_roles.py
```

---

### 6️⃣ Run the Application

```bash
uvicorn main:app --reload
```

Open:

```
http://127.0.0.1:8000
```

---

## 🧠 How Matching Works

1. Role profiles are embedded using SentenceTransformer.
2. Resume text is converted into an embedding vector.
3. Endee performs cosine similarity search.
4. The highest matching role vector is retrieved.
5. Structured evaluation calculates:
   - Skill coverage percentage
   - Matched skills
   - Missing skills
   - Confidence score
6. An executive summary is generated based on evaluation results.

---

## 📊 Output Includes

- Overall Match Percentage
- Similarity Score
- Confidence Level
- Matched Skills
- Missing Skills
- Recommendation Status
- Executive Summary

---

## 🔒 Notes

- Requires Endee vector database running locally.
- Designed for evaluation and demonstration purposes.
- Embedding model: `all-MiniLM-L6-v2`.

---

## 📜 License

This project builds upon the Endee open-source repository (Apache 2.0 License).

---

## 👩‍💻 Author

Ananya Bala  
AI Resume Intelligence System – HireSense
