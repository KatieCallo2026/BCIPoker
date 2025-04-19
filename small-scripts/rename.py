import os

# Path to your card images
card_dir = "./server-display/static/cards"

# Mapping of suits
suit_map = {
    "spades": "S",
    "hearts": "H",
    "diamonds": "D",
    "clubs": "C"
}

# Mapping of ranks
rank_map = {
    "ace": "A",
    "2": "2", "3": "3", "4": "4", "5": "5",
    "6": "6", "7": "7", "8": "8", "9": "9",
    "10": "10",
    "jack": "J",
    "queen": "Q",
    "king": "K"
}

# Loop through files
for filename in os.listdir(card_dir):
    if filename.endswith(".png") and "_of_" in filename:
        name = filename.replace(".png", "")
        rank_str, suit_str = name.split("_of_")
        rank = rank_map.get(rank_str.lower())
        suit = suit_map.get(suit_str.lower())
        if rank and suit:
            new_name = f"{rank}{suit}.png"
            old_path = os.path.join(card_dir, filename)
            new_path = os.path.join(card_dir, new_name)
            os.rename(old_path, new_path)
            print(f"✅ Renamed: {filename} → {new_name}")
