
# 🚀 CryptoPulse AI

### AI-Powered Cryptography & Fintech Intelligence Newsletter

CryptoPulse AI is an automated research and newsletter-generation system that collects, verifies, analyzes, and summarizes important developments in cryptography, fintech, payment security, and cybersecurity.

It uses AI agents to transform information from research papers, official announcements, security advisories, and industry sources into a structured newsletter.

The goal is to help fintech professionals, researchers, developers, and technology enthusiasts stay informed without manually searching multiple websites every day.

---

# 📌 Table of Contents

1. About the Project
2. Key Features
3. How It Works
4. Technology Stack
5. Project Structure
6. Requirements
7. Getting Started
8. Running on a Mobile Phone
9. Running on Windows
10. Environment Configuration
11. Running Tests
12. Newsletter Schedule
13. Troubleshooting
14. Security and API Keys
15. Future Improvements
16. Contributing
17. License

---

# 1. About the Project

Keeping up with cryptography and fintech developments requires monitoring multiple sources, including:

- Research papers
- Cryptographic standards
- Payment security announcements
- RBI notifications
- NPCI updates
- Cybersecurity advisories
- Industry news

CryptoPulse AI automates this research process.

It uses multiple AI-powered stages to:

1. Discover relevant information.
2. Identify useful articles and research papers.
3. Remove duplicate links.
4. Score content based on relevance.
5. Verify that source pages are accessible.
6. Generate technical summaries.
7. Explain practical fintech implications.
8. Organize everything into a newsletter.
9. Deliver the newsletter through email.

The initial version is designed for a small group of subscribers, with the architecture intended to support expansion later.

---

# 2. Key Features

| Feature | Description |
|---|---|
| Automated Research | Searches multiple information sources |
| Research Paper Discovery | Retrieves relevant arXiv papers |
| Official Source Monitoring | Monitors NIST, RBI and CERT-In |
| Relevance Scoring | Ranks articles based on topic relevance |
| Duplicate Detection | Removes duplicate article URLs |
| Source Verification | Checks whether source pages contain readable content |
| AI Analysis | Generates summaries and fintech impact explanations |
| Newsletter Generation | Organizes articles into readable sections |
| Email Delivery | Sends newsletters through Gmail SMTP |
| Scheduled Execution | Designed for automated GitHub Actions runs |

---

# 3. How It Works

CryptoPulse AI follows a multi-stage workflow.

Research Sources
        ↓
Research Agent
        ↓
Article Normalization
        ↓
Relevance Agent
        ↓
Duplicate Removal
        ↓
Verification Agent
        ↓
Analysis Agent
        ↓
Newsletter Agent
        ↓
HTML Newsletter
        ↓
Email Delivery

### Stage 1: Research

Collect information from sources such as:

- Tavily web search
- arXiv research papers
- NIST
- CERT-In
- RBI

### Stage 2: Relevance Filtering

Articles receive a relevance score based on their relationship to cryptography, fintech, payment security, and cybersecurity.

### Stage 3: Verification

The application attempts to retrieve the original article page and checks whether useful content is available.

### Stage 4: AI Analysis

Groq-powered language models generate:

- Short summaries
- Technical explanations
- Practical fintech implications

### Stage 5: Newsletter Generation

The selected articles are grouped into categories and converted into an HTML newsletter.

### Stage 6: Email Delivery

The newsletter can be delivered to configured subscribers using Gmail SMTP.

---

# 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12+ | Main programming language |
| LangChain | LLM integration |
| LangGraph | Agent workflow orchestration |
| Groq | AI inference |
| Tavily | Web research |
| arXiv API | Research paper discovery |
| Pydantic | Data validation |
| BeautifulSoup | Web content extraction |
| HTTPX | HTTP requests |
| SQLite | Local database foundation |
| Gmail SMTP | Email delivery |
| GitHub Actions | Scheduled automation |

---

# 5. Project Structure

```text
cryptopulse_ai/
│
├── app/
│   ├── agents/
│   │   ├── research_agent.py
│   │   ├── relevance_agent.py
│   │   ├── verification_agent.py
│   │   ├── analysis_agent.py
│   │   └── newsletter_agent.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │   ├── topics.yaml
│   │   ├── sources.yaml
│   │   └── logging_config.py
│   │
│   ├── graph/
│   │   ├── state.py
│   │   ├── nodes.py
│   │   ├── edges.py
│   │   └── workflow.py
│   │
│   ├── schemas/
│   ├── services/
│   ├── tools/
│   └── utils/
│
├── data/
├── logs/
├── scripts/
├── templates/
├── tests/
├── .github/
│   └── workflows/
│
├── .env.example
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── README.md
└── LICENSE
```

---

# 6. Requirements

Before running the project locally, install:

- Python 3.12 or newer
- Git
- A Groq API key
- A Tavily API key
- A Gmail account with an App Password

### Get API keys

**Groq API**

https://console.groq.com/

**Tavily API**

https://app.tavily.com/

**Gmail App Password**

https://myaccount.google.com/apppasswords

An app password is different from your normal Gmail password.

Never share your API keys or commit them to GitHub.

---

# 7. Getting Started

## Step 1: Download the project

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd cryptopulse_ai
```

Alternatively, download the repository as a ZIP file from GitHub and extract it.

## Step 2: Create a virtual environment

```bash
python -m venv venv
```

## Step 3: Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source venv/bin/activate
```

## Step 4: Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Step 5: Configure environment variables

Copy `.env.example` to `.env`.

Windows:

```powershell
Copy-Item .env.example .env
```

macOS / Linux:

```bash
cp .env.example .env
```

Open `.env` and add your credentials.

Refer to the Environment Configuration section below.

## Step 6: Run tests

```bash
python -m pytest
```

## Step 7: Run CryptoPulse AI

```bash
python -m scripts.run_local
```

Check the terminal and the `logs/` directory for execution information.

---

# 8. Running on a Mobile Phone

You do not need to install Python directly on your phone.

The recommended option is GitHub Codespaces.

Codespaces provides a cloud development environment that can be opened in a mobile browser.

### What you need

- A GitHub account
- Your CryptoPulse AI repository uploaded to GitHub
- A mobile browser
- Internet access

### Step 1: Open GitHub

Visit:

https://github.com/

Sign in to your account.

### Step 2: Open your repository

Navigate to your CryptoPulse AI repository.

### Step 3: Create a Codespace

1. Open the repository.
2. Tap the green **Code** button.
3. Select the **Codespaces** tab.
4. Select **Create codespace on main**.

GitHub will prepare a cloud development environment.

### Step 4: Open the terminal

When the Codespace loads:

1. Open the terminal.
2. Check that the repository files are visible.
3. Run:

```bash
python --version
```

If Python is available, continue.

### Step 5: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 6: Configure secrets

Do not upload your real `.env` file to GitHub.

For a temporary Codespaces session, create a `.env` file in the terminal and add your credentials securely.

For example:

```bash
nano .env
```

Enter your actual credentials in the editor, save, and exit.

Do not paste secrets into public issues, commits, or screenshots.

### Step 7: Run the application

```bash
python -m scripts.run_local
```

### Important mobile note

Codespaces runs on a cloud machine, not directly on your phone.

It may have usage limits or incur charges depending on your GitHub account and Codespaces allowance.

For scheduled newsletter delivery, GitHub Actions is a better long-term option because it can run without keeping Codespaces open.

---

# 9. Running on Windows

Open PowerShell inside the project folder.

Activate your virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies if this is your first setup:

```powershell
python -m pip install -r requirements.txt
```

Run tests:

```powershell
python -m pytest
```

Run the application:

```powershell
python -m scripts.run_local
```

If PowerShell blocks virtual environment activation, use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

---

# 10. Environment Configuration

The `.env.example` file contains the configuration template.

Create your own `.env` file using the following variables:

