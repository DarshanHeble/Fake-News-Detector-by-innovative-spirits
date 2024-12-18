# import json
# import os

# print(os.getcwd())

# Load the reputability database
# with open('backend/app/data/source.json', 'r', encoding="utf-8") as f:
#     reputability_data = json.load(f)
    

reputability_data=[
  {
    "source_name": "Reuters",
    "reliability_score": 0.95,
    "bias": "Center",
    "last_updated": "2024-11-01"
  },
  {
    "source_name": "BBC News",
    "reliability_score": 0.92,
    "bias": "Center-Left",
    "last_updated": "2024-10-20"
  },
  {
    "source_name": "The New York Times",
    "reliability_score": 0.89,
    "bias": "Left",
    "last_updated": "2024-09-15"
  },
  {
    "source_name": "Fox News",
    "reliability_score": 0.7,
    "bias": "Right",
    "last_updated": "2024-08-05"
  },
  {
    "source_name": "BuzzFeed News",
    "reliability_score": 0.6,
    "bias": "Center-Left",
    "last_updated": "2024-10-12"
  },
  {
    "source_name": "Infowars",
    "reliability_score": 0.3,
    "bias": "Far-Right",
    "last_updated": "2024-07-30"
  }
]

def get_reliability_score(source_name):
    """
    Retrieves the reliability score for a given source name.
    
    Args:
        source_name: The name of the source.
    
    Returns:
        The reliability score for the source. Defaults to 0.5 if the source is not found.
    """
    
    for source in reputability_data:
        if source['source_name'].lower() == source_name.lower():
            return source['reliability_score']
    return 0.5  # Default score if source not found

# Example usage
# source_name = "BBC News"
# reliability_score = get_reliability_score(source_name)
# print(f"Reliability score for {source_name}: {reliability_score}")
