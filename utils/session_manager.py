# utils/session_manager.py
import streamlit as st

def init_session():
    """Initializes all necessary session state variables."""
    if 'current_mcqs' not in st.session_state:
        st.session_state.current_mcqs = [] # Questions currently displayed/being worked on
    if 'saved_question_sets' not in st.session_state:
        st.session_state.saved_question_sets = {} # Dictionary to store saved sets
    if 'current_quiz_questions' not in st.session_state:
        st.session_state.current_quiz_questions = [] # Questions for the active quiz
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {} # User's answers for the active quiz
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False # Flag to check if quiz was submitted
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0 # Score for the current quiz


def save_set(set_name: str, questions: list):
    """Saves a list of questions as a named set in session state."""
    if set_name and questions:
        st.session_state.saved_question_sets[set_name] = questions
    else:
        st.error("Set name or questions cannot be empty.")

def load_set(set_name: str) -> list:
    """Loads a named question set from session state."""
    return st.session_state.saved_question_sets.get(set_name, [])

def delete_set(set_name: str):
    """Deletes a named question set from session state."""
    if set_name in st.session_state.saved_question_sets:
        del st.session_state.saved_question_sets[set_name]

def get_all_sets() -> dict:
    """Returns all saved question sets."""
    return st.session_state.saved_question_sets

