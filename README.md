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

### Getting an OpenAI API Key
#### Recommended if you don't have a dedicated GPU to run Ollama locally

1. Follow OpenAI's [quickstart guide](https://platform.openai.com/docs/quickstart) to get your API key
2. Copy `.env.example` and rename it `.env`
3. Paste your key as `OPENAI_API_KEY`

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

# Search for the name of an item and get back the most likely Deity to have created it
python main.py get-most-likely [query]

# Utilizes AI to discover relationships between Deities, based on item descriptions
python main.py family-tree
```

## Configuration

Configuration can be set by adding values in a `.env` file:
