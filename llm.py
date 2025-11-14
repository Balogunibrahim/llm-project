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