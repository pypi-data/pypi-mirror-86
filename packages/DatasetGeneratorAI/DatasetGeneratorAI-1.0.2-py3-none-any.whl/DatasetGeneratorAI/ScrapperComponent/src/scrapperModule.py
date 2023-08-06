import flickrapi
import requests
import io
import os

import tqdm
from tqdm.contrib import tenumerate

from concurrent.futures import ThreadPoolExecutor
from PIL import Image

class ScrapperModule:

    def __init__(self, label_name, page_size, flickr_api_key, flickr_secret):
        self.flickr = flickrapi.FlickrAPI(flickr_api_key, flickr_secret, cache=True)
        self.label_name = label_name
        self.page_size = page_size

        self.generator = self.flickr.walk(text=self.label_name,
                tag_mode='all',
                tags=self.label_name,
                extras='url_c',
                per_page=self.page_size,
                sort='relevance')

        self.urls = []
        self.last_picture = 0


    def search_download_exact(self, quantity_exact, dest_folder):
        total_imgs_downloaded = 0
                
        # Don't stop until the desired number of images has been downloaded
        while total_imgs_downloaded < quantity_exact:
            self.search(quantity_exact - total_imgs_downloaded)
            step_downloaded = self.download(quantity_exact - total_imgs_downloaded, dest_folder)
            total_imgs_downloaded += step_downloaded


    def search(self, quantity):
        pbar = tqdm.tqdm(total=quantity, desc="Searching for " + self.label_name + " pictures")

        for _ in range(quantity):
            url = None

            while url is None:
                try:
                    photo = next(self.generator)
                    url = photo.get('url_c')
                    pbar.update()
                except StopIteration:
                    pbar.close()
                    return

            self.urls.append(url)

        pbar.close()

    def download(self, quantity, dest_folder):
        os.makedirs(dest_folder, exist_ok=True)

        start_count = len(self.urls) - quantity
        urls_and_paths = [ ( url, os.path.join(dest_folder, self.label_name + "." + str(start_count + i) + ".jpg") ) for i, url in enumerate(self.urls[-quantity:]) ]

        pool = ThreadPoolExecutor(max_workers=10)
        results_generator = pool.map(self.download_task, urls_and_paths, timeout=None)

        results = []

        for r in tenumerate(results_generator, total=quantity, desc="Downloading " + self.label_name + " pictures"):
            results.append(r)

        return [r[1] for r in results].count(True)

    def download_task(self, url_path):
        try:
            res = requests.get(url_path[0], stream=True)
            count = 1
            while res.status_code != 200 and count <= 5:
                res = requests.get(url_path[0], stream=True)
                count += 1

            i = Image.open(io.BytesIO(res.content))
            i.save(url_path[1])

            return True
        except:
            return False