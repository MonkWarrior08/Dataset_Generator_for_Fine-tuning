# Dataset Generator for Fine-tuning 📊

A Streamlit-based tool for generating training datasets from text files and PDFs for fine-tuning language models. This tool supports multiple AI models (Gemini, Claude, OpenAI) to generate high-quality question-answer pairs in various formats compatible with different models.

## Features ✨

- **Multiple AI Models**: Choose from Gemini, Claude, or OpenAI for dataset generation
- **File Upload**: Support for both text files (.txt) and PDF files (.pdf)
- **Smart Chunking**: Split content by word count instead of manual delimiters
- **Customizable Generation**: Control number of questions per chunk and conversation exchanges
- **Multiple Model Formats**: Support for Gemma, Llama, ChatML, Alpaca, ShareGPT, and Generic formats
- **Custom Prompts**: Write your own prompts for dataset generation
- **Real-time Progress**: Live progress tracking during generation
- **Instant Download**: Download generated datasets in JSONL format

## Installation 🛠️

1. Clone or download the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your API keys:
   - Create a `.env` file in the project directory
   - Add your API keys (see API Requirements section)
   - Or enter them directly in the app interface

## Usage 🚀

1. **Start the application**:
   ```bash
   streamlit run app.py
   ```

2. **Configure settings**:
   - Select your AI model (Gemini, Claude, or OpenAI)
   - Enter your API key
   - Upload a text file or PDF
   - Set chunking parameters (words per chunk)
   - Choose number of questions per chunk
   - Select conversation exchanges (1 or 2)
   - Choose your target model format

3. **Generate dataset**:
   - Write or customize your generation prompt
   - Click "Generate Dataset"
   - Monitor progress in real-time
   - Download the generated JSONL file

## API Requirements 🔑

You'll need an API key for at least one of the supported AI models:

### Google Gemini
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Add `GEMINI_API_KEY=your_key_here` to your `.env` file

### Anthropic Claude
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Create an API key
3. Add `ANTHROPIC_API_KEY=your_key_here` to your `.env` file

### OpenAI
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create an API key
3. Add `OPENAI_API_KEY=your_key_here` to your `.env` file

## Configuration Options ⚙️

- **Words per chunk**: 50-2000 words (default: 300)
- **Questions per chunk**: 1-10 questions (default: 3)
- **Conversation exchanges**: 1 or 2 exchanges
- **Model format**: Choose from 6 supported formats
- **Custom prompt**: Personalize the generation instructions

## License 📄

This project is open source and available under the MIT License.

## Support 💬

For issues or questions, please create an issue in the repository or contact the maintainers.

## Step 3: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501` 