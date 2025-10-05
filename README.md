Bruin Buddy — UCLA Virtual Student Advisor 🐻💙

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!(Disclaimer: It may not work due to the use of knowledge base from aws workshop, also credentials are require to connect to them, this is only used to provide the source code and for competition purposes and will not work without the aws credentials. But you can add your own knowledge base in the tool.py and your own aws credential for the project to run!)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

A Streamlit-based chat UI that wraps a Strands agent to provide UCLA-focused help (clubs, academics, career resources). This repo contains the Streamlit front-end and a small bruin_buddy agent wrapper. The app streams agent replies, shows quick-action buttons, and uses UCLA colors in the UI.

Overview

Friendly, student-focused assistant for UCLA students (clubs, career, campus questions).

Built with Streamlit for the UI and an agent (via bruin_buddy.get_agent()) for routing/searching knowledge bases.

Uses @st.cache_resource to keep the agent instance resident and streams outputs to the UI.

Quick start
Prerequisites

Python 3.10+

Git

pip (or a virtualenv/venv)

Recommended local install

# clone (replace with your repo URL)

git clone git@github.com:your-username/BruinBuddy.git
cd BruinBuddy

# create a venv (optional but recommended)

python -m venv .venv
source .venv/bin/activate # macOS / Linux

# .venv\Scripts\activate # Windows

# install dependencies

1. pip install poetry
   poetry install

2. pip install -r requirements.txt

# run the Streamlit app

streamlit run app.py

If your main Streamlit file is named differently (e.g., streamlit_app.py), run streamlit run <your-file>.py.

Configuration (environment & secrets)

Create a .env (do not commit it) or set environment variables in your deploy platform. Example .env keys used by the code snippet you provided:

BRUIN_CLUB_TOOL1_ID= <Your knowledge base1>
BRUIN_CAREER_TOOL2_ID= <Your knowledge base2>
AWS_REGION=<Your Region>
BRUIN_SYSTEM_PROMPT_FILE=./system_prompt.txt # optional: path to system prompt

Security note: The system_prompt contains internal routing instructions — treat it like a secret. Do not commit real API keys or the system prompt to a public repository; use your host's secret manager or .env and include .env in .gitignore. Keep your own aws credentials save with

aws configure
<your credentials>
