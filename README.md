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
- **Conversation exchanges**: 1-5 exchanges (default: 1)
- **Model format**: Choose from 4 supported formats
- **Custom prompt**: Personalize the generation instructions with enhanced prompt area

## Model Recommendations 💡

### For Beginners
- **Gemini 2.5-flash**: Free tier available, good performance
- **Claude 3.5-haiku**: Fast and reliable for simple tasks

### For High Quality
- **Claude Sonnet-4**: Best overall quality and reasoning
- **Gemini 2.5-pro**: Excellent for complex content

### For Cost Efficiency
- **OpenAI gpt-4o-mini**: Good balance of cost and quality
- **Gemini 2.5-flash**: Free tier for testing

### For Advanced Reasoning
- **OpenAI o3-mini**: Specialized reasoning capabilities
- **Claude 3-7-sonnet**: Enhanced analytical thinking

## Tips for Best Results 🎯

1. **Chunk Size**: Use 200-500 words per chunk for optimal results
2. **Questions**: Start with 2-4 questions per chunk
3. **Prompts**: Be specific about the type of content you want to generate
4. **File Quality**: Ensure your source files are well-formatted and readable
5. **Model Selection**: Choose models based on your content complexity and budget

## Troubleshooting 🔧

- **API Errors**: Check your API key in the .env file and internet connection
- **PDF Issues**: Ensure PDF files are text-based (not scanned images)
- **Memory Issues**: Reduce chunk size or questions per chunk for large files
- **Generation Failures**: Try adjusting your custom prompt or reducing complexity
- **OpenAI o3-mini errors**: The model uses different API parameters automatically handled by the app

## Example Use Cases 📝

- Educational content fine-tuning
- Domain-specific knowledge training
- Customer service chatbot training
- Technical documentation Q&A
- Creative writing assistance
- Multi-turn conversation datasets

## License 📄

This project is open source and available under the MIT License.

## Support 💬

For issues or questions, please create an issue in the repository or contact the maintainers.

