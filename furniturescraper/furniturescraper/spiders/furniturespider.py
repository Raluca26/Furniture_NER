import scrapy
import csv
# import json
from itertools import islice
# import string
# import nltk
from nltk.corpus import stopwords
# import os
from googletrans import Translator



# nltk.download('wordnet')  # Make sure to download WordNet data if you haven't already
# lemmatizer = WordNetLemmatizer()

class FurnitureSpider(scrapy.Spider):
    name = "furniturespider"

    def start_requests(self):
        with open('/Users/PesikaMau/Desktop/veridion-5/pages.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in islice(csv_reader, 200): # Read the first 200 rows for trianing 
            # for row in islice(csv_reader, 200, None):  # read from 200 to end for the prediction
                link = row[0]  # get links
                yield scrapy.Request(url=link, callback=self.parse, meta={'original_url': link})

    def parse(self, response):
        if response.status == 200:
            # Extract text content and join it all
            headers1 = response.xpath("//body//h1//text()").extract()
            headers2 = response.xpath("//body//h2//text()").extract()
            headers3 = response.xpath("//body//h3//text()").extract()
            paragraph = response.xpath("//body//p//text()").extract()
            spans = response.xpath("//body//span//text()").extract()

            all_text = headers1 + headers2 + headers3 + paragraph + spans 

            # Combine all_text into a single string
            text = ' '.join(all_text)

            # Remove leading and trailing spaces
            text = text.strip()

            # Remove unnecessary line breaks and multiple spaces.
            text = ' '.join(text.split())
            text = ''.join([char for char in text if  char.isalpha() or char.isspace()]) #  Remove numerical output and punctuation
            text = text.lower()

            # Remove stopwords, single-letter words and words longer than 14 characters 
            stop_words = set(stopwords.words('english'))
            text = ' '.join(word for word in text.split() if word not in stop_words and len(word) > 1 and len(word) < 14)

            # Translate text content to English
            translator = Translator()
            translated_text = translator.translate(text, src='auto', dest='en').text

            #lemmatizer = WordNetLemmatizer()
            #lemmatized_text = ' '.join(lemmatizer.lemmatize(word) for word in translated_text.split())

            # Create a JSON structure with the link and the translated text
            data = {
                'url': response.meta['original_url'],
                'text_content': translated_text,
            }
            yield data
        else:
            self.logger.warning(f"Failed to fetch: {response.url}")


