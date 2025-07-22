import streamlit as st
import os
from utils.ai_generator import generate_mcqs
from utils.file_parser import extract_text_from_pdf, extract_text_from_docx
from utils.exporter import export_to_json, export_to_pdf
from utils.session_manager import init_session, save_set, load_set, get_all_sets, delete_set
from dotenv import load_dotenv

# Load environment variables (e.g., Gemini API Key)
load_dotenv()

# Initialize session state variables
init_session()

# --- Configuration ---
st.set_page_config(
    page_title="QuizGenius - AI MCQ Generator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Function to load custom CSS
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Error: CSS file '{file_name}' not found. Please ensure it's in the 'assets' directory.")

# Load the main UI CSS (this will style Streamlit's native widgets)
load_css("assets/styles.css")

# --- Simplified Streamlit UI ---

st.title("QuizGenius - AI MCQ Generator")
st.write("Create, manage, and take multiple-choice quizzes effortlessly.")

# Main navigation tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "AI Generator", "Manual Entry", "Upload Doc", "Take Quiz", "Manage Sets", "Export"
])

with tab1:
    st.header("Generate MCQs from Text")
    st.write("Enter text below to generate multiple-choice questions using AI.")
    
    text_input = st.text_area("Enter your content here:", height=300, key="ai_text_input",
                              placeholder="Paste your learning material, notes, or article here...")
    
    num_questions = st.number_input(
        "Number of questions to generate:", min_value=1, max_value=20, value=5, key="num_q_ai_gen"
    )
    difficulty = st.selectbox(
        "Difficulty Level:", ["Easy", "Medium", "Hard"], key="difficulty_ai_gen"
    )
    category = st.text_input(
        "Category (optional):", key="category_ai_gen", placeholder="e.g., Science, History"
    )

    if st.button("Generate MCQs", key="generate_mcqs_btn"):
        if text_input:
            with st.spinner("Generating questions... This may take a moment."):
                mcqs = generate_mcqs(text_input, num_questions, difficulty, category)
                if mcqs:
                    st.session_state.current_mcqs = mcqs
                    st.success(f"Successfully generated {len(mcqs)} MCQs!")
                    st.markdown("---")
                    st.subheader("Generated Questions")
                    for i, q in enumerate(st.session_state.current_mcqs):
                        st.markdown(f"**{i+1}. {q['question']}**")
                        for opt_idx, opt in enumerate(q['options']):
                            st.write(f"    {chr(65 + opt_idx)}. {opt}")
                        st.write(f"    **Correct Answer:** {q['correct_answer']}")
                        st.write(f"    *Difficulty: {q['difficulty']} | Category: {q['category']}*")
                        st.markdown("---")
                else:
                    st.error("Failed to generate MCQs. Please try again with different text or check your API key.")
        else:
            st.warning("Please enter some text to generate MCQs.")

with tab2:
    st.header("Manually Create Questions")
    st.write("Add your own custom Multiple Choice Questions.")

    with st.form("manual_question_form"):
        question_text = st.text_input("Question Text:", placeholder="e.g., What is the capital of France?")
        options_text = st.text_area("Options (one per line):", placeholder="e.g.,\nParis\nLondon\nBerlin\nRome")
        correct_answer = st.text_input("Correct Answer:", placeholder="e.g., Paris (must match one of the options)")
        difficulty = st.selectbox("Difficulty Level:", ["Easy", "Medium", "Hard"])
        category = st.text_input("Category:", placeholder="e.g., Geography")
        
        submitted = st.form_submit_button("Add Question")
        
        if submitted:
            if question_text and options_text and correct_answer:
                options_list = [opt.strip() for opt in options_text.split('\n') if opt.strip()]
                if correct_answer in options_list:
                    new_question = {
                        "question": question_text,
                        "options": options_list,
                        "correct_answer": correct_answer,
                        "difficulty": difficulty,
                        "category": category
                    }
                    st.session_state.current_mcqs.append(new_question)
                    st.success("Question added successfully!")
                else:
                    st.error("Correct answer must be one of the provided options.")
            else:
                st.error("Please fill in all required fields.")
    
    st.markdown("---")
    st.subheader("Current Manual Questions")
    if st.session_state.current_mcqs:
        # Filter for questions that might have been manually added (no 'source' key from AI)
        manual_questions_only = [q for q in st.session_state.current_mcqs if 'source' not in q]
        if not manual_questions_only: # If no explicit source, show all current_mcqs
            manual_questions_only = st.session_state.current_mcqs

        if manual_questions_only:
            for i, q in enumerate(manual_questions_only):
                st.markdown(f"**{i+1}. {q['question']}**")
                for opt_idx, opt in enumerate(q['options']):
                    st.write(f"    {chr(65 + opt_idx)}. {opt}")
                st.write(f"    **Correct Answer:** {q['correct_answer']}")
                st.write(f"    *Difficulty: {q['difficulty']} | Category: {q['category']}*")
                st.markdown("---")
        else:
            st.info("No questions added manually yet.")
    else:
        st.info("No questions added manually yet.")

