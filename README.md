# Synthetic Lab: AI-Powered Synthetic Users for Product Research

Synthetic Lab is an AI-powered research platform that generates realistic synthetic user personas and simulates surveys and interviews to help researchers explore product ideas, understand user preferences, and identify potential insights.

## Overview

Traditional product research can require significant time and resources to recruit participants and collect feedback. Synthetic Lab provides an AI-assisted environment for preliminary research and hypothesis exploration using simulated users.

The platform generates synthetic personas with demographic and behavioral characteristics, conducts simulated research interactions, analyzes responses, and generates research reports.

> **Note:** Synthetic user responses are simulated and should not be treated as a substitute for feedback from real users.

## Features

- **AI Persona Generation:** Create synthetic user personas based on a target audience and research objective.
- **Survey Mode:** Generate simulated survey responses from synthetic personas.
- **Interview Mode:** Conduct AI-powered interviews with synthetic users.
- **Persona Consistency Validation:** Check whether responses remain consistent with persona characteristics.
- **Insight Analysis:** Identify themes and summarize patterns in research responses.
- **Adoption Evaluation:** Estimate whether synthetic users indicate interest in a proposed product.
- **Research Dashboard:** Review research outputs and validation results.
- **PDF Report Generation:** Generate downloadable research reports.

## Technology Stack

- **Programming Language:** Python
- **Frontend:** Streamlit
- **Backend:** FastAPI
- **AI Model:** Google Gemini
- **AI Integration:** LangChain
- **Vector Storage:** ChromaDB
- **Data Validation:** Pydantic
- **Testing:** Pytest
- **Version Control:** Git and GitHub

## Project Structure

```text
synthetic-user-platform/
├── agents/
├── models/
├── services/
├── tests/
├── database/
├── app.py
├── dashboard_page.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

## Prerequisites

- Python installed on your system
- Git
- A Google Gemini API key

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Rakshith-Kn/synthetic-user-platform.git
cd synthetic-user-platform
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root using `.env.example` as a reference.

Add your Gemini API key:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own API key. Never commit your actual `.env` file or expose your API key publicly.

### 5. Start the backend

Open a terminal in the project directory and run:

```powershell
uvicorn main:app --reload
```

The FastAPI backend will be available at:

`http://127.0.0.1:8000`

API documentation:

`http://127.0.0.1:8000/docs`

### 6. Start the frontend

Open a second terminal, activate the virtual environment, and run:

```powershell
python -m streamlit run app.py
```

Streamlit will display a local URL in the terminal, usually:

`http://localhost:8501`

## Testing

Run the available tests with:

```powershell
python -m pytest
```

## Example Use Case

CareSphere AI is an example healthcare and wellness platform that can be explored using synthetic personas. Researchers can simulate how different user profiles might respond to features such as appointment management, wellness tracking, medication reminders, and an AI health assistant.

These simulated responses can help identify questions and hypotheses to investigate with real users. They do not establish clinical accuracy or actual market demand.

## Limitations

- Synthetic responses may contain inaccuracies or reflect biases in the underlying AI model.
- Simulated preferences do not guarantee real-world user behavior.
- Research findings should be validated with real participants before making important product decisions.
- AI-generated outputs should be reviewed before being used in reports or decisions.

## Future Enhancements

- Improved persona memory and response consistency
- More advanced research analytics and visualizations
- Expanded persona evaluation and validation
- Persistent storage of research experiments
- Deployment as an accessible web application

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

**Rakshitha K N**

AI-Powered Synthetic Users for Product Research

GitHub: [Rakshith-Kn](https://github.com/Rakshith-Kn)
