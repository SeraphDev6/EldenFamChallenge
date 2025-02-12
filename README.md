# EldenFam CLI

A command-line interface tool built with Typer and integrated with Ollama for local LLM operations.

## Prerequisites

Before installing this CLI tool, you need to either:
- Have Ollama installed on your system.
- Put your OpenAI API key in a .env file

### Installing Ollama

#### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### MacOS and Windows
1. Download Ollama from the [Official Website](https://ollama.com/download)
2. Run the executable to startup Ollama


After installation, verify Ollama is working:
```bash
ollama pull llama3:8b
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/my-cli-tool.git
cd my-cli-tool
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install the package dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The CLI provides several commands for interacting with the data provide:

```bash
# Get help
python main.py --help

# Normalize data to Lists or Objects, making working with the LLM easier
python main.py normalize

# Search the data to answer a question from the user
python main.py ask [query]
```

## Configuration

Configuration can be set by adding values in a `.env` file:
