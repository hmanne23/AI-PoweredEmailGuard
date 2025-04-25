Smart Email Classifier

Introduction:

Smart Email Classifier is a web-based machine learning application designed to classify incoming emails as Spam or Not Spam.
It uses Natural Language Processing (NLP) and classification algorithms (Naive Bayes and SVM) to enhance email security and user trust.

Key Features:
	•	User registration and login
	•	Email spam classification with confidence score
	•	Model options: Naive Bayes and Support Vector Machine
	•	User-specific classification history
	•	Clean UI with light/dark mode toggle

Project Structure:

Smart Email Classifier/
│
├── main.py                   # Flask backend and route handling
├── requirements.txt          # List of all Python dependencies
├── Naive_model.pkl           # Pre-trained Naive Bayes pipeline
├── emails.csv                # Email dataset used for training
├── templates/                # HTML UI templates
│   ├── index.html            # Input form for email text
│   ├── show.html             # Displays classification result
│   ├── login.html            # User login page
│   ├── register.html         # User registration page
│   ├── history.html          # Displays past classification history
├── .gitignore                # Files/folders to be ignored by Git
├── Email Spam_with_pipeline.ipynb  # Model training using pipeline
├── Email Spam.ipynb          # Direct Naive Bayes model training

Usage:
	1.	Clone the repository or download the project folder.
	2.	(Recommended) Create and activate a virtual environment:
	•	python -m venv spam-env
	•	source spam-env/bin/activate (macOS/Linux)
	•	spam-env\Scripts\activate (Windows)
	3.	Install dependencies:
	•	pip install -r requirements.txt
	4.	Run the Flask app:
	•	python main.py
	5.	Open your browser and navigate to:
	•	http://127.0.0.1:5001/
	6.	Register a user account and log in.
	7.	Enter email content, choose a model, and classify.
	8.	View your classification history under the history tab.

Contributors:
	•	Harshitha Manne
	•	Sanjana Reddy Kondam
	•	Rohit Arikatla

Acknowledgments:

This project was created as part of the ITCS 6100 – Big Data Analytics for Competitive Advantage course at UNC Charlotte, under the guidance of Professor Gabriel Terejanu.
