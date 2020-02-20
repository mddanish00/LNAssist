import uuid

from bs4 import BeautifulSoup
from datetime import datetime


def content_opf(full_title='[Main title here]'):
    """""content.opf default template
    """
    soup = BeautifulSoup(features='xml')

    package = soup.new_tag('package')
    package['version'] = '3.0'
    package['unique-identifier'] = 'book_id'
    package['xmlns'] = 'http://www.idpf.org/2007/opf'

    metadata = soup.new_tag('metadata')
    metadata['xmlns:dc'] = 'http://purl.org/dc/elements/1.1/'
    language = soup.new_tag('dc:language')
    language.append('en')
    # urn:uuid:5c8a0bb7-bbc9-4273-aa5b-7c586b84bf3e
    identifier = soup.new_tag('dc:identifier', id='book_id')
    identifier.append('urn:uuid:' + str(uuid.uuid4()))
    title = soup.new_tag('dc:title')
    title.append(full_title)
    meta_td = soup.new_tag('meta', property='dcterms:modified')
    date = datetime.now()
    # 2020-02-11T22:03:36Z
    date = date.strftime('%Y-%m-%dT%H:%M:%SZ')
    meta_td.append(date)
    metadata.append(language)
    metadata.append(identifier)
    metadata.append(title)
    metadata.append(meta_td)
    package.append(metadata)

    manifest = soup.new_tag('manifest')
    item1 = soup.new_tag('item', id='sgc-nav.css', href='Styles/sgc-nav.css')
    item1['media-type'] = 'text/css'
    item2 = soup.new_tag('item', id='nav.xhtml', href='Text/nav.xhtml', properties='nav')
    item2['media-type'] = 'application/xhtml+xml'
    manifest.append(item1)
    manifest.append(item2)
    package.append(manifest)

    spine = soup.new_tag('spine')
    itemref = soup.new_tag('itemref', idref='nav.xhtml', linear='no')
    spine.append(itemref)
    package.append(spine)

    soup.append(package)
    return soup


def container_xml():
    """""container.xml default template
    """
    soup = BeautifulSoup(features='xml')
    container = soup.new_tag('container', version='1.0', xmlns='urn:oasis:names:tc:opendocument:xmlns:container')
    rootfiles = soup.new_tag('rootfiles')
    rootfile = soup.new_tag('rootfile')
    rootfile['full-path'] = 'OEBPS/content.opf'
    rootfile['media-type'] = 'application/oebps-package+xml'
    rootfiles.append(rootfile)
    container.append(rootfiles)

    soup.append(container)
    return soup


def nav_xhtml():
    """""nav.xhtml default template
    """
    nav = '<?xml version="1.0" encoding="utf-8"?><!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" ' \
          'xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en"><head><title></title>' \
          '<meta charset="utf-8" /><link href="../Styles/sgc-nav.css" rel="stylesheet" type="text/css"/></head>' \
          '<body epub:type="frontmatter"><nav epub:type="toc" id="toc"><h1>Table of Contents</h1><ol><li></li></ol>' \
          '</nav><nav epub:type="landmarks" id="landmarks" hidden=""><h2>Landmarks</h2><ol><li>' \
          '<a epub:type="toc" href="#toc">Table of Contents</a></li></ol></nav></body></html>'

    soup = BeautifulSoup(nav, 'xml')
    return soup


def mimetype():
    """""mimetype default template
    """
    mime = 'application/epub+zip'
    return mime


def nav_css():
    """""nav.css default template
    """
    css = 'nav#landmarks {display:none;} ' \
          'nav#page-list {display:none;}' \
          'ol {list-style-type: none;}'

    return css
