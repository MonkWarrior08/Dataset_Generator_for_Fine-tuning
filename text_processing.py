"""
Text processing utilities for chunking and parsing responses.
"""

import re
from typing import List, Dict


class TextProcessor:
    """Handles text processing tasks."""
    
    @staticmethod
    def split_by_word_count(text: str, words_per_chunk: int) -> List[str]:
        """Split text into chunks based on word count."""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), words_per_chunk):
            chunk = ' '.join(words[i:i + words_per_chunk])
            if chunk.strip():
                chunks.append(chunk.strip())
        
        return chunks
    
    @staticmethod
    def create_prompt_template(custom_prompt: str, num_questions: int, num_exchanges: int) -> str:
        """Create prompt template for Q&A generation."""
        if num_exchanges == 1:
            format_instructions = """
Format for each conversation:
CONVERSATION X:
QUESTION: [user question, all lowercase]
ANSWER: [AI response based on text]
"""
        else:
            format_instructions = f"""
Format for each conversation:
CONVERSATION X:
QUESTION: [initial question from user, all lowercase]
ANSWER: [AI response based on text]
{'FOLLOW-UP: [follow-up question, all lowercase]' * (num_exchanges - 1)}
{'FOLLOW-UP ANSWER: [AI response to follow-up, also based on text]' * (num_exchanges - 1)}
"""
        
        return f"""
{custom_prompt}

Based on the following text, generate {num_questions} conversation pairs with {num_exchanges} exchange(s) each.

Requirements:
- User questions should be natural and use lowercase
- AI responses should be informative and based on the provided text
- Cover the major concepts mentioned in the text
- Each conversation should feel natural and educational

{format_instructions}

Text content:
{{chunk}}

Generate exactly {num_questions} conversations that thoroughly cover the content:
"""
    
    @staticmethod
    def parse_qa_response(response_text: str, num_exchanges: int) -> List[Dict]:
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
                    # Parse multi-exchange conversation
                    if 'QUESTION:' in part and 'ANSWER:' in part:
                        sections = part.split('QUESTION:', 1)[1]
                        
                        if 'ANSWER:' in sections:
                            question_part, rest = sections.split('ANSWER:', 1)
                            question = question_part.strip()
                            
                            # Extract first answer
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