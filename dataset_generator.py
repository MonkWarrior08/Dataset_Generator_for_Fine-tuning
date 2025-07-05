"""
Core dataset generation logic that ties all components together.
"""

import streamlit as st
import time
from typing import List, Dict

from models import ModelManager
from file_handlers import FileHandler
from text_processing import TextProcessor
from output_formats import OutputFormatter


class DatasetGenerator:
    """Main class for generating datasets from text files."""
    
    def __init__(self, model_provider: str, specific_model: str, api_key: str):
        """Initialize the dataset generator with selected AI model."""
        self.model_provider = model_provider
        self.specific_model = specific_model
        self.api_key = api_key
        self.model = ModelManager.initialize_model(model_provider, specific_model, api_key)
    
    def read_file_content(self, uploaded_file) -> str:
        """Read content from uploaded file."""
        return FileHandler.read_file(uploaded_file)
    
    def split_text_into_chunks(self, text: str, words_per_chunk: int) -> List[str]:
        """Split text into chunks."""
        return TextProcessor.split_by_word_count(text, words_per_chunk)
    
    def generate_qa_pairs(self, chunk: str, custom_prompt: str, num_questions: int, num_exchanges: int) -> List[Dict]:
        """Generate Q&A pairs for a given chunk using selected AI model."""
        prompt_template = TextProcessor.create_prompt_template(custom_prompt, num_questions, num_exchanges)
        prompt = prompt_template.format(chunk=chunk)
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response_text = ModelManager.get_model_response(
                    self.model, self.model_provider, self.specific_model, prompt
                )
                if response_text:
                    return TextProcessor.parse_qa_response(response_text, num_exchanges)
                else:
                    st.warning(f"Empty response from {self.model_provider} on attempt {attempt + 1}")
            except Exception as e:
                st.error(f"Error generating Q&A pairs (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(3)
                else:
                    st.error("Max retries reached, skipping this chunk")
        
        return []
    
    def format_conversations(self, conversations: List[Dict], model_format: str, num_exchanges: int) -> List[str]:
        """Format conversations for the target model."""
        return OutputFormatter.format_for_model(conversations, model_format, num_exchanges)
    
    def generate_dataset(self, text_content: str, config: Dict) -> List[str]:
        """Generate complete dataset from text content."""
        # Extract configuration
        words_per_chunk = config['words_per_chunk']
        questions_per_chunk = config['questions_per_chunk']
        num_exchanges = config['num_exchanges']
        model_format = config['model_format']
        custom_prompt = config['custom_prompt']
        
        # Split text into chunks
        chunks = self.split_text_into_chunks(text_content, words_per_chunk)
        
        # Generate examples
        generated_examples = []
        
        for i, chunk in enumerate(chunks):
            st.write(f"Processing chunk {i+1}/{len(chunks)} with {self.model_provider} ({self.specific_model})...")
            
            conversations = self.generate_qa_pairs(
                chunk, custom_prompt, questions_per_chunk, num_exchanges
            )
            
            if conversations:
                formatted_examples = self.format_conversations(
                    conversations, model_format, num_exchanges
                )
                generated_examples.extend(formatted_examples)
            
            # Add delay to be respectful to API
            time.sleep(1)
        
        return generated_examples 