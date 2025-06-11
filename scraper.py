# import json
# import time
# import random
# import logging
# from datetime import datetime
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import os
# from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


# class CricbuzzScraper:
#     def __init__(self):
#         self.base_url = "https://www.cricbuzz.com"
#         self.data_dir = "data"
#         os.makedirs(self.data_dir, exist_ok=True)
        
#         # Configure logging
#         self.setup_logging()
#         self.logger = logging.getLogger('CricbuzzScraper')
        
#         # Configure Selenium with headers and options
#         self.user_agents = [
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#             "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#         ]
        
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')
#         options.add_argument(f'user-agent={random.choice(self.user_agents)}')
#         # Additional options to improve reliability
#         options.add_argument('--disable-blink-features=AutomationControlled')  # Avoid detection
#         options.add_argument('--window-size=1920,1080')  # Ensure elements are visible
        
#         self.driver = webdriver.Chrome(
#             service=Service(ChromeDriverManager().install()),
#             options=options
#         )
#         self.wait = WebDriverWait(self.driver, 15)
        
#         # Set page load timeout
#         self.driver.set_page_load_timeout(30)
    
#     def setup_logging(self):
#         """Configure logging to file and console"""
#         logging.basicConfig(
#             level=logging.INFO,
#             format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#             handlers=[
#                 logging.FileHandler(os.path.join(self.data_dir, 'scraper.log')),
#                 logging.StreamHandler()
#             ]
#         )
    
#     def add_random_delay(self, min_sec=1, max_sec=3):
#         """Add random delay to mimic human behavior"""
#         delay = random.uniform(min_sec, max_sec)
#         time.sleep(delay)
    
#     def log_page_state(self, message):
#         """Log current page state with screenshot"""
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         screenshot_path = os.path.join(self.data_dir, f"page_{timestamp}.png")
#         try:
#             self.driver.save_screenshot(screenshot_path)
#             self.logger.info(f"{message} - Screenshot saved to {screenshot_path}")
            
#             # Log page source for debugging
#             source_path = os.path.join(self.data_dir, f"page_source_{timestamp}.html")
#             with open(source_path, 'w', encoding='utf-8') as f:
#                 f.write(self.driver.page_source)
#             self.logger.info(f"Page source saved to {source_path}")
#         except Exception as e:
#             self.logger.error(f"Failed to capture page state: {e}")
    
#     def safe_click(self, element, context=""):
#         """Handle click interception issues with multiple strategies"""
#         context_info = f" ({context})" if context else ""
#         try:
#             self.logger.info(f"Attempting direct click{context_info}")
#             element.click()
#             self.add_random_delay(1, 2)
#             return True
#         except Exception as e:
#             self.logger.warning(f"Direct click failed{context_info}: {e}")
            
#             # Strategy 1: JavaScript click
#             try:
#                 self.logger.info(f"Attempting JavaScript click{context_info}")
#                 self.driver.execute_script("arguments[0].click();", element)
#                 self.add_random_delay(1, 2)
#                 return True
#             except Exception as e:
#                 self.logger.warning(f"JavaScript click failed{context_info}: {e}")
            
#             # Strategy 2: Scroll into view and try again
#             try:
#                 self.logger.info(f"Scrolling element into view{context_info}")
#                 self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#                 self.add_random_delay(1, 2)
#                 element.click()
#                 self.add_random_delay(1, 2)
#                 return True
#             except Exception as e:
#                 self.logger.warning(f"Scroll and click failed{context_info}: {e}")
            
#             # Strategy 3: Actions click
#             try:
#                 self.logger.info(f"Attempting Actions click{context_info}")
#                 from selenium.webdriver.common.action_chains import ActionChains
#                 actions = ActionChains(self.driver)
#                 actions.move_to_element(element).click().perform()
#                 self.add_random_delay(1, 2)
#                 return True
#             except Exception as e:
#                 self.logger.error(f"All click strategies failed{context_info}: {e}")
#                 return False
    
#     def safe_find(self, by, value, multiple=False, context=None, timeout=15, retries=2):
#         """Safe element finding with multiple retry strategies"""
#         context_info = f" (Context: {context})" if context else ""
#         self.logger.info(f"Looking for element: {by}={value}{context_info}")
        
#         for attempt in range(retries + 1):
#             try:
#                 if multiple:
#                     elements = self.wait.until(EC.presence_of_all_elements_located((by, value)))
#                     if elements:
#                         self.logger.info(f"Found {len(elements)} elements matching {by}={value}")
#                         return elements
#                     else:
#                         self.logger.warning(f"No elements found for {by}={value} (attempt {attempt+1})")
#                 else:
#                     element = self.wait.until(EC.presence_of_element_located((by, value)))
#                     if element:
#                         self.logger.info(f"Found element matching {by}={value}")
#                         return element
#                     else:
#                         self.logger.warning(f"Element not found for {by}={value} (attempt {attempt+1})")
                        
#             except TimeoutException:
#                 if attempt < retries:
#                     self.logger.warning(f"Timeout finding {by}={value}{context_info}, retry {attempt+1}")
#                     # Try refreshing the page on timeout
#                     if attempt == 0:
#                         self.logger.info("Refreshing page")
#                         self.driver.refresh()
#                         self.add_random_delay(2, 4)
#                 else:
#                     self.logger.error(f"Element not found after {retries} retries: {by}={value}{context_info}")
#             except StaleElementReferenceException:
#                 if attempt < retries:
#                     self.logger.warning(f"Stale element {by}={value}{context_info}, retry {attempt+1}")
#                     self.add_random_delay(1, 2)
#                 else:
#                     self.logger.error(f"Stale element not resolved after {retries} retries: {by}={value}{context_info}")
#             except Exception as e:
#                 if attempt < retries:
#                     self.logger.warning(f"Error finding {by}={value}{context_info}: {e}, retry {attempt+1}")
#                     self.add_random_delay(1, 2)
#                 else:
#                     self.logger.error(f"Error finding {by}={value}{context_info} after {retries} retries: {e}")
        
#         # All retries failed
#         self.log_page_state(f"Element not found: {value}")
#         return [] if multiple else None

#     def wait_for_ajax_complete(self, timeout=10):
#         """Wait for AJAX requests to complete"""
#         try:
#             self.logger.info("Waiting for AJAX completion")
#             WebDriverWait(self.driver, timeout).until(
#                 lambda d: d.execute_script("return jQuery.active == 0")
#             )
#             self.logger.info("AJAX requests completed")
#             return True
#         except Exception as e:
#             self.logger.warning(f"Error waiting for AJAX or no jQuery detected: {e}")
#             return False

#     def navigate_to_url(self, url, description, max_retries=2):
#         """Navigate to URL with retry logic"""
#         self.logger.info(f"Navigating to {url} ({description})")
        
#         for attempt in range(max_retries + 1):
#             try:
#                 self.driver.get(url)
#                 self.logger.info(f"Successfully loaded {url}")
                
#                 # Wait for page to stabilize
#                 self.add_random_delay(3, 5)
                
#                 # Try waiting for AJAX if available
#                 self.wait_for_ajax_complete()
                
#                 return True
#             except Exception as e:
#                 if attempt < max_retries:
#                     self.logger.warning(f"Failed to load {url} (attempt {attempt+1}): {str(e)}")
#                     self.add_random_delay(2, 5)  # Back off before retry
#                 else:
#                     self.logger.error(f"Failed to load {url} after {max_retries} retries: {str(e)}")
#                     self.log_page_state(f"Failed to load {url}")
#                     return False
    
#     def handle_cookies(self):
#         """Handle cookie acceptance with multiple selectors"""
#         self.logger.info("Checking for cookie consent dialogs")
#         cookie_selectors = [
#             (By.XPATH, '//button[contains(text(), "Accept") or contains(text(), "Got it")]'),
#             (By.XPATH, '//button[contains(text(), "Accept All")]'),
#             (By.ID, 'onetrust-accept-btn-handler'),
#             (By.CSS_SELECTOR, '.cookie-consent-agree'),
#             (By.CSS_SELECTOR, '.cookie-policy-banner__accept')
#         ]
        
#         for by, selector in cookie_selectors:
#             try:
#                 btn = self.driver.find_element(by, selector)
#                 if btn and btn.is_displayed():
#                     self.logger.info(f"Found cookie button with {by}={selector}")
#                     self.safe_click(btn, "Cookie acceptance")
#                     self.add_random_delay(1, 2)
#                     return True
#             except Exception:
#                 continue
        
#         self.logger.info("No cookie dialogs found or already accepted")
#         return False

#     def get_ipl_schedule(self):
#         """Scrape IPL schedule with improved error handling"""
#         self.logger.info("Starting IPL schedule scraping")
        
#         # Try multiple schedule URLs
#         schedule_urls = [
#             (f"{self.base_url}/cricket-schedule/upcoming-series/international", "International schedule"),
#             (f"{self.base_url}/cricket-schedule/upcoming-series", "General schedule"),
#             (f"{self.base_url}/cricket-schedule/series/ipl-2025", "IPL 2025 schedule"),
#             (f"{self.base_url}/cricket-schedule", "All cricket schedule")
#         ]
        
#         for url, description in schedule_urls:
#             if self.navigate_to_url(url, description):
#                 break
#         else:
#             self.logger.error("Failed to load any schedule page")
#             return []
        
#         # Handle potential cookie dialogs
#         self.handle_cookies()
        
#         matches = []
        
#         # Updated selectors for match cards
#         selectors = [
#             ('div.cb-col.cb-col-100.cb-schdl', "Primary schedule cards"),
#             ('div[itemprop="subEvent"]', "Schema.org markup"),
#             ('div.cb-mtch-lst', "Alternative match list"),
#             ('div.cb-series-matches', "Series matches container"),
#             ('div.cb-schdl', "Schedule container"),
#             ('div.schedule-item', "Schedule item")
#         ]
        
#         match_cards = None
#         for selector, description in selectors:
#             match_cards = self.safe_find(By.CSS_SELECTOR, selector, multiple=True, 
#                                        context=f"Schedule cards - {description}")
#             if match_cards and len(match_cards) > 0:
#                 self.logger.info(f"Using selector: {selector} ({description})")
#                 break
        
#         if not match_cards or len(match_cards) == 0:
#             self.logger.error("No match cards found with any selector")
#             self.log_page_state("No match cards found")
            
#             # Last resort: try parsing the entire schedule section
#             try:
#                 schedule_section = self.safe_find(By.CSS_SELECTOR, '.cb-schdl')
#                 if schedule_section:
#                     self.logger.info("Attempting to parse entire schedule section")
#                     # Extract match text from the entire section
#                     match_info = {
#                         'raw_text': schedule_section.text,
#                         'source': 'fallback_parser'
#                     }
#                     matches.append(match_info)
#             except Exception as e:
#                 self.logger.error(f"Fallback parsing failed: {e}")
                
#             # Save whatever we have
#             output_path = os.path.join(self.data_dir, 'ipl_schedule.json')
#             with open(output_path, 'w') as f:
#                 json.dump(matches, f, indent=2)
#             self.logger.info(f"Saved {len(matches)} matches to {output_path}")
#             return matches
        
#         self.logger.info(f"Found {len(match_cards)} match cards to process")
        
#         for i, card in enumerate(match_cards):
#             try:
#                 self.logger.info(f"Processing match card {i+1}/{len(match_cards)}")
#                 match_info = {}
                
#                 # Improved team extraction with fallback to any text content
#                 team_selectors = [
#                     ('span.cb-schdl-team-name', "Primary team name"),
#                     ('span[itemprop="name"]', "Schema.org team name"),
#                     ('a.cb-ovr-flo', "Alternative team link"),
#                     ('.cb-team-name', "Team name class"),
#                     ('.cb-match-teams', "Match teams container")
#                 ]
                
#                 # Extract using selectors
#                 teams_found = False
#                 for selector, description in team_selectors:
#                     try:
#                         teams = card.find_elements(By.CSS_SELECTOR, selector)
#                         if len(teams) >= 2:
#                             match_info['team1'] = teams[0].text.strip()
#                             match_info['team2'] = teams[1].text.strip()
#                             self.logger.info(f"Found teams using {description} selector")
#                             teams_found = True
#                             break
#                     except Exception as e:
#                         self.logger.debug(f"Selector {selector} failed: {e}")
                
#                 # Fallback to parsing text content
#                 if not teams_found:
#                     try:
#                         card_text = card.text
#                         self.logger.info(f"Using text fallback. Card text: {card_text[:100]}...")
#                         # Store raw text for later parsing
#                         match_info['raw_text'] = card_text
#                     except Exception as e:
#                         self.logger.warning(f"Text extraction failed for card {i+1}: {e}")
                
#                 # Extract venue with multiple selectors
#                 venue_selectors = [
#                     ('div.cb-schdl-venue', "Primary venue"),
#                     ('div[itemprop="location"]', "Schema.org location"),
#                     ('span.cb-ovr-flo', "Alternative venue"),
#                     ('.cb-venue', "Venue class"),
#                     ('.cb-match-venue', "Match venue")
#                 ]
                
#                 venue_found = False
#                 for selector, description in venue_selectors:
#                     try:
#                         venue = card.find_element(By.CSS_SELECTOR, selector)
#                         venue_text = venue.text.strip()
#                         if venue_text:
#                             match_info['venue'] = venue_text.split(',')[0].strip()
#                             self.logger.info(f"Found venue using {description} selector")
#                             venue_found = True
#                             break
#                     except Exception:
#                         continue
                
#                 # Extract date and match info
#                 header_selectors = [
#                     ('h3.cb-schdl-heading', "Primary header"),
#                     ('h3[itemprop="name"]', "Schema.org name"),
#                     ('span.cb-mtch-dt', "Alternative date"),
#                     ('.cb-match-title', "Match title"),
#                     ('.cb-match-info', "Match info")
#                 ]
                
#                 header_found = False
#                 for selector, description in header_selectors:
#                     try:
#                         header = card.find_element(By.CSS_SELECTOR, selector)
#                         header_text = header.text.strip()
#                         if header_text:
#                             match_info['match_number'] = header_text
#                             self.logger.info(f"Found header using {description} selector")
#                             header_found = True
#                             break
#                     except Exception:
#                         continue
                
#                 # Extract date
#                 date_selectors = [
#                     ('.cb-match-date', "Match date"),
#                     ('.cb-schdl-date', "Schedule date"),
#                     ('span[itemprop="startDate"]', "Start date")
#                 ]
                
#                 for selector, description in date_selectors:
#                     try:
#                         date = card.find_element(By.CSS_SELECTOR, selector)
#                         date_text = date.text.strip()
#                         if date_text:
#                             match_info['date'] = date_text
#                             self.logger.info(f"Found date using {description} selector")
#                             break
#                     except Exception:
#                         continue
                
#                 matches.append(match_info)
#                 self.logger.info(f"Successfully processed match card {i+1}")
                
#             except Exception as e:
#                 self.logger.error(f"Error processing match card {i+1}: {str(e)}")
#                 continue
        
#         # Save results
#         output_path = os.path.join(self.data_dir, 'ipl_schedule.json')
#         with open(output_path, 'w') as f:
#             json.dump(matches, f, indent=2)
#         self.logger.info(f"Saved {len(matches)} matches to {output_path}")
        
#         return matches
    
#     def get_player_stats(self):
#         """Scrape player statistics with improved approach"""
#         self.logger.info("Starting player stats scraping")
#         stats = {'batting': [], 'bowling': []}
        
#         # Try multiple stats page URLs
#         stats_urls = [
#             (f"{self.base_url}/cricket-team/india/2/stats", "Team India stats page"),
#             (f"{self.base_url}/cricket-stats/ipl", "IPL stats page"),
#             (f"{self.base_url}/cricket-stats", "Main stats page")
#         ]
        
#         for url, description in stats_urls:
#             if self.navigate_to_url(url, description):
#                 break
#         else:
#             self.logger.error("Failed to load any stats page")
#             return stats
        
#         # Handle cookie dialogs
#         self.handle_cookies()
        
#         # Process batting stats
#         if self.switch_to_tab('Batting'):
#             # Wait for tab content to load
#             self.add_random_delay(2, 4)
            
#             # Try multiple table selectors
#             table_selectors = [
#                 ('table.cb-stats-table', "Primary stats table"),
#                 ('table.table', "Generic table"),
#                 ('div.cb-col.cb-col-100.cb-ltst-wgt-hdr', "Stats container")
#             ]
            
#             for selector, description in table_selectors:
#                 try:
#                     table = self.safe_find(By.CSS_SELECTOR, selector, context=f"Batting table - {description}")
#                     if table:
#                         self.logger.info(f"Found batting table with {description}")
#                         rows = table.find_elements(By.TAG_NAME, 'tr')
#                         if rows and len(rows) > 1:  # At least header + one data row
#                             self.logger.info(f"Found {len(rows)} rows in batting table")
#                             stats['batting'] = self.process_stats_rows(rows, 'batting')
#                             break
#                 except Exception as e:
#                     self.logger.warning(f"Error processing batting table with {description}: {e}")
            
#             if not stats['batting']:
#                 self.logger.warning("No batting stats rows found with any selector")
        
#         # Process bowling stats
#         if self.switch_to_tab('Bowling'):
#             # Wait for tab content to load
#             self.add_random_delay(2, 4)
            
#             # Try multiple table selectors
#             for selector, description in table_selectors:
#                 try:
#                     table = self.safe_find(By.CSS_SELECTOR, selector, context=f"Bowling table - {description}")
#                     if table:
#                         self.logger.info(f"Found bowling table with {description}")
#                         rows = table.find_elements(By.TAG_NAME, 'tr')
#                         if rows and len(rows) > 1:
#                             self.logger.info(f"Found {len(rows)} rows in bowling table")
#                             stats['bowling'] = self.process_stats_rows(rows, 'bowling')
#                             break
#                 except Exception as e:
#                     self.logger.warning(f"Error processing bowling table with {description}: {e}")
            
#             if not stats['bowling']:
#                 self.logger.warning("No bowling stats rows found with any selector")
        
#         # Save results
#         output_path = os.path.join(self.data_dir, 'player_stats.json')
#         with open(output_path, 'w') as f:
#             json.dump(stats, f, indent=2)
#         self.logger.info(f"Saved player stats to {output_path}")
        
#         return stats
    
#     def switch_to_tab(self, tab_name):
#         """Switch to specific stats tab with robust handling"""
#         self.logger.info(f"Attempting to switch to {tab_name} tab")
        
#         tab_selectors = [
#             (By.XPATH, f'//a[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{tab_name.lower()}")]'),
#             (By.XPATH, f'//a[contains(@class, "cb-nav-tab") and contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{tab_name.lower()}")]'),
#             (By.XPATH, f'//li[contains(@class, "nav-item")]//a[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{tab_name.lower()}")]'),
#             (By.CSS_SELECTOR, f'.cb-subnav-item:contains("{tab_name}")'),
#             (By.CSS_SELECTOR, f'a[data-tab="{tab_name.lower()}"]')
#         ]
        
#         for by, selector in tab_selectors:
#             tab = self.safe_find(by, selector, context=f"{tab_name} tab")
#             if tab:
#                 if self.safe_click(tab, f"{tab_name} tab"):
#                     self.logger.info(f"Successfully switched to {tab_name} tab")
#                     self.add_random_delay(2, 4)  # Wait for tab content to load
#                     return True
        
#         # Special case: try to find link by anchor text
#         try:
#             self.logger.info(f"Trying to find {tab_name} tab by link text")
#             tab = self.driver.find_element(By.LINK_TEXT, tab_name)
#             if tab and self.safe_click(tab, f"{tab_name} tab by link text"):
#                 self.logger.info(f"Successfully switched to {tab_name} tab by link text")
#                 self.add_random_delay(2, 4)
#                 return True
#         except Exception as e:
#             self.logger.warning(f"Could not find {tab_name} tab by link text: {e}")
        
#         self.logger.error(f"Could not find or switch to {tab_name} tab with any selector")
#         self.log_page_state(f"Failed to switch to {tab_name} tab")
#         return False
    
#     def process_stats_rows(self, rows, stats_type):
#         """Process stats rows with improved handling"""
#         stats = []
        
#         # Get header row to determine column positions
#         header_row = rows[0] if rows else None
#         if not header_row:
#             self.logger.error(f"No header row found for {stats_type} stats")
#             return stats
        
#         try:
#             # Extract header texts
#             headers = [h.text.strip().lower() for h in header_row.find_elements(By.TAG_NAME, 'th')]
#             self.logger.info(f"Found headers: {headers}")
            
#             # Process data rows
#             for i, row in enumerate(rows[1:]):  # Skip header row
#                 try:
#                     # Get all columns
#                     cols = row.find_elements(By.TAG_NAME, 'td')
#                     if not cols or len(cols) < 2:
#                         self.logger.warning(f"Insufficient columns in row {i+1}")
#                         continue
                    
#                     # Extract text from each column
#                     col_values = [col.text.strip() for col in cols]
#                     self.logger.debug(f"Row {i+1} values: {col_values}")
                    
#                     # Build stats object dynamically based on headers
#                     stat = {}
#                     for j, header in enumerate(headers):
#                         if j < len(col_values):
#                             # Map common header variations
#                             if header in ['player', 'batsman', 'bowler', 'name']:
#                                 stat['player'] = col_values[j]
#                             elif header in ['m', 'matches', 'mat']:
#                                 stat['matches'] = col_values[j]
#                             elif header in ['r', 'runs', 'run']:
#                                 stat['runs'] = col_values[j]
#                             elif header in ['w', 'wkts', 'wickets']:
#                                 stat['wickets'] = col_values[j]
#                             elif header in ['avg', 'average']:
#                                 stat['avg'] = col_values[j]
#                             elif header in ['sr', 'strike rate', 'strikerate']:
#                                 stat['sr'] = col_values[j]
#                             elif header in ['100s', 'centuries']:
#                                 stat['100s'] = col_values[j]
#                             elif header in ['50s', 'half centuries']:
#                                 stat['50s'] = col_values[j]
#                             elif header in ['4s', 'fours']:
#                                 stat['4s'] = col_values[j]
#                             elif header in ['6s', 'sixes']:
#                                 stat['6s'] = col_values[j]
#                             elif header in ['econ', 'economy']:
#                                 stat['economy'] = col_values[j]
#                             elif header in ['4w', '4 wickets']:
#                                 stat['4w'] = col_values[j]
#                             elif header in ['5w', '5 wickets']:
#                                 stat['5w'] = col_values[j]
#                             else:
#                                 # Use header as is for other cases
#                                 stat[header] = col_values[j]
                    
#                     # Only add if we have player name
#                     if 'player' in stat:
#                         stats.append(stat)
#                         self.logger.debug(f"Processed {stats_type} row {i+1}: {stat}")
#                     else:
#                         self.logger.warning(f"No player name found in row {i+1}")
                        
#                 except Exception as e:
#                     self.logger.error(f"Error processing {stats_type} row {i+1}: {str(e)}")
#                     continue
                
#         except Exception as e:
#             self.logger.error(f"Error processing {stats_type} headers: {str(e)}")
        
#         self.logger.info(f"Successfully processed {len(stats)} {stats_type} records")
#         return stats
    
#     def get_news_articles(self):
#         """Scrape news articles with improved search handling"""
#         self.logger.info("Starting news scraping")
#         articles = []
        
#         # Try multiple news page URLs
#         news_urls = [
#             (f"{self.base_url}/cricket-news", "Main news page"),
#             (f"{self.base_url}/cricket-news/latest-news", "Latest news"),
#             (f"{self.base_url}/cricket-news/archives", "News archives")
#         ]
        
#         for url, description in news_urls:
#             if self.navigate_to_url(url, description):
#                 break
#         else:
#             self.logger.error("Failed to load any news page")
#             return articles
        
#         # Handle cookie dialogs
#         self.handle_cookies()
        
#         # Try multiple article selectors
#         article_selectors = [
#             ('div.cb-col.cb-col-100.cb-lst-itm', "Primary article container"),
#             ('div.news-card', "News card"),
#             ('div.cb-news-item', "News item"),
#             ('article', "Generic article"),
#             ('div.cb-col.cb-col-33', "Alternative column layout")
#         ]
        
#         article_elements = None
#         for selector, description in article_selectors:
#             article_elements = self.safe_find(By.CSS_SELECTOR, selector, multiple=True,
#                                             context=f"News articles - {description}")
#             if article_elements and len(article_elements) > 0:
#                 self.logger.info(f"Using selector: {selector} ({description})")
#                 break
        
#         if not article_elements or len(article_elements) == 0:
#             self.logger.error("No article elements found with any selector")
#             self.log_page_state("No articles found")
#             return articles
        
#         self.logger.info(f"Found {len(article_elements)} articles to process")
        
#         for i, article in enumerate(article_elements):
#             try:
#                 self.logger.info(f"Processing article {i+1}/{len(article_elements)}")
#                 article_info = {}
                
#                 # Extract title with multiple selectors
#                 title_selectors = [
#                     ('a.cb-nws-hdln-ancr', "Primary headline"),
#                     ('h2.cb-nws-hdln', "Headline"),
#                     ('h2', "Generic h2"),
#                     ('a.title', "Title class"),
#                     ('[itemprop="headline"]', "Schema.org headline")
#                 ]
                
#                 for selector, description in title_selectors:
#                     try:
#                         title = article.find_element(By.CSS_SELECTOR, selector)
#                         title_text = title.text.strip()
#                         if title_text:
#                             article_info['title'] = title_text
#                             # Try to get URL if available
#                             try:
#                                 article_info['url'] = title.get_attribute('href')
#                             except:
#                                 pass
#                             self.logger.info(f"Found title using {description} selector")
#                             break
#                     except Exception:
#                         continue
                
#                 # Extract summary/description
#                 desc_selectors = [
#                     ('div.cb-nws-time', "Time and description"),
#                     ('div.cb-nws-desc', "Description"),
#                     ('p', "Generic paragraph"),
#                     ('[itemprop="description"]', "Schema.org description")
#                 ]
                
#                 for selector, description in desc_selectors:
#                     try:
#                         desc = article.find_element(By.CSS_SELECTOR, selector)
#                         desc_text = desc.text.strip()
#                         if desc_text:
#                             article_info['description'] = desc_text
#                             self.logger.info(f"Found description using {description} selector")
#                             break
#                     except Exception:
#                         continue
                
#                 # Extract date/time
#                 date_selectors = [
#                     ('span.cb-nws-time', "Time stamp"),
#                     ('time', "Time element"),
#                     ('[itemprop="datePublished"]', "Schema.org date"),
#                     ('.date', "Date class")
#                 ]
                
#                 for selector, description in date_selectors:
#                     try:
#                         date = article.find_element(By.CSS_SELECTOR, selector)
#                         date_text = date.text.strip()
#                         if date_text:
#                             article_info['date'] = date_text
#                             # Try to get datetime attribute if available
#                             try:
#                                 article_info['datetime'] = date.get_attribute('datetime')
#                             except:
#                                 pass
#                             self.logger.info(f"Found date using {description} selector")
#                             break
#                     except Exception:
#                         continue
                
#                 # Extract image if available
#                 img_selectors = [
#                     ('img.cb-nws-img', "News image"),
#                     ('img', "Generic image"),
#                     ('[itemprop="image"]', "Schema.org image")
#                 ]
                
#                 for selector, description in img_selectors:
#                     try:
#                         img = article.find_element(By.CSS_SELECTOR, selector)
#                         img_src = img.get_attribute('src')
#                         if img_src:
#                             article_info['image'] = img_src
#                             self.logger.info(f"Found image using {description} selector")
#                             break
#                     except Exception:
#                         continue
                
#                 if 'title' in article_info:  # Only add if we have at least a title
#                     articles.append(article_info)
#                     self.logger.info(f"Successfully processed article {i+1}")
#                 else:
#                     self.logger.warning(f"Article {i+1} skipped - no title found")
                
#             except Exception as e:
#                 self.logger.error(f"Error processing article {i+1}: {str(e)}")
#                 continue
        
#         # Save results
#         output_path = os.path.join(self.data_dir, 'news_articles.json')
#         with open(output_path, 'w') as f:
#             json.dump(articles, f, indent=2)
#         self.logger.info(f"Saved {len(articles)} articles to {output_path}")
        
#         return articles

#     def close(self):
#         """Clean up resources"""
#         self.logger.info("Closing scraper")
#         try:
#             self.driver.quit()
#         except Exception as e:
#             self.logger.error(f"Error closing driver: {e}")

#     def __del__(self):
#         """Destructor to ensure resources are cleaned up"""
#         self.close()


# if __name__ == "__main__":
#     # Main execution block
#     scraper = CricbuzzScraper()
#     try:
#         print("Starting Cricbuzz scraper...")
        
#         # Scrape IPL schedule
#         print("\nScraping IPL schedule...")
#         ipl_schedule = scraper.get_ipl_schedule()
#         print(f"Found {len(ipl_schedule)} IPL matches")
#         if ipl_schedule:
#             print("Sample match:", json.dumps(ipl_schedule[0], indent=2))
        
#         # Scrape player stats
#         print("\nScraping player stats...")
#         player_stats = scraper.get_player_stats()
#         print(f"Found {len(player_stats['batting'])} batting records")
#         print(f"Found {len(player_stats['bowling'])} bowling records")
#         if player_stats['batting']:
#             print("Sample batting record:", json.dumps(player_stats['batting'][0], indent=2))
#         if player_stats['bowling']:
#             print("Sample bowling record:", json.dumps(player_stats['bowling'][0], indent=2))
        
#         # Scrape news articles
#         print("\nScraping news articles...")
#         news_articles = scraper.get_news_articles()
#         print(f"Found {len(news_articles)} news articles")
#         if news_articles:
#             print("Sample article:", json.dumps(news_articles[0], indent=2))
        
#     except Exception as e:
#         print(f"Error during scraping: {e}")
#     finally:
#         scraper.close()
#         print("\nScraping completed. Check the 'data' directory for output files.")






















# ipl players,news
import json
import time
import random
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


