import markovify
import json
import time
from sklearn.feature_extraction.text import TfidfVectorizer
import re


class TiktokCaption:

    best_caption = {
        "caption": None,
        "similarity": 0,
    }

    def __init__(self, caption: str):
        self.caption = caption
        with open("../data/scraped_results.json", "r") as scraped_results:
            self.ds = json.load(scraped_results)
            print(len(self.ds))

        self.generated_caption = self.generate_caption()

    def generate_caption(self):
        text_model = markovify.NewlineText(self.ds)

        # First loop for indefinite iteration until title is relevant
        # Second loop is for succesfull sentence generation
        title = None
        while not title:
            candidate = None
            while not candidate:
                candidate = text_model.make_sentence(
                    max_overlap_ratio=0.8, min_words=11, max_words=23
                )
            if self.is_relevant(candidate):
                title = candidate

        return title

    def is_relevant(self, candidate):
        # Preprocess the captions
        candidate = self.preprocess(candidate)
        input_caption = self.preprocess(self.caption)

        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([input_caption, candidate])

        # Calculate cosine similarity
        similarity = vectors.tocsr()[0].dot(vectors.tocsr()[1].T)[0, 0]
        if similarity > self.best_caption["similarity"]:
            self.best_caption = {
                "caption": candidate,
                "similarity": similarity,
            }
            print(self.best_caption)

        # Check if the similarity exceeds a threshold
        threshold = 0.3
        return similarity >= threshold

    def preprocess(self, text):
        # Remove special characters and convert to lowercase
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text.lower())
        return text


if __name__ == "__main__":
    tiktok = TiktokCaption(
        """
                          Needed a couple days off but let’s get back into the grind.
.
.
.
.
.
.
.
.
Grateful for the support from
@badgeskins @cherrytuningperformance @anarchyautocare @socalgarageworks
#carphotography #automotivephotography #carswithoutlimits #cargram #rizz #life #brisbane #ncultr #photography #lowglow #black #sxthelement #n #30n #elantran #avanten #performance #hyundai #beautiful #livin #KDM #carsofinstagram #hothatch #carlife #cars #neverjustdrive #revs #shotbynthusiasts #hyundai #underground #newbeginnings
                           """
    )

    print(tiktok.generated_caption)
