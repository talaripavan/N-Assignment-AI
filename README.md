# N-Assignment-AI

AI-powered document classification and extraction system using OpenAI API.

## Features

- **Document Classification**: Automatically classify document types from images
- **Data Extraction**: Extract structured data from documents based on custom schemas
- **Accuracy Evaluation**: Evaluate classification accuracy with detailed metrics

## Prerequisites

- Python version = 3.11.0
- OpenAI API key
- Git

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/talaripavan/N-Assignment-AI.git
cd N-Assignment-AI
```

### 2. Set Up Virtual Environment

```bash
python -m venv env
./env/scripts/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual OpenAI API key.

## Usage

### Document Classification

Classify document types from images:

```bash
python test_classifier.py
```

### Data Extraction

Extract structured data from documents based on a specific schema:

```bash
python test_extraction_schema.py
```

### Accuracy Evaluation

Evaluate classification accuracy with performance metrics:

```bash
python test_evaluator.py
```

## Project Structure

- `test_classifier.py` - Document type classification script
- `test_extraction_schema.py` - Schema-based data extraction script
- `test_evaluator.py` - Classification accuracy evaluation script
- `requirements.txt` - Python dependencies

## Limitations

### Image Quality Requirements

The system's accuracy depends heavily on image quality. **Blurry or unclear images will result in poor extraction results.**

#### Known Issues by Document Type

The following document types have shown detection failures with unclear/blurry images:

- **Bank Statements**: Images [2, 98]
- **Check Statements**: Images [1, 3, 4, 88, 81, 83]
- **ITR Forms 16**: Images [12, 14]
- **Salary Slip**: Images [43, 101]
- **Utility Bills**: Images [1, 91]

**Note**: If the image quality is poor or text is difficult to read with the naked eye, the system will not be able to accurately predict the output.

## Troubleshooting

- **Virtual environment not activating**: Ensure you're using PowerShell or Command Prompt (not Git Bash)
- **API key errors**: Verify your `.env` file is in the project root and contains a valid OpenAI API key
- **Module not found**: Run `pip install -r requirements.txt` again
- **Poor extraction results**: Check image quality - ensure documents are clear and well-lit (see Limitations section)
