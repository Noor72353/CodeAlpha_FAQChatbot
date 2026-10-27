import re
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# FAQ KNOWLEDGE BASE
# --------------------------------------------------
faqs = [
    {
        "question": "What is your name?",
        "answer": "I am FAQ Bot, a chatbot designed to answer frequently asked questions.",
        "keywords": ["name", "who are you", "your identity"]
    },
    {
        "question": "What can you do?",
        "answer": "I can answer common questions about courses, admissions, fees, contact details, scholarships, and technical support.",
        "keywords": ["help", "capabilities", "functions", "features"]
    },
    {
        "question": "What courses do you offer?",
        "answer": "We offer example courses in computer science, programming, web development, artificial intelligence, and data science.",
        "keywords": ["course", "courses", "program", "programs", "subjects", "study"]
    },
    {
        "question": "How can I apply for admission?",
        "answer": "You can apply by completing the online application form and submitting the required academic documents.",
        "keywords": ["apply", "application", "admission", "enroll", "enrollment"]
    },
    {
        "question": "What are the admission requirements?",
        "answer": "Admission requirements depend on the program. Generally, applicants need the relevant previous academic qualifications and supporting documents.",
        "keywords": ["requirements", "eligibility", "eligible", "qualifications", "documents"]
    },
    {
        "question": "How much are the course fees?",
        "answer": "Course fees depend on the selected program. Please contact the administration for the latest fee details.",
        "keywords": ["fee", "fees", "tuition", "cost", "price", "payment"]
    },
    {
        "question": "Do you offer scholarships?",
        "answer": "Scholarships may be available for eligible students. Contact the administration to learn about current opportunities and eligibility criteria.",
        "keywords": ["scholarship", "scholarships", "financial aid", "funding"]
    },
    {
        "question": "How can I contact support?",
        "answer": "You can contact the support team through the organization's official contact page or email address.",
        "keywords": ["contact", "support", "email", "phone", "help desk"]
    },
    {
        "question": "What are your office hours?",
        "answer": "Office hours depend on the organization. Please check its official website for the current schedule.",
        "keywords": ["hours", "opening", "closing", "working hours", "office"]
    },
    {
        "question": "Thank you",
        "answer": "You're welcome! Feel free to ask another question.",
        "keywords": ["thanks", "thank you", "appreciate"]
    },
    {
        "question": "Goodbye",
        "answer": "Goodbye! Have a great day.",
        "keywords": ["bye", "goodbye", "see you"]
    }
]


# --------------------------------------------------
# PREPARE THE NLP MODEL
# --------------------------------------------------
questions = [faq["question"] for faq in faqs]

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2),
    sublinear_tf=True
)

question_vectors = vectorizer.fit_transform(questions)


# --------------------------------------------------
# QUESTION MATCHING
# --------------------------------------------------
def get_answer(user_question):
    """Return the most relevant FAQ answer or a fallback response."""

    cleaned_question = re.sub(r"\s+", " ", user_question).strip()
    normalized = cleaned_question.lower()
    normalized = re.sub(r"[^\w\s]", "", normalized).strip()

    fallback = (
        "Sorry, I couldn't find a suitable answer in my FAQ knowledge base. "
        "Please ask about courses, admissions, fees, scholarships, "
        "office hours, or support."
    )

    if not normalized:
        return "Please enter a question so I can help you.", 0.0

    # Handle greetings directly.
    greetings = {
        "hi", "hello", "hey", "hi there", "hello there",
        "good morning", "good afternoon", "good evening"
    }

    if normalized in greetings:
        return (
            "Hello! How can I help you today? You can ask me about "
            "courses, admissions, fees, scholarships, or support.",
            1.0
        )

    # Handle simple farewells.
    farewells = {"bye", "goodbye", "see you", "see you later"}

    if normalized in farewells:
        return "Goodbye! Have a great day.", 1.0

    # Handle common social phrases.
    if normalized in {"thanks", "thank you", "thanks a lot"}:
        return faqs[9]["answer"], 1.0

    # Detect questions that are clearly outside the FAQ scope.
    unrelated_topics = [
        "weather", "football", "soccer", "cricket", "basketball",
        "stock market", "celebrity", "president", "news today",
        "politics", "recipe", "movie", "music", "traffic"
    ]

    if any(topic in normalized for topic in unrelated_topics):
        return fallback, 0.0

    # Match important FAQ topics and their alternative wording.
    topic_rules = [
        (
            ["scholarship", "scholarships", "financial aid", "funding"],
            6
        ),
        (
            ["course", "courses", "programming", "web development",
             "artificial intelligence", "data science", "computer science"],
            2
        ),
        (
            ["fee", "fees", "tuition", "cost", "price", "payment"],
            5
        ),
        (
            ["support", "contact", "email address", "phone number", "help desk"],
            7
        ),
        (
            ["office hours", "working hours", "opening hours", "closing hours"],
            8
        )
    ]

    for keywords, faq_index in topic_rules:
        if any(keyword in normalized for keyword in keywords):
            return faqs[faq_index]["answer"], 1.0

    # Distinguish admission application questions from requirements questions.
    admission_terms = [
        "admission", "apply", "application", "enroll", "enrollment"
    ]
    requirement_terms = [
        "requirement", "requirements", "eligibility", "eligible",
        "qualification", "qualifications", "documents needed"
    ]

    if any(term in normalized for term in admission_terms):
        if any(term in normalized for term in requirement_terms):
            return faqs[4]["answer"], 1.0
        return faqs[3]["answer"], 1.0

    # Handle identity and capability questions.
    if (
        normalized in {"name", "your name", "what is your name"}
        or "who are you" in normalized
    ):
        return faqs[0]["answer"], 1.0

    if any(term in normalized for term in [
        "what can you do", "how can you help", "your capabilities"
    ]):
        return faqs[1]["answer"], 1.0

    # Use TF-IDF and cosine similarity for remaining questions.
    user_vector = vectorizer.transform([cleaned_question])
    similarities = cosine_similarity(
        user_vector, question_vectors
    )[0]

    best_index = int(similarities.argmax())
    best_score = float(similarities[best_index])

    # Require a stronger match to reduce unrelated answers.
    if best_score < 0.30:
        return fallback, best_score

    return faqs[best_index]["answer"], best_score


# --------------------------------------------------
# STREAMLIT USER INTERFACE
# --------------------------------------------------
st.set_page_config(
    page_title="FAQ Chatbot",
    page_icon="💬",
    layout="centered"
)

st.title("💬 FAQ Chatbot")

st.write(
    "Welcome! Ask me about courses, admissions, fees, "
    "scholarships, office hours, or support."
)

with st.sidebar:
    st.header("About this chatbot")
    st.write(
        "This chatbot uses Natural Language Processing (NLP), "
        "TF-IDF, and cosine similarity to identify relevant FAQ answers."
    )
    st.caption("Built with Python, scikit-learn, and Streamlit.")

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()


if "messages" not in st.session_state:
    st.session_state.messages = []


# Display conversation history.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Accept and answer new questions.
user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    answer, score = get_answer(user_input)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.markdown(answer)
