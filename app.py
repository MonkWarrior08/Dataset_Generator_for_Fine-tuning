import streamlit as st
import os
import json
import re
from typing import List, Dict, Tuple
import google.generativeai as genai
from pathlib import Path
import time
from dotenv import load_dotenv
import PyPDF2
import io
from datetime import datetime

# Optional imports with error handling
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Load environment variables
load_dotenv()

class DatasetGenerator:
    def __init__(self, model_provider: str, api_key: str):
        """Initialize the dataset generator with selected AI model."""
        self.model_provider = model_provider
        self.api_key = api_key
        
        if model_provider == "Gemini":
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        elif model_provider == "Claude" and ANTHROPIC_AVAILABLE:
            self.model = anthropic.Anthropic(api_key=api_key)
        elif model_provider == "OpenAI" and OPENAI_AVAILABLE:
            self.model = openai.OpenAI(api_key=api_key)
        else:
            raise ValueError(f"Unsupported model provider: {model_provider}")
        
    def read_text_file(self, uploaded_file) -> str:
        """Read uploaded text file."""
        try:
            return str(uploaded_file.read(), "utf-8")
        except Exception as e:
            st.error(f"Error reading text file: {e}")
            return ""
    
    def read_pdf_file(self, uploaded_file) -> str:
        """Read uploaded PDF file."""
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading PDF file: {e}")
            return ""
    
    def split_by_word_count(self, text: str, words_per_chunk: int) -> List[str]:
        """Split text into chunks based on word count."""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), words_per_chunk):
            chunk = ' '.join(words[i:i + words_per_chunk])
            if chunk.strip():
                chunks.append(chunk.strip())
        
        return chunks
    
    def generate_qa_pairs(self, chunk: str, custom_prompt: str, num_questions: int, num_exchanges: int) -> List[Dict]:
        """Generate Q&A pairs for a given chunk using selected AI model."""
        
        if num_exchanges == 1:
            format_instructions = """
Format for each conversation:
CONVERSATION X:
QUESTION: [user question, all lowercase]
ANSWER: [AI response based on text]
"""
        else:  # num_exchanges == 2
            format_instructions = """
Format for each conversation:
CONVERSATION X:
QUESTION: [initial question from user, all lowercase]
ANSWER: [AI response based on text]
FOLLOW-UP: [natural follow-up question, all lowercase]
FOLLOW-UP ANSWER: [AI response to follow-up, also based on text]
"""
        
        prompt = f"""
{custom_prompt}

Based on the following text, generate {num_questions} conversation pairs with {num_exchanges} exchange(s) each.

Requirements:
- User questions should be natural and use lowercase
- AI responses should be informative and based on the provided text
- Cover the major concepts mentioned in the text
- Each conversation should feel natural and educational

{format_instructions}

Text content:
{chunk}

Generate exactly {num_questions} conversations that thoroughly cover the content:
"""
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response_text = self._get_model_response(prompt)
                if response_text:
                    return self.parse_qa_response(response_text, num_exchanges)
                else:
                    st.warning(f"Empty response from {self.model_provider} on attempt {attempt + 1}")
            except Exception as e:
                st.error(f"Error generating Q&A pairs (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(3)
                else:
                    st.error("Max retries reached, skipping this chunk")
        
        return []
    
    def _get_model_response(self, prompt: str) -> str:
        """Get response from the selected AI model."""
        if self.model_provider == "Gemini":
            response = self.model.generate_content(prompt)
            return response.text if response.text else ""
        
        elif self.model_provider == "Claude":
            response = self.model.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text if response.content else ""
        
        elif self.model_provider == "OpenAI":
            response = self.model.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000,
                temperature=0.7
            )
            return response.choices[0].message.content if response.choices else ""
        
        else:
            raise ValueError(f"Unsupported model provider: {self.model_provider}")
    
    def parse_qa_response(self, response_text: str, num_exchanges: int) -> List[Dict]:
        """Parse response into structured conversation pairs."""
        conversations = []
        
        # Split by CONVERSATION to find each conversation
        parts = response_text.split('CONVERSATION')[1:]  # Skip first empty part
        
        for part in parts:
            try:
                if num_exchanges == 1:
                    # Parse single exchange conversation
                    if 'QUESTION:' in part and 'ANSWER:' in part:
                        sections = part.split('QUESTION:', 1)[1]
                        
                        if 'ANSWER:' in sections:
                            question_part, answer_part = sections.split('ANSWER:', 1)
                            question = question_part.strip()
                            answer = answer_part.strip()
                            
                            # Clean up formatting
                            question = re.sub(r'^[0-9]+\.?\s*', '', question).strip().lower()
                            answer = re.sub(r'\n\n+', '\n\n', answer).strip()
                            
                            if question and answer:
                                conversations.append({
                                    'question': question,
                                    'answer': answer
                                })
                else:
                    # Parse two exchange conversation
                    if 'QUESTION:' in part and 'ANSWER:' in part and 'FOLLOW-UP:' in part and 'FOLLOW-UP ANSWER:' in part:
                        sections = part.split('QUESTION:', 1)[1]
                        
                        if 'ANSWER:' in sections:
                            question_part, rest = sections.split('ANSWER:', 1)
                            question = question_part.strip()
                            
                            if 'FOLLOW-UP:' in rest:
                                answer_part, followup_rest = rest.split('FOLLOW-UP:', 1)
                                answer = answer_part.strip()
                                
                                if 'FOLLOW-UP ANSWER:' in followup_rest:
                                    followup_question_part, followup_answer_part = followup_rest.split('FOLLOW-UP ANSWER:', 1)
                                    followup_question = followup_question_part.strip()
                                    followup_answer = followup_answer_part.strip()
                                    
                                    # Clean up formatting
                                    question = re.sub(r'^[0-9]+\.?\s*', '', question).strip().lower()
                                    answer = re.sub(r'\n\n+', '\n\n', answer).strip()
                                    followup_question = re.sub(r'^[0-9]+\.?\s*', '', followup_question).strip().lower()
                                    followup_answer = re.sub(r'\n\n+', '\n\n', followup_answer).strip()
                                    
                                    if question and answer and followup_question and followup_answer:
                                        conversations.append({
                                            'question': question,
                                            'answer': answer,
                                            'followup_question': followup_question,
                                            'followup_answer': followup_answer
                                        })
            except Exception as e:
                continue
        
        return conversations
    
    def format_for_model(self, conversations: List[Dict], model_format: str, num_exchanges: int) -> List[str]:
        """Format conversation pairs based on the selected model format."""
        formatted_examples = []
        
        for conv in conversations:
            if model_format == "Gemma":
                if num_exchanges == 1:
                    conversation = {
                        "text": f"<start_of_turn>user\n{conv['question']}<end_of_turn>\n<start_of_turn>model\n{conv['answer']}<end_of_turn>"
                    }
                else:
                    conversation = {
                        "text": f"<start_of_turn>user\n{conv['question']}<end_of_turn>\n<start_of_turn>model\n{conv['answer']}<end_of_turn>\n<start_of_turn>user\n{conv['followup_question']}<end_of_turn>\n<start_of_turn>model\n{conv['followup_answer']}<end_of_turn>"
                    }
            
            elif model_format == "Llama":
                if num_exchanges == 1:
                    conversation = {
                        "text": f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{conv['question']}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n{conv['answer']}<|eot_id|>"
                    }
                else:
                    conversation = {
                        "text": f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{conv['question']}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n{conv['answer']}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{conv['followup_question']}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n{conv['followup_answer']}<|eot_id|>"
                    }
            
            elif model_format == "ChatML":
                if num_exchanges == 1:
                    conversation = {
                        "text": f"<|im_start|>user\n{conv['question']}<|im_end|>\n<|im_start|>assistant\n{conv['answer']}<|im_end|>"
                    }
                else:
                    conversation = {
                        "text": f"<|im_start|>user\n{conv['question']}<|im_end|>\n<|im_start|>assistant\n{conv['answer']}<|im_end|>\n<|im_start|>user\n{conv['followup_question']}<|im_end|>\n<|im_start|>assistant\n{conv['followup_answer']}<|im_end|>"
                    }
            
            elif model_format == "Alpaca":
                if num_exchanges == 1:
                    conversation = {
                        "instruction": conv['question'],
                        "input": "",
                        "output": conv['answer']
                    }
                else:
                    conversation = {
                        "instruction": conv['question'],
                        "input": "",
                        "output": conv['answer'],
                        "follow_up_instruction": conv['followup_question'],
                        "follow_up_output": conv['followup_answer']
                    }
            
            elif model_format == "ShareGPT":
                if num_exchanges == 1:
                    conversation = {
                        "conversations": [
                            {"from": "human", "value": conv['question']},
                            {"from": "gpt", "value": conv['answer']}
                        ]
                    }
                else:
                    conversation = {
                        "conversations": [
                            {"from": "human", "value": conv['question']},
                            {"from": "gpt", "value": conv['answer']},
                            {"from": "human", "value": conv['followup_question']},
                            {"from": "gpt", "value": conv['followup_answer']}
                        ]
                    }
            
            else:  # Generic format
                conversation = conv
            
            formatted_examples.append(json.dumps(conversation, ensure_ascii=False))
        
        return formatted_examples

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
    available_models = ["Gemini"]
    if ANTHROPIC_AVAILABLE:
        available_models.append("Claude")
    if OPENAI_AVAILABLE:
        available_models.append("OpenAI")
    
    selected_model = st.sidebar.selectbox(
        "Choose AI Model",
        options=available_models,
        index=0,
        help="Select the AI model to generate your dataset"
    )
    
    # API Key input based on selected model
    if selected_model == "Gemini":
        api_key = st.sidebar.text_input(
            "Gemini API Key",
            value=os.getenv('GEMINI_API_KEY', ''),
            type="password",
            help="Enter your Google Gemini API key"
        )
    elif selected_model == "Claude":
        api_key = st.sidebar.text_input(
            "Claude API Key",
            value=os.getenv('ANTHROPIC_API_KEY', ''),
            type="password",
            help="Enter your Anthropic Claude API key"
        )
    elif selected_model == "OpenAI":
        api_key = st.sidebar.text_input(
            "OpenAI API Key",
            value=os.getenv('OPENAI_API_KEY', ''),
            type="password",
            help="Enter your OpenAI API key"
        )
    
    if not api_key:
        st.warning(f"Please enter your {selected_model} API key to continue")
        return
    
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
        options=[1, 2],
        index=0,
        help="1 = Single exchange (User → Assistant), 2 = Two exchanges (User → Assistant → User → Assistant)"
    )
    
    model_format = st.sidebar.selectbox(
        "Output format",
        options=["Gemma", "Llama", "ChatML", "Alpaca", "ShareGPT", "Generic"],
        index=0,
        help="Select the format for your target model"
    )
    
    # Custom prompt
    st.sidebar.subheader("✍️ Custom Prompt")
    custom_prompt = st.sidebar.text_area(
        "Generation prompt",
        value="Generate educational question-answer pairs that help users understand the content. Focus on practical applications and clear explanations.",
        height=150,
        help="Customize the prompt for generating Q&A pairs"
    )
    
    # Main content area
    st.subheader("🚀 Generate Dataset")
    
    # Initialize generator
    try:
        generator = DatasetGenerator(selected_model, api_key)
        
        # Read file content
        if uploaded_file.type == "text/plain":
            text_content = generator.read_text_file(uploaded_file)
        else:  # PDF
            text_content = generator.read_pdf_file(uploaded_file)
        
        if text_content:
            # Split into chunks
            chunks = generator.split_by_word_count(text_content, words_per_chunk)
            st.info(f"📊 File will be split into {len(chunks)} chunks of ~{words_per_chunk} words each")
            
            if st.button("Generate Dataset", type="primary"):
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                generated_examples = []
                
                for i, chunk in enumerate(chunks):
                    status_text.text(f"Processing chunk {i+1}/{len(chunks)} with {selected_model}...")
                    progress_bar.progress((i + 1) / len(chunks))
                    
                    conversations = generator.generate_qa_pairs(
                        chunk, custom_prompt, questions_per_chunk, num_exchanges
                    )
                    
                    if conversations:
                        formatted_examples = generator.format_for_model(
                            conversations, model_format, num_exchanges
                        )
                        generated_examples.extend(formatted_examples)
                    
                    # Add delay to be respectful to API
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
                        mime="application/json"
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