with tab3:
    st.header("Generate MCQs from Document Upload")
    st.write("Upload a PDF, DOCX, or TXT file to automatically generate MCQs.")

    uploaded_file = st.file_uploader(
        "Choose a file", type=["pdf", "docx", "txt"], key="doc_uploader"
    )

    num_questions_doc = st.number_input(
        "Number of questions to generate from document:", min_value=1, max_value=20, value=5, key="num_q_doc_gen"
    )
    difficulty_doc = st.selectbox(
        "Difficulty Level (Document):", ["Easy", "Medium", "Hard"], key="difficulty_doc_gen"
    )
    category_doc = st.text_input(
        "Category (optional, Document):", key="category_doc_gen", placeholder="e.g., Biology, Computer Science"
    )

    if st.button("Generate from Document", key="generate_doc_btn"):
        if uploaded_file is not None:
            file_type = uploaded_file.type
            extracted_text = ""
            
            with st.spinner("Extracting text from document..."):
                if "pdf" in file_type:
                    extracted_text = extract_text_from_pdf(uploaded_file)
                elif "docx" in file_type:
                    extracted_text = extract_text_from_docx(uploaded_file)
                elif "text" in file_type:
                    extracted_text = uploaded_file.read().decode("utf-8")
                else:
                    st.error("Unsupported file type. Please upload PDF, DOCX, or TXT.")
            
            if extracted_text:
                with st.spinner("Generating questions from document content..."):
                    mcqs = generate_mcqs(extracted_text, num_questions_doc, difficulty_doc, category_doc)
                    if mcqs:
                        st.session_state.current_mcqs = mcqs
                        st.success(f"Successfully generated {len(mcqs)} MCQs!")
                        st.markdown("---")
                        st.subheader("Generated Questions from Document")
                        for i, q in enumerate(st.session_state.current_mcqs):
                            st.markdown(f"**{i+1}. {q['question']}**")
                            for opt_idx, opt in enumerate(q['options']):
                                st.write(f"    {chr(65 + opt_idx)}. {opt}")
                            st.write(f"    **Correct Answer:** {q['correct_answer']}")
                            st.write(f"    *Difficulty: {q['difficulty']} | Category: {q['category']}*")
                            st.markdown("---")
                    else:
                        st.error("Failed to generate MCQs from document. Please check the document content or API key.")
            else:
                st.error("Could not extract text from the uploaded document.")
        else:
            st.warning("Please upload a document first.")

