import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# ✅ Download required NLTK data safely
for resource, path in [
    ('punkt',     'tokenizers/punkt'),
    ('punkt_tab', 'tokenizers/punkt_tab'),
    ('stopwords', 'corpora/stopwords'),
]:
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(resource)

ps = PorterStemmer()
stop_words = set(stopwords.words('english'))


def transform_text(text):
    text = text.lower()
    words = nltk.word_tokenize(text)
    words = [w for w in words if w.isalnum()]
    words = [w for w in words if w not in stop_words and w not in string.punctuation]
    words = [ps.stem(w) for w in words]
    return " ".join(words)


tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

# ─────────────────────────────────────────────
#  Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SpamGuard",
    page_icon="🛡️",
    layout="centered",
)

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: #080C14 !important;
    color: #DCE0F0;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 1.5rem !important;
    max-width: 660px !important;
}

/* ── Header ── */
.sg-hero {
    text-align: center;
    padding: 2.5rem 0 2rem;
}
.sg-badge {
    display: inline-block;
    background: linear-gradient(135deg, #3B5BF6, #9333EA);
    border-radius: 16px;
    padding: 1rem 1.1rem;
    font-size: 2.2rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 0 50px rgba(59,91,246,0.45);
}
.sg-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    background: linear-gradient(120deg, #ffffff 0%, #9BA8D8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.4rem;
    line-height: 1.15;
}
.sg-sub {
    color: #4A5270;
    font-size: 0.92rem;
    font-weight: 300;
    letter-spacing: 0.03em;
}

/* ── Stat chips ── */
.sg-chips {
    display: flex;
    justify-content: center;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-bottom: 2rem;
}
.sg-chip {
    background: #111623;
    border: 1px solid #1D2438;
    border-radius: 999px;
    padding: 0.35rem 1rem;
    font-size: 0.78rem;
    color: #5B6A99;
    letter-spacing: 0.04em;
}
.sg-chip span {
    color: #3B5BF6;
    font-weight: 600;
    margin-right: 0.3rem;
}

/* ── Card ── */
.sg-card {
    background: #0F1420;
    border: 1px solid #181F30;
    border-radius: 22px;
    padding: 2rem 2rem 1.6rem;
    box-shadow: 0 8px 48px rgba(0,0,0,0.5);
}
.sg-field-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #3B5BF6;
    margin-bottom: 0.55rem;
}

/* ── Textarea ── */
textarea {
    background: #080C14 !important;
    border: 1px solid #1D2438 !important;
    border-radius: 14px !important;
    color: #DCE0F0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.93rem !important;
    line-height: 1.65 !important;
    padding: 1rem 1.1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
textarea:focus {
    border-color: #3B5BF6 !important;
    box-shadow: 0 0 0 3px rgba(59,91,246,0.12) !important;
    outline: none !important;
}
textarea::placeholder { color: #2A3050 !important; }

/* ── Button ── */
div.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #3B5BF6 0%, #7C3AED 100%) !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.85rem 1rem !important;
    margin-top: 0.8rem !important;
    cursor: pointer !important;
    box-shadow: 0 4px 28px rgba(59,91,246,0.4) !important;
    transition: transform 0.15s, opacity 0.2s !important;
}
div.stButton > button:hover {
    opacity: 0.85 !important;
    transform: translateY(-2px) !important;
}
div.stButton > button:active { transform: translateY(0) !important; }

/* ── Result ── */
.sg-result {
    border-radius: 16px;
    padding: 1.5rem 1.6rem;
    margin-top: 1.6rem;
    display: flex;
    align-items: center;
    gap: 1.1rem;
    animation: rise 0.4s cubic-bezier(.22,.68,0,1.2) both;
}
@keyframes rise {
    from { opacity: 0; transform: translateY(14px) scale(0.97); }
    to   { opacity: 1; transform: translateY(0)   scale(1);    }
}
.sg-result.spam {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.25);
}
.sg-result.safe {
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.25);
}
.sg-result-icon { font-size: 2.4rem; flex-shrink: 0; }
.sg-result-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}
.sg-result.spam .sg-result-title { color: #F87171; }
.sg-result.safe .sg-result-title { color: #34D399; }
.sg-result-desc { font-size: 0.83rem; color: #4A5270; line-height: 1.5; }

/* ── Warning ── */
.sg-warn {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.25);
    border-radius: 12px;
    padding: 0.85rem 1.1rem;
    color: #FCD34D;
    font-size: 0.86rem;
    margin-top: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

/* ── Divider ── */
.sg-divider {
    border: none;
    border-top: 1px solid #141824;
    margin: 1.6rem 0 0;
}

/* ── Footer ── */
.sg-footer {
    text-align: center;
    color: #1E2538;
    font-size: 0.75rem;
    padding: 1.8rem 0 0.5rem;
    letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Hero
# ─────────────────────────────────────────────
st.markdown("""
<div class="sg-hero">
    <div class="sg-badge">🛡️</div>
    <div class="sg-title">SpamGuard</div>
    <div class="sg-sub">Intelligent email &amp; SMS spam detection</div>
</div>

<div class="sg-chips">
    <div class="sg-chip"><span>98.2%</span> Accuracy</div>
    <div class="sg-chip"><span>NLP</span> Powered</div>
    <div class="sg-chip"><span>&lt;1s</span> Detection</div>
    <div class="sg-chip"><span>TF-IDF</span> Vectorizer</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Input card
# ─────────────────────────────────────────────
st.markdown('<div class="sg-card"><div class="sg-field-label">✦ Paste your message</div>', unsafe_allow_html=True)

input_sms = st.text_area(
    label="",
    placeholder="Type or paste an email / SMS here to check if it's spam…",
    height=170,
    label_visibility="collapsed",
)

clicked = st.button("🔍  Analyse Message")
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Result
# ─────────────────────────────────────────────
if clicked:
    if input_sms.strip() == "":
        st.markdown("""
        <div class="sg-warn">⚠️&nbsp; Please enter a message before analysing.</div>
        """, unsafe_allow_html=True)
    else:
        transformed_sms = transform_text(input_sms)
        vector_input    = tfidf.transform([transformed_sms])
        result          = model.predict(vector_input)[0]
        word_count      = len(input_sms.split())
        char_count      = len(input_sms)

        if result == 1:
            st.markdown(f"""
            <div class="sg-result spam">
                <div class="sg-result-icon">🚨</div>
                <div>
                    <div class="sg-result-title">Spam Detected</div>
                    <div class="sg-result-desc">
                        This message contains spam indicators.<br>
                        {word_count} words &nbsp;·&nbsp; {char_count} characters analysed.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="sg-result safe">
                <div class="sg-result-icon">✅</div>
                <div>
                    <div class="sg-result-title">Looks Legitimate</div>
                    <div class="sg-result-desc">
                        No spam indicators found in this message.<br>
                        {word_count} words &nbsp;·&nbsp; {char_count} characters analysed.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Footer
# ─────────────────────────────────────────────
st.markdown("""
<hr class="sg-divider">
<div class="sg-footer">SPAMGUARD &nbsp;·&nbsp; NAIVE BAYES + TF-IDF &nbsp;·&nbsp; BUILT WITH STREAMLIT</div>
""", unsafe_allow_html=True)