class CricbuzzScraper:
    def __init__(self):
        self.base_url = "https://www.cricbuzz.com"
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Configure logging
        self.setup_logging()
        self.logger = logging.getLogger('CricbuzzScraper')
        
        # Configure Selenium with headers and options
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'user-agent={random.choice(self.user_agents)}')
        # Additional options to improve reliability
        options.add_argument('--disable-blink-features=AutomationControlled')  # Avoid detection
        options.add_argument('--window-size=1920,1080')  # Ensure elements are visible
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.wait = WebDriverWait(self.driver, 15)
        
        # Set page load timeout
        self.driver.set_page_load_timeout(30)
    
    def setup_logging(self):
        """Configure logging to file and console"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(self.data_dir, 'scraper.log')),
                logging.StreamHandler()
            ]
        )
    
    def add_random_delay(self, min_sec=1, max_sec=3):
        """Add random delay to mimic human behavior"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
    
    def log_page_state(self, message):
        """Log current page state with screenshot"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(self.data_dir, f"page_{timestamp}.png")
        try:
            self.driver.save_screenshot(screenshot_path)
            self.logger.info(f"{message} - Screenshot saved to {screenshot_path}")
            
            # Log page source for debugging
            source_path = os.path.join(self.data_dir, f"page_source_{timestamp}.html")
            with open(source_path, 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)
            self.logger.info(f"Page source saved to {source_path}")
        except Exception as e:
            self.logger.error(f"Failed to capture page state: {e}")
    
    def safe_click(self, element, context=""):
        """Handle click interception issues with multiple strategies"""
        context_info = f" ({context})" if context else ""
        try:
            self.logger.info(f"Attempting direct click{context_info}")
            element.click()
            self.add_random_delay(1, 2)
            return True
        except Exception as e:
            self.logger.warning(f"Direct click failed{context_info}: {e}")
            
            # Strategy 1: JavaScript click
            try:
                self.logger.info(f"Attempting JavaScript click{context_info}")
                self.driver.execute_script("arguments[0].click();", element)
                self.add_random_delay(1, 2)
                return True
            except Exception as e:
                self.logger.warning(f"JavaScript click failed{context_info}: {e}")
            
            # Strategy 2: Scroll into view and try again
            try:
                self.logger.info(f"Scrolling element into view{context_info}")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                self.add_random_delay(1, 2)
                element.click()
                self.add_random_delay(1, 2)
                return True
            except Exception as e:
                self.logger.warning(f"Scroll and click failed{context_info}: {e}")
            
            # Strategy 3: Actions click
            try:
                self.logger.info(f"Attempting Actions click{context_info}")
                from selenium.webdriver.common.action_chains import ActionChains
                actions = ActionChains(self.driver)
                actions.move_to_element(element).click().perform()
                self.add_random_delay(1, 2)
                return True
            except Exception as e:
                self.logger.error(f"All click strategies failed{context_info}: {e}")
                return False
    
    def safe_find(self, by, value, multiple=False, context=None, timeout=15, retries=2):
        """Safe element finding with multiple retry strategies"""
        context_info = f" (Context: {context})" if context else ""
        self.logger.info(f"Looking for element: {by}={value}{context_info}")
        
        for attempt in range(retries + 1):
            try:
                if multiple:
                    elements = self.wait.until(EC.presence_of_all_elements_located((by, value)))
                    if elements:
                        self.logger.info(f"Found {len(elements)} elements matching {by}={value}")
                        return elements
                    else:
                        self.logger.warning(f"No elements found for {by}={value} (attempt {attempt+1})")
                else:
                    element = self.wait.until(EC.presence_of_element_located((by, value)))
                    if element:
                        self.logger.info(f"Found element matching {by}={value}")
                        return element
                    else:
                        self.logger.warning(f"Element not found for {by}={value} (attempt {attempt+1})")
                        
            except TimeoutException:
                if attempt < retries:
                    self.logger.warning(f"Timeout finding {by}={value}{context_info}, retry {attempt+1}")
                    # Try refreshing the page on timeout
                    if attempt == 0:
                        self.logger.info("Refreshing page")
                        self.driver.refresh()
                        self.add_random_delay(2, 4)
                else:
                    self.logger.error(f"Element not found after {retries} retries: {by}={value}{context_info}")
            except StaleElementReferenceException:
                if attempt < retries:
                    self.logger.warning(f"Stale element {by}={value}{context_info}, retry {attempt+1}")
                    self.add_random_delay(1, 2)
                else:
                    self.logger.error(f"Stale element not resolved after {retries} retries: {by}={value}{context_info}")
            except Exception as e:
                if attempt < retries:
                    self.logger.warning(f"Error finding {by}={value}{context_info}: {e}, retry {attempt+1}")
                    self.add_random_delay(1, 2)
                else:
                    self.logger.error(f"Error finding {by}={value}{context_info} after {retries} retries: {e}")
        
        # All retries failed
        self.log_page_state(f"Element not found: {value}")
        return [] if multiple else None

    def wait_for_ajax_complete(self, timeout=10):
        """Wait for AJAX requests to complete"""
        try:
            self.logger.info("Waiting for AJAX completion")
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return jQuery.active == 0")
            )
            self.logger.info("AJAX requests completed")
            return True
        except Exception as e:
            self.logger.warning(f"Error waiting for AJAX or no jQuery detected: {e}")
            return False

    def navigate_to_url(self, url, description, max_retries=2):
        """Navigate to URL with retry logic"""
        self.logger.info(f"Navigating to {url} ({description})")
        
        for attempt in range(max_retries + 1):
            try:
                self.driver.get(url)
                self.logger.info(f"Successfully loaded {url}")
                
                # Wait for page to stabilize
                self.add_random_delay(3, 5)
                
                # Try waiting for AJAX if available
                self.wait_for_ajax_complete()
                
                return True
            except Exception as e:
                if attempt < max_retries:
                    self.logger.warning(f"Failed to load {url} (attempt {attempt+1}): {str(e)}")
                    self.add_random_delay(2, 5)  # Back off before retry
                else:
                    self.logger.error(f"Failed to load {url} after {max_retries} retries: {str(e)}")
                    self.log_page_state(f"Failed to load {url}")
                    return False
    
    def handle_cookies(self):
        """Handle cookie acceptance with multiple selectors"""
        self.logger.info("Checking for cookie consent dialogs")
        cookie_selectors = [
            (By.XPATH, '//button[contains(text(), "Accept") or contains(text(), "Got it")]'),
            (By.XPATH, '//button[contains(text(), "Accept All")]'),
            (By.ID, 'onetrust-accept-btn-handler'),
            (By.CSS_SELECTOR, '.cookie-consent-agree'),
            (By.CSS_SELECTOR, '.cookie-policy-banner__accept')
        ]
        
        for by, selector in cookie_selectors:
            try:
                btn = self.driver.find_element(by, selector)
                if btn and btn.is_displayed():
                    self.logger.info(f"Found cookie button with {by}={selector}")
                    self.safe_click(btn, "Cookie acceptance")
                    self.add_random_delay(1, 2)
                    return True
            except Exception:
                continue
        
        self.logger.info("No cookie dialogs found or already accepted")
        return False

    def get_ipl_schedule(self):
        """Scrape IPL schedule with improved error handling"""
        self.logger.info("Starting IPL schedule scraping")
        
        # Try multiple schedule URLs
        schedule_urls = [
            (f"{self.base_url}/cricket-schedule/upcoming-series/international", "International schedule"),
            (f"{self.base_url}/cricket-schedule/upcoming-series", "General schedule"),
            (f"{self.base_url}/cricket-schedule/series/ipl-2025", "IPL 2025 schedule"),
            (f"{self.base_url}/cricket-schedule", "All cricket schedule")
        ]
        
        for url, description in schedule_urls:
            if self.navigate_to_url(url, description):
                break
        else:
            self.logger.error("Failed to load any schedule page")
            return []
        
        # Handle potential cookie dialogs
        self.handle_cookies()
        
        matches = []
        
        # Updated selectors for match cards
        selectors = [
            ('div.cb-col.cb-col-100.cb-schdl', "Primary schedule cards"),
            ('div[itemprop="subEvent"]', "Schema.org markup"),
            ('div.cb-mtch-lst', "Alternative match list"),
            ('div.cb-series-matches', "Series matches container"),
            ('div.cb-schdl', "Schedule container"),
            ('div.schedule-item', "Schedule item")
        ]
        
        match_cards = None
        for selector, description in selectors:
            match_cards = self.safe_find(By.CSS_SELECTOR, selector, multiple=True, 
                                       context=f"Schedule cards - {description}")
            if match_cards and len(match_cards) > 0:
                self.logger.info(f"Using selector: {selector} ({description})")
                break
        
        if not match_cards or len(match_cards) == 0:
            self.logger.error("No match cards found with any selector")
            self.log_page_state("No match cards found")
            
            # Last resort: try parsing the entire schedule section
            try:
                schedule_section = self.safe_find(By.CSS_SELECTOR, '.cb-schdl')
                if schedule_section:
                    self.logger.info("Attempting to parse entire schedule section")
                    # Extract match text from the entire section
                    match_info = {
                        'raw_text': schedule_section.text,
                        'source': 'fallback_parser'
                    }
                    matches.append(match_info)
            except Exception as e:
                self.logger.error(f"Fallback parsing failed: {e}")
                
            # Save whatever we have
            output_path = os.path.join(self.data_dir, 'ipl_schedule.json')
            with open(output_path, 'w') as f:
                json.dump(matches, f, indent=2)
            self.logger.info(f"Saved {len(matches)} matches to {output_path}")
            return matches
        
        self.logger.info(f"Found {len(match_cards)} match cards to process")
        
        for i, card in enumerate(match_cards):
            try:
                self.logger.info(f"Processing match card {i+1}/{len(match_cards)}")
                match_info = {}
                
                # Improved team extraction with fallback to any text content
                team_selectors = [
                    ('span.cb-schdl-team-name', "Primary team name"),
                    ('span[itemprop="name"]', "Schema.org team name"),
                    ('a.cb-ovr-flo', "Alternative team link"),
                    ('.cb-team-name', "Team name class"),
                    ('.cb-match-teams', "Match teams container")
                ]
                
                # Extract using selectors
                teams_found = False
                for selector, description in team_selectors:
                    try:
                        teams = card.find_elements(By.CSS_SELECTOR, selector)
                        if len(teams) >= 2:
                            match_info['team1'] = teams[0].text.strip()
                            match_info['team2'] = teams[1].text.strip()
                            self.logger.info(f"Found teams using {description} selector")
                            teams_found = True
                            break
                    except Exception as e:
                        self.logger.debug(f"Selector {selector} failed: {e}")
                
                # Fallback to parsing text content
                if not teams_found:
                    try:
                        card_text = card.text
                        self.logger.info(f"Using text fallback. Card text: {card_text[:100]}...")
                        # Store raw text for later parsing
                        match_info['raw_text'] = card_text
                    except Exception as e:
                        self.logger.warning(f"Text extraction failed for card {i+1}: {e}")
                
                # Extract venue with multiple selectors
                venue_selectors = [
                    ('div.cb-schdl-venue', "Primary venue"),
                    ('div[itemprop="location"]', "Schema.org location"),
                    ('span.cb-ovr-flo', "Alternative venue"),
                    ('.cb-venue', "Venue class"),
                    ('.cb-match-venue', "Match venue")
                ]
                
                venue_found = False
                for selector, description in venue_selectors:
                    try:
                        venue = card.find_element(By.CSS_SELECTOR, selector)
                        venue_text = venue.text.strip()
                        if venue_text:
                            match_info['venue'] = venue_text.split(',')[0].strip()
                            self.logger.info(f"Found venue using {description} selector")
                            venue_found = True
                            break
                    except Exception:
                        continue
                
                # Extract date and match info
                header_selectors = [
                    ('h3.cb-schdl-heading', "Primary header"),
                    ('h3[itemprop="name"]', "Schema.org name"),
                    ('span.cb-mtch-dt', "Alternative date"),
                    ('.cb-match-title', "Match title"),
                    ('.cb-match-info', "Match info")
                ]
                
                header_found = False
                for selector, description in header_selectors:
                    try:
                        header = card.find_element(By.CSS_SELECTOR, selector)
                        header_text = header.text.strip()
                        if header_text:
                            match_info['match_number'] = header_text
                            self.logger.info(f"Found header using {description} selector")
                            header_found = True
                            break
                    except Exception:
                        continue
                
                # Extract date
                date_selectors = [
                    ('.cb-match-date', "Match date"),
                    ('.cb-schdl-date', "Schedule date"),
                    ('span[itemprop="startDate"]', "Start date")
                ]
                
                for selector, description in date_selectors:
                    try:
                        date = card.find_element(By.CSS_SELECTOR, selector)
                        date_text = date.text.strip()
                        if date_text:
                            match_info['date'] = date_text
                            self.logger.info(f"Found date using {description} selector")
                            break
                    except Exception:
                        continue
                
                matches.append(match_info)
                self.logger.info(f"Successfully processed match card {i+1}")
                
            except Exception as e:
                self.logger.error(f"Error processing match card {i+1}: {str(e)}")
                continue
        
        # Save results
        output_path = os.path.join(self.data_dir, 'ipl_schedule.json')
        with open(output_path, 'w') as f:
            json.dump(matches, f, indent=2)
        self.logger.info(f"Saved {len(matches)} matches to {output_path}")
        
        return matches
    
    def get_player_stats(self):
        """Scrape IPL 2024 player statistics from the stats page"""
        self.logger.info("Starting IPL 2025 player stats scraping")
        stats = {'batting': [], 'bowling': []}
        
        # Navigate to IPL 2024 stats page
        stats_url = f"{self.base_url}/cricket-series/9237/indian-premier-league-2025/stats"
        if not self.navigate_to_url(stats_url, "IPL 2025 stats page"):
            self.logger.error("Failed to load IPL 2025 stats page")
            return stats
        
        # Handle cookie dialogs
        self.handle_cookies()
        
        # Process batting stats
        if self.switch_to_tab('Most Runs'):
            self.logger.info("Processing batting stats")
            self.add_random_delay(2, 4)
            
            # Try to find the batting stats table
            batting_table = self.safe_find(By.CSS_SELECTOR, 'table.cb-series-stats', context="Batting stats table")
            if batting_table:
                self.logger.info("Found batting stats table")
                rows = batting_table.find_elements(By.TAG_NAME, 'tr')
                if rows and len(rows) > 1:  # At least header + one data row
                    self.logger.info(f"Processing {len(rows)} batting rows")
                    stats['batting'] = self.process_ipl_stats_rows(rows, 'batting')
                else:
                    self.logger.warning("No batting data rows found")
            else:
                self.logger.error("Batting stats table not found")
                self.log_page_state("Batting stats missing")
        
        # Process bowling stats
        if self.switch_to_tab('Most Wickets'):
            self.logger.info("Processing bowling stats")
            self.add_random_delay(2, 4)
            
            # Try to find the bowling stats table
            bowling_table = self.safe_find(By.CSS_SELECTOR, 'table.cb-series-stats', context="Bowling stats table")
            if bowling_table:
                self.logger.info("Found bowling stats table")
                rows = bowling_table.find_elements(By.TAG_NAME, 'tr')
                if rows and len(rows) > 1:
                    self.logger.info(f"Processing {len(rows)} bowling rows")
                    stats['bowling'] = self.process_ipl_stats_rows(rows, 'bowling')
                else:
                    self.logger.warning("No bowling data rows found")
            else:
                self.logger.error("Bowling stats table not found")
                self.log_page_state("Bowling stats missing")
        
        # Save results
        output_path = os.path.join(self.data_dir, 'ipl_player_stats.json')
        with open(output_path, 'w') as f:
            json.dump(stats, f, indent=2)
        self.logger.info(f"Saved IPL 2024 player stats to {output_path}")
        
        return stats
    
    def process_ipl_stats_rows(self, rows, stats_type):
        """Process IPL stats rows with specific column mapping"""
        stats = []
        
        if not rows or len(rows) < 2:
            self.logger.warning(f"No data rows found for {stats_type} stats")
            return stats
        
        # Get header row to determine column positions
        header_row = rows[0]
        headers = [h.text.strip().lower() for h in header_row.find_elements(By.TAG_NAME, 'th')]
        self.logger.info(f"Found {stats_type} headers: {headers}")
        
        # Process data rows
        for i, row in enumerate(rows[1:]):  # Skip header row
            try:
                cols = row.find_elements(By.TAG_NAME, 'td')
                if not cols or len(cols) < 2:
                    self.logger.warning(f"Skipping row {i+1} - insufficient columns")
                    continue
                
                col_values = [col.text.strip() for col in cols]
                self.logger.debug(f"Row {i+1} values: {col_values}")
                
                # Build stats object based on headers and stats type
                stat = {}
                
                # Common fields for both batting and bowling
                if len(headers) > 0 and len(col_values) > 0:
                    stat['pos'] = col_values[0]  # Position
                
                if len(headers) > 1 and len(col_values) > 1:
                    stat['player'] = col_values[1]  # Player name
                
                if stats_type == 'batting':
                    # Batting specific fields
                    if len(headers) > 2 and len(col_values) > 2:
                        stat['matches'] = col_values[2]
                    if len(headers) > 3 and len(col_values) > 3:
                        stat['innings'] = col_values[3]
                    if len(headers) > 4 and len(col_values) > 4:
                        stat['runs'] = col_values[4]
                    if len(headers) > 5 and len(col_values) > 5:
                        stat['highest'] = col_values[5]
                    if len(headers) > 6 and len(col_values) > 6:
                        stat['avg'] = col_values[6]
                    if len(headers) > 7 and len(col_values) > 7:
                        stat['sr'] = col_values[7]
                    if len(headers) > 8 and len(col_values) > 8:
                        stat['100s'] = col_values[8]
                    if len(headers) > 9 and len(col_values) > 9:
                        stat['50s'] = col_values[9]
                    if len(headers) > 10 and len(col_values) > 10:
                        stat['4s'] = col_values[10]
                    if len(headers) > 11 and len(col_values) > 11:
                        stat['6s'] = col_values[11]
                
                elif stats_type == 'bowling':
                    # Bowling specific fields
                    if len(headers) > 2 and len(col_values) > 2:
                        stat['matches'] = col_values[2]
                    if len(headers) > 3 and len(col_values) > 3:
                        stat['innings'] = col_values[3]
                    if len(headers) > 4 and len(col_values) > 4:
                        stat['overs'] = col_values[4]
                    if len(headers) > 5 and len(col_values) > 5:
                        stat['wickets'] = col_values[5]
                    if len(headers) > 6 and len(col_values) > 6:
                        stat['best'] = col_values[6]
                    if len(headers) > 7 and len(col_values) > 7:
                        stat['avg'] = col_values[7]
                    if len(headers) > 8 and len(col_values) > 8:
                        stat['economy'] = col_values[8]
                    if len(headers) > 9 and len(col_values) > 9:
                        stat['sr'] = col_values[9]
                    if len(headers) > 10 and len(col_values) > 10:
                        stat['4w'] = col_values[10]
                    if len(headers) > 11 and len(col_values) > 11:
                        stat['5w'] = col_values[11]
                
                # Only add if we have player name
                if 'player' in stat:
                    stats.append(stat)
                    self.logger.debug(f"Processed {stats_type} row {i+1}: {stat}")
                else:
                    self.logger.warning(f"No player name found in row {i+1}")
                    
            except Exception as e:
                self.logger.error(f"Error processing {stats_type} row {i+1}: {str(e)}")
                continue
        
        self.logger.info(f"Successfully processed {len(stats)} {stats_type} records")
        return stats
    
    def switch_to_tab(self, tab_name):
        """Switch to specific stats tab in IPL stats page"""
        self.logger.info(f"Attempting to switch to {tab_name} tab")
        
        # Try multiple tab selectors specific to IPL stats page
        tab_selectors = [
            (By.XPATH, f'//a[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{tab_name.lower()}")]'),
            (By.XPATH, f'//div[contains(@class, "cb-nav-subhdr")]//a[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{tab_name.lower()}")]'),
            (By.CSS_SELECTOR, f'a[href*="{tab_name.lower().replace(" ", "-")}"]'),
            (By.CSS_SELECTOR, f'a.cb-nav-tab:contains("{tab_name}")'),
            (By.CSS_SELECTOR, f'a[title*="{tab_name}"]')
        ]
        
        for by, selector in tab_selectors:
            tab = self.safe_find(by, selector, context=f"{tab_name} tab")
            if tab:
                if self.safe_click(tab, f"{tab_name} tab"):
                    self.logger.info(f"Successfully switched to {tab_name} tab")
                    self.add_random_delay(2, 4)  # Wait for tab content to load
                    return True
        
        self.logger.error(f"Could not find or switch to {tab_name} tab with any selector")
        self.log_page_state(f"Failed to switch to {tab_name} tab")
        return False
    
    def get_news_articles(self):
        """Scrape news articles with improved search handling"""
        self.logger.info("Starting news scraping")
        articles = []
        
        # Try multiple news page URLs
        news_urls = [
            (f"{self.base_url}/cricket-news", "Main news page"),
            (f"{self.base_url}/cricket-news/latest-news", "Latest news"),
            (f"{self.base_url}/cricket-news/archives", "News archives")
        ]
        
        for url, description in news_urls:
            if self.navigate_to_url(url, description):
                break
        else:
            self.logger.error("Failed to load any news page")
            return articles
        
        # Handle cookie dialogs
        self.handle_cookies()
        
        # Try multiple article selectors
        article_selectors = [
            ('div.cb-col.cb-col-100.cb-lst-itm', "Primary article container"),
            ('div.news-card', "News card"),
            ('div.cb-news-item', "News item"),
            ('article', "Generic article"),
            ('div.cb-col.cb-col-33', "Alternative column layout")
        ]
        
        article_elements = None
        for selector, description in article_selectors:
            article_elements = self.safe_find(By.CSS_SELECTOR, selector, multiple=True,
                                            context=f"News articles - {description}")
            if article_elements and len(article_elements) > 0:
                self.logger.info(f"Using selector: {selector} ({description})")
                break
        
        if not article_elements or len(article_elements) == 0:
            self.logger.error("No article elements found with any selector")
            self.log_page_state("No articles found")
            return articles
        
        self.logger.info(f"Found {len(article_elements)} articles to process")
        
        for i, article in enumerate(article_elements):
            try:
                self.logger.info(f"Processing article {i+1}/{len(article_elements)}")
                article_info = {}
                
                # Extract title with multiple selectors
                title_selectors = [
                    ('a.cb-nws-hdln-ancr', "Primary headline"),
                    ('h2.cb-nws-hdln', "Headline"),
                    ('h2', "Generic h2"),
                    ('a.title', "Title class"),
                    ('[itemprop="headline"]', "Schema.org headline")
                ]
                
                for selector, description in title_selectors:
                    try:
                        title = article.find_element(By.CSS_SELECTOR, selector)
                        title_text = title.text.strip()
                        if title_text:
                            article_info['title'] = title_text
                            # Try to get URL if available
                            try:
                                article_info['url'] = title.get_attribute('href')
                            except:
                                pass
                            self.logger.info(f"Found title using {description} selector")
                            break
                    except Exception:
                        continue
                
                # Extract summary/description
                desc_selectors = [
                    ('div.cb-nws-time', "Time and description"),
                    ('div.cb-nws-desc', "Description"),
                    ('p', "Generic paragraph"),
                    ('[itemprop="description"]', "Schema.org description")
                ]
                
                for selector, description in desc_selectors:
                    try:
                        desc = article.find_element(By.CSS_SELECTOR, selector)
                        desc_text = desc.text.strip()
                        if desc_text:
                            article_info['description'] = desc_text
                            self.logger.info(f"Found description using {description} selector")
                            break
                    except Exception:
                        continue
                
                # Extract date/time
                date_selectors = [
                    ('span.cb-nws-time', "Time stamp"),
                    ('time', "Time element"),
                    ('[itemprop="datePublished"]', "Schema.org date"),
                    ('.date', "Date class")
                ]
                
                for selector, description in date_selectors:
                    try:
                        date = article.find_element(By.CSS_SELECTOR, selector)
                        date_text = date.text.strip()
                        if date_text:
                            article_info['date'] = date_text
                            # Try to get datetime attribute if available
                            try:
                                article_info['datetime'] = date.get_attribute('datetime')
                            except:
                                pass
                            self.logger.info(f"Found date using {description} selector")
                            break
                    except Exception:
                        continue
                
                # Extract image if available
                img_selectors = [
                    ('img.cb-nws-img', "News image"),
                    ('img', "Generic image"),
                    ('[itemprop="image"]', "Schema.org image")
                ]
                
                for selector, description in img_selectors:
                    try:
                        img = article.find_element(By.CSS_SELECTOR, selector)
                        img_src = img.get_attribute('src')
                        if img_src:
                            article_info['image'] = img_src
                            self.logger.info(f"Found image using {description} selector")
                            break
                    except Exception:
                        continue
                
                if 'title' in article_info:  # Only add if we have at least a title
                    articles.append(article_info)
                    self.logger.info(f"Successfully processed article {i+1}")
                else:
                    self.logger.warning(f"Article {i+1} skipped - no title found")
                
            except Exception as e:
                self.logger.error(f"Error processing article {i+1}: {str(e)}")
                continue
        
        # Save results
        output_path = os.path.join(self.data_dir, 'news_articles.json')
        with open(output_path, 'w') as f:
            json.dump(articles, f, indent=2)
        self.logger.info(f"Saved {len(articles)} articles to {output_path}")
        
        return articles

    def close(self):
        """Clean up resources"""
        self.logger.info("Closing scraper")
        try:
            self.driver.quit()
        except Exception as e:
            self.logger.error(f"Error closing driver: {e}")

    def __del__(self):
        """Destructor to ensure resources are cleaned up"""
        self.close()


if __name__ == "__main__":
    # Main execution block
    scraper = CricbuzzScraper()
    try:
        print("Starting Cricbuzz scraper...")
        
        # Scrape IPL schedule
        print("\nScraping IPL schedule...")
        ipl_schedule = scraper.get_ipl_schedule()
        print(f"Found {len(ipl_schedule)} IPL matches")
        if ipl_schedule:
            print("Sample match:", json.dumps(ipl_schedule[0], indent=2))
        
        # Scrape IPL 2024 player stats
        print("\nScraping IPL 2024 player stats...")
        player_stats = scraper.get_player_stats()
        print(f"Found {len(player_stats['batting'])} batting records")
        print(f"Found {len(player_stats['bowling'])} bowling records")
        if player_stats['batting']:
            print("Sample batting record:", json.dumps(player_stats['batting'][0], indent=2))
        if player_stats['bowling']:
            print("Sample bowling record:", json.dumps(player_stats['bowling'][0], indent=2))
        
        # Scrape news articles
        print("\nScraping news articles...")
        news_articles = scraper.get_news_articles()
        print(f"Found {len(news_articles)} news articles")
        if news_articles:
            print("Sample article:", json.dumps(news_articles[0], indent=2))
        
    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        scraper.close()
        print("\nScraping completed. Check the 'data' directory for output files.")
        
        
        
        
        
        
        
        
        
        
        
# all tabs discover
# import json
# import time
# import random
# import logging
# from datetime import datetime
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import os
# from selenium.common.exceptions import (TimeoutException, 
#                                       NoSuchElementException,
#                                       ElementClickInterceptedException,
#                                       StaleElementReferenceException)

# class CricbuzzStatsScraper:
#     def __init__(self):
#         self.base_url = "https://m.cricbuzz.com/cricket-team/india/2/stats"
#         self.data_dir = "data"
#         os.makedirs(self.data_dir, exist_ok=True)
        
#         self.setup_logging()
#         self.logger = logging.getLogger('CricbuzzScraper')
        
#         # Configure Chrome options
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless=new')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')
#         options.add_argument('--window-size=1200,800')
#         options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
#         self.driver = webdriver.Chrome(
#             service=Service(ChromeDriverManager().install()),
#             options=options
#         )
#         self.wait = WebDriverWait(self.driver, 20)
    
#     def setup_logging(self):
#         """Configure logging to file and console"""
#         logging.basicConfig(
#             level=logging.INFO,
#             format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#             handlers=[
#                 logging.FileHandler(os.path.join(self.data_dir, 'scraper.log')),
#                 logging.StreamHandler()
#             ]
#         )
    
#     def save_page_state(self, context=""):
#         """Save current page state for debugging"""
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         try:
#             # Save screenshot
#             screenshot_path = os.path.join(self.data_dir, f"screenshot_{context}_{timestamp}.png")
#             self.driver.save_screenshot(screenshot_path)
#             self.logger.info(f"Screenshot saved to {screenshot_path}")
            
#             # Save page source
#             source_path = os.path.join(self.data_dir, f"source_{context}_{timestamp}.html")
#             with open(source_path, 'w', encoding='utf-8') as f:
#                 f.write(self.driver.page_source)
#             self.logger.info(f"Page source saved to {source_path}")
#         except Exception as e:
#             self.logger.error(f"Failed to save page state: {e}")

#     def click_with_retry(self, element, max_attempts=3):
#         """Attempt to click an element with retries"""
#         for attempt in range(max_attempts):
#             try:
#                 element.click()
#                 return True
#             except (ElementClickInterceptedException, StaleElementReferenceException) as e:
#                 self.logger.warning(f"Click attempt {attempt + 1} failed: {e}")
#                 time.sleep(1 + attempt)  # Progressive delay
#                 if attempt == max_attempts - 1:
#                     self.logger.error(f"Failed to click after {max_attempts} attempts")
#                     return False
#                 continue
#         return False

#     def navigate_to_stats_page(self):
#         """Navigate to stats page and wait for it to load"""
#         self.logger.info(f"Navigating to {self.base_url}")
#         try:
#             self.driver.get(self.base_url)
#             # Wait for either the tabs or the stats container to load
#             self.wait.until(
#                 EC.presence_of_element_located(
#                     (By.CSS_SELECTOR, 'div[class*="flex flex-col tb:grid"]')
#                 )
#             )
#             self.logger.info("Stats page loaded successfully")
#             return True
#         except Exception as e:
#             self.logger.error(f"Failed to load stats page: {e}")
#             self.save_page_state("page_load_failed")
#             return False

#     def get_all_tabs(self):
#         self.logger.info("Looking for all stat tabs including batting and bowling")
#         all_tabs = []
#         try:
#             tabs_container = self.wait.until(
#             EC.presence_of_element_located(
#                 (By.CSS_SELECTOR, 'div[class*="flex flex-col tb:grid"]')
#             )
#         )
#             tab_elements = tabs_container.find_elements(
#             By.CSS_SELECTOR, 'div[class*="flex items-center justify-between"]'
#         )
        
#             for tab in tab_elements:
#                 try:
#                     tab_name = tab.find_element(By.TAG_NAME, 'span').text.strip()
#                     if tab_name:
#                         all_tabs.append((tab_name, tab))
#                 except Exception as e:
#                     self.logger.warning(f"Couldn't get tab name: {e}")
#                     continue
#         except Exception as e:
#             self.logger.error(f"Failed to find main tabs: {e}")
#             self.save_page_state("main_tabs_not_found")

#         # Then get the bowling-specific tabs
#         try:
#             # Locate the bowling header element
#             bowling_header = self.wait.until(
#                 EC.presence_of_element_located(
#                     (By.XPATH, '//div[contains(@class, "bg-cbGrpHdrBkg") and contains(., "Bowling")]')
#                 )
#             )
            
#             # Find the parent container that holds all the bowling tabs
#             # Changed XPath to be more specific to the actual structure
#             bowling_container = bowling_header.find_element(
#                 By.XPATH, 
#                 './following-sibling::div[contains(@class, "flex flex-col tb:grid")]'
#             )
            
#             # Find all bowling tab elements
#             bowling_tab_elements = bowling_container.find_elements(
#                 By.XPATH, './/div[contains(@class, "flex items-center justify-between")]'
#             )
            
#             for tab in bowling_tab_elements:
#                 try:
#                     tab_name = tab.find_element(By.TAG_NAME, 'span').text.strip()
#                     if tab_name:
#                         # Add "Bowling" prefix to distinguish these tabs
#                         all_tabs.append((f"Bowling - {tab_name}", tab))
#                 except Exception as e:
#                     self.logger.warning(f"Couldn't get bowling tab name: {e}")
#                     continue
#         except Exception as e:
#             self.logger.error(f"Failed to find bowling tabs: {e}")
#             self.save_page_state("bowling_tabs_not_found")

#         self.logger.info(f"Found {len(all_tabs)} total tabs: {[t[0] for t in all_tabs]}")
#         return all_tabs

#     def scrape_table(self, table):
#         """Scrape data from a single table with more precise selectors"""
#         try:
#             # Get all header elements
#             headers = [th.text.strip() for th in table.find_elements(By.CSS_SELECTOR, 'thead th')]
            
#             rows = []
            
#             # Find all rows in the table body
#             for row in table.find_elements(By.CSS_SELECTOR, 'tbody tr'):
#                 try:
#                     # Get all columns in the row
#                     cols = row.find_elements(By.CSS_SELECTOR, 'td')
#                     if len(cols) != len(headers):
#                         self.logger.warning(f"Header/column mismatch: {len(headers)} headers vs {len(cols)} columns")
#                         continue
                    
#                     row_data = {}
#                     for i in range(len(headers)):
#                         # Special handling for player name column (contains link)
#                         if headers[i].lower() in ['batter', 'bowler', 'player']:
#                             try:
#                                 # Try to get the link text first
#                                 link = cols[i].find_element(By.CSS_SELECTOR, 'a')
#                                 row_data[headers[i]] = link.text.strip()
#                                 row_data[f"{headers[i]}_link"] = link.get_attribute('href')
#                             except NoSuchElementException:
#                                 # Fall back to regular text if no link
#                                 row_data[headers[i]] = cols[i].text.strip()
#                         else:
#                             row_data[headers[i]] = cols[i].text.strip()
                    
#                     rows.append(row_data)
#                 except Exception as e:
#                     self.logger.warning(f"Error processing row: {e}")
#                     continue
            
#             return rows
#         except Exception as e:
#             self.logger.error(f"Error scraping table: {e}")
#             self.save_page_state("table_scrape_error")
#             return []

#     def scrape_tab_data(self, tab_name, tab_element):
#         """Scrape data from a specific tab with improved table finding"""
#         self.logger.info(f"Processing tab: {tab_name}")
        
#         if not self.click_with_retry(tab_element):
#             self.logger.error(f"Failed to activate tab: {tab_name}")
#             return None
        
#         # Wait for content to load
#         time.sleep(2)  # Slightly longer pause for content to load
        
#         try:
#             # Find the stats table container with more specific selector
#             table_container = self.wait.until(
#                 EC.presence_of_element_located(
#                     (By.CSS_SELECTOR, 'div[id="teamStatsTable"]')
#                 )
#             )
            
#             # Find all tables in this tab
#             tables = table_container.find_elements(By.CSS_SELECTOR, 'table.cb-series-stats')
#             if not tables:
#                 self.logger.warning(f"No tables found in {tab_name} tab")
#                 return None
            
#             tab_data = []
            
#             for table in tables:
#                 table_data = self.scrape_table(table)
#                 if table_data:
#                     tab_data.extend(table_data)
            
#             self.logger.info(f"Found {len(tab_data)} records in {tab_name} tab")
#             return tab_data
#         except Exception as e:
#             self.logger.error(f"Failed to scrape {tab_name} tab: {e}")
#             self.save_page_state(f"tab_{tab_name}_failed")
#             return None

#     def scrape_all_stats(self):
#         """Main method to scrape all statistics"""
#         self.logger.info("Starting stats scraping")
        
#         if not self.navigate_to_stats_page():
#             return None
        
#         all_stats = {}
#         tabs = self.get_all_tabs()
        
#         if not tabs:
#             self.logger.error("No tabs found to scrape")
#             return None
        
#         for tab_name, tab_element in tabs:
#             tab_data = self.scrape_tab_data(tab_name, tab_element)
#             if tab_data:
#                 all_stats[tab_name] = tab_data
#             # Random delay between tabs to appear more natural
#             time.sleep(random.uniform(1, 3))
        
#         if all_stats:
#             self.save_stats(all_stats)
#             return all_stats
#         else:
#             self.logger.error("No data scraped from any tab")
#             return None
    
#     def save_stats(self, stats_data):
#         """Save scraped data to JSON file"""
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         filename = os.path.join(self.data_dir, f"cricbuzz_stats_{timestamp}.json")
        
#         try:
#             with open(filename, 'w', encoding='utf-8') as f:
#                 json.dump(stats_data, f, indent=2, ensure_ascii=False)
#             self.logger.info(f"Stats saved to {filename}")
#         except Exception as e:
#             self.logger.error(f"Failed to save stats: {e}")

#     def close(self):
#         """Clean up resources"""
#         try:
#             self.driver.quit()
#             self.logger.info("Browser closed successfully")
#         except Exception as e:
#             self.logger.error(f"Error closing browser: {e}")

#     def __del__(self):
#         """Destructor to ensure cleanup"""
#         self.close()


# if __name__ == "__main__":
#     scraper = CricbuzzStatsScraper()
#     try:
#         print("Starting Cricbuzz stats scraper...")
#         stats = scraper.scrape_all_stats()
        
#         if stats:
#             print("\nSuccessfully scraped stats from:")
#             for tab_name, data in stats.items():
#                 print(f"- {tab_name}: {len(data)} records")
            
#             # Print sample data
#             first_tab = next(iter(stats))
#             print(f"\nSample from {first_tab}:")
#             print(json.dumps(stats[first_tab][0], indent=2))
#         else:
#             print("\nFailed to scrape any stats data")
        
#     except Exception as e:
#         print(f"\nError during scraping: {e}")
#     finally:
#         print("\nScraping completed. Check the logs in the 'data' directory for details.")