"""Retrieve and preprocess magic card images."""
import argparse
import download
import transform

PARSER = argparse.ArgumentParser()
PARSER.add_argument("-d",
                    "--deck-yml",
                    default=download.DEFAULT_DECK_YAML_PATH,
                    help="Path to a YAML file defining a deck"
                    + "(default: %(default)s)")
PARSER.add_argument("-o",
                    "--output-dir",
                    default=download.DEFAULT_OUTPUT_PATH,
                    help="Path to store the downloaded and transformed images"
                    + "(default: %(default)s)")
ARGS = PARSER.parse_args()

DECK = download.load_deck(download.DEFAULT_DECK_YAML_PATH)
download.download_deck(DECK, download.DEFAULT_OUTPUT_PATH)
transform.rotate_images(download.DEFAULT_OUTPUT_PATH)
