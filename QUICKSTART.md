# Quick Start Guide 🚀

Get your dataset generator up and running in just 3 steps!

## Step 1: Setup Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp env_template.txt .env
```

## Step 2: Get Your API Key

Choose one of the supported AI models and get an API key:

### Option A: Google Gemini (Recommended)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key
4. Edit `.env` file and replace `your_gemini_api_key_here` with your actual API key

### Option B: Anthropic Claude
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Create an API key
3. Copy your API key
4. Edit `.env` file and replace `your_claude_api_key_here` with your actual API key

### Option C: OpenAI
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create an API key
3. Copy your API key
4. Edit `.env` file and replace `your_openai_api_key_here` with your actual API key

## Step 3: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## First Dataset Generation

1. **Select AI model**: Choose from Gemini, Claude, or OpenAI
2. **Choose specific model**: Select the exact model variant you want
3. **Upload a file**: Click "Choose a file" and upload a .txt or .pdf file
4. **Configure settings**:
   - Words per chunk: 300 (good starting point)
   - Questions per chunk: 3
   - Conversation exchanges: 1-5 (number of back-and-forth exchanges)
   - Output format: Choose your target model format
5. **Write custom prompt**: Enter your generation prompt in the main area
6. **Generate**: Click "Generate Dataset" and wait for completion
7. **Download**: Click "Download Dataset" to save your JSONL file

## Available Models

### Gemini Models
- **gemini-2.5-flash**: Fast and efficient
- **gemini-2.5-pro**: Higher quality, slower
- **gemini-1.5-flash**: Previous generation, fast

### Claude Models
- **claude-3-5-sonnet**: Best balance of speed and quality
- **claude-3-5-haiku**: Fastest, good for simple tasks

### OpenAI Models
- **gpt-4o**: Latest and most capable
- **gpt-4o-mini**: Smaller, faster version
- **o3-mini**: Advanced reasoning model

## Output Formats

- **Gemma**: Google's Gemma model format
- **Llama**: Meta's Llama model format
- **OpenAI**: OpenAI's message format
- **Alpaca**: Stanford's Alpaca format

Ready to create your first dataset? Let's go! 🎉 