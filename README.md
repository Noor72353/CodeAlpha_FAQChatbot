# FAQ Chatbot Using NLP

## Project Overview

This project is an interactive FAQ chatbot developed using Python, Natural Language Processing (NLP), scikit-learn, and Streamlit. It answers frequently asked questions by matching user queries with a predefined FAQ knowledge base.

The chatbot can respond to questions about courses, admissions, admission requirements, fees, scholarships, office hours, and technical support. It also handles common greetings and provides a fallback response when it cannot find a suitable answer.

## Features

- Interactive chat interface built with Streamlit.
- FAQ knowledge base containing predefined questions and answers.
- Text preprocessing and normalization.
- TF-IDF vectorization for converting text into numerical features.
- Cosine similarity for matching user questions with FAQ questions.
- Topic-based matching for common questions and alternative wording.
- Fallback responses for unsupported or unrelated questions.
- Conversation history during the session.
- Option to clear the conversation.

## Technologies Used

- **Python** — Core programming language.
- **Natural Language Processing (NLP)** — Processing and matching user questions.
- **scikit-learn** — TF-IDF vectorization and cosine similarity.
- **Streamlit** — Interactive web-based chatbot interface.

## How It Works

1. The chatbot loads a predefined FAQ knowledge base.
2. TF-IDF converts the FAQ questions into numerical vectors.
3. The user enters a question through the chat interface.
4. The chatbot normalizes the input and checks for common greetings, topic keywords, and known question patterns.
5. If no rule matches, cosine similarity compares the user's question with the FAQ questions.
6. The chatbot returns the most relevant answer when the similarity score meets the configured threshold.
7. If no suitable match is found, the chatbot displays a fallback response.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Noor72353/CodeAlpha_FAQChatbot.git
cd CodeAlpha_FAQChatbot
```

### 2. Create a virtual environment

```bash
py -3.13 -m venv venv
```

### 3. Activate the virtual environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install scikit-learn streamlit
```

### 5. Run the chatbot

```bash
streamlit run app.py
```

Streamlit will provide a local URL, usually `http://localhost:8501`, where you can interact with the chatbot in your browser.

## Example Questions

Try asking:

- Hello!
- What is your name?
- What courses do you offer?
- How can I apply for admission?
- What are the admission requirements?
- How much are the course fees?
- Do you offer scholarships?
- How can I contact support?
- What are your office hours?
- What is the weather today?

The chatbot responds to supported questions and provides a fallback message for unrelated topics.

## Project Structure

```text
CodeAlpha_FAQChatbot/
├── app.py
├── README.md
├── .gitignore
└── venv/
```

The virtual environment should not be uploaded to GitHub. The `.gitignore` file should exclude it.

## Limitations

- The chatbot uses a predefined FAQ knowledge base rather than a large language model.
- It cannot reliably answer questions that are not covered by its stored information.
- The responses are general examples and should be customized for a real organization.
- Its matching ability depends on the FAQ content and the text-matching rules.

## Future Improvements

- Add more FAQs and organization-specific information.
- Improve handling of spelling mistakes and varied sentence structures.
- Add support for storing FAQs in a database or external file.
- Include automated tests for different question types.
- Deploy the chatbot online for public access.

## Author

Developed as a Python and NLP project for the CodeAlpha internship.

## License

This project is intended for educational and learning purposes.
