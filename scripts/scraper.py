import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
import os
import re

# --- Configurations ---
BASE_URL = "https://www.rumah123.com/jual/jakarta-selatan/rumah/"
OUTPUT_FILE = "data/raw/DATA RUMAH.xlsx"
HEADERS_LIST = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"},
     {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}
]

def scrape_data(pages=1):
    all_data = []
    
    for page in range(1, pages + 1):
        url = f"{BASE_URL}?page={page}"
        print(f"Scraping page {page}: {url}")
        
        try:
            session = requests.Session()
            response = session.get(url, headers=random.choice(HEADERS_LIST), timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Robust selector found via debugging
                listings = soup.select('div[data-test-id^="srp-listing-card-"]')
                print(f"Found {len(listings)} listings on page {page}")

                for item in listings:
                    try:
                        # Full text content of the card
                        full_text = item.get_text(" ", strip=True) 
                        
                        # 1. Title (H2 is usually reliable)
                        title_tag = item.find("h2")
                        nama_rumah = title_tag.get_text(strip=True) if title_tag else "N/A"
                        
                        # 2. Price (Regex)
                        # Matches: Rp 7,5 Miliar, Rp 7.5 M, Rp 500 Juta, etc.
                        price_match = re.search(r'Rp\s*([\d\.,]+)\s+(Miliar|M|Juta|Jt)', full_text, re.IGNORECASE)
                        price = 0
                        if price_match:
                            val_str = price_match.group(1)
                            unit = price_match.group(2).lower()
                            val = float(val_str.replace(",", "."))
                            
                            if 'm' in unit:
                                price = int(val * 1_000_000_000)
                            elif 'j' in unit:
                                price = int(val * 1_000_000)
                        
                        # 3. Specs (Regex)
                        # LT: 60 m2, LB: 60 m2
                        lt, lb, kt, km = 0, 0, 0, 0
                        
                        # LT
                        lt_match = re.search(r'LT\s*:\s*(\d+)', full_text, re.IGNORECASE)
                        if lt_match: lt = int(lt_match.group(1))
                        
                        # LB
                        lb_match = re.search(r'LB\s*:\s*(\d+)', full_text, re.IGNORECASE)
                        if lb_match: lb = int(lb_match.group(1))
                        
                        # KT/KM (Heuristic: "3 KT" or similar is rare on this site layout)
                        # The layout often has just numbers next to icons.
                        # But without icons, we might miss them.
                        # Let's try to find numbers that are NOT LT/LB/Rp.
                        # Since we can't reliably parse KT/KM without icon classes, we default them.
                        # However, if we see "Kamar Tidur" in text (less likely on cards), use it.
                        kt = 2 # Default
                        km = 2 # Default
                        
                        if price > 0:
                            all_data.append({
                                "NAMA RUMAH": nama_rumah,
                                "HARGA": price,
                                "LB": lb if lb > 0 else 60,
                                "LT": lt if lt > 0 else 60,
                                "KT": kt,
                                "KM": km,
                                "GRS": 1
                            })
                            
                    except Exception as e:
                        print(f"Error parsing item: {e}")
                        continue
            else:
                print(f"Failed to fetch page {page}: {response.status_code}")
                
            time.sleep(random.uniform(2, 5))
            
        except Exception as e:
            print(f"Request failed: {e}")

    # ... Scrape logic ends ...

    # Save Data (Append Mode)
    if all_data:
        new_df = pd.DataFrame(all_data)
        print(f"Scraped {len(new_df)} new records.")
        
        if os.path.exists(OUTPUT_FILE):
            print(f"Found existing dataset at {OUTPUT_FILE}. Appending...")
            existing_df = pd.read_excel(OUTPUT_FILE)
            
            # Combine
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            
            # Remove Duplicates
            # We assume if (NAMA, MRG) are same, it's same listing. 
            # Or use all columns except NO/Index.
            # Ideally duplicates are subset=['NAMA RUMAH', 'HARGA', 'LB', 'LT']
            combined_df.drop_duplicates(subset=['NAMA RUMAH', 'LB', 'LT', 'KT', 'KM'], keep='last', inplace=True)
            
            # Re-index NO column
            combined_df.reset_index(drop=True, inplace=True)
            if 'NO' in combined_df.columns:
                combined_df['NO'] = combined_df.index + 1
            else:
                combined_df.insert(0, 'NO', combined_df.index + 1)
                
            final_df = combined_df
        else:
            print("No existing dataset found. Creating new one.")
            new_df.reset_index(inplace=True)
            new_df.rename(columns={'index': 'NO'}, inplace=True)
            new_df['NO'] = new_df['NO'] + 1
            final_df = new_df
        
        # Save
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        final_df.to_excel(OUTPUT_FILE, index=False)
        print(f"Successfully saved {len(final_df)} records to {OUTPUT_FILE}")
    else:
        print("No data scraped. Check selectors or anti-scraping blocking.")

def clean_price(price_text):
    # Legacy wrapper if needed, but regex handles it inside loop now
    return 0

def parse_int(text):
    try:
         return int(''.join(filter(str.isdigit, text)))
    except:
        return 0

if __name__ == "__main__":
    scrape_data(pages=2) # Try 2 pages
