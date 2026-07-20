# data_collector.py
import random

# Simulated raw feeds
TWITTER_FEED = [
    {"source": "X/Twitter", "text": "BREAKING: Scientists have discovered a secret gate to another dimension in the middle of the desert. Government has blocked access!", "label": 0},
    {"source": "X/Twitter", "text": "A Peer-reviewed study published in Nature Medicine indicates that a new vaccine candidate shows 92% efficacy.", "label": 1},
    {"source": "X/Twitter", "text": "OMG! Giant sea monster captured on camera near the Florida coast. The government is trying to scrub this video!", "label": 0},
    {"source": "X/Twitter", "text": "Technological researchers have developed a highly efficient solar panel that captures 30% more energy than existing models.", "label": 1},
    {"source": "X/Twitter", "text": "URGENT WARNING: The government is planning to shut down the entire internet next week to hide a massive financial collapse!", "label": 0},
    {"source": "X/Twitter", "text": "Local election officials confirmed that all voting ballots have been verified, with final tallies expected by Friday.", "label": 1}
]

REDDIT_FEED = [
    {"source": "Reddit (r/Science)", "text": "Astronomers at the European Southern Observatory have discovered a new exoplanet orbiting a nearby star in the habitable zone.", "label": 1},
    {"source": "Reddit (r/Conspiracy)", "text": "THE TRUTH IS OUT: Aliens have officially taken over the leadership of a major international organization. Leaked video proof inside!", "label": 0},
    {"source": "Reddit (r/Medicine)", "text": "A consensus of climate scientists confirms that global temperatures have risen by an average of 1.1 degrees Celsius.", "label": 1},
    {"source": "Reddit (r/Unbelievable)", "text": "Billionaire plans to release millions of robotic insects to spy on citizens. Hidden camera exposes his compound!", "label": 0},
    {"source": "Reddit (r/Finance)", "text": "The central bank raised interest rates by a quarter of a percentage point in an effort to stabilize rising inflation rates.", "label": 1}
]

LOCAL_CSV_FEED = [
    {"source": "Local CSV File", "text": "Geologists detected a 4.2 magnitude earthquake off the coast, but no tsunami warnings have been issued.", "label": 1},
    {"source": "Local CSV File", "text": "Miracle remedy discovered! Drinking this simple kitchen ingredient cures all cancers in 24 hours. Doctors are furious!", "label": 0},
    {"source": "Local CSV File", "text": "The agricultural department reported a record-high crop yield for wheat this season due to favorable weather conditions.", "label": 1},
    {"source": "Local CSV File", "text": "WARNING: Charging your phone overnight creates a dangerous electromagnetic field that permanently attracts lightning!", "label": 0}
]

def collect_from_source(source_name):
    """Simulates fetching posts from a specified source."""
    if source_name == "Twitter":
        # Add slight random variations to simulate live feed scraping
        posts = []
        for post in TWITTER_FEED:
            posts.append({
                "source": "X/Twitter Feed",
                "text": f"{post['text']} #BreakingNews {random.randint(10, 99)}",
                "label": post["label"]
            })
        return posts
    elif source_name == "Reddit":
        return REDDIT_FEED
    elif source_name == "LocalFiles":
        return LOCAL_CSV_FEED
    return []

def collect_all_sources():
    """Aggregates all simulated sources into a single corpus."""
    all_data = []
    all_data.extend(collect_from_source("Twitter"))
    all_data.extend(collect_from_source("Reddit"))
    all_data.extend(collect_from_source("LocalFiles"))
    return all_data
