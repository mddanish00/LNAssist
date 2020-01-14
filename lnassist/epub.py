from zipfile import ZipFile


class Epub:
    def __init__(self, name):
        self.chapter = []
        self.illustration = []
        self.template = ZipFile('template.epub')
        self.template.extractall('temp/template')
        self.epub = ZipFile(name + '.epub', 'w')

