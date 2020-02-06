# LNAssist
LNAssist is a Python module that  used to scrap fan translations website for text and illustrations for fan EPUB creating purposes.
## Features
- Fetch text only and compile it into EPUB-friendly format web page, XHTML.
- Fetch high-quality illustrations from illustration page.
- Possible to run the above tasks in batch.
- Fetch links from table of content and insert into a batch for running the above tasks. (Not yet implemented)

## Installation
Only Python 3.7 supported. Another version may or may not work.

Installation instructions is on Releases.

## Usage
Usage Example

*Only can be applied for the latest release, not the current development version.
```
from lnassist import ln

ln.set_series('otomege', 'The World of Otome Games is Tough For Mobs', 4)

ln.extract_img('http://xxxxxxxxx/illustrations', image=True)
ln.extract_chapter('http://xxxxxxxxx/v4prologue', 4, prologue=True)
ln.extract_chapter('http://xxxxxxxxx/v4epilogue', 5, epilogue=True)
ln.extract_chapter('http://xxxxxxxxx/v4c2', 2)

ln.add('http://xxxxxxxxx/v4c2',2)
ln.add('http://xxxxxxxxx/v4illustrations',image=True)
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
ln.extract_chapter(url, chapter, *prologue, *epilogue, *afterword, *extra, *sidestory, *interlude)
```
Extract chapter text from the url and repackages into an xhtml for EPUB.

Available flags: prologue, epilogue, afterword, extra, sidestory, interlude

Default value is False.

The generated XHTML will be in: current_path/chapters/

#### Illustrations
```
ln.extract_img(url)
```
Fetch image links from the given url and download the links.

The downloaded illustrations will be in: current_path/illustrations/

### Working with many tasks

#### Add task
```
ln.add(url, *chapter, *prologue, *epilogue, *afterword, *extra, *sidestory, *interlude, *image)
```
Add a task into the queue.

Set illustrations to True if only the current task is intended for illustrations.

Available flags: prologue, epilogue, afterword, extra, sidestory, interlude

Only one of the flags can active in one time.

#### Run all tasks
```
ln.run()
```
Run all the added tasks.

## Advanced

### Clear all files
```
ln.clear()
```
Clear the current path according the current series.

Default path: files/

Change path: files/short name/vol/

### Create new instance of ln object
```
ar = ln.create()
```
Create a new instance of ln object.