import streamlit as st
import pickle
import string
import nltk

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# ✅ Download required NLTK data safely (only if missing)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

ps = PorterStemmer()
stop_words = set(stopwords.words('english'))  # ✅ load once


# ✅ Text preprocessing
def transform_text(text):
    text = text.lower()
    words = nltk.word_tokenize(text)

    # remove non-alphanumeric
    words = [w for w in words if w.isalnum()]

    # remove stopwords & punctuation
    words = [w for w in words if w not in stop_words and w not in string.punctuation]

    # stemming
    words = [ps.stem(w) for w in words]

    return " ".join(words)


# ✅ Load model safely
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))


# ✅ Streamlit UI
st.title("📩 Email/SMS Spam Classifier")

input_sms = st.text_area("Enter the message")

if st.button('Predict'):

    if input_sms.strip() == "":
        st.warning("Please enter a message")
    else:
        # preprocess
        transformed_sms = transform_text(input_sms)

        # vectorize
        vector_input = tfidf.transform([transformed_sms])

        # predict
        result = model.predict(vector_input)[0]

        # display
        if result == 1:
            st.error("🚨 Spam")
        else:
            st.success("✅ Not Spam")