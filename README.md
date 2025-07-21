MCQ_GENERATOR_AI
🧠 QuizGenius - AI-Powered Multiple Choice Question Generator
QuizGenius is an intelligent web application built with Streamlit and Google's Gemini AI model that simplifies the creation and management of multiple-choice questions (MCQs). Whether you need to generate questions from text, upload documents, create them manually, or take quizzes to test your knowledge, QuizGenius has you covered.

✨ Features
AI-Powered MCQ Generation:

Generate MCQs instantly from any provided text content using the Gemini AI model.

Specify the number of questions, difficulty level (Easy, Medium, Hard), and an optional category.

Document Upload & Generation:

Upload PDF, DOCX, or TXT files to automatically extract text and generate MCQs from the document's content.

Manual Question Entry:

Add custom MCQs manually with full control over question text, options, correct answer, difficulty, and category.

Quiz Taking Functionality:

Select from saved question sets to take interactive quizzes.

Receive instant feedback on your answers and a final score.

Question Set Management:

Save generated or manually created questions as named sets.

Load any saved set back into the current session for further use or quizzing.

Delete unwanted question sets.

Export Options:

Export generated/current questions to JSON format for easy sharing or integration. (PDF export is planned for future development).

Responsive UI:

A clean, intuitive, and responsive user interface designed with a dark brown and orange theme for an engaging experience across devices.

🚀 Technologies Used
Streamlit: For building interactive web applications in Python.

Google Gemini API (via LangChain): For advanced AI-powered text generation.

Python-dotenv: For managing environment variables (like API keys).

PyPDF2: For extracting text from PDF documents.

python-docx: For extracting text from DOCX documents.

HTML/CSS: For custom UI elements and styling (integrated within Streamlit).

Tailwind CSS (conceptually): The custom CSS is inspired by Tailwind's utility-first approach for responsive design.

⚙️ Setup and Local Installation
Follow these steps to get QuizGenius running on your local machine.

1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/MCQ_GENERATOR_AI.git
cd MCQ_GENERATOR_AI

(Replace YOUR_USERNAME with your actual GitHub username)

2. Create a Virtual Environment (Recommended)
python -m venv venv

3. Activate the Virtual Environment
On Windows:

.\venv\Scripts\activate

On macOS/Linux:

source venv/bin/activate

4. Install Dependencies
Install all required Python packages using the requirements.txt file:

pip install -r requirements.txt

5. Configure Your Gemini API Key
Get a Gemini API Key: If you don't have one, obtain a Google Gemini API key from Google AI Studio.

Create a .env file: In the root directory of your project (MCQ_GENERATOR_AI/), create a new file named .env.

Add your API Key: Open the .env file and add your Gemini API key in the following format:

GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"

Important: Ensure there are no spaces around the = sign. This file is ignored by Git (.gitignore) to protect your sensitive key.

6. Run the Application
Once all dependencies are installed and your API key is configured, run the Streamlit application:

streamlit run app.py

This command will open the application in your default web browser (usually at http://localhost:8501).

🌐 Deployment to Streamlit Community Cloud
This application is designed for easy deployment to Streamlit Community Cloud.

Host on GitHub: Ensure your project (excluding the .env file, which should be in .gitignore) is pushed to a public GitHub repository.

Streamlit Cloud: Log in to Streamlit Community Cloud with your GitHub account.

New App: Click "New app" and select your MCQ_GENERATOR_AI repository and app.py as the main file.

Secrets: Crucially, add your GEMINI_API_KEY as a secret in the "Advanced settings" section of the deployment configuration. The format should be GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE".

Deploy: Click "Deploy!" to get your live, shareable web link.

💡 Usage
Navigate through the application using the tabs:

AI Generator: Paste text and configure settings to generate MCQs using AI.

Manual Entry: Create questions one by one with custom options and answers.

Upload Doc: Upload PDF, DOCX, or TXT files to generate questions from their content.

Take Quiz: Select a saved question set and test your knowledge.

Manage Sets: Save your current questions, or load/delete previously saved sets.

Export: Download your current questions in JSON format.

🤝 Contributing
Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please feel free to:

Fork the repository.

Create a new branch (git checkout -b feature/YourFeatureName).

Make your changes.

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature/YourFeatureName).

Open a Pull Request.

📄 License
This project is open-source and available under the MIT License.

📧 Contact
For any questions or feedback, please open an issue on the GitHub repository.