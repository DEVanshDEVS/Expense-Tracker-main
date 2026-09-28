# Expense Tracker App

A Flask-based expense tracker that combines transaction management, dashboard analytics, and local LLM-powered financial insights using Llama 3 through Ollama.

## Features

- Add and manage income and expense transactions.
- Dashboard views for income vs. expenses, expense categories, and expenditure over time.
- AI Insights powered by Llama 3 through a local Ollama runtime.
- Structured financial context passed to the LLM with transaction type, category, and amount.

## Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy
- **Forms:** Flask-WTF, WTForms
- **Database:** SQLite through SQLAlchemy
- **AI:** Llama 3, Ollama
- **Frontend:** HTML, CSS, JavaScript, Chart.js

## Project Structure

```text
Expense_Tracker-main/
├── application/
│   ├── ai.py
│   ├── form.py
│   ├── models.py
│   ├── routes.py
│   └── templates/
├── instance/
├── requirements.txt
├── run.py
└── README.md
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/DEVanshDEVS/Expense-Tracker-main.git
cd Expense-Tracker-main/Expense_Tracker-main
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and prepare Ollama

Install Ollama and make sure the Llama 3 model is available locally:

```bash
ollama pull llama3
```

### 5. Run the application

```bash
python run.py
```

Then open:

```text
http://127.0.0.1:5000/
```

## AI Insights Workflow

The AI Insights endpoint retrieves transaction records from the database and converts them into structured context containing:

- Transaction type
- Category
- Amount

The prompt explicitly instructs the model not to infer a currency or time period that is not present in the source data. This keeps the model's analysis grounded in the application's actual records.

The Ollama model runs locally, so transaction data does not need to be sent to a third-party hosted LLM API.

## Configuration

For production deployments, set a `SECRET_KEY` environment variable. If it is not provided, the application generates a temporary key at startup.

Debug mode is disabled by default. To enable it locally:

```text
FLASK_DEBUG=true
```

## License

This project is open-source and free to use.
