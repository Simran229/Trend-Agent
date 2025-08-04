from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
import re

def save_to_txt(data: str, filename: str = "trend_analysis.txt"):
    """
    Saves the data to a text file with the current timestamp.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f" Trend Analysis Report\nTimestamp: {timestamp}\n\n{data}\n\n"
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"{formatted_text}")

    return f"Data successfully saved to {filename}"

def fashion_specific_search(query: str) -> str:
    """
    Performs fashion-specific searches across multiple fashion platforms and blogs.
    """
    fashion_sources = [
        f"site:vogue.com {query}",
        f"site:elle.com {query}",
        f"site:wwd.com {query}",
        f"site:fashionista.com {query}",
        f"site:refinery29.com {query}",
        f"site:whowhatwear.com {query}",
        f"site:stylecaster.com {query}",
        f"site:thecut.com {query}",
        f"site:businessoffashion.com {query}",
        f"site:instagram.com {query} fashion",
        f"site:tiktok.com {query} fashion trend"
    ]
    
    search = DuckDuckGoSearchRun()
    results = []
    
    for source_query in fashion_sources[:5]:  # limit to avoid rate limiting
        try:
            result = search.run(source_query)
            results.append(f"Source: {source_query}\nResult: {result}\n")
        except Exception as e:
            results.append(f"Source: {source_query}\nError: {str(e)}\n")
    
    return "\n".join(results)

def analyze_trend_lifecycle(query: str) -> str:
    """
    Analyzes the lifecycle stage of a fashion trend (emerging, peak, declining).
    """
    search_terms = [
        f"{query} trend analysis",
        f"{query} fashion week",
        f"{query} social media engagement",
        f"{query} retail sales data",
        f"{query} consumer interest decline"
    ]
    
    search = DuckDuckGoSearchRun()
    lifecycle_data = []
    
    for term in search_terms:
        try:
            result = search.run(term)
            lifecycle_data.append(f"Analysis for '{term}': {result}")
        except Exception as e:
            lifecycle_data.append(f"Error analyzing '{term}': {str(e)}")
    
    # simple trend lifecycle analysis based on search results
    positive_indicators = sum(1 for data in lifecycle_data if any(word in data.lower() for word in ['trending', 'popular', 'viral', 'hot', 'new']))
    negative_indicators = sum(1 for data in lifecycle_data if any(word in data.lower() for word in ['decline', 'over', 'passé', 'old', 'outdated']))
    
    if positive_indicators > negative_indicators:
        stage = "emerging or peak"
    elif negative_indicators > positive_indicators:
        stage = "declining"
    else:
        stage = "stable"
    
    return f"Trend Lifecycle Analysis for '{query}':\nStage: {stage}\nPositive indicators: {positive_indicators}\nNegative indicators: {negative_indicators}\n\nDetailed data:\n" + "\n".join(lifecycle_data)

def social_media_trend_analysis(query: str) -> str:
    """
    Analyzes social media trends and engagement for fashion topics.
    """
    social_platforms = [
        f"site:instagram.com {query} fashion",
        f"site:tiktok.com {query} fashion trend",
        f"site:twitter.com {query} fashion",
        f"site:pinterest.com {query} fashion",
        f"site:youtube.com {query} fashion trend"
    ]
    
    search = DuckDuckGoSearchRun()
    social_data = []
    
    for platform_query in social_platforms:
        try:
            result = search.run(platform_query)
            social_data.append(f"Platform: {platform_query}\nData: {result}\n")
        except Exception as e:
            social_data.append(f"Platform: {platform_query}\nError: {str(e)}\n")
    
    # Extract hashtags and trending terms
    hashtags = re.findall(r'#\w+', ' '.join(social_data))
    trending_terms = re.findall(r'\b\w+ fashion\b|\bfashion \w+\b', ' '.join(social_data), re.IGNORECASE)
    
    analysis = f"Social Media Trend Analysis for '{query}':\n"
    analysis += f"Popular hashtags: {', '.join(set(hashtags[:10]))}\n"
    analysis += f"Trending terms: {', '.join(set(trending_terms[:10]))}\n\n"
    analysis += "Platform-specific data:\n" + "\n".join(social_data)
    
    return analysis

def get_fashion_influencers(query: str) -> str:
    """
    Identifies key fashion influencers and celebrities driving trends.
    """
    influencer_queries = [
        f"{query} fashion influencers",
        f"{query} celebrity style",
        f"{query} fashion bloggers",
        f"{query} style icons",
        f"{query} fashion week celebrities"
    ]
    
    search = DuckDuckGoSearchRun()
    influencer_data = []
    
    for influencer_query in influencer_queries:
        try:
            result = search.run(influencer_query)
            influencer_data.append(f"Query: {influencer_query}\nResult: {result}\n")
        except Exception as e:
            influencer_data.append(f"Query: {influencer_query}\nError: {str(e)}\n")
    
    return f"Fashion Influencer Analysis for '{query}':\n" + "\n".join(influencer_data)

def sustainability_analysis(query: str) -> str:
    """
    Analyzes sustainability aspects of fashion trends.
    """
    sustainability_queries = [
        f"{query} sustainable fashion",
        f"{query} eco-friendly materials",
        f"{query} ethical fashion",
        f"{query} environmental impact",
        f"{query} circular fashion"
    ]
    
    search = DuckDuckGoSearchRun()
    sustainability_data = []
    
    for sus_query in sustainability_queries:
        try:
            result = search.run(sus_query)
            sustainability_data.append(f"Query: {sus_query}\nResult: {result}\n")
        except Exception as e:
            sustainability_data.append(f"Query: {sus_query}\nError: {str(e)}\n")
    
    return f"Sustainability Analysis for '{query}':\n" + "\n".join(sustainability_data)

# Enhanced tools
save_tool = Tool(
    name="save_to_txt",
    func=save_to_txt,
    description="Saves the trend analysis report to a text file with a timestamp."
)

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search_instagram",
    func=search.run,
    description="Search for general information on any topic",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

fashion_search_tool = Tool(
    name="fashion_specific_search",
    func=fashion_specific_search,
    description="Search for fashion-specific information across major fashion publications and platforms including Vogue, Elle, WWD, and social media."
)

trend_analysis_tool = Tool(
    name="trend_lifecycle_analysis",
    func=analyze_trend_lifecycle,
    description="Analyze the lifecycle stage of a fashion trend (emerging, peak, declining) based on current data and market indicators."
)

social_media_tool = Tool(
    name="social_media_trend_analysis",
    func=social_media_trend_analysis,
    description="Analyze social media trends, engagement, and viral content related to fashion topics across Instagram, TikTok, Twitter, Pinterest, and YouTube."
)

influencer_tool = Tool(
    name="fashion_influencer_analysis",
    func=get_fashion_influencers,
    description="Identify key fashion influencers, celebrities, and style icons driving current trends."
)

sustainability_tool = Tool(
    name="sustainability_analysis",
    func=sustainability_analysis,
    description="Analyze sustainability and environmental aspects of fashion trends and practices."
)

