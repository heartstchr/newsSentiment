from textblob import TextBlob
import sys

input_text = sys.argv[1]

def main():
    text = input_text
    blob = TextBlob(text)
    print("input_text:"+blob.sentiment.polarity)
main()