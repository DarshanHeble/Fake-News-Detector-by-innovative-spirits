from rake_nltk import Rake

r = Rake()

def extract_keywords(text):
    r.extract_keywords_from_text(text)
    keywords = r.get_ranked_phrases()
    return keywords

# headline = "Artificial Intelligence (AI) is transforming industries by automating processes, enhancing decision-making, and creating new opportunities. However, ethical concerns, such as data privacy and bias, need to be addressed."
# keywords = extract_keywords(headline)
# print(keywords)
