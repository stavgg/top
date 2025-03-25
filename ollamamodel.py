import requests
import json
import ollama

class ollamamodel():   
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "mistral"  # מודל מהיר יותר מ-llama3

    def get_advice(self, question):
        print("📡 Sending to Ollama via requests...")

        try:
            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": question,
                    "stream": False,
                    "options": {
                        "num_predict": 250  # הגבלת אורך התשובה ל-250 תווים
                    }
                }
            )
            response.raise_for_status()

            # קבלת תשובה כטקסט
            text = response.text
            # print("🧾 Raw response text:")
            # print(text)

            data = json.loads(text)
            return data['response']

        except Exception as e:
            print("❌ Error communicating with Ollama:", e)
            return f"⚠️ Error: {str(e)}"
