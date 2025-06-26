
# RVRanger - Rewritten

This is a complete rebuild of RVRanger, focused on:

- Scraping clean Prevost listings (first 20) from prevost-stuff.com
- Serving via FastAPI backend (`api/api.py`)
- Elegant, borderless React frontend (`frontend/`)
- Ready to deploy on Replit with minimal setup

## Run Instructions (Replit-ready)

1. Run the scraper once:
    ```bash
    python scraper/prevost_scraper.py
    ```

2. Start the API server:
    ```bash
    uvicorn api.api:app --reload
    ```

3. In another shell, run the frontend:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

You’re now live on http://localhost:5173 with real scraped data!

---
