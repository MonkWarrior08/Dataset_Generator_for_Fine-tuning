#!/usr/bin/env python3
"""
Demo script showing how to use the DatasetGenerator programmatically.
This can be useful for batch processing or integration into other tools.
"""

import os
from dotenv import load_dotenv
from dataset_generator_app import DatasetGenerator

def demo_text_processing():
    """Demonstrate text processing capabilities."""
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Please set your GEMINI_API_KEY in the .env file")
        return
    
    # Initialize generator
    generator = DatasetGenerator(api_key)
    
    # Sample text for demonstration
    sample_text = """
    Machine learning is a subset of artificial intelligence that focuses on the development of algorithms and statistical models that enable computer systems to improve their performance on a specific task through experience. The core idea is that machines can learn from data, identify patterns, and make decisions with minimal human intervention.

    There are three main types of machine learning: supervised learning, where the algorithm learns from labeled training data; unsupervised learning, where the algorithm finds hidden patterns in data without labeled examples; and reinforcement learning, where an agent learns to make decisions by receiving rewards or penalties for its actions.

    Deep learning, a subset of machine learning, uses neural networks with multiple layers to model and understand complex patterns in data. This approach has revolutionized fields like computer vision, natural language processing, and speech recognition.
    """
    
    print("🚀 Starting dataset generation demo...\n")
    
    # Split text into chunks
    chunks = generator.split_by_word_count(sample_text, words_per_chunk=100)
    print(f"📊 Split text into {len(chunks)} chunks")
    
    # Generate Q&A pairs for each chunk
    all_conversations = []
    custom_prompt = "Generate educational questions about machine learning concepts that help beginners understand the topic."
    
    for i, chunk in enumerate(chunks):
        print(f"\n🔄 Processing chunk {i+1}/{len(chunks)}...")
        
        # Generate 2 conversations with 1 turn each
        conversations = generator.generate_qa_pairs(
            chunk=chunk,
            custom_prompt=custom_prompt,
            num_questions=2,
            num_turns=1
        )
        
        if conversations:
            all_conversations.extend(conversations)
            print(f"✅ Generated {len(conversations)} conversations")
        else:
            print("❌ Failed to generate conversations")
    
    # Format for different models
    model_formats = ["Gemma", "Llama", "ChatML", "Alpaca", "ShareGPT"]
    
    for model_format in model_formats:
        print(f"\n📋 Formatting for {model_format}...")
        formatted_examples = generator.format_for_model(
            conversations=all_conversations,
            model_format=model_format,
            num_turns=1
        )
        
        # Save to file
        filename = f"demo_dataset_{model_format.lower()}.jsonl"
        with open(filename, 'w', encoding='utf-8') as f:
            for example in formatted_examples:
                f.write(example + '\n')
        
        print(f"💾 Saved {len(formatted_examples)} examples to {filename}")
    
    print(f"\n🎉 Demo complete! Generated {len(all_conversations)} conversations in {len(model_formats)} formats")

if __name__ == "__main__":
    demo_text_processing() 