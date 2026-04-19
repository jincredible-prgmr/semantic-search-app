  ---
  Quickstart

  1. Set up your API key
  cp .env.example .env
  # Edit .env and set: OPENAI_API_KEY=sk-your-key-here

  2. Install dependencies
  pip install -r requirements.txt

  3. Ingest data (one-time)
  cd src
  python ingest.py
  # Re-ingest from scratch: python ingest.py --force

  4. Run the app
  cd src
  streamlit run app.py

  The app opens at http://localhost:8501. If ChromaDB is empty it'll prompt you to run ingest.py first.