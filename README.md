# Detecting Stance in Media on Global Warming for Indic Languages

A multilingual Natural Language Processing (NLP) project that aims to identify people's stance toward global warming and climate change from online media comments, particularly Hindi and Bengali YouTube comments.

The system classifies a given sentence into one of three categories:

- **Favour** – The author supports the claim that climate change and global warming are serious concerns.
- **Against** – The author disagrees with or rejects the claim.
- **None** – The sentence does not express a clear position toward the claim.

The project also includes a locally hosted web application where users can enter a sentence and receive a predicted stance.

---

## 1. Problem Statement

Social media platforms contain large amounts of public discussion about climate change and global warming. Understanding public opinion from these discussions is challenging because comments can contain different languages, informal expressions, spelling variations, and regional language patterns.

This project focuses on detecting stance in Hindi and Bengali media discussions, including Romanized forms of Indic languages.

The main objective is to develop a multilingual stance classification system that can distinguish support, opposition, and neutral or unclear positions toward the following claim:

**"Climate change and global warming is a serious concern."**

---

## 2. Objectives

- Collect relevant public YouTube comments related to climate change and global warming.
- Identify and process Hindi, Bengali, Hinglish, and Romanized Indic language comments.
- Prepare a labelled dataset for stance classification.
- Develop and evaluate machine learning models.
- Compare traditional machine learning approaches with multilingual transformer-based models.
- Build a locally hosted interface for sentence-level stance prediction.
- Create a reusable foundation for training models with additional validated datasets.

---

## 3. Supported Languages

The project focuses on:

| Language | Description |
|---|---|
| Hindi | Hindi written in Devanagari |
| Hindi Romanized | Hindi written using the Latin alphabet |
| Bengali | Bengali written in Bengali script |
| Bengali Romanized | Bengali written using the Latin alphabet |
| Hinglish | Combination of Hindi and English |

English comments may also appear during data collection and language identification, but the primary target is Indic-language stance classification.

---

## 4. Stance Categories

| Label | Meaning | Example |
|---|---|---|
| Favour | Supports the seriousness of global warming | "Global warming is a serious threat and we need immediate action." |
| Against | Rejects or downplays the seriousness of global warming | "Global warming is exaggerated and is not a serious threat." |
| None | No clear stance toward the claim | "I watched this documentary yesterday." |

**Important:** Sentiment and stance are different concepts. A negative comment is not automatically Against, and a positive comment is not automatically Favour. Classification must consider the author's position toward the target claim.

---

## 5. Dataset

The project uses YouTube comments collected through the YouTube Data API.

### Data collection

- Comments are collected from videos related to climate change and global warming.
- Multiple collection rounds are maintained separately.
- Language identification and relevance filtering are performed before preparing the final dataset.
- Comments are labelled according to their stance toward the target claim.

### Current dataset

The current prepared dataset contains:

| Attribute | Value |
|---|---:|
| Total labelled comments | 202 |
| Hindi | 89 |
| Hindi Romanized | 83 |
| Bengali | 21 |
| Bengali Romanized | 7 |
| Hinglish | 2 |

### Stance distribution

| Stance | Records |
|---|---:|
| Favour | 158 |
| Against | 11 |
| None | 33 |

The dataset is imbalanced, with considerably fewer Against examples. This is an important limitation when interpreting model performance.

An additional Hindi-Bengali corpus containing 1,085 records has been examined as supplementary material. It is not included in the current stance training dataset because its labels are pending and much of its content does not express a stance toward the target claim.

---

## 6. NLP Concepts and Techniques

The project uses the following NLP and machine learning concepts:

### Text preprocessing
Preparing raw text for classification and handling language-specific variations.

### Language identification
Identifying the language and script of collected comments.

### TF-IDF (Term Frequency-Inverse Document Frequency)
Converting text into numerical feature representations based on the importance of words.

### Word n-grams
Capturing individual words and sequences of words to identify useful textual patterns.

