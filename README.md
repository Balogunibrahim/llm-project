# llm-project — Building a Text Tokenizer from Scratch

My first hands-on project exploring how large language models work under the hood. Instead of using a ready-made library, this project builds a simple text tokenizer from scratch in Python — the first step in how an LLM turns raw text into something a model can learn from.

## What it does

The script takes a real document (a PDF), breaks its text down into tokens, builds a vocabulary, and converts text into numerical IDs and back again. It reads a PDF with pdfplumber to extract the text from a source document (wharton_verdict.pdf). It tokenizes that text using regular expressions to split it into words and punctuation. It then builds a vocabulary by creating a sorted list of every unique token and mapping each one to a unique integer ID. Two tokenizer classes encode text into token IDs and reconstruct the original text from those IDs. The second tokenizer also handles special tokens — an end-of-text marker and an unknown-word token — the same techniques used in real LLM pipelines.

## Why I built it

I wanted to understand what actually happens before text reaches a language model, not just call an API. Building the tokenizer by hand taught me how vocabularies, token IDs, and special tokens work, and gave me a foundation for going deeper into natural language processing and AI.

## Tech

Python, with pdfplumber for PDF text extraction and the re module (regular expressions) for tokenization.

## Run it

Install the dependency with pip install pdfplumber. Update the PDF path near the top of llm.py to point to your file (for example, wharton_verdict.pdf). Then run the script with python llm.py. It prints the total character count, a sample of the extracted tokens, the vocabulary size, and an example of text being encoded to token IDs and decoded back to text.

## What's next

Extend the tokenizer toward byte-pair encoding (BPE), the approach used by modern LLMs, and move from tokenization into building and training a small language model.

A learning project — built to understand LLM fundamentals from the ground up.
