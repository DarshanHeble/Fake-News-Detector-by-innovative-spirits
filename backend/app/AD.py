from .services.fetchNewsFromGoogle import fetch_and_scrape_news_from_google
from .previousSolution.analyseStance import analyze_stance
from .previousSolution.aggregateStance import aggregate_weighted_stance
from .services.getRelatedArticles import fetch_and_scrape_news_from_newsApi
from .services.extractKeywords import extract_keywords
from fastapi import HTTPException

def ad_main(content):
    # Extract keywords from content (User Inputted News)
    try:
        keywords = extract_keywords(content)
        if not keywords:
            raise ValueError("Failed to extract keywords.")
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        raise HTTPException(status_code=400, detail="Failed to extract keywords from the provided content.")
    
    # Fetch articles from NewsAPI
    try:
        articles = fetch_and_scrape_news_from_newsApi(keywords)
        print("Articles using NewsAPI:", articles)
    except Exception as e:
        print(f"Error fetching articles from NewsAPI: {e}")
        articles = []

    # Check if NewsAPI returned sufficient articles; fetch from Google if not
    if not articles or len(articles) < 3:
        try:
            print("Not enough articles found using NewsAPI.")
            additional_articles = fetch_and_scrape_news_from_google(keywords)
            if additional_articles:
                articles.extend(additional_articles)
        except Exception as e:
            print(f"Error fetching articles from Google search: {e}")
    
    if not articles:
        raise HTTPException(status_code=404, detail="No related articles found for the given content.")
    
    print("Final Articles List:", articles)
    
    # Analyze stance
    try:
        analyzed_articles_stances = analyze_stance(content, articles)
        print("Analyzed Stances:", analyzed_articles_stances)
    except Exception as e:
        print(f"Error analyzing stances: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing stances of articles.")
    
    # Aggregate stances
    try:
        result = aggregate_weighted_stance(analyzed_articles_stances)
        print("Final Aggregated Stance:", result)
    except Exception as e:
        print(f"Error aggregating stance: {e}")
        raise HTTPException(status_code=500, detail="Error aggregating stances.")
    
    return result