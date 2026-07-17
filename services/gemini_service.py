import os

from dotenv import load_dotenv
from google import genai

from services.pdf_reader import read_all_pdfs

# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()

# ==========================================
# Gemini Client
# ==========================================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ==========================================
# Load PDF Knowledge Only Once
# ==========================================

PDF_KNOWLEDGE = read_all_pdfs()

# ==========================================
# Ask Gemini
# ==========================================

def ask_gemini(question):

    prompt = f"""
You are FoodExpress Restaurant AI Assistant.

Rules:

1. Answer politely.
2. Use ONLY the Restaurant Knowledge below.
3. Never create fake menu items.
4. Never guess prices.
5. If the answer is unavailable, reply:
   "Sorry, I couldn't find that information in our restaurant knowledge."

==========================================================
Restaurant Knowledge
==========================================================

{PDF_KNOWLEDGE}

==========================================================
Customer Question
==========================================================

{question}

==========================================================
Answer
==========================================================
"""

    try:

        response = client.models.generate_content(
            model="models/gemini-3.5-flash",
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:

        return f"Gemini Error: {e}"