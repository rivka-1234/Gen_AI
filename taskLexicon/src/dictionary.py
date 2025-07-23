import requests
import os
import json
from dotenv import load_dotenv

def generate_dictionary(task_name, task_description):
    """
    Generate a logistics/business dictionary by calling an external LLM API.
    """
    load_dotenv()

    gemini_api_url="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise Exception("GEMINI_API_KEY is not set in the environment variables. Please add it to the .env file.")

    prompt = (
      f"Generate a logistics/business dictionary for the following task:\n\n"
      f"Task Name: {task_name}\n"
      f"Task Description: {task_description}\n\n"
      f"Include terms related to logistics, international deliveries, and cross-border shipping solutions for e-commerce businesses.\n\n"
      f"Return in the array only concepts that appear in the task.\n\n"
      f"Provide the output in the following format:\n"
      f"[{{\"term\": \"Term1\", \"definition\": \"Definition1\"}}, {{\"term\": \"Term2\", \"definition\": \"Definition2\"}}]"
    )

    headers = {
      "Content-Type": "application/json",
      "X-goog-api-key": gemini_api_key,
    }
    data = {
      "contents": [
        {
          "parts": [
            {
              "text": prompt
            }
          ]
        }
      ],
      "generationConfig": {
        "maxOutputTokens": 1500,
        "temperature": 0.3
      },
    }

    response = requests.post(gemini_api_url, headers=headers, json=data)

    if response.status_code == 200:
        try:
            response_data = json.loads(response.text)

            nested_text = response_data["candidates"][0]["content"]["parts"][0]["text"]

            if nested_text.startswith("```json") and nested_text.endswith("```"):
                nested_text = nested_text[7:-3].strip()

            terms_list = json.loads(nested_text)


            terms_html = "".join(f"<li><strong>{term['term']}:</strong> {term['definition']}</li>" for term in terms_list)
            html_content = f"""
            <html>
            <head>
                <title>Logistics/Business Dictionary</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 20px;
                        padding: 20px;
                        background-color: #f9f9f9;
                        color: #333;
                    }}
                    h1 {{
                        color: #2c3e50;
                        border-bottom: 2px solid #3498db;
                        padding-bottom: 10px;
                    }}
                    p {{
                        font-size: 16px;
                        line-height: 1.5;
                    }}
                    h2 {{
                        color: #2980b9;
                        margin-top: 30px;
                    }}
                    ul {{
                        list-style-type: none;
                        padding: 0;
                    }}
                    li {{
                        background: #ecf0f1;
                        margin: 10px 0;
                        padding: 15px;
                        border-radius: 5px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    }}
                    li strong {{
                        color: #2c3e50;
                    }}
                </style>
            </head>
            <body>
                <h1>Dictionary for Task: {task_name}</h1>
                <p><strong>Description:</strong> {task_description}</p>
                <h2>Generated Terms</h2>
                <ul>
                    {terms_html}
                </ul>
            </body>
            </html>
            """

            return  html_content
        except (ValueError, KeyError, json.JSONDecodeError) as e:
            raise Exception(f"Failed to decode the API response: {e}")
    else:
        try:
            error_message = response.json().get("error", {}).get("message", "Unknown error")
        except ValueError:
            error_message = response.text
        raise Exception(f"API call failed: {error_message}")