### Character n-grams
Capturing character-level patterns, spelling variations, and informal Romanized language.

### Feature extraction
Transforming textual input into numerical representations that machine learning models can process.

### Multilingual NLP
Working with text across multiple languages and writing systems.

### Transfer learning
Using knowledge learned by a pretrained language model and adapting it to a specific classification task.

### Fine-tuning
Training a pretrained model on labelled stance data to adapt it to the project's classification objective.

### Class imbalance handling
Using class weighting to reduce the impact of unequal class distributions.

### Group-based cross-validation
Keeping comments from the same YouTube video together when splitting data to reduce data leakage.

---

## 7. Machine Learning Models

### 7.1 Logistic Regression — Implemented

The initial baseline model uses Logistic Regression with TF-IDF features.

Feature extraction includes:

- Word n-grams: 1–2
- Character n-grams: 2–5
- FeatureUnion to combine both feature representations
- Balanced class weights

The model is evaluated using five-fold Stratified Group Cross-Validation, with YouTube video IDs used as groups.

### 7.2 Linear Support Vector Machine — Proposed

LinearSVC is considered as an alternative traditional machine learning classifier.

It can work effectively with high-dimensional sparse TF-IDF representations and will be evaluated against the Logistic Regression baseline.

### 7.3 XLM-RoBERTa — Planned

XLM-RoBERTa is the planned multilingual transformer model.

It uses the Transformer architecture and multilingual pretraining to capture contextual information across languages.

The intended approach is to fine-tune the pretrained model for the three-class stance classification task.

Its performance will be compared with the traditional machine learning baseline.

**Note:** XLM-RoBERTa is a planned experiment, not a completed model in the current implementation.

---

## 8. Model Evaluation

The primary evaluation metric is **Macro F1-score** because the dataset has an imbalanced class distribution.

The evaluation includes:

- Accuracy
- Precision
- Recall
- Macro F1-score
- Weighted F1-score
- Balanced Accuracy
- Matthews Correlation Coefficient (MCC)
- Cohen's Kappa
- Classification Report
- Confusion Matrix

### Current baseline results

The Logistic Regression baseline produced the following results:

| Metric | Result |
|---|---:|
| Mean cross-validation accuracy | 73.71% |
| Mean cross-validation Macro F1 | 0.3014 |

The out-of-fold classification report showed that the model performs substantially better on Favour than on Against and None.

This indicates that the current dataset size and class imbalance limit the baseline model's ability to distinguish all three classes.

Further experiments are required before considering the classifier reliable.

---

## 9. Local Web Application

The project includes a locally hosted web application built using Streamlit.

The application allows users to:

1. Open the application in a web browser.
2. Select the language of the input sentence.
3. Enter a sentence.
4. Submit the sentence for prediction.
5. View the predicted stance.

The application loads the trained machine learning model from the `models/` directory.

### Run the application

Activate the Python virtual environment:

```bash
source lid-env/bin/activate
```

Run:

```bash
streamlit run app.py
```

Open the following address in your browser:

```text
http://localhost:8501
```

The current application uses the Logistic Regression baseline model. Its predictions should be treated as experimental because of the model's limited performance.

---

## 10. Project Structure

