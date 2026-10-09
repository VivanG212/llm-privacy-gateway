# LLM Privacy Protection Gateway

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![spaCy](https://img.shields.io/badge/spaCy-3.x-09A3D5.svg)](https://spacy.io/)

A lightweight, zero-trust client-side middleware proxy engineered to sanitize Personally Identifiable Information (PII) in real-time before transmitting prompts to cloud-hosted Large Language Model (LLM) APIs.

Built for edge-constrained voice interfaces, the gateway enforces local Named Entity Recognition (NER) and dynamic volatile RAM re-hydration to guarantee sub-50ms processing overhead without sacrificing contextual generation fidelity.

---

## Key Features

- **Zero-Trust Client Boundary:** Intercepts outgoing LLM API requests on `127.0.0.1:8000` to prevent unencrypted PII from reaching external cloud logging or model-training infrastructure.
- **Local Named Entity Recognition (NER):** Uses spaCy's `en_core_web_sm` model to extract and sanitize five core entity types: `PERSON`, `ORG`, `GPE`, `DATE`, and `MONEY`.
- **Volatile In-Memory Session Vault:** Stores PII-to-placeholder mappings strictly in RAM (`session_vault`), purged immediately after response re-hydration to prevent persistent storage leaks.
- **Real-Time Sub-50ms Overhead:** Empirical benchmarks demonstrate a mean local redaction overhead of **5.54 ms**, utilizing less than **12%** of the latency budget required for seamless voice assistant interaction.

---

## Architecture & Workflow

```text
[User Voice/Text Input]
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│ Local Execution Boundary (FastAPI Proxy @ 127.0.0.1:8000)  │
│                                                             │
│  1. Extract PII via spaCy NER (`redactor.py`)               │
│  2. Allocate Volatile Session Vault Frame (RAM)              │
│  3. Replace PII with Indexed Tokens ([PERSON_1], [ORG_1])   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                [Sanitized Prompt (HTTPS)]
                               │
                               ▼
                   ┌───────────────────────┐
                   │   Remote Cloud LLM    │
                   │   (e.g., OpenAI API)  │
                   └───────────┬───────────┘
                               │
               [Completion with Placeholders]
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Dynamic Session Re-hydration                                │
│                                                             │
│  1. Substitute Placeholders with Raw PII from RAM Vault     │
│  2. Purge Session Vault Frame from Volatile Storage         │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
[Re-hydrated Response to Client Interface]

## Threat Model
This system operates under a Semi-Honest (Honest-But-Curious) Cloud Provider Threat Model. While external LLM endpoints are assumed to accurately process incoming queries, persistent cloud logging, vendor database breaches, or unauthorized model retraining introduce severe privacy risks.
The security goal of the LLM Privacy Gateway is to ensure that no true entity mappings ever cross the local network interface.

## Empirical Benchmark Performance
Benchmarking was executed on Apple Silicon hardware across varying levels of PII density to evaluate latency constraints for edge voice interfaces (<50 ms target).

| Metric                                  | System Target | Empirical Result | Status     |
| :-------------------------------------: |:------------: |:---------------: |:---------: |
| **Mean Local Redaction Latency**        | `< 50.00 ms`  | **5.54 ms**      | **Passed** |
| **Entity Extraction Recall**            | `> 90.00%`    | **100.00%**      | **Passed** |
| **Session Vault Re-hydration Accuracy** | `100.00%`     | **100.00%**      | **Passed** |

### Latency vs. PII Density
- **High Density (5 Entities):** `10.56 ms`
- **Medium Density (4 Entities):** `3.18 ms`
- **Low Density (3 Entities):** `2.89 ms`

### Installation & Setup

#### Prerequisites
- Python 3.10 or higher
- `pip` package manager

#### 1. Clone the Repository

```bash
git clone https://github.com/gorisariavivan/llm-privacy-gateway.git
cd llm-privacy-gateway
``` 

#### 2. Set Up Virtual Environment & Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

pip install fastapi uvicorn spacy requests pydantic
python -m spacy download en_core_web_sm
``` 

### Usage

#### 1. Run the Gateway Proxy
```bash
uvicorn proxy:app --reload --port 8000
``` 
Access the interactive OpenAPI/Swagger documentation at: http://127.0.0.1:8000/docs

#### 2. Run the Empirical Benchmark Suite
```bash
python benchmark.py
```

### Project Structure

```text
llm-privacy-gateway/
├── proxy.py          # FastAPI interceptor & endpoint handler
├── redactor.py       # spaCy NER entity extraction & volatile vault logic
├── benchmark.py      # Automated latency & recall benchmarking suite
├── requirements.txt  # Python package dependencies
└── README.md         # Documentation
```

---

## Citation & Author Information

**Author:** Vivan Yogesh Gorisaria  
**Affiliation:** Independent Researcher, Mumbai, Maharashtra, India  
**Contact:** `gorisariavivan@gmail.com`  

*Targeted for publication in the Journal of Emerging Investigators (JEI).*
