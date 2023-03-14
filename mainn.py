from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
from urllib.request import urlopen
import os

class TiktokDownloader:
    def __init__(self):
        pass

    def get_user_videos(self, user):
        # driver
        driver = webdriver.Chrome()

        page = f"https://www.tiktok.com/@{user}"  # page to be extracted
        driver.get(page)

        time.sleep(1)  # wait 1 second before closing browser

        # scroll down the page
        #self.scroll(driver)

        # PARSE HTML
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # locate video block with class
        videos = soup.find_all("div", {"class": "tiktok-yz6ijl-DivWrapper e1cg0wnj1"})

        driver.quit()  # close driver

        # iterate through each TikTok video link by parsing html and download
        for index, video in enumerate(videos):
            video_link = video.a["href"]
            self.download(video_link, f"Tiktok Video Number {index}")

            # after each download wait 15 seconds, to avoid spamming server(bot)
            time.sleep(15)

    def download(self, link, id):
        """Download from www.ssstik.io.com"""

        cookies = {
            '_ga': 'GA1.2.213704089.1678813265',
            '_gid': 'GA1.2.1176288011.1678813265',
            '__gads': 'ID=156d23c04b1b4625-227bfea431dc00e4:T=1678813265:RT=1678813265:S=ALNI_MYVcnxgKrqp1Md1M5n7IbFxrjjteg',
            '__gpi': 'UID=00000becebc1b741:T=1678813265:RT=1678813265:S=ALNI_Ma29-K9R_S04tQC80mt6gC6RBUYLg',
            '_gat_UA-3524196-6': '1',
        }

        headers = {
            'authority': 'ssstik.io',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'cookie': '_ga=GA1.2.213704089.1678813265; _gid=GA1.2.1176288011.1678813265; __gads=ID=156d23c04b1b4625-227bfea431dc00e4:T=1678813265:RT=1678813265:S=ALNI_MYVcnxgKrqp1Md1M5n7IbFxrjjteg; __gpi=UID=00000becebc1b741:T=1678813265:RT=1678813265:S=ALNI_Ma29-K9R_S04tQC80mt6gC6RBUYLg; _gat_UA-3524196-6=1',
            'hx-current-url': 'https://ssstik.io/en',
            'hx-request': 'true',
            'hx-target': 'target',
            'hx-trigger': '_gcaptcha_pt',
            'origin': 'https://ssstik.io',
            'referer': 'https://ssstik.io/en',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }

        params = {
            'url': 'dl',
        }

        data = {
            'id': link,
            'locale': 'en',
            'tt': 'YzZSUko0',
        }

        # make request to site from all the above
        response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)

        # parse response from "ssstik.io"
        parser = BeautifulSoup(response.text, "html.parser")
        download_link = parser.a["href"]  # get download link

        # mp4 file (binary)
        mp4File = urlopen(download_link)

        # write data to a new file
        with open(f"downloads/{id}.mp4", "wb") as file:
            while True:
                data = mp4File.read(4096)
                if data:
                    file.write(data)

                else:
                    break

    def scroll(self, driver):
        # Scroll on the page
        print("STEP 2: Scrolling page")
        scroll_pause_time = 1
        screen_height = driver.execute_script("return window.screen.height;")
        i = 1

        while True:
            driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
            i += 1
            time.sleep(scroll_pause_time)
            scroll_height = driver.execute_script("return document.body.scrollHeight;")
            if (screen_height) * i > scroll_height:
                break

    def delete_all_files(self):
        directory = "downloads"  # replace with your directory path

        for filename in os.listdir(directory):
            if filename.endswith(".mp4"):  # all mp4 is deleted
                os.remove(os.path.join(directory, filename))


api = TiktokDownloader()
api.get_user_videos("yeonsaw")


#d = TiktokVid()
#d.download("h", "r")