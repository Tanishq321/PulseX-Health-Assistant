from flask import Flask, render_template, request, redirect, url_for, send_file
from med import generate_pdf, recommend_medicines
import google.generativeai as genai
from markdown import markdown
from hospital_locator import state_city_mapping, get_hospitals_for_city

app = Flask(__name__)

genai.configure(api_key="AIzaSyAvMqp5vZEUasQRG32l-aAzq9vIfVUEuzY")
model = genai.GenerativeModel("gemini-1.5-flash")

chat_history = []

@app.route("/")
def index():
    return render_template("index.html")  # ✅ restored original home page

@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    global chat_history
    if request.method == "POST":
        user_input = request.form.get("prompt")
        if user_input:
            try:
                response = model.generate_content(user_input)
                bot_reply = response.text
            except Exception as e:
                bot_reply = f"⚠️ Error: {str(e)}"
            chat_history = [("user", user_input), ("assistant", bot_reply)]
            return redirect(url_for("chatbot"))
    rendered_history = []
    for sender, message in chat_history:
        if sender == "assistant":
            message = markdown(message)
        rendered_history.append((sender, message))
    return render_template("chatbot.html", chat_history=rendered_history)

@app.route("/medicine", methods=["GET", "POST"])
def medicine():
    error = None
    recommendations = None
    symptom = ""

    if request.method == "POST":
        symptom = request.form.get("symptom", "").strip()
        if not symptom:
            error = "⚠️ Please enter some symptoms!"
        else:
            recommendations = recommend_medicines(symptom)
            if "error" in recommendations[0]:
                error = recommendations[0]["error"]
                recommendations = None

    return render_template('medicine.html',
                           error=error,
                           recommendations=recommendations,
                           user_input=symptom)

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    user_input = request.form.get('user_input', '').strip()
    results = recommend_medicines(user_input)

    if not results or not isinstance(results, list) or not all("name" in r for r in results):
        return "⚠️ Failed to generate PDF: No valid recommendations found.", 400

    pdf_bytes = generate_pdf(results, user_input)
    return send_file(
        pdf_bytes,
        as_attachment=True,
        download_name="medicine_report.pdf",
        mimetype="application/pdf"
    )

@app.route("/hospital", methods=["GET", "POST"])
def hospital():
    selected_state = None
    selected_city = None
    hospitals = []
    cities = []

    if request.method == "POST":
        selected_state = request.form.get("state")
        selected_city = request.form.get("city")

        if selected_state:
            cities = state_city_mapping.get(selected_state, [])

        if selected_city:
            hospitals = get_hospitals_for_city(selected_city)

    return render_template("hospital.html",
                           states=list(state_city_mapping.keys()),
                           cities=cities,
                           selected_state=selected_state,
                           selected_city=selected_city,
                           hospitals=hospitals)

if __name__ == "__main__":
    app.run(debug=True)
