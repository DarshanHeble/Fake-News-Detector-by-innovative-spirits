import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.environ.get("GOOGLE_API_KEY")
)  # get api key from environment variable

model = genai.GenerativeModel("gemini-2.0-flash")


def analyze_stances(input_headline, fetched_news):
    snippets = []
    stances = []
    results = []

    for news in fetched_news:
        snippets.append(news["snippet"])

    prompt = f"""
        Analyze these news snippets compared to the input headline.
        Return ONLY a array of stances, where each stance must be exactly one of: "agree", "disagree", "unrelated", or "discuss".
        Example response format: ["agree", "disagree", "discuss"]

        Input headline: {input_headline}
        
        News snippets:
        {[f"{i+1}. {snippet}" for i, snippet in enumerate(snippets)]}
    """

    # print(prompt)

    response = model.generate_content(prompt)
    # print(response.text)

    # Parse JSON response
    stances = json.loads(response.text)
    print("stance length from gemini: ", len(stances))

    for i, news in enumerate(fetched_news):
        results.append(
            {**news, "stance": stances[i] if i < len(stances) else "Stance Unavailable"}
        )
    # print(results)
    return results


async def verify_text_with_gemini(text: str):
    prompt = f"""
        Analyze the following input, which can be a news headline, a text, or the content of a URL, and determine if it is "real", "fake", or "neutral".
        Return ONLY the verdict as a single word.

        Input: "{text}"
    """
    response = await model.generate_content_async(prompt)
    return response.text.strip().lower()
