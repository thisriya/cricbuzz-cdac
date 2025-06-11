# main.py
from scraper import CricbuzzScraper
from data_processor import DataProcessor
from vector_db import VectorDatabase
from chatbot import IPL2025Chatbot
import argparse

def main():
    parser = argparse.ArgumentParser(description="IPL 2025 Chatbot")
    parser.add_argument('--scrape', action='store_true', help='Scrape fresh data from Cricbuzz')
    parser.add_argument('--process', action='store_true', help='Process scraped data')
    parser.add_argument('--build-index', action='store_true', help='Build FAISS index')
    parser.add_argument('--chat', action='store_true', help='Start the chatbot')
    
    args = parser.parse_args()
    
    if args.scrape:
        print("Starting scraping process...")
        scraper = CricbuzzScraper()
        try:
            scraper.scrape_all()
        finally:
            scraper.close()
    
    if args.process:
        print("Processing data...")
        processor = DataProcessor()
        processor.process_all_data()
    
    if args.build_index:
        print("Building vector database...")
        db = VectorDatabase()
        db.initialize_database()
    
    if args.chat:
        print("Starting IPL 2025 Chatbot...")
        chatbot = IPL2025Chatbot()
        chatbot.chat()

if __name__ == "__main__":
    main()