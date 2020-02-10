from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED
from pathlib import Path
from bs4 import Tag
from lnassist.epubtemplate import container_xml, content_opf, nav_css, mimetype, nav_html

output_path = Path('out')


def check_dir(pth: Path):
    if not pth.is_dir():
        pth.mkdir(parents=True)


class Epub:
    def __init__(self, name: str, pth: Path = Path('files')):
        self.chapter = []
        self.illustration = []
        check_dir(output_path)
        filename = name + '.epub'
        filename = output_path / filename
        self.epub = ZipFile(filename, 'w', ZIP_DEFLATED)
        self.file_path = pth

    def addall(self, chapter=True, illus=True):
        chp = self.file_path / 'chapters'
        ill = self.file_path / 'illustrations'

        if chp.is_dir() is False and chapter is True:
            print('No chapters available. Scrap chapters first.')
            return

        if ill.is_dir() is False and illus is True:
            print('No illustrations available. Scrap illustrations first.')
            return

        for ch in chp.glob('**/*.xhtml'):
            self.chapter.append(ch)

        for il in ill.iterdir():
            self.illustration.append(il)

    def output(self):
        soup_cont = content_opf()
        manifest_tag = soup_cont.manifest
        manifest_tag: Tag
        spine_tag = soup_cont.spine
        spine_tag: Tag
        chp_path = Path('OEBPS/Text')
        img_path = Path('OEBPS/Images')
        self.epub.writestr('mimetype', mimetype(), ZIP_STORED)
        self.epub.writestr('META-INF/container.xml', container_xml().prettify(), ZIP_DEFLATED)
        self.epub.writestr('OEBPS/Styles/sgc-nav.css', nav_css(), ZIP_DEFLATED)
        self.epub.writestr('OEBPS/Text/nav.xhtml', nav_html().prettify(), ZIP_DEFLATED)

        for chp in self.chapter:
            chp: Path
            chp_path_cont = chp_path / chp.name
            self.epub.write(chp, chp_path_cont, ZIP_DEFLATED)
            new_m_tag = soup_cont.new_tag("item", id=chp.name, href='Text/' + chp.name)
            new_m_tag['media-type'] = 'application/xhtml+xml'
            manifest_tag.append(new_m_tag)
            new_s_tag = soup_cont.new_tag('itemref', idref=chp.name)
            spine_tag.append(new_s_tag)

        for img in self.illustration:
            img: Path
            img_path_cont = img_path / img.name
            self.epub.write(img, img_path_cont, ZIP_DEFLATED)
            new_m_tag = soup_cont.new_tag("item", id=img.name, href='Images/' + img.name)
            if img.name.find('png'):
                new_m_tag['media-type'] = 'image/png'
            else:
                new_m_tag['media-type'] = 'image/jpeg'
            manifest_tag.append(new_m_tag)

        self.epub.writestr('OEBPS/content.opf', soup_cont.prettify(), ZIP_DEFLATED)
        self.epub.close()
