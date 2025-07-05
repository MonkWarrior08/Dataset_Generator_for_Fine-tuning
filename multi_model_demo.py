#!/usr/bin/env python3
"""
Multi-Model Demo: Compare dataset generation across Gemini, Claude, and OpenAI
This demo shows how to use all three AI models and compare their outputs.
"""

import os
import json
from dotenv import load_dotenv
from app import DatasetGenerator, ANTHROPIC_AVAILABLE, OPENAI_AVAILABLE

def get_available_models():
    """Get list of available models based on installed packages and API keys."""
    models = []
    
    # Check Gemini
    if os.getenv('GEMINI_API_KEY'):
        models.append(("Gemini", os.getenv('GEMINI_API_KEY')))
    
    # Check Claude
    if ANTHROPIC_AVAILABLE and os.getenv('ANTHROPIC_API_KEY'):
        models.append(("Claude", os.getenv('ANTHROPIC_API_KEY')))
    
    # Check OpenAI
    if OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY'):
        models.append(("OpenAI", os.getenv('OPENAI_API_KEY')))
    
    return models

def demo_single_model(model_name, api_key, sample_text, prompt):
    """Generate dataset using a single model."""
    print(f"\n🔄 Testing {model_name}...")
    
    try:
        # Initialize generator
        generator = DatasetGenerator(model_name, api_key)
        
        # Split text into chunks
        chunks = generator.split_by_word_count(sample_text, words_per_chunk=150)
        print(f"📊 Split into {len(chunks)} chunks")
        
        # Generate Q&A pairs
        all_conversations = []
        for i, chunk in enumerate(chunks):
            print(f"  Processing chunk {i+1}/{len(chunks)}...")
            
            conversations = generator.generate_qa_pairs(
                chunk=chunk,
                custom_prompt=prompt,
                num_questions=2,
                num_turns=1
            )
            
            if conversations:
                all_conversations.extend(conversations)
                print(f"  ✅ Generated {len(conversations)} conversations")
            else:
                print(f"  ❌ Failed to generate conversations")
        
        print(f"✅ {model_name} completed: {len(all_conversations)} total conversations")
        return all_conversations
        
    except Exception as e:
        print(f"❌ {model_name} failed: {e}")
        return []

def save_comparison_results(results, model_formats):
    """Save comparison results to files."""
    print(f"\n💾 Saving comparison results...")
    
    # Create comparison report
    comparison_report = {
        "models_tested": list(results.keys()),
        "total_conversations": {model: len(convs) for model, convs in results.items()},
        "sample_outputs": {}
    }
    
    # Add sample outputs for comparison
    for model, conversations in results.items():
        if conversations:
            comparison_report["sample_outputs"][model] = conversations[0]
    
    # Save comparison report
    with open('model_comparison_report.json', 'w', encoding='utf-8') as f:
        json.dump(comparison_report, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Comparison report saved to: model_comparison_report.json")
    
    # Save formatted datasets for each model
    for model, conversations in results.items():
        if conversations:
            # Create a sample generator to use formatting functions
            sample_generator = DatasetGenerator(model, "dummy_key")
            
            for format_name in model_formats:
                try:
                    formatted_examples = sample_generator.format_for_model(
                        conversations, format_name, num_turns=1
                    )
                    
                    filename = f"comparison_{model.lower()}_{format_name.lower()}.jsonl"
                    with open(filename, 'w', encoding='utf-8') as f:
                        for example in formatted_examples:
                            f.write(example + '\n')
                    
                    print(f"📁 {model} dataset saved: {filename}")
                    
                except Exception as e:
                    print(f"⚠️  Error formatting {model} for {format_name}: {e}")

def main():
    """Main demo function."""
    print("🚀 Multi-Model Dataset Generation Demo")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Get available models
    available_models = get_available_models()
    
    if not available_models:
        print("❌ No models available. Please check your API keys in .env file:")
        print("   - GEMINI_API_KEY=your_gemini_key")
        print("   - ANTHROPIC_API_KEY=your_claude_key")
        print("   - OPENAI_API_KEY=your_openai_key")
        return
    
    print(f"🤖 Available models: {', '.join([model[0] for model in available_models])}")
    
    # Sample text for testing
    sample_text = """
    Artificial intelligence (AI) has become increasingly important in modern technology. AI systems can process large amounts of data, recognize patterns, and make decisions without explicit programming for each scenario. Machine learning, a subset of AI, allows computers to learn and improve from experience.
    
    There are several types of machine learning: supervised learning uses labeled data to train models, unsupervised learning finds patterns in unlabeled data, and reinforcement learning learns through trial and error with rewards and penalties. Deep learning, which uses neural networks with many layers, has been particularly successful in tasks like image recognition and natural language processing.
    
    AI applications are everywhere today: from recommendation systems on streaming platforms to autonomous vehicles, from medical diagnosis to financial trading. As AI continues to evolve, it's important to consider both its benefits and potential challenges, including ethical considerations around bias, privacy, and job displacement.
    """
    
    # Custom prompt for generation
    custom_prompt = """
    Generate educational question-answer pairs about artificial intelligence and machine learning. 
    Focus on making complex concepts accessible to beginners while maintaining accuracy.
    Create questions that encourage understanding of key concepts and practical applications.
    """
    
    # Test each available model
    results = {}
    
    for model_name, api_key in available_models:
        conversations = demo_single_model(model_name, api_key, sample_text, custom_prompt)
        if conversations:
            results[model_name] = conversations
    
    # Display results summary
    print(f"\n📈 Results Summary:")
    print("=" * 30)
    for model, conversations in results.items():
        print(f"{model}: {len(conversations)} conversations generated")
    
    # Save comparison results
    if results:
        model_formats = ["Gemma", "Llama", "ChatML", "Alpaca", "ShareGPT"]
        save_comparison_results(results, model_formats)
        
        print(f"\n🎉 Demo completed!")
        print(f"📊 Generated datasets with {len(results)} models")
        print(f"📁 Check generated files for detailed comparison")
        
        # Show sample outputs
        print(f"\n🔍 Sample Output Comparison:")
        print("=" * 40)
        for model, conversations in results.items():
            if conversations:
                print(f"\n{model} Sample:")
                print(f"Q: {conversations[0]['question']}")
                print(f"A: {conversations[0]['answer'][:100]}...")
    
    else:
        print("❌ No successful generations. Check your API keys and try again.")

if __name__ == "__main__":
    main() 