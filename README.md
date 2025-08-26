# Temporal-Multi-Document-Summarizer
An NLP tool for creating chronological summaries from multiple sources, like news articles or historical texts, using temporal annotation (TimeML).


# Temporal Multi-Document Summarizer

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An NLP project to build a robust temporal annotation tool (TimeML) as the foundational component for a future chronological multi-document summarizer.

## Table of Contents

1.  [About The Project](#about-the-project)
2.  [Project Status](#project-status)
3.  [Tech Stack](#tech-stack)
4.  [Getting Started](#getting-started)
5.  [Usage](#usage)
6.  [License](#license)
7.  [Contact](#contact)

## About The Project

Narratives describing complex events are often spread across multiple documents, resulting in varied perspectives and timelines that are difficult for both humans and machines to synthesize. A simple concatenation or standard summarization of these texts often loses the critical chronological context of *when* events occurred and in what sequence.

This project addresses this challenge by establishing a robust pipeline, with its primary focus on the development of a **Temporal Annotation Tool**. This tool is designed to parse raw text and enrich it with the ISO-TimeML standard, creating a structured, machine-readable timeline of events. This annotated data serves as the essential ground truth for the project's ultimate vision: to power a **Temporal Multi-Document Summarizer**.

By first understanding the explicit temporal relationships within and between documents, the future summarization model will be capable of generating a single, coherent, and chronologically accurate narrative. The initial use-case for developing and testing this annotation tool is the harmonizing of the Holy Week accounts from the four Gospels.

## Project Status

This project is divided into two main components:

1.  **`temporal_annotator` (In Active Development):** The core focus of the current work. This tool takes raw text files as input and produces TimeML-annotated XML files.
2.  **`multi_doc_summarizer` (Planned for Future Development):** This component will consume the annotated data to produce summaries. Development will begin after the annotation tool is stable and validated.

## Tech Stack

* **Python 3.9+**
* **LangChain:** For orchestrating LLM-based annotation.
* **Google Gemini / OpenAI GPT:** As the core LLM for NLP tasks.

## Getting Started

### Prerequisites

* Python 3.9 or higher
* Git

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/temporal-multi-document-summarizer.git](https://github.com/your-username/temporal-multi-document-summarizer.git)
    cd temporal-multi-document-summarizer
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up your API Key:**
    Create a file named `.env` in the root directory and add your API key:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```

## Usage

The primary entry point for the project is the temporal annotation tool. You can run it from the command line.

**To annotate a single file:**

```sh
python src/temporal_annotator/main.py --input_file data/raw/matthew.txt --output_file data/processed/matthew_timeml.xml
```

This will read the specified input file, process it through the annotation pipeline, and save the TimeML output to the processed data folder.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

André Felipe Cunha - [LinkedIn Profile]([https://www.linkedin.com/](https://www.linkedin.com/in/andre-felipe-cunha)) - afcc2000@gmail.com

Project Link:  [https://github.com/afcc2000/Temporal-Multi-Document-Summarizer)](https://www.linkedin.com/in/andre-felipe-cunha)
