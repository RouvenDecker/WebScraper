import argparse
import os
from pathlib import Path


from webscraper import Webscraper


parser = argparse.ArgumentParser()
parser.add_argument(
    "-u",
    "--url",
    required=True,
    help="target url webpage"
)

parser.add_argument(
    "-i",
    "--image",
    action="store_true",
    help="download all images from webpage"
)

parser.add_argument(
    "-t",
    "--text",
    action="store_true",
    help="dowload all text from webpage"
)

parser.add_argument(
    "-l",
    "--links",
    action="store_true",
    help="download all links from webpage"
)

args = parser.parse_args()

image = args.image
text = args.text
url = args.url
links = args.links
folder = Path("data")


def main():
    print(f"image: {image}")
    print(f"text: {text}")
    print(f"target url: {url}")
    print(f"folder {folder}")

    if not os.path.exists(folder):
        os.makedirs(folder)

    scraper = Webscraper(url)

    if image:
        img_folder = Path("images")
        if not os.path.exists(img_folder):
            os.makedirs(img_folder)
        scraper.scrape_images(img_folder)

    if text:
        scraper.scrape_text(folder)

    if links:
        url_folder = Path("url")
        if not os.path.exists(url_folder):
            os.makedirs(url_folder)
        scraper.scrape_links(url_folder)


if __name__ == "__main__":
    main()
