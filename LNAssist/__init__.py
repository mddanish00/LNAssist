import os
import shutil

import requests
from bs4 import BeautifulSoup
from readability import Document
from tqdm import tqdm


def is_valid(url):
    """
    Check if the url is valid
    """
    parsed = requests.utils.urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def is_image(url):
    """
    Check if the image url is in known file format
    """
    if url.find(".png") == url.find(".jpg") == url.find(".gif") == url.find(".jpeg"):
        return False
    else:
        return True


def is_absolute(url):
    """
    Check if the url is absolute path
    """
    return bool(requests.utils.urlparse(url).netloc)


def request_url(url):
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print('For some reason, the content cannot be fetched from Internet.')
        print('- Check your internet connection.')
        print('- Check if your url provided is valid.')
        print('Error: ', end='')
        print(e)
        return exit(2)  # No internet connection exit code

    return response


class LNAssist:
    def __init__(self):
        self.series: str = 'None'  # Current series's short name. Example: Otomege
        self.full_series: str = 'None'  # Current series's full name.
        # Example: The World of Otome Games is Tough For Mobs
        self.vol: int = 0  # Current volume
        self.chp_tasks_list = []  # List of chapter tasks
        self.img_tasks_list = []  # List of img tasks
        self.path: str = 'files'  # Current working path; use only if none series specified

    def set_series(self, ser: str, full_ser: str, vl: str):
        """
        Set the current series and the volume
        ser: short name of the series
        full_ser: full name of the series
        vl: the current vol count
        """
        # global series, full_series, vol
        self.full_series = full_ser
        self.series = ser.lower()  # convert to lower case
        self.vol = vl
        self.path = 'files' + '/' + self.series + '/' + 'vol' + str(self.vol)
        text = str(full_ser) + ' Volume ' + str(vl)
        print(text)
        x = 0
        while x < len(text):
            print('-', end='')
            x = x + 1
        print('')

    def add(self, url: str, chapter: float = 0, epilogue: bool = False, image: bool = False):
        """
        Add a task into the queue
        url: url of new task
        chapter: the current chapter count; chapter 0 is count as prologue
        epilogue: flag if this chapter is epilogue or not
        image: flag if this task is for image
        """
        if image is False:
            self.chp_tasks_list.append(Task(chapter, url, epilogue, image))
        else:
            self.img_tasks_list.append(Task(chapter, url, epilogue, image))

    def run(self):
        """
        Run all the added tasks
        """
        if len(self.chp_tasks_list) is 0 and len(self.img_tasks_list) is 0:
            print("No task available. Please add task first.")

        if len(self.chp_tasks_list) is not 0:
            for x in tqdm(self.chp_tasks_list, "Executing chapter tasks  ", unit="tk"):
                x: Task
                self.extract_chapter(x.chapter, x.url, x.epilogue)  # chapter
                self.chp_tasks_list.remove(x)

        if len(self.img_tasks_list) is not 0:
            for x in self.img_tasks_list:
                x: Task
                self.extract_img(x.url)  # image task
                self.img_tasks_list.remove(x)

    def clear(self):
        """
        Clear the current working folder according the current series
        """
        if os.path.exists(self.path):
            shutil.rmtree(self.path)
            print('Current folder cleared!')

    def extract_chapter(self, chapter: float, url: str, prologue: bool = False, epilogue: bool = False):
        """
        Extract chapter text from the url and repackages into an xhtml for EPUB
        chapter: the current chapter count; chapter 0 is count as prologue
        url: url of new task
        epilogue: flag if this chapter is epilogue or not
        """
        if prologue is True:
            file_name = 'prologue.xhtml'
        elif epilogue is True:
            file_name = 'epilogue.xhtml'
        else:
            file_name = 'chp' + str(chapter) + '.xhtml'

        response = request_url(url)

        doc = Document(response.text)
        soup = BeautifulSoup(doc.summary(), "xml")
        soup.html['xmlns'] = 'http://www.w3.org/1999/xhtml'
        soup.html['xmlns:epub'] = 'http://www.idpf.org/2007/ops'
        # The tags that necessary for EPUB xhtml files

        if not os.path.isdir(self.path + '/' + 'chapters'):
            os.makedirs(self.path + '/' + 'chapters')

        file = open(self.path + '/' + 'chapters' + '/' + file_name, 'w',
                    encoding='UTF-8')
        file.write(soup.prettify())
        file.close()

    def extract_img(self, url):
        """
        Process image task. Fetch links from the given url and download the image
        url: url of current image task
        """
        response = request_url(url)

        soup = BeautifulSoup(response.content, "lxml")
        urls = []
        for img in tqdm(soup.find_all("img"), "Extracting images links  ", unit="img"):
            img_url = img.attrs.get("src")
            if not img_url:
                continue

            if not is_image(img_url):
                continue

            if not is_absolute(img_url):
                img_url = requests.sessions.urljoin(url, img_url)

            try:
                pos = img_url.index("?")
                img_url = img_url[:pos]
            except ValueError:
                pass

            if is_valid(img_url):
                urls.append(img_url)

        for img in tqdm(urls, "Downloading images       ", unit="img"):
            self.download_img(img)

    def download_img(self, url):
        """
        Downloads a file given an URL and puts it in the folder `pathname`
        url: url of current image task
        """
        pathname = self.path + '/' + "illustrations"
        buffer_size = 1024
        if not os.path.isdir(pathname):
            os.makedirs(pathname)
        response = requests.get(url, stream=True)
        filename = os.path.join(pathname, url.split("/")[-1])
        with open(filename, "wb") as f:
            for chunk in response.iter_content(buffer_size):
                if chunk:
                    f.write(chunk)


ln = LNAssist()  # for use


class Task:
    def __init__(self, chapter: float, url: str, epilogue: bool, image: bool):
        self.chapter = chapter
        self.url = url
        self.epilogue = epilogue
        self.image = image
