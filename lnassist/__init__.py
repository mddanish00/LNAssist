import shutil
from pathlib import Path

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
    """
    Request url.
    """
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print('For some reason, the content cannot be fetched from Internet.')
        print('- Check your internet connection.')
        print('- Check if your url provided is valid.')
        print('Error: ' + e)
        return exit(2)  # No internet connection exit code

    return response


def if_only_true(*args):
    """
    Check if only one flags is True.
    """
    found = False
    already_found = False
    for it in args:
        if it is True:
            found = True
            if already_found is True:
                found = False
                break
            else:
                already_found = True

    return found


def create():
    """
    Create a new instance of ln object.
    """
    return LNAssist()


class LNAssist:
    def __init__(self):
        self.series: str = 'None'  # Current series's short name. Example: Otomege
        self.full_series: str = 'None'  # Current series's full name.
        # Example: The World of Otome Games is Tough For Mobs
        self.vol: int = 0  # Current volume
        self.chp_tasks_list = []  # List of chapter tasks
        self.img_tasks_list = []  # List of img tasks
        self.path: Path = Path('files')  # Current working path; use only if none series specified

    def set_series(self, short_name: str, full_name: str, volume: str):
        """
        Set the current series and the current volume numbering.

        Arguments:
        ser -- short name of the series
        full_ser -- full name of the series
        vl -- the current vol count
        """
        self.full_series: str = full_name
        self.series: str = short_name.lower()  # convert to lower case
        self.vol: int = volume
        self.path: Path = self.path / self.series / 'vol' / str(self.vol)
        # self.path: Path = Path('files' + '/' + self.series + '/' + 'vol' + str(self.vol))
        # self.path = 'files' + '/' + self.series + '/' + 'vol' + str(self.vol)
        text = str(full_name) + ' Volume ' + str(volume)
        print(text)
        x = 0
        while x < len(text):
            print('-', end='')
            x = x + 1
        print('')

    def add(self, url: str, chapter: float = 0, prologue: bool = False, epilogue: bool = False, afterword: bool = False,
            illustrations: bool = False, extra: bool = False, sidestory: bool = False, interlude: bool = False):
        """
        Add a task into the queue.

        Arguments:
        url -- Current task url
        chapter -- Current task chapter count. Optional.

        Flags:
        prologue -- if current task chapter is prologue
        epilogue -- if current task chapter is epilogue
        afterword -- if current task chapter is afterword
        extra -- if current task chapter is extra
        sidestory -- if current task chapter is side story
        interlude -- if current task chapter is interlude
        illustrations -- if current task is for illustrations
        """
        if illustrations is False:
            if prologue or epilogue or afterword or extra or sidestory or interlude:
                if if_only_true(prologue, epilogue, afterword, extra, sidestory, interlude) is False:
                    print('Only one of these flags (prologue, epilogue, afterword, extra, sidestory, interlude) can be '
                          'enabled at one time.')
                    return
            self.chp_tasks_list.append(Task(url, chapter, prologue=prologue, epilogue=epilogue, afterword=afterword,
                                            extra=extra, sidestory=sidestory, interlude=interlude))
        else:
            self.img_tasks_list.append(Task(url, illustrations=illustrations))

    def run(self):
        """
        Run all the added tasks.
        """
        if len(self.chp_tasks_list) is 0 and len(self.img_tasks_list) is 0:
            print("No task available. Please add task first.")

        if len(self.chp_tasks_list) is not 0:
            for x in tqdm(self.chp_tasks_list, "Executing chapter tasks  ", unit="tsk"):
                x: Task
                self.extract_chapter(x.url, x.chapter, x.prologue, x.epilogue, x.afterword, x.extra, x.sidestory,
                                     x.interlude)  # chapter
            self.chp_tasks_list.clear()

        if len(self.img_tasks_list) is not 0:
            for x in self.img_tasks_list:
                x: Task
                self.extract_img(x.url)  # image task
            self.img_tasks_list.clear()

    def clear(self, all: bool = False):
        """
        Clear the current path according the current series.

        Optional:
        all -- True if you want to delete entire files directory instead of current path. Default is False.
        """
        if all is True:
            current = Path('files')
        else:
            current = self.path

        if current.is_dir():
            shutil.rmtree(current)
            print('Current folder cleared!')
        else:
            print('Current path not exist or already cleared!')

    def extract_chapter(self, url: str, chapter: float = 0, prologue: bool = False, epilogue: bool = False,
                        afterword: bool = False, extra: bool = False, sidestory: bool = False, interlude: bool = False):
        """
        Extract chapter text from the url and repackages into an xhtml for EPUB.

        Arguments:
        url -- Current url
        chapter -- Current chapter count. Optional.

        Flags:
        prologue -- if current chapter is prologue
        epilogue -- if current chapter is epilogue
        afterword -- if current chapter is afterword
        extra -- if current chapter is extra
        sidestory -- if current chapter is side story
        interlude -- if current chapter is interlude
        """
        if prologue or epilogue or afterword or extra or sidestory or interlude:
            if if_only_true(prologue, epilogue, afterword, extra, sidestory, interlude) is False:
                print('Only one of these flags (prologue, epilogue, afterword, extra, sidestory, interlude) can be '
                      'enabled at one time.')
                return

        if prologue is True:
            file_name = 'prologue.xhtml'
        elif epilogue is True:
            file_name = 'epilogue.xhtml'
        elif afterword is True:
            file_name = 'afterword.xhtml'
        elif extra is True and chapter is 0:
            file_name = 'extra.xhtml'
        elif extra is True:
            file_name = 'extra' + str(chapter) + '.xhtml'
        elif sidestory is True and chapter is 0:
            file_name = 'ss.xhtml'
        elif sidestory is True:
            file_name = 'ss' + str(chapter) + '.xhtml'
        elif interlude is True and chapter is 0:
            file_name = 'interlude.xhtml'
        elif interlude is True:
            file_name = 'interlude' + str(chapter) + '.xhtml'
        else:
            file_name = 'chp' + str(chapter) + '.xhtml'

        response = request_url(url)

        doc = Document(response.text)
        soup = BeautifulSoup(doc.summary(), "xml")
        soup.html['xmlns'] = 'http://www.w3.org/1999/xhtml'
        soup.html['xmlns:epub'] = 'http://www.idpf.org/2007/ops'
        # The tags that necessary for EPUB xhtml files

        chapter_path = self.path / 'chapters'
        if not chapter_path.is_dir():
            chapter_path.mkdir(parents=True)

        chapter_path = chapter_path / file_name
        chapter_path.write_text(soup.prettify(), encoding='UTF-8')
        # file = open(chapter_path, 'w', encoding='UTF-8')
        # file.write(soup.prettify())
        # file.close()

    def extract_img(self, url):
        """
        Fetch image links from the given url and download the links.

        Arguments:
        url -- Current url
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
        Downloads a image given an URL and puts it in the current path.

        Arguments:
        url -- Current url
        """
        pathname = self.path / "illustrations"
        buffer_size = 1024
        if not pathname.is_dir():
            pathname.mkdir(parents=True)

        response = requests.get(url, stream=True)
        filename = pathname / url.split("/")[-1]
        # filename = os.path.join(pathname, url.split("/")[-1])
        with filename.open("wb") as f:
            for chunk in response.iter_content(buffer_size):
                if chunk:
                    f.write(chunk)

            f.close()


ln = LNAssist()  # for use


class Task:
    def __init__(self, url: str, chapter: float = 0, prologue: bool = False, epilogue: bool = False,
                 afterword: bool = False, illustrations: bool = False, extra: bool = False, sidestory: bool = False,
                 interlude: bool = False):
        self.chapter = chapter
        self.url = url
        self.prologue = prologue
        self.epilogue = epilogue
        self.afterword = afterword
        self.extra = extra
        self.sidestory = sidestory
        self.interlude = interlude
        self.illustrations = illustrations
