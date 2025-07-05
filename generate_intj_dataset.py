import os
import json
import re
from typing import List, Dict
import google.generativeai as genai
from pathlib import Path
import time
from dotenv import load_dotenv

class INTJDatasetGenerator:
    def __init__(self, api_key: str):
        """Initialize the dataset generator with Gemini API key."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.output_file = "intj_training_data.jsonl"
        
    def read_intj_guide(self, file_path: str) -> str:
        """Read the INTJ Developmental Guide text file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""
    
    def split_into_chunks(self, text: str) -> List[str]:
        """Split text into chunks based on --cut-- delimiter."""
        chunks = text.split('--cut--')
        # Filter out empty chunks and strip whitespace
        chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
        
        # Filter out chunks that are too small to be meaningful (less than 20 words)
        meaningful_chunks = []
        for chunk in chunks:
            word_count = len(chunk.split())
            if word_count >= 20:  # Only process chunks with at least 20 words
                meaningful_chunks.append(chunk)
            else:
                print(f"Skipping chunk with only {word_count} words")
        
        print(f"Found {len(meaningful_chunks)} meaningful chunks in the document (filtered from {len(chunks)} total)")
        return meaningful_chunks
    
    def calculate_questions_per_chunk(self, chunk: str, base_questions: int = 4) -> int:
        """Calculate number of questions based on chunk length."""
        word_count = len(chunk.split())
        
        if word_count < 100:
            return 2
        elif word_count < 300:
            return 3
        elif word_count < 500:
            return base_questions
        elif word_count < 1000:
            return base_questions + 4
        else:
            return base_questions + 6
    
    def generate_qa_pairs(self, chunk: str, num_questions: int) -> List[Dict]:
        """Generate Q&A pairs for a given chunk using Gemini."""
        
        prompt = f"""
Based on the following text about brain regions, EEG patterns, and cognitive functions, generate {num_questions} conversation pairs where each includes an initial question, AI response, follow-up question, and AI response.

Requirements:
- Initial questions or wanting to know should be SIMPLE and SHORT (5-15 words), natural, from the user's perspective using "i", "my", "me". All words in the user's questions should be lowercase.
- AI responses use "you", "your" (NOT "my" or "i") and are based on the provided text.
- Follow-up questions should be natural responses to what the AI just said, and also be entirely lowercase.
- Each conversation should feel natural and educational.
- Cover ALL major concepts mentioned in the text.

Format for each conversation:
CONVERSATION X:
QUESTION: [short initial question from user, all lowercase]
ANSWER: [AI response using "you/your", based on text]
FOLLOW-UP: [natural follow-up question, all lowercase]
FOLLOW-UP ANSWER: [AI response to follow-up, also based on text]

Examples of good questions:
- "what's a zen state?"
- "tell me about my fp1 region"
- "why am i bad at remembering facts?"
- "what does it mean to overuse a brain region?"
- "how can i be more focused?"
- "what part of my brain is Te?
- "what are the regions name for the frontal lobe?"
- "which regions are associated with the temporal lobe?"
- "which region belongs to Fi?"
- "how can i know if my left frontal lobe is functioning well?"

Text content:
{chunk}

Generate exactly {num_questions} conversations that thoroughly cover the content:
"""
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                if response.text:
                    return self.parse_qa_response(response.text)
                else:
                    print(f"Empty response from Gemini on attempt {attempt + 1}")
            except Exception as e:
                print(f"Error generating Q&A pairs (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    print("Retrying in 3 seconds...")
                    time.sleep(3)
                else:
                    print("Max retries reached, skipping this chunk")
        
        return []
    
    def parse_qa_response(self, response_text: str) -> List[Dict]:
        """Parse Gemini response into structured conversation pairs."""
        conversations = []
        
        # Split by CONVERSATION to find each conversation
        parts = response_text.split('CONVERSATION')[1:]  # Skip first empty part
        
        for part in parts:
            try:
                # Extract components
                if 'QUESTION:' in part and 'ANSWER:' in part and 'FOLLOW-UP:' in part and 'FOLLOW-UP ANSWER:' in part:
                    # Split into sections
                    sections = part.split('QUESTION:', 1)[1]  # Remove conversation number
                    
                    # Parse initial Q&A
                    if 'ANSWER:' in sections:
                        question_part, rest = sections.split('ANSWER:', 1)
                        question = question_part.strip()
                        
                        # Parse answer and follow-up
                        if 'FOLLOW-UP:' in rest:
                            answer_part, followup_rest = rest.split('FOLLOW-UP:', 1)
                            answer = answer_part.strip()
                            
                            # Parse follow-up Q&A
                            if 'FOLLOW-UP ANSWER:' in followup_rest:
                                followup_question_part, followup_answer_part = followup_rest.split('FOLLOW-UP ANSWER:', 1)
                                followup_question = followup_question_part.strip()
                                followup_answer = followup_answer_part.strip()
                                
                                # Clean up formatting
                                question = re.sub(r'^[0-9]+\.?\s*', '', question).strip()
                                answer = re.sub(r'\n\n+', '\n\n', answer).strip()
                                followup_question = re.sub(r'^[0-9]+\.?\s*', '', followup_question).strip()
                                followup_answer = re.sub(r'\n\n+', '\n\n', followup_answer).strip()
                                
                                # Ensure user questions are entirely lowercase
                                if question:
                                    question = question.lower()
                                if followup_question:
                                    followup_question = followup_question.lower()

                                if question and answer and followup_question and followup_answer:
                                    conversations.append({
                                        'question': question,
                                        'answer': answer,
                                        'followup_question': followup_question,
                                        'followup_answer': followup_answer
                                    })
            except Exception as e:
                print(f"Error parsing conversation: {e}")
                continue
        
        return conversations
    
    def format_for_training(self, conversations: List[Dict]) -> List[str]:
        """Format conversation pairs into the training data format."""
        formatted_examples = []
        
        for conv in conversations:
            # Create the multi-turn conversation format
            conversation = {
                "text": f"<start_of_turn>user\n{conv['question']}<end_of_turn>\n<start_of_turn>model\n{conv['answer']}<end_of_turn>\n<start_of_turn>user\n{conv['followup_question']}<end_of_turn>\n<start_of_turn>model\n{conv['followup_answer']}<end_of_turn>"
            }
            formatted_examples.append(json.dumps(conversation))
        
        return formatted_examples
    
    def generate_dataset(self, file_path: str):
        """Main method to generate the complete dataset."""
        print("Reading Mbti EEG data...")
        text = self.read_intj_guide(file_path)
        
        if not text:
            print("Failed to read the file. Exiting.")
            return
        
        print("Splitting into chunks...")
        chunks = self.split_into_chunks(text)
        
        # Initialize counters and file
        successful_chunks = 0
        failed_chunks = 0
        total_examples = 0
        
        # Check if output file already exists
        if os.path.exists(self.output_file):
            response = input(f"\n📋 {self.output_file} already exists. (o)verwrite or (a)ppend? [o/a]: ").lower().strip()
            if response == 'a':
                mode = 'a'
                print(f"📝 Appending new results to existing {self.output_file}")
            else:
                mode = 'w'
                print(f"📝 Overwriting {self.output_file}")
        else:
            mode = 'w'
            print(f"📝 Creating new file {self.output_file}")
        
        # Open file for incremental writing
        try:
            with open(self.output_file, mode, encoding='utf-8') as f:
                print(f"📝 Writing results incrementally...")
                
                for i, chunk in enumerate(chunks, 1):
                    print(f"\nProcessing chunk {i}/{len(chunks)}...")
                    print(f"Chunk length: {len(chunk.split())} words")
                    
                    # Show a preview of the chunk content
                    preview = chunk[:100] + "..." if len(chunk) > 100 else chunk
                    print(f"Chunk preview: {preview}")
                    
                    num_questions = self.calculate_questions_per_chunk(chunk)
                    print(f"Generating {num_questions} conversations...")
                    
                    conversations = self.generate_qa_pairs(chunk, num_questions)
                    
                    if conversations:
                        formatted_examples = self.format_for_training(conversations)
                        
                        # Write examples immediately to file
                        for example in formatted_examples:
                            f.write(example + '\n')
                            f.flush()  # Ensure data is written immediately
                        
                        total_examples += len(formatted_examples)
                        successful_chunks += 1
                        print(f"✓ Generated and saved {len(conversations)} conversations for chunk {i}")
                        print(f"   Running total: {total_examples} examples")
                    else:
                        failed_chunks += 1
                        print(f"✗ Failed to generate conversations for chunk {i}")
                    
                    # Add a small delay to be respectful to the API
                    time.sleep(2)
                    
        except KeyboardInterrupt:
            print(f"\n\n⚠️  Process interrupted by user!")
            print(f"💾 Data saved up to chunk {i-1}")
        except Exception as e:
            print(f"\n❌ Error during processing: {e}")
        
        # Final summary
        print(f"\n📊 Final Results:")
        print(f"Total training examples saved: {total_examples}")
        print(f"Successful chunks: {successful_chunks}")
        print(f"Failed chunks: {failed_chunks}")
        print(f"File location: {self.output_file}")
        
        if total_examples == 0:
            print("\n⚠️  No training examples generated. Please check your API key and internet connection.")
        else:
            print(f"\n✅ Successfully generated {total_examples} training examples!")
            print(f"📁 Data is saved in {self.output_file} and ready for fine-tuning!")

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment variable or user input
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("No GEMINI_API_KEY found in .env file or environment variables.")
        api_key = input("Enter your Gemini API key: ").strip()
    
    if not api_key:
        print("❌ API key is required to proceed.")
        return
    
    print("✅ API key loaded successfully")
    
    # Initialize generator
    try:
        generator = INTJDatasetGenerator(api_key)
        print("✅ Gemini model initialized")
    except Exception as e:
        print(f"❌ Failed to initialize Gemini model: {e}")
        return
    
    # Path to the MBTI EEG file
    mbti_eeg_file_path = "data/Mbti EEG.txt"
    
    # Check if file exists
    if not Path(mbti_eeg_file_path).exists():
        print(f"Error: {mbti_eeg_file_path} not found")
        return
    
    # Generate dataset
    generator.generate_dataset(mbti_eeg_file_path)

if __name__ == "__main__":
    main() 