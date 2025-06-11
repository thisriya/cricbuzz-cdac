# # data_processor.py
# import json
# import pandas as pd
# from typing import List, Dict
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# import os

# class DataProcessor:
#     def __init__(self):
#         self.data_dir = "data"
#         self.processed_dir = "processed_data"
#         os.makedirs(self.processed_dir, exist_ok=True)
#         self.text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=500,
#             chunk_overlap=100,
#             length_function=len,
#             is_separator_regex=False,
#         )
    
#     def process_schedule_data(self) -> List[Dict]:
#         """Process schedule data into chunks"""
#         with open(f"{self.data_dir}/ipl2025_schedule.json", 'r') as f:
#             schedule = json.load(f)
        
#         chunks = []
#         for match in schedule:
#             text = f"Match: {match.get('match_number', '')}\n"
#             text += f"Teams: {match.get('team1', '')} vs {match.get('team2', '')}\n"
#             text += f"Venue: {match.get('venue', '')}\n"
#             text += f"Date & Time: {match.get('date_time', '')}"
            
#             chunks.append({
#                 "text": text,
#                 "metadata": {
#                     "source": "schedule",
#                     "match_number": match.get('match_number', ''),
#                     "teams": f"{match.get('team1', '')} vs {match.get('team2', '')}"
#                 }
#             })
        
#         return chunks
    
#     def process_player_stats(self) -> List[Dict]:
#         """Process player statistics into chunks"""
#         with open(f"{self.data_dir}/player_stats.json", 'r') as f:
#             stats = json.load(f)
        
#         chunks = []
        
#         # Process batting stats
#         if 'batting' in stats:
#             for player in stats['batting']:
#                 text = f"Player: {player['player']} (Batsman)\n"
#                 text += f"Matches: {player['matches']}\n"
#                 text += f"Innings: {player['inns']}\n"
#                 text += f"Runs: {player['runs']}\n"
#                 text += f"Average: {player['avg']}\n"
#                 text += f"Strike Rate: {player['sr']}\n"
#                 text += f"Boundaries: {player['4s']} fours, {player['6s']} sixes"
                
#                 chunks.append({
#                     "text": text,
#                     "metadata": {
#                         "source": "player_stats",
#                         "player": player['player'],
#                         "type": "batting"
#                     }
#                 })
        
#         # Process bowling stats
#         if 'bowling' in stats:
#             for player in stats['bowling']:
#                 text = f"Player: {player['player']} (Batsman)\n"
#                 text += f"Matches: {player['matches']}\n"
#                 text += f"Innings: {player['inns']}\n"
#                 text += f"Runs: {player['runs']}\n"
#                 text += f"Average: {player['avg']}\n"
#                 text += f"Strike Rate: {player['sr']}\n"
#                 text += f"Boundaries: {player['4s']} fours, {player['6s']} sixes"
                
#                 chunks.append({
#                     "text": text,
#                     "metadata": {
#                         "source": "player_stats",
#                         "player": player['player'],
#                         "type": "bowling"
#                     }
#                 })
        
#         return chunks
    
#     def process_news_articles(self) -> List[Dict]:
#         """Process news articles into chunks"""
#         with open(f"{self.data_dir}/ipl2025_news.json", 'r') as f:
#             news = json.load(f)
        
#         chunks = []
#         for article in news:
#             # Split longer articles into chunks
#             text = f"Headline: {article['headline']}\n"
#             text += f"Summary: {article['summary']}\n"
#             text += f"Date: {article['date']}"
            
#             # Use the text splitter for longer content if needed
#             if len(text) > 500:
#                 splits = self.text_splitter.split_text(text)
#                 for i, split in enumerate(splits):
#                     chunks.append({
#                         "text": split,
#                         "metadata": {
#                             "source": "news",
#                             "headline": article['headline'],
#                             "chunk_num": i+1
#                         }
#                     })
#             else:
#                 chunks.append({
#                     "text": text,
#                     "metadata": {
#                         "source": "news",
#                         "headline": article['headline']
#                     }
#                 })
        
#         return chunks
    
#     def process_all_data(self):
#         """Process all data sources and save to a single file"""
#         schedule_chunks = self.process_schedule_data()
#         player_chunks = self.process_player_stats()
#         news_chunks = self.process_news_articles()
        
#         all_chunks = schedule_chunks + player_chunks + news_chunks
        
#         # Convert to DataFrame and save
#         df = pd.DataFrame(all_chunks)
#         df.to_parquet(f"{self.processed_dir}/ipl2025_processed.parquet", index=False)
        
#         print(f"Processed {len(all_chunks)} chunks of data.")
#         return all_chunks

# if __name__ == "__main__":
#     processor = DataProcessor()
#     processor.process_all_data()








# data_processor.py
import json
import pandas as pd
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

class DataProcessor:
    def __init__(self):
        self.data_dir = "data"
        self.processed_dir = "processed_data"
        os.makedirs(self.processed_dir, exist_ok=True)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len,
            is_separator_regex=False,
        )
    
    def process_schedule_data(self) -> List[Dict]:
        """Process schedule data into chunks"""
        with open(f"{self.data_dir}/ipl_schedule.json", 'r') as f:
            schedule = json.load(f)
        
        chunks = []
        for match in schedule:
            text = f"Match: {match.get('match_number', '')}\n"
            text += f"Teams: {match.get('team1', '')} vs {match.get('team2', '')}\n"
            text += f"Venue: {match.get('venue', '')}\n"
            text += f"Date & Time: {match.get('date_time', '')}"
            
            chunks.append({
                "text": text,
                "metadata": {
                    "source": "schedule",
                    "match_number": match.get('match_number', ''),
                    "teams": f"{match.get('team1', '')} vs {match.get('team2', '')}"
                }
            })
        
        return chunks
    
    def process_player_stats(self) -> List[Dict]:
        with open(f"{self.data_dir}/ipl_player_stats.json", 'r') as f:
            stats = json.load(f)
        
        chunks = []
        
        # Process batting stats
        if 'batting' in stats:
            # Convert runs to integers for proper sorting
            for player in stats['batting']:
                player['runs'] = int(player['runs'])
            
            # Sort by runs descending (for top performers)
            batting_stats_desc = sorted(stats['batting'], key=lambda x: x['runs'], reverse=True)
            # Sort by runs ascending (for lowest performers)
            batting_stats_asc = sorted(stats['batting'], key=lambda x: x['runs'])
            
            # Create individual player chunks with ranking
            for rank, player in enumerate(batting_stats_desc, 1):
                text = f"Rank: {rank}\n"
                text += f"Player: {player['player']} (Batsman)\n"
                text += f"Matches: {player['matches']}\n"
                text += f"Innings: {player['innings']}\n"
                text += f"Runs: {player['runs']}\n"
                text += f"Highest: {player['highest']}\n"
                text += f"Average: {player['avg']}\n"
                text += f"Strike Rate: {player['sr']}\n"
                text += f"100s: {player['100s']}\n"
                
                chunks.append({
                    "text": text,
                    "metadata": {
                        "source": "ipl_player_stats",
                        "player": player['player'],
                        "type": "batting",
                        "rank": rank,
                        "runs": player['runs']
                    }
                })
            
            # Add summary chunks for quick retrieval
            top_5_text = "Top 5 Batsmen by Runs:\n" + \
                        "\n".join([f"{i+1}. {p['player']} - {p['runs']} runs" 
                                for i, p in enumerate(batting_stats_desc[:5])])
            
            bottom_5_text = "Bottom 5 Batsmen by Runs:\n" + \
                        "\n".join([f"{i+1}. {p['player']} - {p['runs']} runs" 
                                    for i, p in enumerate(batting_stats_asc[:5])])
            
            chunks.extend([
                {
                    "text": top_5_text,
                    "metadata": {
                        "source": "ipl_stats_summary",
                        "type": "batting_summary",
                        "summary_type": "top_batsmen"
                    }
                },
                {
                    "text": bottom_5_text,
                    "metadata": {
                        "source": "ipl_stats_summary",
                        "type": "batting_summary",
                        "summary_type": "bottom_batsmen"
                    }
                }
            ])
        
        # Process bowling stats (with corrected labels)
        if 'bowling' in stats:
            # Convert wickets to integers for proper sorting
            for player in stats['bowling']:
                player['wickets'] = int(player['wickets'])
            
            # Sort by wickets descending
            bowling_stats = sorted(stats['bowling'], key=lambda x: x['wickets'], reverse=True)
            
            for rank, player in enumerate(bowling_stats, 1):
                text = f"Rank: {rank}\n"
                text += f"Player: {player['player']} (Bowler)\n"  # Corrected to Bowler
                text += f"Matches: {player['matches']}\n"
                text += f"Innings: {player['innings']}\n"
                text += f"Overs: {player['overs']}\n"
                text += f"Wickets: {player['wickets']}\n"
                text += f"Best: {player['best']}\n"
                text += f"Avg: {player['avg']}\n"
                text += f"Economy: {player['economy']}\n"
                
                chunks.append({
                    "text": text,
                    "metadata": {
                        "source": "ipl_player_stats",
                        "player": player['player'],
                        "type": "bowling",
                        "rank": rank,
                        "wickets": player['wickets']
                    }
                })
            
            # Add bowling summary
            top_5_bowlers = "Top 5 Bowlers by Wickets:\n" + \
                        "\n".join([f"{i+1}. {p['player']} - {p['wickets']} wickets" 
                                    for i, p in enumerate(bowling_stats[:5])])
            
            chunks.append({
                "text": top_5_bowlers,
                "metadata": {
                    "source": "ipl_stats_summary",
                    "type": "bowling_summary",
                    "summary_type": "top_bowlers"
                }
            })
        
        return chunks
    
    def process_news_articles(self) -> List[Dict]:
        """Process news articles into chunks"""
        with open(f"{self.data_dir}/news_articles.json", 'r') as f:
            news = json.load(f)
        
        chunks = []
        for article in news:
            # Build text safely with get() method to handle missing keys
            text = f"Headline: {article.get('title', 'No Title')}\n"
            text += f"Url: {article.get('url', 'No URL')}\n"
            text += f"Description: {article.get('description', 'No Description')}\n"  # Note the added \n here
            text += f"Date: {article.get('date', 'No Date')}"
            
            # Use the text splitter for longer content if needed
            if len(text) > 500:
                splits = self.text_splitter.split_text(text)
                for i, split in enumerate(splits):
                    chunks.append({
                        "text": split,
                        "metadata": {
                            "source": "news",
                            "headline": article.get('title', 'No Title'),
                            "chunk_num": i+1
                        }
                    })
            else:
                chunks.append({
                    "text": text,
                    "metadata": {
                        "source": "news",
                        "headline": article.get('title', 'No Title')
                    }
                })
        
        return chunks
    
    def process_all_data(self):
        """Process all data sources and save to a single file"""
        schedule_chunks = self.process_schedule_data()
        player_chunks = self.process_player_stats()
        news_chunks = self.process_news_articles()
        
        all_chunks = schedule_chunks + player_chunks + news_chunks
        
        # Convert to DataFrame and save
        df = pd.DataFrame(all_chunks)
        df.to_parquet(f"{self.processed_dir}/ipl2025_processed.parquet", index=False)
        
        print(f"Processed {len(all_chunks)} chunks of data.")
        return all_chunks

if __name__ == "__main__":
    processor = DataProcessor()
    processor.process_all_data()



