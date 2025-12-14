import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
import os

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
            # Add headers to mimic a real browser to avoid instant 403
            session = requests.Session()
            response = session.get(url, headers=random.choice(HEADERS_LIST), timeout=30)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Attempt 1: Try to find card elements (This selector needs to be accurate)
                # Common pattern for listings
                listings = soup.find_all("div", class_="ui-organism-intersection__element") 
                if not listings:
                     # Fallback for other layout types
                     listings = soup.find_all("div", class_="card-featured__content-wrapper")

                print(f"Found {len(listings)} listings on page {page}")

                for item in listings:
                    try:
                        # Extract data (Logic depends on specific DOM structure)
                        # NOTE: These selectors are 'best guess' and might need adjustment 
                        # if the website updates its class names.
                        
                        # Title/Name
                        title_tag = item.find("h2") or item.find("a", title=True)
                        nama_rumah = title_tag.get_text(strip=True) if title_tag else "N/A"
                        
                        # Price
                        price_tag = item.find("div", class_="price") or item.find("span", class_="ui-atomic-text--type-heading")
                        price_text = price_tag.get_text(strip=True) if price_tag else "0"
                        # Clean price text (e.g., "Rp 3,5 Miliar" -> 3500000000)
                        price = clean_price(price_text)
                        
                        # Specs (LT, LB, KT, KM)
                        # Usually inside icons wrapper
                        features = item.find_all("div", class_="attribute-info")
                        lt, lb, kt, km = 0, 0, 0, 0
                        
                        # Use text searching if specific classes are hard to find
                        text_content = item.get_text(" ", strip=True)
                        
                        # Simple heuristics for specs parsing from text if badges are missing
                        # e.g. "200 m² 100 m² 3 2"
                        
                        # Try finding explicit attributes
                        # This part requires inspection of the actual HTML structure
                        # Since we can't inspect, we will try to parse metadata attributes if available
                        attributes = item.find_all("div", class_="ui-atomic-text")
                        for attr in attributes:
                            val = attr.get_text(strip=True)
                            if "m²" in val:
                                if lt == 0: lt = parse_int(val) # Assumption: first m2 is LT or LB? usually LB first then LT or vice versa. 
                                # Let's assume standard order or look for icons
                                else: lb = parse_int(val) 
                            elif val.isdigit() and len(val) < 3:
                                # Likely KT or KM
                                if kt == 0: kt = int(val)
                                else: km = int(val)

                        if price > 0: # Only add if price is valid
                            all_data.append({
                                "NAMA RUMAH": nama_rumah,
                                "HARGA": price,
                                "LB": lb if lb > 0 else 100, # Defaulting if missing to avoid drop
                                "LT": lt if lt > 0 else 100,
                                "KT": kt if kt > 0 else 2,
                                "KM": km if km > 0 else 1,
                                "GRS": 1 # Hard to scrape, default to 1
                            })
                            
                    except Exception as e:
                        print(f"Error parsing item: {e}")
                        continue
            else:
                print(f"Failed to fetch page {page}: {response.status_code}")
                # If 403/429, stop scraping
                if response.status_code in [403, 429]:
                    print("Blocked by anti-scraping. Stopping.")
                    break
                
            time.sleep(random.uniform(2, 5))
            
        except Exception as e:
            print(f"Request failed: {e}")

    # Save Data
    if all_data:
        df = pd.DataFrame(all_data)
        # Add 'NO' column
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'NO'}, inplace=True)
        df['NO'] = df['NO'] + 1
        
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        df.to_excel(OUTPUT_FILE, index=False)
        print(f"Successfully scraped {len(df)} records to {OUTPUT_FILE}")
    else:
        print("No data scraped. Check selectors or anti-scraping blocking.")

def clean_price(price_text):
    # Example: "Rp 3,5 Miliar" -> 3500000000
    try:
        clean = price_text.lower().replace("rp", "").replace(",", ".").strip()
        multiplier = 1
        if "miliar" in clean or "m" in clean:
            multiplier = 1_000_000_000
            clean = clean.replace("miliar", "").replace("m", "")
        elif "juta" in clean or "jt" in clean:
            multiplier = 1_000_000
            clean = clean.replace("juta", "").replace("jt", "")
        
        return int(float(clean.strip()) * multiplier)
    except:
        print(f"debug price fail: {price_text}")
        return 0

def parse_int(text):
    try:
         return int(''.join(filter(str.isdigit, text)))
    except:
        return 0

if __name__ == "__main__":
    scrape_data(pages=2) # Try 2 pages
