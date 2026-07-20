# seed_data.py
import random

# Base lists of real and fake posts/headlines across political, health, technology, science, and world news categories.
REAL_SAMPLES = [
    "The World Health Organization has declared a new global health initiative to combat malaria in tropical regions.",
    "Astronomers at the European Southern Observatory have discovered a new exoplanet orbiting a nearby star, potentially in the habitable zone.",
    "The federal government announced a 2.5% increase in funding for public infrastructure projects including railways and bridges.",
    "A peer-reviewed study published in Nature Medicine indicates that a new vaccine candidate shows 92% efficacy against the virus.",
    "Local election officials confirmed that all voting ballots have been verified, with final tallies expected by Friday evening.",
    "The central bank raised interest rates by a quarter of a percentage point in an effort to stabilize rising inflation rates.",
    "Technological researchers have developed a highly efficient solar panel that captures 30% more energy than existing models.",
    "A major storm is expected to hit the eastern coast tomorrow morning, with wind speeds reaching up to 75 miles per hour.",
    "The local city council approved a budget amendment to build three new community parks and upgrade public transit systems.",
    "A study from Oxford University reveals that consistent physical exercise reduces the risk of cardiovascular disease by 40%.",
    "Global leaders gathered at the climate summit in Geneva to sign a pledge reducing greenhouse gas emissions by 2030.",
    "The Supreme Court ruled 7-2 in favor of protecting individual consumer privacy rights on major internet platforms.",
    "NASA's rover successfully collected its latest soil sample from the Martian crater, seeking evidence of ancient microbial life.",
    "Economists predict a steady recovery in the manufacturing sector following the reopening of international supply chains.",
    "The agricultural department reported a record-high crop yield for wheat this season due to favorable weather conditions.",
    "State health officials recommend annual flu shots for children and the elderly to reduce hospitalizations.",
    "A new public high school is scheduled to open next September, accommodating over 1,500 students in the district.",
    "The national library announced it will digitize over 100,000 historical documents, making them accessible to the public for free.",
    "Doctors warn that sleeping fewer than six hours a night can significantly impact cognitive function and memory retention.",
    "Tech company announces a voluntary recall of its latest laptop model due to a battery overheating issue in early batches.",
    "Geologists detected a 4.2 magnitude earthquake off the coast, but no tsunami warnings have been issued.",
    "A team of marine biologists discovered three new species of deep-sea jellyfish during an expedition in the Pacific Ocean.",
    "The annual arts festival will feature over 150 local and international artists starting next weekend in the downtown square.",
    "Major automobile manufacturers have agreed to phase out gasoline engines in favor of electric vehicles by 2040.",
    "The department of transportation is implementing new safety regulations for commercial airline pilots to prevent fatigue.",
    "Scientists at MIT have synthesized a new biodegradable material that decomposes within six months in landfill conditions.",
    "The regional hospital group is expanding its telemedicine services to reach patients in remote rural areas.",
    "A non-profit organization launched a program to plant 10,000 trees across urban areas to combat heat island effects.",
    "Archaeologists in Egypt uncovered an intact tomb dating back to the New Kingdom, containing pottery and statues.",
    "The international space station crew completed a six-hour spacewalk to upgrade the station's solar arrays.",
    "The food and drug administration approved a new targeted therapy for patients with advanced lung cancer mutations.",
    "A consensus of climate scientists confirms that global temperatures have risen by an average of 1.1 degrees Celsius since the industrial era."
]

