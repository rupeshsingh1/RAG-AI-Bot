import google.generativeai as genai
from app.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

class GeminiService:

    def __init__(self):

        self.model = genai.GenerativeModel("gemini-pro")

    def generate(self, prompt):

        response = self.model.generate_content(prompt)

        return response.text