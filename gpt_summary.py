# gpt_summary.py

USE_GPT = False  # Change to True when using real GPT API with a valid key

if USE_GPT:
    from openai import OpenAI
    client = OpenAI(api_key="sk-...")  # Replace with your OpenAI key

    def generate_summary(prompt_text):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a business analyst who generates concise summaries from EDA insights."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.4,
            max_tokens=800
        )
        return response.choices[0].message.content
else:
    # ✅ Mock summary (dynamic output)
    def generate_summary(prompt_text):
        return (
            "📌 Auto-generated Summary (Mock Mode):\n\n"
            + prompt_text[:1000] +  # Show first 1000 characters of EDA insight
            "\n\n⚠️ This is a simulated GPT output. Replace with actual GPT once API is active."
        )
