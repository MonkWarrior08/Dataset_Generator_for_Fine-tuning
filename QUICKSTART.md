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

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key
4. Edit `.env` file and replace `your_api_key_here` with your actual API key

## Step 3: Run the Application

```bash
streamlit run dataset_generator_app.py
```

The application will open in your browser at `http://localhost:8501`

## First Dataset Generation

1. **Upload a file**: Click "Choose a file" and upload a .txt or .pdf file
2. **Configure settings**:
   - Words per chunk: 300 (good starting point)
   - Questions per chunk: 3
   - Number of turns: 2 (for conversations)
   - Model format: Choose your target model (e.g., "Gemma")
3. **Customize prompt**: Edit the generation prompt if needed
4. **Generate**: Click "Generate Dataset" and wait for completion
5. **Download**: Click "Download Dataset" to save your JSONL file

## Example Files to Try

Create a sample text file with this content:

```
Climate change refers to long-term shifts in global temperatures and weather patterns. While climate variations occur naturally, human activities have become the primary driver of climate change since the 1800s. The burning of fossil fuels like coal, oil, and gas produces greenhouse gases that trap heat in Earth's atmosphere.

The effects of climate change include rising sea levels, more frequent extreme weather events, changes in precipitation patterns, and shifts in wildlife habitats. These changes pose significant challenges to human societies, economies, and ecosystems worldwide.

Addressing climate change requires both mitigation efforts to reduce greenhouse gas emissions and adaptation strategies to cope with unavoidable changes. This includes transitioning to renewable energy sources, improving energy efficiency, protecting and restoring natural ecosystems, and developing climate-resilient infrastructure.
```

Save this as `climate_change.txt` and upload it to test the generator!

## Troubleshooting

- **API Key Error**: Make sure your API key is correctly set in the `.env` file
- **File Upload Issues**: Ensure your file is in .txt or .pdf format
- **Generation Failures**: Try reducing the number of questions per chunk
- **PDF Problems**: Make sure your PDF contains searchable text (not just images)

## Pro Tips 💡

- Start with smaller files (under 10 pages) to test the system
- Use 200-500 words per chunk for optimal results
- Adjust the custom prompt based on your specific use case
- Download your datasets regularly - they're not saved automatically

Ready to create your first dataset? Let's go! 🎉 