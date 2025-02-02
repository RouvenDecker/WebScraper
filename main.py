import argparse
from webscraper import Webscraper


parser = argparse.ArgumentParser()
parser.add_argument(
    "-u",
    "--url",
    required=True,
    help="target url webpage"
)

parser.add_argument(
    "-f",
    "--folder",
    help="download folder"
)


parser.add_argument(
    "-i",
    "--image",
    action="store_true",
    help="download all images of the webpage"
)

parser.add_argument(
    "-t",
    "--text",
    action="store_true",
    help="dowload all text of the webpage"
)

parser.add_argument(
    "-l",
    "--links",
    action="store_true",
    help="download all links on the webpage"
)

args = parser.parse_args()

image = args.image
text = args.text
url = args.url
links = args.links
folder = args.folder if args.folder else "data/data.txt"


def main():
    print(f"image: {image}")
    print(f"text: {text}")
    print(f"target url: {url}")
    print(f"folder {folder}")
    scraper = Webscraper(url)

    if image:
        img_folder = "data/"
        scraper.scrape_images(img_folder)

    if text:
        scraper.scrape_text(folder)

    if links:
        url_folder = "url"
        scraper.scrape_links(url_folder)


if __name__ == "__main__":
    main()