FAKE_SAMPLES = [
    "SHOCKING: Government secret project is spraying chemicals over major cities to control minds! Share before it gets taken down!",
    "Miracle remedy discovered! Drinking this simple kitchen ingredient cures all cancers in 24 hours. Doctors are furious!",
    "URGENT WARNING: The government is planning to shut down the entire internet next week to hide a massive financial collapse!",
    "Billionaire plans to release millions of robotic insects to spy on citizens. Exposed video inside!",
    "ALERT: Major scientific study proves that mobile phones are completely frying your brain cells and causing instant memory loss!",
    "BREAKING: Pope Francis shocks the world, endorses controversial candidate for president, citing divine intervention!",
    "Unbelievable! This 5-minute trick lets you hack any ATM and withdraw unlimited free cash. Hidden video tutorial link here!",
    "PROOF: NASA faked the latest Mars landing in a Hollywood studio. You can clearly see a stage light in the background of this photo!",
    "Warning! Eating this common vegetable will cause permanent damage to your internal organs. The food industry is hiding the truth!",
    "SECRET REPORT: Secret underground bases discovered under every major airport. They are hiding aliens and advanced technology!",
    "OMG! Giant sea monster captured on camera near the Florida coast. The government is trying to scrub this video from the web!",
    "Doctors are in shock! This herbal tea destroys all viral infections and builds a 100% immune shield. The big pharma doesn't want you to know!",
    "CONFIRMED: The moon is actually a hollow space station built by ancient civilizations. Read the leaked documents here!",
    "WARNING: New law passed in secret allows the police to enter your home without a warrant at any time. Share this immediately!",
    "Unbelievable! A 12-year-old child successfully built a fully functioning nuclear reactor in their backyard using old microwave parts!",
    "Breaking news: Scientists have discovered a secret gate to another dimension in the middle of the desert. Government has blocked access!",
    "SCANDAL: Top health officials caught on tape admitting that the common cold was engineered in a lab to sell more cough syrup!",
    "URGENT: Drinking tap water is slowly turning people into zombies. Here is the list of ingredients they are secretly adding to the reservoir!",
    "Shocking discovery: Sleeping with onions in your socks overnight completely cures diabetes and flushes out all toxins!",
    "THE TRUTH IS OUT: Aliens have officially taken over the leadership of a major international organization. Secret video proof!",
    "ALERT: A giant asteroid is 100% guaranteed to hit Earth next month, and space agencies are keeping it quiet to prevent panic!",
    "Breaking: Famous actor reveals he is actually a clone and the original died ten years ago. Incredible video interview inside!",
    "WARNING: Charging your phone overnight creates a dangerous electromagnetic field that permanently attracts lightning to your house!",
    "Shocking: Leaked email reveals major tech company is planning to charge users $100 per month just to access their basic email account!",
    "MUST SEE: This ancient device found in a cave generates free electricity forever. Energy companies are desperately trying to ban it!",
    "URGENT: New microchips are being secretly added to all food packaging to track where you shop. Check the barcodes for the secret red dot!",
    "Breaking: Major city announced it will completely ban cars starting Monday, forcing all citizens to walk or ride bicycles!",
    "ALERT: A mysterious signal from space is causing all computers to slowly lose their memory. Back up your files offline now!",
    "Wow! This natural fruit contains 1000x more vitamin C than oranges and completely prevents aging. Click here to buy!",
    "SCANDAL EXPOSED: The lottery is completely rigged by computer hackers. This secret algorithm predicts the winning numbers every single time!",
    "WARNING: The air conditioning units in all offices are secretly broadcasting frequencies that make employees work faster and sleep less!",
    "BOMBSHELL: Ancient tablets found under the pyramids predict that the world will undergo a major geographical shift next Tuesday!"
]

# Vocabulary helpers to generate synthetic variations and enrich the dataset size
TOPICS = {
    "health": {
        "real": ["medical study", "clinical trial", "health organization", "vaccine efficacy", "cardiovascular health", "nutrition research", "peer-reviewed journal"],
        "fake": ["miracle cure", "big pharma cover-up", "secret recipe", "toxic ingredients", "instant healing", "doctors are furious", "hidden cure"]
    },
    "politics": {
        "real": ["parliament voted", "official statement", "bilateral talks", "election commission", "government agency", "policy revision", "legislative bill"],
        "fake": ["secret plot", "rigged elections", "underground alliance", "leaked memo", "shocking betrayal", "deep state agenda", "unmasked corrupt politicians"]
    },
    "science": {
        "real": ["astronomical discovery", "laboratory synthesis", "biodegradable compound", "deep-sea expedition", "quantum computing research", "fossil excavation"],
        "fake": ["alien coverup", "dimensional portal", "hollow earth", "perpetual energy device", "time travel experiment", "flat earth proof"]
    }
}

