# X (Twitter) Sentiment Analyzer 📊🕊️

CLI tool to fetch tweets on any topic from X (Twitter) and analyze their sentiment in real-time using both traditional NLP and transformer models.

## 🔍 What It Does

- Fetches tweets using Tweepy (up to 1,000+ with pagination)
- Cleans text, removes noise (mentions, links, emojis)
- Applies sentiment scoring via:
  - VADER (lexicon-based)
  - BERT (transformer-based, optional)
- Visualizes sentiment distribution with Matplotlib

## 🛠 Tech Stack

- **Python**: Core language
- **Tweepy**: Twitter API client
- **TextBlob / VADER / HuggingFace**: Sentiment models
- **Matplotlib**: Graphing
- **argparse**: CLI controls

- ## ⚙️ How to Run

1. Clone repo
2. Add your Bearer Token in `bearer.txt`
3. Run with:

```bash
python sentiment.py --query "elon musk"
