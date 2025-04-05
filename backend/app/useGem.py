from .services.extractKeywords import extract_keywords_yake
from .services.serper import search_news_with_serper
from .services.gemini import analyze_stances

# Define a list of trusted sources
TRUSTED_SOURCES = {
    "factcheck.org": {"name": "FactCheck", "credibility": 95},
    "snopes.com": {"name": "Snopes", "credibility": 94},
    "politifact.com": {"name": "PolitiFact", "credibility": 93},
    "washingtonpost.com": {"name": "The Washington Post", "credibility": 91},
    "reuters.com": {"name": "Reuters", "credibility": 95},
    "apnews.com": {"name": "Associated Press News", "credibility": 95},
    "bbc.com": {"name": "BBC", "credibility": 92},
    "nytimes.com": {"name": "The New York Times", "credibility": 91},
    "guardian.com": {"name": "The Guardian", "credibility": 90},
    "forbes.com": {"name": "Forbes", "credibility": 88},
    "npr.org": {"name": "NPR", "credibility": 91},
    "usatoday.com": {"name": "USA Today", "credibility": 89},
    "abcnews.go.com": {"name": "ABC News", "credibility": 89},
    "cbsnews.com": {"name": "CBS News", "credibility": 89},
    "pewresearch.org": {"name": "Pew Research Center", "credibility": 96},
    "investopedia.com": {"name": "Investopedia", "credibility": 93},
    "economist.com": {"name": "The Economist", "credibility": 92},
    "propublica.org": {"name": "ProPublica", "credibility": 95},
    "truthout.org": {
        "name": "Truthout",
        "credibility": 82,
    },  # Higher potential for bias
    "fullfact.org": {"name": "Full Fact", "credibility": 94},
    "leadstories.com": {"name": "Lead Stories", "credibility": 93},
    "mediafactcheck.org": {"name": "Media Fact Check", "credibility": 92},
    "theconversation.com": {"name": "The Conversation", "credibility": 91},
    "thedispatch.com": {"name": "The Dispatch", "credibility": 89},
    "verifythis.com": {"name": "Verify This", "credibility": 93},
    "openfactchecking.org": {"name": "Open Fact Checking", "credibility": 92},
    "factscan.ca": {"name": "FactScan", "credibility": 93},
    "africacheck.org": {"name": "Africa Check", "credibility": 94},
    "altnews.in": {"name": "Alt News", "credibility": 93},
    "boomlive.in": {"name": "BOOM Live", "credibility": 93},
    "truthorfiction.com": {"name": "Truth or Fiction", "credibility": 90},
    "timesofindia.indiatimes.com": {
        "name": "Times of India",
        "credibility": 84,
    },  # variable bias
    "www.thehindu.com": {"name": "The Hindu", "credibility": 90},
    "www.news18.com": {"name": "News18", "credibility": 78},  # variable bias
    "www.business-standard.com": {"name": "Business Standard", "credibility": 88},
    "indianexpress.com": {"name": "The Indian Express", "credibility": 90},
    "hindustantimes.com": {"name": "Hindustan Times", "credibility": 87},
    "deccanherald.com": {"name": "Deccan Herald", "credibility": 88},
    "telegraphindia.com": {"name": "The Telegraph", "credibility": 86},
    "economictimes.indiatimes.com": {"name": "The Economic Times", "credibility": 87},
    "livemint.com": {"name": "Mint", "credibility": 89},
    "tribuneindia.com": {"name": "The Tribune", "credibility": 87},
    "pib.gov.in": {
        "name": "Press Information Bureau",
        "credibility": 89,
    },  # Government source, potential bias.
    "republicworld.com": {
        "name": "Republic World",
        "credibility": 72,
    },  # high potential for bias
    "timesnownews.com": {
        "name": "Times Now",
        "credibility": 76,
    },  # high potential for bias
    "mathrubhumi.com": {"name": "Mathrubhumi", "credibility": 85},
    "manoramaonline.com": {"name": "Malayala Manorama", "credibility": 85},
    "dinakaran.com": {"name": "Dinakaran", "credibility": 81},
    "anandabazar.com": {"name": "Ananda Bazar Patrika", "credibility": 85},
    "lokmat.com": {"name": "Lokmat", "credibility": 84},
    "theprint.in": {"name": "The Print", "credibility": 88},
    "scroll.in": {"name": "Scroll.in", "credibility": 87},
    "thewire.in": {"name": "The Wire", "credibility": 86},
    "newsclick.in": {"name": "NewsClick.in", "credibility": 80},
    "rediff.com": {"name": "Rediff.com", "credibility": 83},
    "www.independent.co.uk": {"name": "The Independent", "credibility": 74},
}


async def evaluate_news(trusted_sources, headline, stance_results):
    # Initialize counters
    agree_count = 0
    disagree_count = 0
    unrelated_count = 0
    discuss_count = 0
    trusted_count = 0

    # Initialize lists to store news for each stance
    agree_news = []
    disagree_news = []
    discuss_news = []

    # Process each stance result
    for news in stance_results:
        source = news["source"]
        stance = news["stance"]

        # Check if source matches any trusted source name
        if any(source == value["name"] for value in trusted_sources.values()):
            trusted_count += 1
            if stance == "agree":
                agree_count += 1
                agree_news.append(news)
            elif stance == "disagree":
                disagree_count += 1
                disagree_news.append(news)
            elif stance == "discuss":
                discuss_count += 1
                discuss_news.append(news)
            elif stance == "unrelated":
                unrelated_count += 1

    # Decision logic
    if trusted_count == 0:
        verdict = "neutral"
        relevant_news = []
    elif agree_count > disagree_count:
        verdict = "real"
        relevant_news = agree_news
        if len(relevant_news) < 5 and discuss_news:
            relevant_news += discuss_news[: 5 - len(relevant_news)]
    elif disagree_count > agree_count:
        verdict = "fake"
        relevant_news = disagree_news
        if len(relevant_news) < 5 and discuss_news:
            relevant_news += discuss_news[: 5 - len(relevant_news)]
    else:
        verdict = "neutral"
        relevant_news = discuss_news if discuss_news else agree_news + disagree_news

    return {
        "headline": headline,
        "agree_count": agree_count,
        "disagree_count": disagree_count,
        "discuss_count": discuss_count,
        "trusted_count": trusted_count,
        "verdict": verdict,
        "relevant_news": relevant_news,
    }


async def gem_main(news_headline):
    keywords = extract_keywords_yake(news_headline)
    print(keywords)
    fetched_news = search_news_with_serper(keywords)
    print("length of fected news article : ", len(fetched_news))

    stance_results = analyze_stances(news_headline, fetched_news)

    for news in stance_results:
        print("headline :", news_headline)
        print("news headline :", news["title"])
        print("news description :", news["snippet"])
        print("Source :", news["source"])
        print("link :", news["link"])
        print("Stance :", news["stance"])
        print("-" * 100)

    final_result = await evaluate_news(TRUSTED_SOURCES, news_headline, stance_results)
    print(final_result)
    return final_result