```text
climate-stance-nlp/
│
├── app.py
│
├── scripts/
│   ├── collect_comments.py
│   ├── collect_comments_round2.py
│   ├── analyze_scripts.py
│   ├── prepare_language_review.py
│   ├── analyze_video_quality.py
│   ├── prepare_round2_review.py
│   ├── prepare_final_dataset.py
│   ├── train_baseline.py
│   ├── train_svm.py
│   └── evaluate_model.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── final/
│       ├── climate_stance_dataset.csv
│       ├── baseline_oof_predictions.csv
│       └── baseline_fold_results.csv
│
├── models/
│   └── baseline_tfidf_logreg.joblib
│
├── reports/
│   └── evaluation/
│
├── lid-env/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

*The structure shows the main project organization. Some files and folders are created as different stages of the pipeline are executed.*

---

## 11. Technologies and Libraries

| Technology | Purpose |
|---|---|
| Python 3.12 | Main programming language |
| Pandas | Dataset handling and manipulation |
| NumPy | Numerical operations |
| Scikit-learn | Machine learning, feature extraction and evaluation |
| Joblib | Saving and loading trained models |
| Streamlit | Local web application |
| FastText | Language identification support |
| MIRA-IndicLID | Indic language identification experiments |
| Google YouTube Data API v3 | YouTube comment collection |
| python-dotenv | Environment variable management |
| PyTorch | Planned transformer model training |
| Hugging Face Transformers | Planned XLM-RoBERTa implementation |

---

## 12. Requirements

### Software requirements

- Python 3.10 or newer (Python 3.12 used during development).
- pip package manager.
- Git.
- Internet connection for initial package installation and YouTube API data collection.
- A modern web browser.
- NVIDIA GPU with compatible CUDA support is recommended for transformer fine-tuning, but is not mandatory for the current TF-IDF baseline.

### Python dependencies

The current baseline and application require:

```text
pandas
numpy
scikit-learn
joblib
streamlit
python-dotenv
google-api-python-client
fasttext-wheel
huggingface-hub
```

For the planned XLM-RoBERTa experiment, additional dependencies will be needed:

```text
torch
transformers
accelerate
```

The transformer dependencies are for the planned upgrade and are not required to run the current Logistic Regression application.

### Environment setup

Create and activate a virtual environment:

```bash
python3 -m venv lid-env
source lid-env/bin/activate
```

Install the current dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install pandas numpy scikit-learn joblib streamlit python-dotenv google-api-python-client fasttext-wheel huggingface-hub
```

For YouTube data collection, create a `.env` file in the project root:

```env
YOUTUBE_API_KEY=your_youtube_api_key
```

Do not commit `.env` or expose API credentials publicly.

---

## 13. Training and Evaluation

### Train the Logistic Regression baseline

```bash
python scripts/train_baseline.py
```

This script performs feature extraction, grouped cross-validation, model evaluation, and saves the trained baseline model and out-of-fold predictions.

### Evaluate saved predictions

```bash
python scripts/evaluate_model.py \
  --true-column stance \
  --pred-column predicted_stance
```

The evaluation script generates overall metrics, a classification report, and a confusion matrix.

Reports are saved under:

```text
reports/evaluation/
```

The exact prediction column names must match the input CSV. The command above assumes the current baseline prediction file uses `stance` and `predicted_stance`.

---

## 14. Limitations

- The current labelled dataset is relatively small.
- The stance labels are imbalanced, particularly for the Against class.
- Romanized Hindi and Bengali can have inconsistent spelling and informal expressions.
- The current baseline relies on word and character patterns rather than deep contextual understanding.
- Comments from a limited number of videos may not represent the broader public.
- Predictions should not be treated as definitive measurements of public opinion.
- Transformer-based improvements still need to be trained and evaluated.

---

## 15. Future Scope

- Fine-tune XLM-RoBERTa for multilingual stance classification.
- Compare Logistic Regression, LinearSVC, and XLM-RoBERTa using the same evaluation strategy.
- Improve minority-class recognition.
- Support additional Indic languages.
- Develop a reusable training pipeline for validated external datasets.
- Improve prediction explanations and application usability.
- Expand the dataset with more diverse and reliable stance-labelled examples.

---

## 16. Conclusion

This project explores multilingual stance detection for climate change and global warming discussions in Indic languages.

It combines traditional NLP techniques, machine learning, multilingual language processing, and a locally hosted prediction interface.

The Logistic Regression baseline establishes an initial working system. Further experimentation with multilingual transformer models such as XLM-RoBERTa will help evaluate whether contextual language representations can improve stance classification across Hindi and Bengali text.