# 📩 End-to-End Spam Detection System

This is a **college project** that implements an end-to-end Machine Learning system to **detect and classify spam emails/SMS messages**.

The system is designed to accurately identify spam while minimizing false positives using NLP techniques and a trained ML model.

---

## 🚀 Features

- Spam vs Not Spam classification
- Text preprocessing using NLP techniques
- Interactive web app using Streamlit
- Fast predictions using trained model
- Lightweight and easy to deploy

---

## 🛠️ Technologies & Modules Used

### 1. Streamlit
An open-source Python library used to create and deploy interactive web applications for machine learning and data science projects.

### 2. Pickle
Used for **serializing and deserializing** machine learning models (saving and loading trained models).

### 3. String
Provides utility functions for text processing and manipulation.

### 4. NLTK (Natural Language Toolkit)
A powerful Python library used for:
- Tokenization
- Stopword removal
- Text preprocessing

---

## ⚙️ How It Works

1. Input message is taken from the user
2. Text is preprocessed:
   - Lowercasing
   - Tokenization
   - Stopword removal
   - Stemming
3. Text is converted into numerical form using TF-IDF
4. Trained ML model predicts whether the message is:
   - 🚨 Spam
   - ✅ Not Spam

---

## ▶️ How to Run the Project

1. Clone the repository:
```bash
git clone <https://github.com/sd45saswat/End-To-End-Spam-Detection-.git>