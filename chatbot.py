# chatbot.py
from transformers import BertTokenizer, BertForQuestionAnswering
import torch
from vector_db import VectorDatabase
from typing import List, Dict
import numpy as np
import re
class IPL2025Chatbot:
    def __init__(self):
        # Initialize vector database
        self.vector_db = VectorDatabase()
        self.vector_db.load_index()
        
        # Initialize BERT QA model
        self.qa_tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        self.qa_model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.qa_model.to(self.device)
    
    def retrieve_relevant_documents(self, query: str, k: int = 3) -> List[str]:
        query_lower=query.lower()
        """Retrieve relevant documents from the vector database"""
        if "most runs" in query.lower() or "top scorer" in query.lower() or "highest runs" in query.lower() or "more runs" in query.lower():
            results = self.vector_db.search("player runs ranking", k=k)
        elif "lowest runs" in query_lower or "less runs" in query.lower() or "less scorer" in query.lower() or "less runs" in query.lower()  :
            results = self.vector_db.search("Bottom 5 Batsmen by Runs", k=1)
        else:
            results = self.vector_db.search(query, k=k)
        return [doc['text'] for doc, _ in results]
    
    def generate_answer(self, question: str, context: str) -> Dict:
        """Generate an answer using BERT QA model"""
        inputs = self.qa_tokenizer(question, context, return_tensors='pt', truncation=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.qa_model(**inputs)
        
        answer_start = torch.argmax(outputs.start_logits)
        answer_end = torch.argmax(outputs.end_logits) + 1
        
        answer = self.qa_tokenizer.convert_tokens_to_string(
            self.qa_tokenizer.convert_ids_to_tokens(
                inputs['input_ids'][0][answer_start:answer_end]
            )
        )
        
        return {
            'answer': answer,
            'confidence': (outputs.start_logits[0][answer_start] + outputs.end_logits[0][answer_end-1]).item(),
            'context': context
        }
        
    def retrieve_relevant_documents(self, query: str, k: int = 3) -> List[str]:
        query_lower = query.lower()
        """Retrieve relevant documents from the vector database"""
        if ("most runs" in query_lower or "top scorer" in query_lower or 
            "highest runs" in query_lower or "more runs" in query_lower):
            results = self.vector_db.search("Top 5 Batsmen by Runs", k=1)
        elif ("lowest runs" in query_lower or "less runs" in query_lower or 
            "least runs" in query_lower or "less scorer" in query_lower):
            results = self.vector_db.search("Bottom 5 Batsmen by Runs", k=1)
        else:
            results = self.vector_db.search(query, k=k)
        return [doc['text'] for doc, _ in results]

    def generate_stat_answer(self, question: str, contexts: List[str]):
        """Generate answers for statistical queries"""
        question_lower = question.lower()
        
        # Handle lowest runs queries
        if "less runs" in question_lower or "less scorer" in question_lower:
            for text in contexts:
                if "Bottom 5 Batsmen by Runs:" in text:
                    players = text.split('\n')[1:]  # Skip header
                    if players:
                        return {
                            'answer': players[0].strip(),  # First player is highest
                            'confidence': 10.0,
                            'sources': [text]
                        }
            
        # Handle most runs queries
        elif "most runs" in question_lower or "top scorer" in question_lower:
            for text in contexts:
                if "Top 5 Batsmen by Runs:" in text:
                    players = text.split('\n')[1:]  # Skip header
                    if players:
                        return {
                            'answer': players[0].strip(),  # First player is highest
                            'confidence': 10.0,
                            'sources': [text]
                        }
        
        # Handle individual player stats
        players = []
        for text in contexts:
            if "Runs:" in text:
                try:
                    name = text.split("Player:")[1].split("(")[0].strip()
                    runs = int(text.split("Runs:")[1].split("\n")[0].strip())
                    players.append((name, runs))
                except (IndexError, ValueError):
                    continue
        
        if not players:
            return None
            
        # Default to most runs if no specific query matched
        top_player = max(players, key=lambda x: x[1])
        return {
            'answer': f"{top_player[0]} scored the most runs with {top_player[1]}",
            'confidence': 10.0,
            'sources': ["\n".join(contexts)]
        }
        
    def answer_question(self, question: str) -> Dict:
    # Initialize default response
        default_response = {
            'answer': "I couldn't find any information about that in IPL 2025 data.",
            'confidence': 0.0,
            'sources': []
        }
        
        try:
            # Step 1: Retrieve relevant documents
            contexts = self.retrieve_relevant_documents(question)
            
            if not contexts:
                return default_response
            
            # Step 2: Generate answers for each context
            answers = []
            for context in contexts:
                try:
                    answer = self.generate_answer(question, context)
                    answers.append(answer)
                except Exception as e:
                    print(f"Error generating answer: {e}")
                    continue
            
            if not answers:
                return default_response
            
            # Step 3: Select the best answer based on confidence
            best_answer = max(answers, key=lambda x: x['confidence'])
            
            return {
                'answer': best_answer['answer'],
                'confidence': best_answer['confidence'],
                'sources': [best_answer['context']]
            }
            
        except Exception as e:
            print(f"Error processing question: {e}")
            return default_response
        
    def chat(self):
        """Interactive chat interface"""
        print("Welcome to IPL 2025 Chatbot! Ask me anything about IPL 2025.")
        print("Type 'quit' to exit.\n")
        
        while True:
            user_input = input("You: ")
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break
            
            response = self.answer_question(user_input)
            
            print("\nBot:", response['answer'])
            if response['sources']:
                print("\nSource context:")
                print(response['sources'][0][:200] + "...")
            print("-" * 50)

if __name__ == "__main__":
    chatbot = IPL2025Chatbot()
    chatbot.chat()








