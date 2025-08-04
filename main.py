from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool, fashion_search_tool, trend_analysis_tool, social_media_tool
from typing import List, Optional
import json

load_dotenv()

class TrendAnalysis(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]
    trend_category: str
    confidence_score: float 
    key_influencers: List[str]
    trending_keywords: List[str]
    season_relevance: str  # spring, summer, fall, winter, year-round
    price_range: str
    sustainability_score: Optional[float]  # 0-1 scale
    market_potential: str  # emerging, peak, declining


llm = ChatOpenAI(model="gpt-4o-mini")
parser = PydanticOutputParser(pydantic_object=TrendAnalysis)

prompt = ChatPromptTemplate.from_messages([
    ("system", 
     """You are an expert fashion trend analyst with deep knowledge of the fashion industry, social media trends, and consumer behavior.
     
     Your analysis should include:
     1. Comprehensive trend identification across multiple platforms
     2. Categorization of trends (streetwear, luxury, sustainable, vintage, etc.)
     3. Assessment of trend lifecycle stage (emerging, peak, declining)
     4. Identification of key influencers and brands driving the trend
     5. Analysis of seasonal relevance and market positioning
     6. Evaluation of sustainability aspects when applicable
     7. Confidence scoring based on data quality and trend consistency
     
     Use all available tools to gather comprehensive data from:
     - Fashion blogs and magazines
     - Social media platforms (Instagram, TikTok, Twitter)
     - Fashion week reports
     - Retail data and consumer behavior
     - Celebrity and influencer fashion choices
     
     Provide detailed, actionable insights that would be valuable for fashion professionals, retailers, and consumers.
     
     Wrap the output in this format and provide no other text\n{format_instructions}
     """
    ),
    ("placeholder", "{chat_history}"),
    ("human", "{query}"),
    ("placeholder", "{agent_scratchpad}"),
]).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, save_tool, fashion_search_tool, trend_analysis_tool, social_media_tool]
agent = create_tool_calling_agent(
    llm = llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=10)

def analyze_fashion_trend(query: str):
    """
    Comprehensive fashion trend analysis function
    """
    print(f"Analyzing: {query}")
    print("=" * 50)
    
    raw_response = agent_executor.invoke({"query": query})
    
    try:
        structured_response = parser.parse(raw_response.get("output")[0]["text"])
        
        # Enhanced output formatting
        print("\nFASHION TREND ANALYSIS REPORT")
        print("=" * 50)
        print(f"Topic: {structured_response.topic}")
        print(f"Summary: {structured_response.summary}")
        print(f"Category: {structured_response.trend_category}")
        print(f"Confidence: {structured_response.confidence_score:.2f}")
        print(f"Sustainability Score: {structured_response.sustainability_score:.2f}" if structured_response.sustainability_score else "🌱 Sustainability Score: N/A")
        print(f"Season: {structured_response.season_relevance}")
        print(f"Price Range: {structured_response.price_range}")
        print(f"Market Potential: {structured_response.market_potential}")
        
        print(f"\n Key Influencers:")
        for influencer in structured_response.key_influencers:
            print(f"  • {influencer}")
            
        print(f"\n Trending Keywords:")
        for keyword in structured_response.trending_keywords:
            print(f"  • {keyword}")
            
        print(f"\n Sources:")
        for source in structured_response.sources:
            print(f"  • {source}")
            
        print(f"\n Tools Used:")
        for tool in structured_response.tools_used:
            print(f"  • {tool}")
            
        # Save detailed analysis
        save_tool.func(json.dumps(structured_response.model_dump(), indent=2), "detailed_trend_analysis.txt")
        
        return structured_response
        
    except Exception as e:
        print(f"Error parsing response: {e}")
        print("Raw response:", raw_response)
        return None

if __name__ == "__main__":
    print("FASHION TREND ANALYZER")
    print("=" * 50)
    print("Ask me about any fashion trend, style, or fashion-related topic!")
    print("Examples:")
    print("• What are the latest streetwear trends?")
    print("• How is sustainable fashion evolving?")
    print("• What's trending in luxury fashion this season?")
    print("• Tell me about vintage fashion trends")
    print("=" * 50)
    
    query = input("\n What would you like to analyze? ")
    if query.strip():
        analyze_fashion_trend(query)
    else:
        # Default query if none provided
        analyze_fashion_trend("What are the current trending fashion styles and why are they popular?")
