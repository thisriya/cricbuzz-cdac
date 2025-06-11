# vector_db.py
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os
from typing import List, Dict, Tuple

class VectorDatabase:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight model
        self.index = None
        self.data = []
        self.processed_dir = "processed_data"
        self.db_dir = "vector_db"
        os.makedirs(self.db_dir, exist_ok=True)
    
    def load_data(self) -> List[Dict]:
        """Load processed data from parquet file"""
        df = pd.read_parquet(f"{self.processed_dir}/ipl2025_processed.parquet")
        return df.to_dict('records')
    
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """Create embeddings for the given texts"""
        return self.model.encode(texts, show_progress_bar=True)
    
    def build_index(self, embeddings: np.ndarray):
        """Build FAISS index from embeddings"""
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)  # Using L2 distance
        self.index.add(embeddings)
    
    def save_index(self):
        """Save the FAISS index and metadata"""
        faiss.write_index(self.index, f"{self.db_dir}/ipl2025.index")
        
        # Save metadata
        import json
        with open(f"{self.db_dir}/metadata.json", 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def load_index(self):
        """Load the FAISS index and metadata"""
        self.index = faiss.read_index(f"{self.db_dir}/ipl2025.index")
        
        # Load metadata
        import json
        with open(f"{self.db_dir}/metadata.json", 'r') as f:
            self.data = json.load(f)
    
    def initialize_database(self):
        """Initialize the vector database from scratch"""
        print("Loading processed data...")
        self.data = self.load_data()
        
        print("Creating embeddings...")
        texts = [item['text'] for item in self.data]
        embeddings = self.create_embeddings(texts)
        
        print("Building FAISS index...")
        self.build_index(embeddings)
        
        print("Saving index and metadata...")
        self.save_index()
        
        print("Vector database initialized successfully!")
    
    def search(self, query: str, k: int = 5) -> List[Tuple[Dict, float]]:
        """Search the database for relevant documents"""
        if self.index is None:
            self.load_index()
        
        # Embed the query
        query_embedding = self.create_embeddings([query])
        
        # Search the index
        distances, indices = self.index.search(query_embedding, k)
        
        # Retrieve the relevant documents with scores
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx >= 0:  # -1 indicates no result
                doc = self.data[idx]
                results.append((doc, float(distance)))
        
        return results

if __name__ == "__main__":
    db = VectorDatabase()
    db.initialize_database()
    
    # Test search
    test_query = "Who scored the most runs in IPL 2025?"
    results = db.search(test_query)
    print(f"\nResults for query: '{test_query}':")
    for doc, score in results:
        print(f"\nScore: {score:.4f}")
        print(doc['text'][:200] + "...")



















