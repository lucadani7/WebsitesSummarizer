import requests
from bs4 import BeautifulSoup
from nltk import sent_tokenize, download
from collections import Counter

# Attempt to download 'punkt' data
try:
    download('punkt')
    download('punkt_tab')
except Exception as e:
    print(f"Could not download punkt: {e}")


class WebpageSummarizer:
    def __init__(self, url):
        self.url = url
        self.summary = None

    def fetch_and_summarize(self, sentence_count=5):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract text content
            article_text = ' '.join([p.get_text() for p in soup.find_all('p')])
            sentences = sent_tokenize(article_text)

            # Simple frequency-based summarization
            word_freq = Counter(article_text.split())
            ranked_sentences = sorted(sentences, key=lambda s: sum(word_freq[word] for word in s.split()), reverse=True)

            self.summary = ranked_sentences[:sentence_count]
        except Exception as e:
            print(f"Error: {e}")
            raise Exception(f"Failed to fetch and summarize the webpage: {e}")

    def save_summary(self, output_file='summary.txt'):
        if not self.summary:
            raise ValueError("Summary is empty. Nothing to save.")

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for sentence in self.summary:
                    f.write(sentence + '\n')
        except IOError as e:
            raise Exception(f"Failed to save summary to file: {e}")
        print(f"Summary successfully written to {output_file}")


def main():
    try:
        url = input("Enter the URL of the website: ")
        summarizer = WebpageSummarizer(url)

        summarizer.fetch_and_summarize()
        summarizer.save_summary()

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
