import os
from transformers import RagTokenizer, RagTokenForGeneration
from datasets import load_dataset

dataset_path = '/Users/nurdiyanah/Desktop/chatbot' 

dataset = load_dataset(dataset_path, "")

model_name = 'facebook/rag-token-base'
tokenizer = RagTokenizer.from_pretrained(model_name)
model = RagTokenForGeneration.from_pretrained(model_name)
