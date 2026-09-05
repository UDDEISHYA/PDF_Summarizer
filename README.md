# AI Business Document Summarizer

An AI-powered Streamlit application that transforms lengthy business PDF documents — such as earnings call transcripts — into structured, actionable summaries using OpenAI's GPT models and LangChain.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.1%2B-1C3C3C?logo=chainlink&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Running the Streamlit App](#running-the-streamlit-app)
  - [Running the Script (CLI)](#running-the-script-cli)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
  - [Summarization Pipeline](#summarization-pipeline)
  - [Prompt Template](#prompt-template)
  - [PDF Export Pipeline](#pdf-export-pipeline)
- [Technology Stack](#technology-stack)
- [Sample Output](#sample-output)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Overview

Manually reading through 30+ page earnings transcripts and financial documents is time-consuming. This application automates that process by:

1. **Extracting** text from uploaded PDF documents.
2. **Summarizing** the content using OpenAI's GPT-4o-mini via LangChain's document chains.
3. **Presenting** the summary in a clean, structured Markdown format within a Streamlit web interface.
4. **Exporting** the summary as a downloadable PDF report rendered through Quarto.

The app ships with a sample Nike Q3 FY24 Earnings Call Transcript for immediate experimentation.

---

## Features

| Feature | Description |
|---|---|
| 📄 **PDF Upload** | Drag-and-drop or browse to upload any PDF document |
| 🤖 **AI Summarization** | Powered by GPT-4o-mini via LangChain's `StuffDocumentsChain` |
| 📝 **Dual Output Modes** | Choose between structured bullet-point reports or paragraph summaries |
| 📊 **Structured Reports** | Bullet-point mode generates organized sections: Earnings Summary, Financials, Risks, and Conclusions |
| 📥 **PDF Export** | Auto-generates a PDF report via Quarto and saves it to your Downloads folder |
| 🖥️ **Two-Column Layout** | Clean side-by-side interface — upload on the left, results on the right |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Streamlit Frontend                          │
│  ┌──────────────────────┐    ┌──────────────────────────────────┐  │
│  │   col1: Upload PDF   │    │   col2: Summarization Result     │  │
│  │   ☑ Template toggle  │    │   • Rendered Markdown            │  │
│  │   ▶ Summarize button │    │   • PDF download confirmation    │  │
│  └──────────┬───────────┘    └──────────────┬───────────────────┘  │
└─────────────┼───────────────────────────────┼─────────────────────┘
              │                               ▲
              ▼                               │
┌─────────────────────────────┐   ┌───────────┴───────────────────┐
│       PyPDFLoader           │   │     StuffDocumentsChain       │
│  PDF → List[Document]       │──▶│  All pages → single prompt    │
└─────────────────────────────┘   │        + LLMChain             │
                                  │   (PromptTemplate + ChatOpenAI)│
                                  └───────────┬───────────────────┘
                                              │
                                              ▼
                                  ┌───────────────────────────────┐
                                  │    Quarto Render Pipeline     │
                                  │  Markdown → .qmd → .pdf      │
                                  │  → moved to ~/Downloads       │
                                  └───────────────────────────────┘
```

---

## Prerequisites

Ensure the following are installed on your system before proceeding:

| Requirement | Version | Installation |
|---|---|---|
| **Python** | ≥ 3.9 | [python.org](https://www.python.org/downloads/) |
| **pip** | Latest | Bundled with Python |
| **Quarto** | ≥ 1.3 | [quarto.org/docs/get-started](https://quarto.org/docs/get-started/) |
| **OpenAI API Key** | — | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |

> [!NOTE]
> Quarto is required only for the PDF export feature. The summarization works without it.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/AI-Business-Summarization-App.git
cd AI-Business-Summarization-App
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install streamlit langchain langchain-community langchain-openai pypdf pyyaml
```

Or, if a `requirements.txt` is provided:

```bash
pip install -r requirements.txt
```

<details>
<summary><strong>📦 Full Dependency List</strong></summary>

| Package | Purpose |
|---|---|
| `streamlit` | Web application framework |
| `langchain` | LLM orchestration and chaining |
| `langchain-community` | Community document loaders (`PyPDFLoader`) |
| `langchain-openai` | OpenAI model integration (`ChatOpenAI`) |
| `pypdf` | PDF text extraction backend |
| `pyyaml` | YAML configuration file parsing |

</details>

---

## Configuration

### Setting Up Your API Key

1. Create a file named `credentials.yml` in the project root:

```yaml
openai: sk-proj-YOUR_API_KEY_HERE
```

2. Replace `sk-proj-YOUR_API_KEY_HERE` with your actual OpenAI API key.

> [!CAUTION]
> **Never commit your API key to version control.** Add `credentials.yml` to your `.gitignore`:
> ```bash
> echo "credentials.yml" >> .gitignore
> ```

### Environment Variable Alternative

For production deployments, prefer environment variables over config files:

```bash
export OPENAI_API_KEY="sk-proj-YOUR_API_KEY_HERE"
```

---

## Usage

### Running the Streamlit App

Launch the interactive web application:

```bash
streamlit run 02_document_summarizer_app.py
```

The app will open in your default browser at `http://localhost:8501`.

#### Step-by-Step

1. **Upload** a PDF document using the file uploader in the left column.
2. **Toggle** the "Use numbered bullet points?" checkbox to choose between:
   - ☑ **Checked** — Structured report with numbered sections (Earnings Summary, Financials, Risks, Conclusions).
   - ☐ **Unchecked** — Free-form paragraph summary.
3. **Click** "Summarize Document" to start the summarization.
4. **View** the AI-generated summary rendered as Markdown in the right column.
5. **Collect** the exported PDF from your `~/Downloads` folder.

### Running the Script (CLI)

For quick experimentation without the web interface, use the standalone script:

```bash
python 01_document_summarization.py
```

This processes the included Nike earnings transcript and prints the summary to stdout.

---

## Project Structure

```
AI-Business-Summarization-App/
│
├── 01_document_summarization.py    # Standalone CLI summarization script
├── 02_document_summarizer_app.py   # Streamlit web application (main app)
├── credentials.yml                 # API key configuration (DO NOT COMMIT)
├── LIBRARY_GUIDE.md                # Detailed guide to all libraries used
├── logic_flow.md                   # Application logic flow with diagrams
├── README.md                       # This file
│
└── pdf/
    └── NIKE-Inc-Q3FY24-OFFICIAL-Transcript-FINAL.pdf   # Sample document
```

| File | Description |
|---|---|
| `01_document_summarization.py` | Minimal script demonstrating core LangChain summarization concepts — document loading, prompt templates, and chain execution. Intended as a learning entry point. |
| `02_document_summarizer_app.py` | Full-featured Streamlit application with PDF upload, dual summarization modes, and PDF export via Quarto. |
| `LIBRARY_GUIDE.md` | Beginner-friendly walkthrough of every library in the project — what it does, why it's needed, and how it connects to the pipeline. |
| `logic_flow.md` | ASCII flow diagrams documenting the application's complete call graph and data flow. |
| `credentials.yml` | YAML file storing the OpenAI API key. Must be created locally and excluded from version control. |

---

## How It Works

### Summarization Pipeline

```
PDF File (upload)
     │
     ▼
┌──────────────────┐
│   PyPDFLoader    │  Extract text from each page
│   → List[Doc]    │  into LangChain Document objects
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  PromptTemplate  │  Define the structure for the
│  + LLMChain      │  AI's response
└────────┬─────────┘
         │
         ▼
┌──────────────────────┐
│ StuffDocumentsChain  │  Combine all pages into a single
│ .invoke(docs)        │  prompt and send to GPT-4o-mini
└────────┬─────────────┘
         │
         ▼
   Markdown Summary
```

The "stuff" strategy concatenates all document pages into a single prompt. This works well for documents within the model's context window (~128K tokens for GPT-4o-mini). For very large documents, consider switching to `map_reduce` or `refine` chain types.

### Prompt Template

When bullet-point mode is enabled, the following structured template guides the LLM output:

```
# Insert Descriptive Report Title

## Earnings Call Summary
Use 3 to 7 numbered bullet points

## Important Financials
Describe the most important financials discussed during the call.
Use 3 to 5 numbered bullet points.

## Key Business Risks
Describe any key business risks discussed on the call.
Use 3 to 5 numbered bullets.

## Conclusions
Conclude with any overarching business actions the company is pursuing
that may have positive or negative implications, and what those are.
```

### PDF Export Pipeline

```
Markdown Summary
     │
     ▼
┌──────────────────────┐
│  NamedTemporaryFile  │  Write summary as .qmd
│  (suffix=".qmd")    │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  quarto render       │  Convert .qmd → .pdf
│  --to pdf            │  via Quarto CLI
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│  shutil.move()       │  Move PDF to ~/Downloads
└──────────────────────┘
```

---

## Technology Stack

| Layer | Technology | Role |
|---|---|---|
| **Frontend** | [Streamlit](https://streamlit.io/) | Interactive web UI with file upload, toggles, and Markdown rendering |
| **LLM** | [OpenAI GPT-4o-mini](https://platform.openai.com/docs/models) | Language model for text comprehension and summarization |
| **Orchestration** | [LangChain](https://python.langchain.com/) | Chains, prompts, and document loaders for LLM workflows |
| **PDF Parsing** | [PyPDF](https://pypdf.readthedocs.io/) | Text extraction from PDF documents |
| **PDF Generation** | [Quarto](https://quarto.org/) | Markdown-to-PDF rendering engine |
| **Configuration** | [PyYAML](https://pyyaml.org/) | YAML-based credential management |

---

## Sample Output

When processing the included Nike Q3 FY24 Earnings Call Transcript with bullet-point mode enabled, the app produces a report structured as:

> ### Nike Q3 FY24 Earnings Call Report
>
> **Earnings Call Summary**
> 1. Revenue declined 1% on a reported basis...
> 2. NIKE Direct revenues were $5.4 billion...
> 3. ...
>
> **Important Financials**
> 1. Gross margin expanded 150 basis points to 44.8%...
> 2. ...
>
> **Key Business Risks**
> 1. Consumer traffic softness in key markets...
> 2. ...
>
> **Conclusions**
> Nike is pursuing a multi-year innovation cycle...

*Actual output varies based on document content and model responses.*

---

## Troubleshooting

<details>
<summary><strong>❌ <code>ValidationError</code> — Invalid API Key Format</strong></summary>

**Cause:** The `credentials.yml` file is not formatted correctly.

**Fix:** Ensure the file contains a valid YAML key-value pair:

```yaml
openai: sk-proj-YOUR_ACTUAL_KEY
```

Do **not** wrap the key in quotes unless it contains special YAML characters.

</details>

<details>
<summary><strong>❌ <code>FileNotFoundError: credentials.yml</code></strong></summary>

**Cause:** The credentials file is missing from the project root.

**Fix:** Create the file as described in the [Configuration](#configuration) section.

</details>

<details>
<summary><strong>❌ <code>quarto: command not found</code></strong></summary>

**Cause:** Quarto is not installed or not on your system PATH.

**Fix:** Install Quarto from [quarto.org/docs/get-started](https://quarto.org/docs/get-started/) and restart your terminal.

</details>

<details>
<summary><strong>❌ <code>ModuleNotFoundError: No module named 'langchain_community'</code></strong></summary>

**Cause:** Missing Python packages.

**Fix:**

```bash
pip install langchain langchain-community langchain-openai pypdf
```

</details>

<details>
<summary><strong>⚠️ Summary is incomplete or cuts off</strong></summary>

**Cause:** The document may exceed the model's context window, or `max_tokens` is too low.

**Fix:** For very large documents, modify the chain type in the code:

```python
# Change from "stuff" to "map_reduce" for large documents
summarizer_chain = load_summarize_chain(llm=model, chain_type="map_reduce")
```

</details>

---

## Contributing

Contributions are welcome. To contribute:

1. **Fork** the repository.
2. **Create** a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit** your changes with clear, descriptive messages.
4. **Push** to your fork and open a **Pull Request**.

Please ensure your code follows the existing style and includes relevant documentation updates.

---

## License

This project is distributed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

## Acknowledgements

- [Business Science University](https://www.business-science.io/) — Python for Generative AI Course
- [LangChain](https://python.langchain.com/) — LLM application framework
- [OpenAI](https://openai.com/) — GPT-4o-mini language model
- [Streamlit](https://streamlit.io/) — Rapid web app prototyping
- [Quarto](https://quarto.org/) — Scientific and technical publishing
