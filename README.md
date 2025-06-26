# FireSure Assignment

## Overview

This project extracts structured data and attachments from Indian ROC Form ADT-1 PDF files, saves the data as JSON, and generates a professional summary using Google Gemini AI.

## Features

- Extracts form fields and structured data from PDF.
- Extracts embedded file attachments from PDF.
- Outputs structured data as JSON.
- Generates a formal summary using Gemini AI.
- Saves summary as a text file.

## Setup

1. **Clone the repository and navigate to the project directory.**

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your `.env` file:**

   - Create a file named `.env` in the root directory.
   - Add your Gemini API key:

     ```env
     GEMINI_API_KEY=your_api_key_here
     ```

5. **Place your input PDF in the `input_pdfs/` directory.**

## Usage

Run the main script:

```bash
python main.py
```

- Extracted JSON will be saved to `output_json/output.json`.
- Attachments will be saved to `output_json/attachments/`.
- The summary will be saved to `output_json/summary.txt`.

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies.

## Project Structure

```tree
.
├── main.py
├── requirements.txt
├── generative_ai_script/
│   ├── __init__.py
│   └── summary_generator.py
├── input_pdfs/
└── output_json/
```

## Notes

- Ensure your PDF has AcroForm fields and/or embedded attachments.
- The script prints helpful messages if fields or attachments are missing.

---

For any issues, please check the error messages or contact the maintainer.
