"""
Output format handlers for different model types.
"""

import json
from typing import List, Dict


class OutputFormatter:
    """Handles formatting conversations for different model types."""
    
    @staticmethod
    def get_available_formats() -> List[str]:
        """Get list of available output formats."""
        return ["Gemma", "Llama", "OpenAI", "Alpaca"]
    
    @staticmethod
    def format_for_model(conversations: List[Dict], model_format: str, num_exchanges: int) -> List[str]:
        """Format conversation pairs based on the selected model format."""
        formatted_examples = []
        
        for conv in conversations:
            if model_format == "Gemma":
                conversation = OutputFormatter._format_gemma(conv, num_exchanges)
            elif model_format == "Llama":
                conversation = OutputFormatter._format_llama(conv, num_exchanges)
            elif model_format == "OpenAI":
                conversation = OutputFormatter._format_openai(conv, num_exchanges)
            elif model_format == "Alpaca":
                conversation = OutputFormatter._format_alpaca(conv, num_exchanges)
            else:  # Default format
                conversation = conv
            
            formatted_examples.append(json.dumps(conversation, ensure_ascii=False))
        
        return formatted_examples
    
    @staticmethod
    def _format_gemma(conv: Dict, num_exchanges: int) -> Dict:
        """Format for Gemma model."""
        if num_exchanges == 1:
            return {
                "text": f"<start_of_turn>user\n{conv['question']}<end_of_turn>\n<start_of_turn>model\n{conv['answer']}<end_of_turn>"
            }
        else:
            return {
                "text": f"<start_of_turn>user\n{conv['question']}<end_of_turn>\n<start_of_turn>model\n{conv['answer']}<end_of_turn>\n<start_of_turn>user\n{conv['followup_question']}<end_of_turn>\n<start_of_turn>model\n{conv['followup_answer']}<end_of_turn>"
            }
    
    @staticmethod
    def _format_llama(conv: Dict, num_exchanges: int) -> Dict:
        """Format for Llama model."""
        if num_exchanges == 1:
            return {
                "text": f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{conv['question']}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n{conv['answer']}<|eot_id|>"
            }
        else:
            return {
                "text": f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{conv['question']}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n{conv['answer']}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{conv['followup_question']}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n{conv['followup_answer']}<|eot_id|>"
            }
    
    @staticmethod
    def _format_openai(conv: Dict, num_exchanges: int) -> Dict:
        """Format for OpenAI model."""
        if num_exchanges == 1:
            return {
                "messages": [
                    {"role": "user", "content": conv['question']},
                    {"role": "assistant", "content": conv['answer']}
                ]
            }
        else:
            return {
                "messages": [
                    {"role": "user", "content": conv['question']},
                    {"role": "assistant", "content": conv['answer']},
                    {"role": "user", "content": conv['followup_question']},
                    {"role": "assistant", "content": conv['followup_answer']}
                ]
            }
    
    @staticmethod
    def _format_alpaca(conv: Dict, num_exchanges: int) -> Dict:
        """Format for Alpaca model."""
        if num_exchanges == 1:
            return {
                "instruction": conv['question'],
                "input": "",
                "output": conv['answer']
            }
        else:
            return {
                "instruction": conv['question'],
                "input": "",
                "output": conv['answer'],
                "follow_up_instruction": conv['followup_question'],
                "follow_up_output": conv['followup_answer']
            } 