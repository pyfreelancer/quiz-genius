# utils/exporter.py
import json
import io
import streamlit as st # For st.warning/error

from fpdf import FPDF # Uncommented for PDF export

def export_to_json(questions: list) -> str:
    """Exports a list of questions to a JSON string."""
    try:
        return json.dumps(questions, indent=4)
    except Exception as e:
        st.error(f"Error exporting to JSON: {e}")
        return "{}"

def export_to_pdf(questions: list) -> bytes:
    """
    Exports a list of questions to a PDF byte stream using FPDF.
    """
    try:
        pdf = FPDF()
        # FIX: Change 'auto_page_break' to 'auto'
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.multi_cell(0, 10, "QuizGenius - Generated MCQs", align='C')
        pdf.ln(10) # Add some space

        for i, q in enumerate(questions):
            # Question
            pdf.set_font("Arial", "B", 12) # Bold for question
            pdf.multi_cell(0, 8, f"{i+1}. {q['question']}")
            pdf.ln(2)

            # Options
            pdf.set_font("Arial", size=10) # Regular for options
            for opt_idx, opt in enumerate(q['options']):
                pdf.multi_cell(0, 6, f"    {chr(65 + opt_idx)}. {opt}")
            pdf.ln(2)

            # Correct Answer & Details
            pdf.set_font("Arial", "I", 10) # Italic for details
            pdf.multi_cell(0, 6, f"    Correct Answer: {q['correct_answer']}")
            pdf.multi_cell(0, 6, f"    Difficulty: {q['difficulty']} | Category: {q['category']}")
            pdf.ln(8) # Space after each question

        # Output the PDF as bytes
        return pdf.output(dest='S').encode('latin-1')
    except Exception as e:
        st.error(f"Error exporting to PDF: {e}")
        print(f"PDF Export Error: {e}") # For console debugging
        return b"" # Return empty bytes on error

