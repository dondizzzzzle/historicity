# historicity

This is an open source module designed to perform the following tasks:
- scour your current working directory for appropriate file formats:
  - plaintext
  - PDFs
- analyse the above file formats in various ways
- plot or export your analysis in various formats
    
Attributes:
- `default`: Yields the user's default working directory.
- `english`: A list containing nearly every word in the English language.
- `stops`: A list containing every stopword / function word in the English language.
- `punctuation`: A string containing all ASCII punctuation characters.
- `scifi_list`: A list containing science fiction indexing terms. Good to use as a default.
    
Classes:
- `Extract`: extracts information from the specified directory
- `Analyze`: plots or exports analysis of the user's choice (not finished)
