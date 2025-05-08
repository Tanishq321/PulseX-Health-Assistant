# PulseX Smart Health Assistant

PulseX is a Smart Health Assistant web application that provides users with personalized medicine recommendations, nearby hospital suggestions, and a chatbot interface—all via a sleek Flask web interface.

## 🚀 Features

- 💊 **Medicine Recommender**: Uses NLP and cosine similarity to suggest medicines based on user symptoms.
- 📄 **PDF Export**: Allows users to download medicine recommendations as a PDF file.
- 🏥 **Hospital Locator**: Provides hospitals by city and state with mapping stored in code.
- 🤖 **AI Chatbot**: Utilizes Google Generative AI for interactive health-related conversations.
- 🌐 **Web-based UI**: User-friendly interface using HTML templates.

## 🗂️ Project Structure

```

PulseX Smart Health Assistant flask version/
├── app.py                  # Main Flask app with routes
├── hospital\_locator.py     # Hospital finder logic
├── med.py                  # Medicine recommendation + PDF generation
├── medicine.csv            # Dataset with symptoms and medicines
├── requirements.txt        # Python package dependencies
├── templates/              # HTML files for front-end rendering
├── static/                 # (Optional) CSS/JS/Images if used

```

## ⚙️ Installation

1. Clone this repository or extract the ZIP file.
2. Navigate to the project directory.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Running the App

Run the application with:

```bash
python app.py
```

Then open your browser and go to:
`http://127.0.0.1:5000`

## 📄 Key Components

### `app.py`

* Defines routes:

  * `/` – Homepage
  * `/chatbot` – Chat with AI
  * `/medicine` – Get medicine recommendations
  * `/download_pdf` – Download recommendations as PDF
  * `/hospital` – Find hospitals by city/state

### `med.py`

* `recommend_medicines(symptom_query)` – Uses cosine similarity to match symptoms.
* `is_valid_query(query)` – Filters invalid symptom inputs.
* `generate_pdf(results, user_input)` – Exports results to a downloadable PDF.

### `hospital_locator.py`

* `get_hospitals_for_city(city)` – Returns a list of hospitals for a city.
* `state_city_mapping` – Dictionary with 30 major cities for each Indian state.

## 📦 Dependencies

* Flask
* pandas
* scikit-learn
* markdown
* fpdf
* google-generativeai

## 📜 License

This project is for educational purposes only.