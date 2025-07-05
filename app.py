"""
Streamlit app for dataset generation.
"""

import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

from models import ModelManager
from dataset_generator import DatasetGenerator
from output_formats import OutputFormatter

# Load environment variables
load_dotenv()


def main():
    st.set_page_config(
        page_title="Dataset Generator",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Dataset Generator for Fine-tuning")
    st.markdown("Generate training datasets from your text files for fine-tuning language models")
    
    # Sidebar for configuration
    st.sidebar.header("⚙️ Configuration")
    
    # Model selection
    st.sidebar.subheader("🤖 AI Model Selection")
    available_models = ModelManager.get_available_models()
    
    selected_model = st.sidebar.selectbox(
        "Choose AI Provider",
        options=available_models,
        index=0,
        help="Select the AI model provider"
    )
    
    # Specific model selection based on provider
    model_variants = ModelManager.get_model_variants(selected_model)
    specific_model = st.sidebar.selectbox(
        f"Choose {selected_model} Model",
        options=model_variants,
        index=0,
        help=f"Select specific {selected_model} model"
    )
    
    # Get API key from environment
    api_key_map = {
        "Gemini": "GEMINI_API_KEY",
        "Claude": "ANTHROPIC_API_KEY",
        "OpenAI": "OPENAI_API_KEY"
    }
    
    api_key = os.getenv(api_key_map.get(selected_model, ''), '')
    
    if not api_key:
        st.error(f"Please set your {selected_model} API key in the .env file")
        st.stop()
    
    # File upload
    st.sidebar.subheader("📁 Upload File")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a file",
        type=['txt', 'pdf'],
        help="Upload a text file or PDF to generate dataset from"
    )
    
    if not uploaded_file:
        st.info("Please upload a text file or PDF to get started")
        return
    
    # Configuration options
    st.sidebar.subheader("🔧 Generation Settings")
    
    words_per_chunk = st.sidebar.slider(
        "Words per chunk",
        min_value=50,
        max_value=2000,
        value=300,
        step=50,
        help="Number of words to include in each chunk"
    )
    
    questions_per_chunk = st.sidebar.slider(
        "Questions per chunk",
        min_value=1,
        max_value=10,
        value=3,
        help="Number of Q&A pairs to generate per chunk"
    )
    
    num_exchanges = st.sidebar.selectbox(
        "Conversation exchanges",
        options=[1, 2, 3, 4, 5],
        index=0,
        help="Number of back-and-forth exchanges in each conversation"
    )
    
    model_format = st.sidebar.selectbox(
        "Output format",
        options=OutputFormatter.get_available_formats(),
        index=0,
        help="Select the format for your target model"
    )
    
    # Custom prompt in main area
    st.subheader("✍️ Custom Generation Prompt")
    st.markdown("""
    This prompt will guide how the AI generates questions and answers from your content.
    """)
    custom_prompt = st.text_area(
        "Enter your custom prompt for dataset generation:",
        value="",
        placeholder="Generate educational question-answer pairs that help users understand the content. Focus on practical applications and clear explanations.",
        height=150,
        help="Customize the prompt for generating Q&A pairs. This prompt will guide how the AI generates questions and answers from your content."
    )
    
    # Use default prompt if custom prompt is empty
    if not custom_prompt.strip():
        custom_prompt = "Generate educational question-answer pairs that help users understand the content. Focus on practical applications and clear explanations."
    
    # Initialize generator
    try:
        generator = DatasetGenerator(selected_model, specific_model, api_key)
        
        # Read file content
        text_content = generator.read_file_content(uploaded_file)
        
        if text_content:
            # Split into chunks
            chunks = generator.split_text_into_chunks(text_content, words_per_chunk)
            st.info(f"📊 File will be split into {len(chunks)} chunks of ~{words_per_chunk} words each")
            
            if st.button("Generate Dataset", type="primary", use_container_width=True):
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                config = {
                    'words_per_chunk': words_per_chunk,
                    'questions_per_chunk': questions_per_chunk,
                    'num_exchanges': num_exchanges,
                    'model_format': model_format,
                    'custom_prompt': custom_prompt
                }
                
                generated_examples = []
                
                for i, chunk in enumerate(chunks):
                    status_text.text(f"Processing chunk {i+1}/{len(chunks)} with {selected_model} ({specific_model})...")
                    progress_bar.progress((i + 1) / len(chunks))
                    
                    conversations = generator.generate_qa_pairs(
                        chunk, custom_prompt, questions_per_chunk, num_exchanges
                    )
                    
                    if conversations:
                        formatted_examples = generator.format_conversations(
                            conversations, model_format, num_exchanges
                        )
                        generated_examples.extend(formatted_examples)
                    
                    # Add delay to be respectful to API
                    import time
                    time.sleep(1)
                
                status_text.text("Dataset generation complete!")
                
                if generated_examples:
                    st.success(f"✅ Generated {len(generated_examples)} training examples!")
                    
                    # Show sample
                    with st.expander("Preview generated examples"):
                        for i, example in enumerate(generated_examples[:3]):
                            st.write(f"**Example {i+1}:**")
                            st.code(example, language="json")
                            st.write("---")
                    
                    # Download button
                    dataset_content = "\n".join(generated_examples)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"dataset_{model_format.lower()}_{timestamp}.jsonl"
                    
                    st.download_button(
                        label="📥 Download Dataset",
                        data=dataset_content,
                        file_name=filename,
                        mime="application/json",
                        use_container_width=True
                    )
                    
                    # Show statistics
                    st.subheader("📈 Generation Statistics")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Examples", len(generated_examples))
                    with col2:
                        st.metric("Chunks Processed", len(chunks))
                    with col3:
                        st.metric("Success Rate", f"{len(generated_examples)/(len(chunks)*questions_per_chunk)*100:.1f}%")
                    
                else:
                    st.error("No examples were generated. Please check your settings and try again.")
        
    except Exception as e:
        st.error(f"Error initializing generator: {e}")
        return


if __name__ == "__main__":
    main() 