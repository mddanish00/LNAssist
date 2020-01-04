# LNAssist
LNAssist is a Python module that  used to scrap fan translations website for text and illustrations for fan EPUB creating purposes.
## Features
- Fetch text only and compile it into EPUB-friendly format webpage, XHTML.
- Fetch high-quality illustrations from illustration page.
- Possible to run the above tasks in batch.
- Fetch links from table of content and insert into a batch for running the above tasks. (Not yet implemented)

## Installation
Only Python 3.7 supported. Another version may or may not work.

```
setup.py install
```

## Usage
Usage Example
```
from LNAssist import LNAssist

ln = LNAssist
ln.set_series('otomege', 'The World of Otome Games is Tough For Mobs', 4)

ln.extract_img('http://xxxxxxxxx/illustrations', image=True)
ln.extract_chapter(4, 'http://xxxxxxxxx/c4', epilogue=True)
ln.extract_chapter(4, 'http://xxxxxxxxx/c2')

ln.add('http://xxxxxxxxx/c2',2)
ln.add('http://xxxxxxxxx/illustrations',image=True)
ln.run()

```

### Set Series and Volume
```
ln.set_series(short name, full name, vol)
```
Fill in the short name, full name and the volume in the function. 

This function is used to assign the file created 
and download after this in the appropriate folder. You have to run this function every time the current series that 
you work changed.

Default path: files/

Change path: files/short name/vol/

### Working with only one task

#### Chapter
```
ln.extract_chapter(chapter, url, *epilogue)
```
Fill in chapter and the url. 

The optional value is epilogue, True only if the current chapter is epilogue. 
Default value is False.

The generated XHTML will be in: current_path/chapters/

#### Illustrations
```
ln.extract_img(url)
```
Fill the url of the illustration page.

The downloaded illustrations will be in: current_path/illustrations/

### Working with many tasks

#### Add task
```
ln.add(url,*chapter,*epilogue,*image)
```
Fill in the url of the page that you want to be scrapped or download.
The optional value is chapter, epilogue and image. 

Set chapter value if the url is for chapter.

Set epilogue to True if the current task is epilogue chapter.

Set image to True if the current task is for illustrations.

#### Run all tasks
```
ln.run()
```
The function will run all the tasks added.

### Clear all files
```
ln.clear()
```
This function will clear all files in the current path.

Default path: files/

Change path: files/short name/vol/