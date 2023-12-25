# Your Interactive Python & SQL Learning Companion
Unlock Your Coding Potential: Explore, Learn, and Code with Our Interactive Python and SQL ChatBot!

## Table of Contents

[[_TOC_]]

## Prerequisites

Before start working, please make sure you have installed and configured the following prerequisites.

### 📦 Installation

Run the followind command to complete the required Python packages.

```bash
poetry install
``````

## Project Architecture

The project structure of this repository is as follows:

```bash
.
├── README.md
├── app
│   ├── __init__.py
│   ├── config.py
│   ├── db
│   │   ├── __init__.py
│   │   ├── data_model.py
│   │   ├── sql.py
│   │   └── vectordb.py
│   ├── dependencies.py
│   ├── routers
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── dashboard.py
│   │   ├── landing.py
│   │   └── users.py
│   └── templates
│       ├── 404.html
│       ├── assets
│       │   ├── CSS,JS and Images
│       ├── chatbot.html
│       ├── dashboard.html
│       ├── forgot-password.html
│       ├── landing
│       │   └── index.html
│       ├── login.html
│       ├── profile.html
│       ├── register.html
│       ├── settings.html
│       ├── shared
│       │   ├── base.html
│       │   ├── footer_script.html
│       │   ├── header_script.html
│       │   ├── navbar.html
│       │   └── sidebar.html
│       └── table.html
├── llms
│   └── __init__.py
├── main.py
├── poetry.lock
├── pyproject.toml
└── pythonqa.db
``````

## Screenshots
### Landing Page
![ Landing Page](https://drive.google.com/uc?id=1tvoQg1n1-PZtQctLmL2hGE_0f9_ewI5l)

### User Dashboard
![User Dashboard](https://drive.google.com/uc?id=1A3utPcXfhkbEtsOMDsvWvJBLXeo5nzWX)

### ChatBot UI
![ChatBot UI](https://drive.google.com/uc?id=1DsodeANGxEhypAKgjkvxdAHRf_0CAFNv)

### Profile Information Update
![Profile Information Update](https://drive.google.com/uc?id=1mdnLWOlND6Gwb4AiWmGlHQ-T5bqT0c7I)

### Password Change
![Password Change](https://drive.google.com/uc?id=1qHM8-FebbgcF3LjJvAe-hv2_nGq4_-2_)