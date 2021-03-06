import pandas as pd
import numpy as np
import pickle
import sys
import re

tweet = str(sys.argv[1:])

from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

stop = stopwords.words('english')
porter = PorterStemmer()

def tokenizer_porter(text):
    return [porter.stem(word) for word in text.split()]

mc_tfidf_lr = pickle.load(open('mc_tfidf_lr.sav', 'rb'))

#clean text
def preprocessor(text):
    text = re.sub('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', 'toperson', text)
    text = re.sub('(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', 'link', text)

    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)',
                           text)
    text = (re.sub('[\W]+', ' ', text.lower()) +
            ' '.join(emoticons).replace('-', ''))
    return [text]

clean_tweet = preprocessor(tweet)

prediction = mc_tfidf_lr.predict(clean_tweet)
probability = mc_tfidf_lr.predict_proba(clean_tweet)

print('{0} '.format(str(prediction[0])) + str(round(np.max(probability), 3)))
