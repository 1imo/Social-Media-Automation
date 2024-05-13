import markovify
import random
import time


def generate_title(description, title_corpus):
    # Analyze the description to determine the overall theme and tone
    themes = ["luxury", "performance", "exclusivity", "rarity", "innovation"]
    tones = ["enthusiastic", "aspirational", "informative", "engaging", "captivating"]

    start_time = time.time()

    theme = random.choice(themes)
    tone = random.choice(tones)

    # Train a Markov chain model on the title corpus
    text_model = markovify.NewlineText(title_corpus)

    # Generate a title based on the theme and tone using the Markov chain model
    title = None
    while not title:
        title = text_model.make_sentence(
            tries=30, max_overlap_ratio=0.8, min_words=11, max_words=23
        )

    # Modify the generated title based on the theme and tone
    if theme == "luxury":
        luxury_modifiers = ["Opulent", "Exquisite", "Refined", "Sumptuous", "Elegant"]
        title = title.replace("_", random.choice(luxury_modifiers), 1)
    elif theme == "performance":
        performance_modifiers = [
            "High-Performance",
            "Powerful",
            "Thrilling",
            "Aggressive",
            "Beastly",
        ]
        title = title.replace("_", random.choice(performance_modifiers), 1)
    elif theme == "exclusivity":
        exclusivity_modifiers = [
            "Exclusive",
            "Rare",
            "Limited Edition",
            "One-of-a-Kind",
            "Bespoke",
        ]
        title = title.replace("_", random.choice(exclusivity_modifiers), 1)
    elif theme == "rarity":
        rarity_modifiers = ["Scarce", "Uncommon", "Sought-After", "Elusive", "Precious"]
        title = title.replace("_", random.choice(rarity_modifiers), 1)
    elif theme == "innovation":
        innovation_modifiers = [
            "Innovative",
            "Cutting-Edge",
            "Futuristic",
            "Revolutionary",
            "Pioneering",
        ]
        title = title.replace("_", random.choice(innovation_modifiers), 1)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time:.2f} seconds")

    return title


# Example usage
description = """
𝐓𝐞𝐚𝐦 𝐏𝐞𝐭𝐫𝐨𝐧𝐚𝐬🖤

𝐌𝐞𝐫𝐜𝐞𝐝𝐞𝐬 𝐁𝐞𝐧𝐳 𝐀𝐌𝐆 𝐎𝐍𝐄 | 𝟏 𝐨𝐟 𝟐𝟕𝟓
𝐌𝐞𝐫𝐜𝐞𝐝𝐞𝐬 𝐁𝐞𝐧𝐳 𝐀𝐌𝐆 𝐆𝐓 𝐁𝐥𝐚𝐜𝐤 𝐒𝐞𝐫𝐢𝐞𝐬 𝐏 𝐨𝐧𝐞 𝐄𝐝𝐢𝐭𝐢𝐨𝐧

𝐃𝐞𝐬𝐜𝐫𝐢𝐛𝐞 𝐭𝐡𝐞𝐦 𝐢𝐧 𝐎𝐍𝐄 𝐰𝐨𝐫𝐝👇🏼

#mercedes #benz #mercedesamg #carshow #dubaicars
"""

title_corpus = [
    "The _ of Automotive Excellence",
    "Unleashing the _ Power of _",
    "Redefining _ on Wheels",
    "Pushing the Boundaries of _",
    "Crafted for the _ Connoisseurs",
    "A _ Masterpiece of Engineering",
    "The _ Pinnacle of _",
    "Where _ Meets Passion",
    "Elevating the _ Driving Experience",
    "The Future of _ Mobility",
    "The Art of _ Performance",
    "_ Elegance Redefined",
    "The _ Standard of Luxury",
    "Breaking the Rules of _",
    "The _ Revolution Begins Here",
    "Uncompromising _ and Style",
    "The _ Icon of the Road",
    "Blazing the Trail of _",
    "The _ Fusion of Form and Function",
    "Unleashing the _ Beast Within",
]

generated_title = generate_title(description, title_corpus)
print(generated_title)
