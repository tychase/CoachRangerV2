import os, re, json, hashlib
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.prevost-stuff.com"
LIST_PAGE = f"{BASE_URL}/forsale/public_list_ads.php"
OUTPUT_JSON = "scraper/listings.json"
IMG_DIR = "frontend/public/images"
HEADERS = {"User-Agent": "CoachRangerBot/1.0"}

os.makedirs(IMG_DIR, exist_ok=True)

def sanitize_filename(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

def md5(data):
    return hashlib.md5(data).hexdigest()[:12]

def download_image(src, title):
    if not src.startswith("http"):
        src = urljoin(BASE_URL, src)
    try:
        r = requests.get(src, headers=HEADERS, timeout=10)
        if r.status_code != 200 or len(r.content) < 25000:
            return None
        fname = f"img_{sanitize_filename(title)}_{md5(r.content)}.jpg"
        path = os.path.join(IMG_DIR, fname)
        with open(path, "wb") as f:
            f.write(r.content)
        return f"/images/{fname}"
    except Exception:
        return None

def scrape():
    r = requests.get(LIST_PAGE, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    listings = []

    for row in soup.select("table tr"):
        if len(listings) >= 20:
            break
        link = row.find("a", href=True)
        if not link:
            continue
        title = link.get_text(strip=True)
        price_match = re.search(r"\$[\d,]+", row.text)
        if not price_match:
            continue
        price = int(price_match.group().replace("$", "").replace(",", ""))
        year = re.search(r"\b(19|20)\d{2}\b", row.text)
        model = re.search(r"Model:\s*([A-Z0-9\-]+)", row.text, re.I)
        slides = re.search(r"Slides?:\s*(\d)", row.text, re.I)
        converter = re.search(r"Converter:\s*([^|]+)", row.text, re.I)

        img_tag = link.find("img")
        img_src = img_tag["src"] if img_tag else None
        image_url = download_image(img_src, title) if img_src else None

        listings.append({
            "title": title,
            "detail_url": urljoin(BASE_URL, link["href"]),
            "price": price,
            "year": int(year.group()) if year else None,
            "model": model.group(1) if model else None,
            "slides": int(slides.group(1)) if slides else 0,
            "converter": converter.group(1).strip() if converter else None,
            "featured_image": image_url
        })

    with open(OUTPUT_JSON, "w") as f:
        json.dump(listings, f, indent=2)
    print(f"Saved {len(listings)} listings to {OUTPUT_JSON}")

if __name__ == "__main__":
    scrape()