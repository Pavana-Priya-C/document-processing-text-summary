import nltk 
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from summarizer import Summarizer
from transformers import BartForConditionalGeneration, BartTokenizer, T5ForConditionalGeneration, T5Tokenizer

nltk.download('punkt')

# Function to summarize text with Sumy (extractive)
def summarize_text_sumy(text, sentences_count=8):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentences_count)
    return " ".join([str(sentence) for sentence in summary])

# Function to summarize text using BERT Transformer
def summarize_text_bert(main_content):
    model = Summarizer('distilbert-base-uncased', hidden=[-1,-2], hidden_concat=True)
    summary = model(main_content, num_sentences=7)
    return summary

# Function to summarize text using BART Transformer
def summarize_text_bart(main_content):
    bart_model_name = "facebook/bart-large-cnn"
    bart_tokenizer = BartTokenizer.from_pretrained(bart_model_name)
    bart_model = BartForConditionalGeneration.from_pretrained(bart_model_name)

    bart_inputs = bart_tokenizer([main_content], max_length=1024, return_tensors='pt', truncation=True)
    bart_summary_ids = bart_model.generate(bart_inputs['input_ids'], max_length=250, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = bart_tokenizer.decode(bart_summary_ids[0], skip_special_tokens=True)
    return summary

# Function to summarize text using T5 Transformer (large)
def summarize_text_t5_large(main_content):
    t5_model_name = "t5-large"
    t5_tokenizer = T5Tokenizer.from_pretrained(t5_model_name)
    t5_model = T5ForConditionalGeneration.from_pretrained(t5_model_name)

    input_text = "summarize: " + main_content
    t5_inputs = t5_tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    t5_summary_ids = t5_model.generate(t5_inputs, max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = t5_tokenizer.decode(t5_summary_ids[0], skip_special_tokens=True)
    return summary

# Function to summarize text using T5 Transformer (base)
def summarize_text_t5_base(main_content):
    t5_base_model_name = "t5-base"
    t5_base_tokenizer = T5Tokenizer.from_pretrained(t5_base_model_name)
    t5_base_model = T5ForConditionalGeneration.from_pretrained(t5_base_model_name)

    base_input_text = "summarize: " + main_content
    t5_base_inputs = t5_base_tokenizer.encode(base_input_text, return_tensors="pt", max_length=512, truncation=True)
    t5_base_summary_ids = t5_base_model.generate(t5_base_inputs, max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = t5_base_tokenizer.decode(t5_base_summary_ids[0], skip_special_tokens=True)
    return summary
