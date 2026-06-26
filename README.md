# CLEAR-AI

An AI-powered pollution prevention and waste-sorting tool for community and healthcare settings.

(CLEAR = Classification, Learning, Education, and Action for Reduction)

---

## Prerequisites

- Python 3.10+
- Node.js 22+
- Ollama
- Webcam (for live detection)

---

## Setup

### 1. Install Ollama

```
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Pull the required models

```
ollama pull llama3.2
ollama pull mxbai-embed-large
```

### 3. Clone the repository

```
git clone https://github.com/Fennerii/CLEAR-AI.git
cd CLEAR-AI
```

### 4. Create and activate a virtual environment

```
python3 -m venv CLEAR-env
source CLEAR-env/bin/activate
```

### 5. Install backend dependencies

```
pip install -r requirements.txt
```

### 6. Install frontend dependencies

```
cd client
npm install
cd ..
```

---

## Knowledge Base

Place your PDFs, DOCX, and HTML disposal guidelines inside:

```
server/docs/
```

The first time the server starts, it will load these documents, split them into
chunks, and build a local vector store at `server/chroma_db/`. This only happens
once — later restarts load the existing vector store instantly instead of
rebuilding it.

---

## Training (optional, model already included)

```
python3 train.py
```

After training, copy the best model to the server folder:

```
cp runs/detect/train_full/weights/best.pt server/best.pt
```

---

## Run the App

### 1. Start the backend

```
cd server
source ../CLEAR-env/bin/activate
uvicorn main:app --reload
```

Backend runs at `http://localhost:8000`

### 2. Start the frontend

In a separate terminal:

```
cd client
npm run dev
```

Frontend runs at `http://localhost:5173`

### 3. Use it

Open `http://localhost:5173` in your browser, upload a photo of an item, and
CLEAR-AI will detect it and tell you how to dispose of it.

---

## Classes

The model detects the following items:

- `closed box`
- `colored plastic bottle`
- `open box`
- `paper`
- `plastic bottle`
- `plastic-bags`
- `plastic-bottles`
- `straw`
- `tuna`
