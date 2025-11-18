# Import the pdfplumber library (used for reading PDF files)
import pdfplumber

# The 're' library (regular expressions) allows us to search, match, 
# and extract patterns from text. 
# We import it so we can tokenize the text (split it into words, 
# punctuation, or sentences) using flexible pattern matching.
import re

# Set the path to your PDF file
# Make sure the file is actually in your Downloads folder
path = "/Users/admin/Downloads/Wharton_verdict.pdf"
# Open the PDF file using pdfplumber
with pdfplumber.open(path) as pdf:

    # Extract text from each page and join them into one long string
    # page.extract_text() pulls out the text on each page
    # or "" avoids errors if a page has no text
    raw_text = "".join(page.extract_text() or "" for page in pdf.pages)

# Print the total number of characters in the extracted text
print("Total characters:", len(raw_text))

#This command prints the first 100 characters of this file for illustration purpose
print(raw_text[:99])

# We use re.split to break the text into tokens based on a pattern.
# The pattern r'([,.:;"()\']|--|\s)' means:
#   - [,.:;"()'] → split on punctuation marks (commas, periods, quotes, parentheses, etc.)
#   - --         → split on double dashes
#   - \s         → split on any whitespace (space, tab, newline)
# The parentheses (...) tell Python to KEEP the punctuation as separate tokens.
preprocessed = re.split(r'([,.:;"()\']|--|\s)', raw_text)

# We clean the list by removing empty strings or pure whitespace.
# item.strip() removes surrounding spaces.
# We only keep items where strip() is not empty.
preprocessed = [item.strip() for item in preprocessed if item.strip()]

# Show the first 30 processed tokens
print(preprocessed[:30])

# Show total numbers of token
print(len(preprocessed))

# Convert the list of tokens (preprocessed) into a set.
# A set automatically removes duplicates, so we get only UNIQUE words.
# Then we sort the set alphabetically to create an ordered vocabulary list.
all_words = sorted(set(preprocessed))

# Count how many unique words are in the vocabulary.
vocab_size = len(all_words)

# Print the size of the vocabulary (number of unique words)
print(vocab_size)

# Create a vocabulary dictionary where:
#   - each UNIQUE token (word) is the key
#   - each token gets assigned a unique integer ID
# enumerate(all_words) gives pairs like: (0, 'a'), (1, 'apple'), (2, 'book'), ...
# The dictionary comprehension flips it to: {'a': 0, 'apple': 1, 'book': 2, ...}
vocab = {token: integer for integer, token in enumerate(all_words) }

# --- SIMPLE TOKENIZER CLASS ---
class SimpleTokenizerV1:
    def __init__(self, vocab):
        # str_to_int: maps words to integers
        self.str_to_int = vocab
        # int_to_str: reverse mapping (integer → word)
        # Needed for decoding
        self.int_to_str = {i:s for s, i in vocab.items()}
    

    def encode(self, text):
        # Split the input text into tokens using a regex pattern.
        # This pattern separates words from punctuation and whitespace.
        preprocessed = re.split(r'([,.:;"()\']|--|\s)', text)
        
        # Remove empty strings and stray spaces from the token list.
        # `strip()` cleans each token, and the condition filters out empty items.
        preprocessed = [ item.strip() for item in preprocessed if item.strip()]

        # Convert each cleaned token into its corresponding integer ID
        # using the vocabulary mapping (string → integer).
        ids = [self.str_to_int[s] for s in preprocessed]

        # Return the list of integer token IDs.
        return ids
    
    def decoder(self, ids):
        # Convert each integer ID back into its corresponding token (word/punctuation)
        # Then join all tokens into a single string separated by spaces.
        text = " ".join([self.int_to_str[i] for i in ids])
         
         # Fix spacing before punctuation.
        # The regex finds spaces before punctuation marks and removes them.
        text = re.sub(r'\s+([,.?!"()\'])', r'\1', text)
        
        # Return the cleaned, human-readable text.
        return text
# 1. Create a sorted list of UNIQUE tokens extracted from the text
# Using set() removes duplicates, sorted() ensures consistent ordering
all_tokens = sorted(list(set(preprocessed)))

# 2. Add special tokens used by LLMs
# <|endoftext|> → marks the end of a message/document
# <|unk|> → represents unknown/rare words not seen during training
all_tokens.extend(["<|endoftext|>", "<|unk|>"])

# 3. Build the vocabulary dictionary
# Maps each token to a unique integer ID using enumerate()
vocab = {token: integer for integer, token in enumerate(all_tokens)}
new_len= len(vocab.items())
print(new_len)

for i, item in enumerate(list (vocab.items())[-5:]):
    print(item)

class SimpleTokenizerV2:
    def __init__(self, vocab):
        # vocab is a dictionary mapping: token → integer ID
        self.str_to_int = vocab
        # Reverse dictionary: integer ID → token
        # This allows decoding (IDs back to text)
        self.int_to_str = { i:s for s,i in vocab.items()}
    
    def encode(self, text):
        # Split input text into words and punctuation using regex
        # The regex separates punctuation marks, symbols, and whitespace
        preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', text)

        # Remove extra spaces and empty strings
        preprocessed = [item.strip() for item in preprocessed if item.strip()]
        
        # Replace any token that is not in the vocabulary with <|unk|>
        # This prevents KeyError when the model sees new/unknown words
        preprocessed = [
            item if item in self.str_to_int 
            else "<|unk|>" for item in preprocessed
        ]
       
        # Convert tokens to their corresponding integer IDs
        ids = [self.str_to_int[s] for s in preprocessed]
        
        # Return encoded list of token IDs
        return ids
        
    def decode(self, ids):
        text = " ".join([self.int_to_str[i] for i in ids])
        # Replace spaces before the specified punctuations
        text = re.sub(r'\s+([,.:;?!"()\'])', r'\1', text)
        return text

tokenizer = SimpleTokenizerV2(vocab)
text1 = "Hello, do you like tea?"
text2 = "In the sunlit terraces of the palace"
text = "<|endoftext|> ".join((text1, text2))

print(text)

sample = tokenizer.encode(text)
print(sample)

sample1 = tokenizer.decode(tokenizer.encode(text))
print(sample1)

"""tokenizer = SimpleTokenizerV1(vocab)

text = It's the last he painted, you know,Mrs. Gisburn said with pardonable pride
ids = tokenizer.encode(text)
print(ids)

decoded_text = tokenizer.decoder(ids)
print(decoded_text)

text = "balogun Ibrahim"
print(tokenizer.encode(text))"""