with tab4:
    st.header("Take a Quiz")
    st.write("Select a question set and test your knowledge!")

    if not st.session_state.current_quiz_questions:
        available_sets = get_all_sets()
        if available_sets:
            set_names = list(available_sets.keys())
            selected_set_name = st.selectbox("Choose a question set for the quiz:", ["-- Select a Set --"] + set_names, key="quiz_set_selector")

            if selected_set_name != "-- Select a Set --":
                questions_for_quiz = available_sets[selected_set_name]
                st.info(f"Selected set '{selected_set_name}' with {len(questions_for_quiz)} questions.")
                if st.button("Start Quiz", key="start_quiz_btn"):
                    st.session_state.current_quiz_questions = questions_for_quiz
                    st.session_state.quiz_answers = {q['question']: None for q in questions_for_quiz}
                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_score = 0
                    st.success("Quiz started!")
                    st.experimental_rerun()
        else:
            st.info("No saved question sets available. Generate or manually create questions and save them first!")
    
    if st.session_state.current_quiz_questions:
        st.markdown("---")
        st.subheader("Active Quiz")
        
        with st.form("quiz_form"):
            for i, q in enumerate(st.session_state.current_quiz_questions):
                st.markdown(f"<div class='quiz-question'>", unsafe_allow_html=True)
                st.markdown(f"**Question {i+1}: {q['question']}**")
                
                current_selection = st.session_state.quiz_answers.get(q['question'])
                try:
                    default_index = q['options'].index(current_selection) if current_selection else 0
                except ValueError:
                    default_index = 0

                selected_option = st.radio(
                    "Select your answer:",
                    options=q['options'],
                    key=f"quiz_q_{i}",
                    index=default_index
                )
                st.session_state.quiz_answers[q['question']] = selected_option
                st.markdown(f"</div>", unsafe_allow_html=True)

            quiz_submit_button = st.form_submit_button("Submit Quiz")

        if quiz_submit_button or st.session_state.quiz_submitted:
            st.session_state.quiz_submitted = True
            st.markdown("---")
            st.subheader("Quiz Results")
            score = 0
            total_questions = len(st.session_state.current_quiz_questions)

            for i, q in enumerate(st.session_state.current_quiz_questions):
                user_answer = st.session_state.quiz_answers.get(q['question'])
                is_correct = (user_answer == q['correct_answer'])

                if is_correct:
                    score += 1
                    st.success(f"✅ Question {i+1}: Correct! Your answer: '{user_answer}'")
                else:
                    st.error(f"❌ Question {i+1}: Incorrect. Your answer: '{user_answer}'. Correct answer: '{q['correct_answer']}'")
                st.markdown(f"**Question:** {q['question']}")
                st.markdown(f"**Options:** {', '.join(q['options'])}")
                st.markdown(f"**Your Answer:** {user_answer if user_answer else 'No answer'}")
                st.markdown(f"**Correct Answer:** {q['correct_answer']}")
                st.markdown("---")
            
            st.metric(label="Your Score", value=f"{score}/{total_questions}", delta=f"{round((score/total_questions)*100, 2) if total_questions > 0 else 0}%")
            
            if st.button("End Quiz", key="end_quiz_btn"):
                st.session_state.current_quiz_questions = []
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.session_state.quiz_score = 0
                st.experimental_rerun()

with tab5:
    st.header("Manage Saved Question Sets")
    st.write("Save the currently displayed questions or load/delete existing sets.")

    st.text_input("Enter a name to save current questions as a new set:", key="new_set_name", placeholder="e.g., 'Biology Chapter 5 Questions'")
    if st.button("Save Current Questions", key="save_current_btn"):
        if st.session_state.current_mcqs:
            save_set(st.session_state.new_set_name, st.session_state.current_mcqs)
            st.success(f"Set '{st.session_state.new_set_name}' saved!")
            st.session_state.new_set_name = ""
            st.experimental_rerun()
        else:
            st.warning("No questions in current session to save.")

    st.markdown("---")
    st.subheader("Your Saved Question Sets")
    saved_sets = get_all_sets()
    if saved_sets:
        for set_name, questions in saved_sets.items():
            st.expander(f"**{set_name}** ({len(questions)} questions)").write(questions)
            col_set1, col_set2 = st.columns(2)
            with col_set1:
                if st.button(f"Load '{set_name}'", key=f"load_set_{set_name}"):
                    st.session_state.current_mcqs = load_set(set_name)
                    st.success(f"Set '{set_name}' loaded into current session.")
                    st.experimental_rerun()
            with col_set2:
                if st.button(f"Delete '{set_name}'", key=f"delete_set_{set_name}"):
                    delete_set(set_name)
                    st.success(f"Set '{set_name}' deleted.")
                    st.experimental_rerun()
            st.markdown("---")
    else:
        st.info("No question sets saved yet.")

with tab6:
    st.header("Export Questions")
    st.write("Export the currently displayed questions to various formats.")

    if st.session_state.current_mcqs:
        st.info(f"You have {len(st.session_state.current_mcqs)} questions ready for export.")

        export_format = st.selectbox("Select Export Format:", ["JSON", "PDF"], key="export_format_selector")

        if export_format == "JSON":
            json_data = export_to_json(st.session_state.current_mcqs)
            st.download_button(
                label="Download Questions as JSON",
                data=json_data,
                file_name="mcq_questions.json",
                mime="application/json"
            )
        elif export_format == "PDF":
            #st.warning("PDF export functionality is under development. Please choose JSON for now.")
            # Add the download button for PDF
            pdf_bytes = export_to_pdf(st.session_state.current_mcqs)
            if pdf_bytes:
                st.download_button(
                    label="Download Questions as PDF",
                    data=pdf_bytes,
                    file_name="mcq_questions.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Failed to generate PDF. Please try again.")
    else:
        st.info("No questions available in the current session to export. Generate or create some first!")

# Simple Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #c89f93;'>&copy; 2024 QuizGenius. All rights reserved.</p>", unsafe_allow_html=True)
