import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from fpdf import FPDF
from io import BytesIO
from datetime import datetime

# Load Medicine Data (only once)
df = pd.read_csv('medicine.csv')
df['tags'] = df['Description'].fillna('') + ' ' + df['Reason'].fillna('')

# Vectorization (once and reused)
cv = CountVectorizer(max_features=5000)
vectors = cv.fit_transform(df['tags']).toarray()
medical_terms = set(cv.get_feature_names_out())

# ✅ Helper function to check input validity
def is_valid_query(query):
    words = re.findall(r'\b\w+\b', query.lower())
    return any(word in medical_terms for word in words)

# ✅ Main recommendation function
def recommend_medicines(symptom_query):
    if not is_valid_query(symptom_query):
        return [{"error": "😥 Sorry, we couldn't find any matching medicines for your symptoms."}]

    query_vec = cv.transform([symptom_query]).toarray()
    similarities = cosine_similarity(vectors, query_vec)
    similar_indices = similarities[:, 0].argsort()[::-1][:5]

    results = []
    for idx in similar_indices:
        score = similarities[idx][0]
        if score > 0.1:
            row = df.iloc[idx]
            results.append({
                'name': row['Drug_Name'],
                'reason': row['Reason'],
                'description': row['Description'],
                'similarity': score
            })

    if not results:
        return [{"error": "😥 Sorry, no strong matching medicines found."}]
    return results

# ✅ PDF generation function
def generate_pdf(results, user_input):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Medicine Recommendation Report", ln=True, align="C")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Generated on: {now}", ln=True, align="C")
    pdf.ln(10)

    pdf.multi_cell(0, 10, f"Input Symptoms/Disease: {user_input}")
    pdf.ln(5)

    for i, item in enumerate(results, 1):
        pdf.set_font("Arial", 'B', size=10)
        pdf.multi_cell(0, 10, f"{i}. {item['name']} (Score: {item['similarity']:.2f})")
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 10, f"Reason: {item['reason']}")
        pdf.multi_cell(0, 10, f"Description: {item['description']}")
        pdf.ln(5)

    pdf_bytes = BytesIO()
    pdf_data = pdf.output(dest='S').encode('latin1')
    pdf_bytes.write(pdf_data)
    pdf_bytes.seek(0)
    return pdf_bytes
