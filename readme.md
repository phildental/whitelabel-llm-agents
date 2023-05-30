# Ask Me Anything 🧞‍♂️

Ask Me Anything is a tool built with Streamlit, allowing users to ask questions about the content of PDF or CSV files. Users can upload a file, process it, and ask questions about the content. The answers are generated using an OpenAI-based model.

## Features

- File upload: Accepts PDF and CSV files.
- File processing: Extracts text from PDF files and transforms it into a query-able format. CSV processing is in the to-do list.
- Text chunking: Splits text into chunks for efficient processing.
- Text embeddings: Transforms text into OpenAI embeddings.
- Question answering: Answers user queries using a trained OpenAI model.

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

The project requires Python 3.7 or later, and the following Python libraries:

- streamlit
- numpy
- pandas
- python-dotenv
- PyPDF2
- langchain (including the required modules)
- OpenAI
- FAISS
- pickle
- os
- tempfile

You can install the dependencies with:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

Note: This project uses the OpenAI API for text embeddings and question answering, so you will need an API key. You can obtain a key by signing up on the [OpenAI website](https://www.openai.com/).

### Running the App
First, clone the repository:

\`\`\`bash
git clone https://github.com/yourusername/ask-me-anything.git
cd ask-me-anything
\`\`\`

Then, run the Streamlit app:

\`\`\`bash
streamlit run main.py
\`\`\`

This will open a web browser window. You can upload a file, process it, and start asking questions about the content!

### Usage

- Click "Browse files" to upload a PDF or CSV file.
- Click "Process and Store as Pickle" to process the file and store it in a pickle format.
- Ask questions about the content of the file in the "Ask me a question" text field.

### Author

phildental

### Acknowledgments

- OpenAI for providing the amazing GPT model.
- Streamlit for making web app creation a breeze for data scientists.

### Contributing

We welcome contributions to improve this project. You can get in touch with us via contact details provided in the Contact section.

Remember to follow good code of conduct and respect everyone in your communications. Happy coding!

Please note that the README.md was last updated on 30 May 2023.

### Disclaimer

This tool is not intended to provide perfect answers to all questions. The performance largely depends on the quality of the data in the uploaded files and the OpenAI model's capability. Use it responsibly.

\`\`\`bash
git clone https://github.com/yourusername/ask-me-anything.git
cd ask-me-anything
\`\`\` 