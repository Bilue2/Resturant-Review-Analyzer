import json
import uuid

# File paths (confirmed)
CRIMSON_PATH = r"C:\Junia'sMainFolder\MyProjects\SSI_FineTuning\crimson_coward.json"
VOCELLI_PATH = r"C:\Junia'sMainFolder\MyProjects\SSI_FineTuning\vocelli_pizza.json"
OUTPUT_PATH = r"C:\Junia'sMainFolder\MyProjects\SSI_FineTuning\combined_corpus.json"

# Restaurant metadata
RESTAURANT_INFO = {
    "crimson_coward": {
        "restaurant_id": "crimson_coward_fairfax",
        "restaurant_name": "Crimson Coward",
        "restaurant_location": "Fairfax, VA"
    },
    "vocelli_pizza": {
        "restaurant_id": "vocelli_pizza_fredericksburg",
        "restaurant_name": "Vocelli Pizza",
        "restaurant_location": "Fredericksburg, VA"
    }
}

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_chunk_id(review_index):
    return f"r{review_index:05d}-c00"

def generate_review_id(review_index):
    return f"r{review_index:05d}"

def reformat_reviews(reviews, restaurant_key, start_index):
    formatted = []
    meta = RESTAURANT_INFO[restaurant_key]

    for i, review in enumerate(reviews, start=start_index):
        formatted.append({
            "chunk_id": generate_chunk_id(i),
            "restaurant_id": meta["restaurant_id"],
            "restaurant_name": meta["restaurant_name"],
            "restaurant_location": meta["restaurant_location"],
            "review_id": generate_review_id(i),
            "rating": review.get("rating"),
            "sentiment": review.get("sentiment"),
            "themes": review.get("themes", []),
            "text": review.get("text")
        })

    return formatted

def main():
    # Load original corpora
    crimson_reviews = load_json(CRIMSON_PATH)
    vocelli_reviews = load_json(VOCELLI_PATH)

    # Reformat and merge
    combined = []
    index = 1

    combined += reformat_reviews(crimson_reviews, "crimson_coward", index)
    index += len(crimson_reviews)

    combined += reformat_reviews(vocelli_reviews, "vocelli_pizza", index)

    # Save output
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    print(f"Combined corpus saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
