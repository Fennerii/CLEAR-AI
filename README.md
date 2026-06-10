# CLEAR-AI
# CLEAR-AI

An AI-powered pollution prevention and waste-sorting tool for community and healthcare settings.

(CLEAR = Classification, Learning, Education, and Action for Reduction)

---

## Prerequisites

- Python 3.10+
- Ollama
- Webcam (for detection)

---

## Setup

### 1. Install Ollama

```
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Pull the required model

```
ollama pull llama3.1:8b
```

### 3. Start the Ollama service

```
ollama serve
```

### 4. Clone the repository

```
git clone https://github.com/Fennerii/CLEAR-AI.git
cd CLEAR-AI
```

### 5. Create and activate a virtual environment

```
python3 -m venv CLEAR-env
source CLEAR-env/bin/activate
```

### 6. Install dependencies

```
pip install -r requirements.txt
```

---

## Training (Desktop)

### 1. Add your dataset

Place your Roboflow dataset inside the project:

```
datasets/
  recyclables/
    train/
    valid/
    test/
    data.yaml
```

### 2. Run training

```
python3 train.py
```

### 3. Copy the trained model to project root

```
cp runs/detect/train/weights/best.pt best.pt
```

---

## Detection (ThinkPad)

### 1. Pull the latest model

```
git pull
```

### 2. Run webcam detection

```
source CLEAR-env/bin/activate
python3 main.py
```

Press `q` to quit.

---

## Classes

The model detects the following recyclable items:

- `can`
- `plastic bottle`
- `colored plastic bottle`
- `paper`
- `straw`
- `tuna`
- `Fork`
