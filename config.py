import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# fashion analysis settings
FASHION_SOURCES = [
    "vogue.com",
    "elle.com", 
    "wwd.com",
    "fashionista.com",
    "refinery29.com",
    "whowhatwear.com",
    "stylecaster.com",
    "thecut.com",
    "businessoffashion.com",
    "instagram.com",
    "tiktok.com"
]

SOCIAL_MEDIA_PLATFORMS = [
    "instagram.com",
    "tiktok.com", 
    "twitter.com",
    "pinterest.com",
    "youtube.com"
]

TREND_CATEGORIES = [
    "streetwear",
    "luxury", 
    "sustainable",
    "vintage",
    "athleisure",
    "minimalist",
    "bohemian",
    "preppy",
    "gothic",
    "cyberpunk",
    "cottagecore",
    "y2k",
    "grunge",
    "preppy"
]

SEASONS = [
    "spring",
    "summer", 
    "fall",
    "winter",
    "year-round"
]

PRICE_RANGES = [
    "budget",
    "mid-range",
    "luxury"
]

MARKET_STAGES = [
    "emerging",
    "peak", 
    "declining"
]

# analysis parameters
MAX_SEARCH_RESULTS = 5
MAX_ITERATIONS = 10
TEMPERATURE = 0.3
MODEL_NAME = "gpt-4o-mini"

# file paths
OUTPUT_DIR = "trend_analysis_output"
DEFAULT_FILENAME = "trend_analysis.txt"
DETAILED_FILENAME = "detailed_trend_analysis.txt"

# create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True) 