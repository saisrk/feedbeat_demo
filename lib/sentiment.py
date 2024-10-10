import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import string
from colorama import Fore, Style


def preprocess_comment(comment: str):
    comment = comment.lower()
    comment = comment.translate(str.maketrans('', '', string.punctuation))
    comment = comment.translate(str.maketrans('', '', string.digits))

    tokens = word_tokenize(comment)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens

def get_sentiment(text: str):
    sid = SentimentIntensityAnalyzer()
    sentiment = sid.polarity_scores(text)
    if sentiment['compound'] >= 0.05:
        return 'positive'
    elif sentiment['compound'] <= -0.05:
        return 'negative'
    else:
        return 'neutral'
    
def analyze_comments(comments: list[str]):
    processed_comments = [preprocess_comment(comment) for comment in comments]
    sentiments = [get_sentiment(comment) for comment in processed_comments]
    neutral_count = sentiments.count('neutral')
    positive_count = sentiments.count('positive')
    negative_count = sentiments.count('negative')
    return {
        'neutral': neutral_count,
        'positive': positive_count,
        'negative': negative_count
    }

    
def get_overall_sentiment(sentiments: dict):
    if sentiments['positive'] > sentiments['negative']:
        overall_sentiment = 'POSITIVE'
        color = Fore.GREEN
    elif sentiments['negative'] > sentiments['positive']:
        overall_sentiment = 'NEGATIVE'
        color = Fore.RED
    else:
        overall_sentiment = 'NEUTRAL'
        color = Fore.YELLOW

    return '\n'+ Style.BRIGHT+ color + overall_sentiment.upper().center(50, ' ') + Style.RESET_ALL