```dotenv
APP_NAME=CryptoPulse AI
APP_ENV=development
TIMEZONE=Asia/Kolkata

LLM_PROVIDER=groq
LLM_MODEL=openai/gpt-oss-120b
LLM_TEMPERATURE=0.2
LLM_MAX_TOKENS=2048

GROQ_API_KEY=
HUGGINGFACE_API_KEY=

TAVILY_API_KEY=
TAVILY_MAX_RESULTS=5
TAVILY_SEARCH_DEPTH=basic
MAX_RESEARCH_ITERATIONS=2

DATABASE_URL=sqlite:///./data/cryptopulse.db

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_SENDER=
EMAIL_PASSWORD=

NEWSLETTER_HOUR=11
NEWSLETTER_MINUTE=0
NEWSLETTER_DAYS=[0,2,4]

MAX_ARTICLES_PER_NEWSLETTER=10
MIN_RELEVANCE_SCORE=60
```

### Configuration explanation

| Variable | Purpose |
|---|---|
| GROQ_API_KEY | Groq authentication |
| TAVILY_API_KEY | Web search authentication |
| EMAIL_SENDER | Gmail address used for delivery |
| EMAIL_PASSWORD | Gmail App Password |
| LLM_MODEL | Selected Groq model |
| TIMEZONE | Newsletter timezone |
| NEWSLETTER_HOUR | Delivery hour |
| NEWSLETTER_DAYS | Monday, Wednesday, Friday |
| MAX_ARTICLES_PER_NEWSLETTER | Maximum article count |
| MIN_RELEVANCE_SCORE | Minimum article score |

Leave `HUGGINGFACE_API_KEY` blank when using Groq.

Never commit `.env` to Git.

---

# 11. Running Tests

Run the complete test suite:

```bash
python -m pytest
```

Run an individual test:

```bash
python -m pytest tests/test_graph.py
```

Run tests with detailed output:

```bash
python -m pytest -v
```

---

# 12. Newsletter Schedule

The intended newsletter schedule is:

| Day | Time |
|---|---|
| Monday | 11:00 AM IST |
| Wednesday | 11:00 AM IST |
| Friday | 11:00 AM IST |

The GitHub Actions workflow will be configured to execute on this schedule.

GitHub Actions uses UTC for scheduled cron expressions.

11:00 AM IST = 05:30 UTC.

Scheduled runs may be delayed by GitHub during periods of high load.

---

# 13. Troubleshooting

### Problem: Python is not recognized

Install Python 3.12+ and ensure it is added to your system PATH.

Check:

```bash
python --version
```

### Problem: Module not found

Activate the virtual environment and install dependencies:

```bash
python -m pip install -r requirements.txt
```

### Problem: API key missing

Check that:

- `.env` exists in the project root.
- The variable name is correct.
- The value is not surrounded by unnecessary quotes or spaces.

### Problem: Gmail authentication failed

Check that:

- Two-step verification is enabled.
- You generated a Gmail App Password.
- You used the App Password instead of your regular Gmail password.

### Problem: No newsletter generated

Check the research logs, relevance scores, and source availability.

Some sources may block automated requests or temporarily become unavailable.

---

# 14. Security and API Keys

Security is important because CryptoPulse AI uses external API credentials.

Follow these rules:

1. Never commit `.env`.
2. Never publish API keys in screenshots.
3. Never share Gmail App Passwords.
4. Use GitHub Secrets for automated deployments.
5. Rotate credentials if they are accidentally exposed.
6. Avoid storing subscriber information in public repositories.

---

# 15. Future Improvements

Planned enhancements include:

- Personalized newsletters for each subscriber.
- SQLite-based subscriber management.
- More research source integrations.
- Better article relevance classification.
- Advanced source verification.
- Newsletter preview dashboard.
- Mobile-friendly web interface.
- Telegram delivery.
- Improved analytics and reporting.
- Automated deployment through GitHub Actions.

---

# 16. Contributing

Contributions and suggestions are welcome.

To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Implement your changes.
4. Run the test suite.
5. Submit a pull request.

Please keep API keys and personal credentials out of commits.

---

# 17. License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

## CryptoPulse AI

**Research smarter. Understand faster. Stay ahead.**
