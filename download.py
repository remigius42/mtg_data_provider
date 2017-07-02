"""Download all images for cards specified in DEFAULT_DECK_YAML_PATH."""

import os.path
import pickle
import urllib.request
import warnings
from joblib import Parallel, delayed
import yaml
from mtgsdk import Card

DEFAULT_DECK_YAML_PATH = "deck.yml"
DEFAULT_OUTPUT_PATH = "data"
DEFAULT_DECK_SET = "Revised Edition"
MAX_CARD_NAME_LENGTH = 42
QUERY_RESULT_CACHE_PICKLE_PATH = "query_result.pickle"

def load_deck(yaml_path):
    """Load magic deck from YAML file at yaml_path."""
    with open(yaml_path) as deck_file:
        deck = yaml.load(deck_file)
        return deck

def _card_to_path(card, output_path):
    """Generate a file name for a card."""
    return "{0}/{1}/{1}_{2}_base.jpg".format(output_path,
                                             card.name[0:MAX_CARD_NAME_LENGTH],
                                             card.multiverse_id)

def _download_card_image(card, output_path):
    """Download the image of a magic card."""
    if not card.image_url is None:
        dest_dir = output_path + "/" + card.name[0:MAX_CARD_NAME_LENGTH]
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)
        urllib.request.urlretrieve(card.image_url,
                                   _card_to_path(card, output_path))

def _handle_card(card_data, output_path):
    """Look for card in database and download all card images found."""
    cards_found = Card.where(set_name=DEFAULT_DECK_SET,
                             name=card_data['name'],
                             artist=card_data['artist']).all()
    if not cards_found:
        warnings.warn("No cards found for: " + card_data)

    for card in cards_found:
        _download_card_image(card, output_path)

def _download_cards(cards, output_path):
    """Iterate in parallel over the cards and call handle_card for each."""
    Parallel(n_jobs=-2)(delayed(_handle_card)(card_data, output_path)
                        for card_data in cards)

def download_deck(deck, output_path):
    """Download images for a given deck."""
    _download_cards(deck['cards'], output_path)

def _pickle_query_result(query_result):
    with open(QUERY_RESULT_CACHE_PICKLE_PATH, "wb") as pickle_file:
        pickle.dump(query_result, pickle_file, pickle.HIGHEST_PROTOCOL)

def download_set(query_set_name, output_path, use_cache=True):
    """Download images for a given set name."""
    if use_cache and os.path.isfile(QUERY_RESULT_CACHE_PICKLE_PATH):
        with open(QUERY_RESULT_CACHE_PICKLE_PATH, "rb") as pickle_file:
            cards_found = pickle.load(pickle_file)
    else:
        cards_found = Card.where(set_name=query_set_name).all()

    if use_cache:
        _pickle_query_result(cards_found)

    Parallel(n_jobs=-2)(delayed(_download_card_image)(card, output_path)
                        for card in cards_found)


if __name__ == '__main__':
    #DECK = load_deck(DEFAULT_DECK_YAML_PATH)
    #download_deck(DECK, DEFAULT_OUTPUT_PATH)
    download_set("Revised Edition", DEFAULT_OUTPUT_PATH)
