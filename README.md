# Dataset Generator for Fine-tuning 📊

A Streamlit-based tool for generating training datasets from text files and PDFs for fine-tuning language models. This tool uses Google's Gemini API to generate high-quality question-answer pairs in various formats compatible with different models.

## Features ✨

- **File Upload**: Support for both text files (.txt) and PDF files (.pdf)
- **Smart Chunking**: Split content by word count instead of manual delimiters
- **Customizable Generation**: Control number of questions per chunk and conversation turns
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

3. Set up your Gemini API key:
   - Create a `.env` file in the project directory
   - Add your API key: `GEMINI_API_KEY=your_api_key_here`
   - Or enter it directly in the app interface

## Usage 🚀

1. **Start the application**:
   ```bash
   streamlit run dataset_generator_app.py
   ```

2. **Configure settings**:
   - Enter your Gemini API key
   - Upload a text file or PDF
   - Set chunking parameters (words per chunk)
   - Choose number of questions per chunk
   - Select conversation turns (1 or 2)
   - Choose your target model format

3. **Generate dataset**:
   - Write or customize your generation prompt
   - Click "Generate Dataset"
   - Monitor progress in real-time
   - Download the generated JSONL file

## Supported Model Formats 🤖

### Gemma
```
<start_of_turn>user
question<end_of_turn>
<start_of_turn>model
answer<end_of_turn>
```

### Llama
```
<|begin_of_text|><|start_header_id|>user<|end_header_id|>
question<|eot_id|><|start_header_id|>assistant<|end_header_id|>
answer<|eot_id|>
```

### ChatML
```
<|im_start|>user
question<|im_end|>
<|im_start|>assistant
answer<|im_end|>
```

### Alpaca
```json
{
  "instruction": "question",
  "input": "",
  "output": "answer"
}
```

### ShareGPT
```json
{
  "conversations": [
    {"from": "human", "value": "question"},
    {"from": "gpt", "value": "answer"}
  ]
}
```

## Configuration Options ⚙️

- **Words per chunk**: 50-2000 words (default: 300)
- **Questions per chunk**: 1-10 questions (default: 3)
- **Number of turns**: 1 or 2 conversation turns
- **Model format**: Choose from 6 supported formats
- **Custom prompt**: Personalize the generation instructions

## API Requirements 🔑

You'll need a Google Gemini API key to use this tool:

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Add it to your `.env` file or enter it in the app

## Tips for Best Results 💡

1. **Chunk Size**: Use 200-500 words per chunk for optimal results
2. **Questions**: Start with 2-4 questions per chunk
3. **Prompts**: Be specific about the type of content you want to generate
4. **File Quality**: Ensure your source files are well-formatted and readable

## Troubleshooting 🔧

- **API Errors**: Check your API key and internet connection
- **PDF Issues**: Ensure PDF files are text-based (not scanned images)
- **Memory Issues**: Reduce chunk size or questions per chunk for large files
- **Generation Failures**: Try adjusting your custom prompt or reducing complexity

## Example Use Cases 📝

- Educational content fine-tuning
- Domain-specific knowledge training
- Customer service chatbot training
- Technical documentation Q&A
- Creative writing assistance

## License 📄

This project is open source and available under the MIT License.

## Support 💬

For issues or questions, please create an issue in the repository or contact the maintainers. 