REAL_TEMPLATES = [
    "Researchers at {institution} have successfully {action} a new method to {benefit}.",
    "According to a report by {source}, the {subject} has seen a {change} over the past year.",
    "Health authorities from {source} recommend that citizens {recommendation} to prevent health risks.",
    "A recent study published in the journal of {institution} indicates that {subject} plays a critical role in {benefit}.",
    "Officials confirmed today that the {subject} has been updated in compliance with {source} standards."
]

FAKE_TEMPLATES = [
    "SHOCKING NEWS: A whistleblower from {institution} just revealed they are {fake_action} to control the public!",
    "You won't believe how {institution} is secretly hiding the fact that {subject} causes {fake_harm}! Click to see the proof!",
    "ALERT: Leaked documents show that {source} is planning to {fake_action} by the end of the month!",
    "This simple {remedy} will completely cure your {subject} in seconds. The medical industry is terrified you'll find out!",
    "BREAKING: Anonymous hackers have exposed a secret {institution} server containing proof of {fake_conspiracy}!"
]

def generate_expanded_dataset():
    """Generates an expanded dataset of real and fake posts/headlines (~600 items)."""
    dataset = []
    
    # 1. Add our high-quality base samples
    for text in REAL_SAMPLES:
        dataset.append({"text": text, "label": 1})
    for text in FAKE_SAMPLES:
        dataset.append({"text": text, "label": 0})
        
    # Institutions, Actions, Benefits, etc. for generating realistic templates
    institutions = ["MIT", "Stanford University", "the World Health Organization", "NASA", "Oxford University", "the National Science Foundation", "Harvard Medical School"]
    sources = ["Reuters", "the Associated Press", "local health departments", "the Department of Energy", "the Federal Reserve", "the United Nations"]
    subjects = ["global climate patterns", "public transit infrastructure", "renewable solar energy", "cardiovascular health", "artificial intelligence safety", "microbial deep-sea life"]
    actions = ["developed", "discovered", "tested", "implemented", "validated", "optimized"]
    benefits = ["reduce industrial pollution", "enhance memory retention", "decrease energy grid strain", "improve early disease detection", "speed up computing power"]
    changes = ["15% increase in efficiency", "gradual stabilization", "marked improvement in safety", "significant decline in rates"]
    recommendations = ["increase physical activity", "maintain a balanced diet", "ensure adequate sleep", "verify online security settings"]
    
    fake_actions = ["spraying secret chemicals", "engineering artificial viruses", "monitoring personal brainwaves", "rigging all smart meters", "faking scientific data"]
    fake_harms = ["permanent DNA alteration", "immediate memory deletion", "uncontrolled cell breakdown", "magnetic alignment issues"]
    remedies = ["kitchen spice mixture", "herbal extract fluid", "detox onion sock trick", "mineral water solution", "frequency sound wave"]
    fake_conspiracies = ["alien tech replication", "fabricated moon landings", "underground control systems", "the hollow earth agenda"]

    # Generate synthetic real data
    random.seed(42)  # For reproducibility
    for _ in range(250):
        tmpl = random.choice(REAL_TEMPLATES)
        text = tmpl.format(
            institution=random.choice(institutions),
            source=random.choice(sources),
            subject=random.choice(subjects),
            action=random.choice(actions),
            benefit=random.choice(benefits),
            change=random.choice(changes),
            recommendation=random.choice(recommendations)
        )
        dataset.append({"text": text, "label": 1})

    # Generate synthetic fake data
    for _ in range(250):
        tmpl = random.choice(FAKE_TEMPLATES)
        text = tmpl.format(
            institution=random.choice(institutions),
            source=random.choice(sources),
            subject=random.choice(subjects),
            fake_action=random.choice(fake_actions),
            fake_harm=random.choice(fake_harms),
            remedy=random.choice(remedies),
            fake_conspiracy=random.choice(fake_conspiracies)
        )
        dataset.append({"text": text, "label": 0})

    # Shuffle the dataset
    random.shuffle(dataset)
    return dataset

if __name__ == "__main__":
    data = generate_expanded_dataset()
    print(f"Generated dataset with {len(data)} items.")
    real_count = sum(1 for item in data if item["label"] == 1)
    fake_count = sum(1 for item in data if item["label"] == 0)
    print(f"Real: {real_count}, Fake: {fake_count}")
