from bs4 import BeautifulSoup
from pathlib import Path
import requests
import re
import shutil


class Webscraper:
    def __init__(self, url: str):
        self.url = url

    def scrape_text(self, folder: Path):
        """scrape all text of the webpage and store it at "folder" as data.txt

        Args:
            folder (str): data folder
        """
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        tags = soup.find_all(["p", "li"])

        with open(folder / "data.txt", "w") as f:
            for tag in tags:
                bunch = tag.get_text()
                bunch = self._newline_every_n_sentences(bunch, 2)
                f.write(bunch)

    def scrape_images(self, folder: Path):
        """scrape all images of a website and store them in "folder"

        Args:
            folder (str): data folder to store the images
        """
        print("URL: ", self.url)
        response = requests.get(self.url).text
        soup = BeautifulSoup(response, "html.parser")
        for i, item in enumerate(soup.find_all("img")):

            img_url = item["src"]
            print(f"Raw Imageurl: {img_url}")
            img_url = self._make_start_with(img_url, self.url)
            img_url_ending = img_url.split(".")[-1]
            print(f"geparste Imageurl: {img_url}")

            res = requests.get(img_url, stream=True)
            print(f"request status: {res.status_code}")
            if res.status_code == 200:
                img_name = "image_" + str(i) + "." + img_url_ending
                full_name = folder / img_name
                with open(full_name, "wb") as f:
                    shutil.copyfileobj(res.raw, f)
                print(f"Image: {img_name} downloaded")
                print(img_url)
                print("")

    def scrape_links(self, folder: str):
        """scrape all urls of a website and store them in "folder"

        Args:
            folder (str): storage folder
        """
        response = requests.get(self.url)
        doc = BeautifulSoup(response.text, "html.parser")

        a_tags = doc.find_all("a")
        for a_tag in a_tags:
            try:
                with open(Path(folder) / "urls.txt", "a") as f:
                    f.write(str(a_tag["href"]) + "\n")
            except KeyError:  # noqa: PERF203
                continue

    def _newline_every_n_sentences(self, s: str, n: int) -> str:
        """add a \n character at the end of every n sentence

        Args:
            s (str): content
            n (int): sentence number

        Returns:
            str: transformed sentences
        """
        sentences = re.split("[.!?;]\\s+", s)
        for i in range(len(sentences)):
            if i % n == 0 or i == 0:
                sentences[i] = sentences[i] + "\n"
        return "".join(sentences)


    def _make_start_with(self, url: str, start):
        if not url.startswith(start):
            return start + url
        else:
            return url
