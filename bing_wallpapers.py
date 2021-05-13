import requests
import os
import pathlib
import random
import string
from termcolor import colored
import datetime
from screeninfo import get_monitors


# get screen rezolution
print(colored('[' + str(datetime.datetime.now()) + ']',
      'green'), colored('Get monitor rezulutins...', 'green'))
monitors = []
for m in get_monitors():
    monitors.append(m)
monitor_width = str(monitors[0].width)
monitor_height = str(monitors[0].height)
print(colored('[' + str(datetime.datetime.now()) + ']',
      'green'), colored('Monitor 0: width = ' + colored(monitor_width, 'white') + 
      colored(' height = ', 'green') + colored(monitor_height, 'white'), 'green'))

# Change current work directory
os.chdir(pathlib.Path().absolute())
homedir = os.environ['HOME']
imagedir = homedir + "/Pictures/"
image_name = ''.join(random.choice(
    string.ascii_lowercase) for i in range(10))
image_name = 'bing_wallpapers_' + image_name + '.jpg'

print(colored('[' + str(datetime.datetime.now()) + ']',
      'green'), colored('Remove old wallpapers files...', 'green'))
# Remove old wallpapers from
for element in os.scandir(imagedir):
    if element.is_file():
        if 'bing_wallpapers_' in element.name:
            os.remove(imagedir + element.name)
print(colored('[' + str(datetime.datetime.now()) + ']',
      'green'), colored('Remove done', 'green'))


# Get xml from url
def get_xml():
    url = 'https://www.bing.com/HPImageArchive.aspx?format=xml&idx=0&n=1&mkt=ru-RU'
    try:
        r = requests.get(url, allow_redirects=True)
        if r.ok:
            open(imagedir + 'bing.xml', 'wb').write(r.content)
            return 'OK'
        else:
            return 'Error'
    except:
        print(colored('[' + str(datetime.datetime.now()) + ']',
                      'red'), colored('Error connect to bing.com...', 'red'))
        return 'Error'


# get url from xml
print(colored('[' + str(datetime.datetime.now()) + ']',
      'green'), colored('Downlod xml from bing.com...', 'green'))
get_xml_rezult = get_xml()
if get_xml_rezult == 'OK':
    print(colored('[' + str(datetime.datetime.now()) + ']',
                  'green'), colored('Download done', 'green'))
    import xml.dom.minidom
    print(colored('[' + str(datetime.datetime.now()) + ']',
                  'green'), colored('Parsing xml file...', 'green'))
    dom = xml.dom.minidom.parse(imagedir + "bing.xml")
    dom.normalize()
    node1 = dom.getElementsByTagName("image")[0]
    node2 = node1.getElementsByTagName('url')[0]
    image_url = node2.childNodes[0].nodeValue
    print(colored('[' + str(datetime.datetime.now()) + ']',
                  'green'), colored('Setup current screen rezolution for image...', 'green'))
    image_url = image_url.replace('1920x1080', monitor_width + 'x' + monitor_height)
    image_url = 'https://www.bing.com' + image_url
    print(colored('[' + str(datetime.datetime.now()) + ']',
                  'green'), colored('Download image...', 'green'))
    r = requests.get(image_url, allow_redirects=True)
    if r.ok:
        print(colored('[' + str(datetime.datetime.now()) + ']',
                      'green'), colored('Download done', 'green'))
        print(colored('[' + str(datetime.datetime.now()) + ']',
                      'green'), colored('Save wallpaper as file...', 'green'))
        open(imagedir + image_name, 'wb').write(r.content)
        print(colored('[' + str(datetime.datetime.now()) + ']',
                      'green'), colored('Save wallpaper as file done', 'green'))
    else:
        print(colored('[' + str(datetime.datetime.now()) + ']',
                      'red'), colored('Error download file!', 'red'))
    import applescript
    script = str('tell application "Finder" to set desktop picture to POSIX file ') + \
        '"' + imagedir + image_name + '"'
    print(colored('[' + str(datetime.datetime.now()) + ']',
                  'green'), colored('Setup wallpaper...', 'green'))
    r = applescript.run(script)
    if r.code == 0:
        print(colored('[' + str(datetime.datetime.now()) + ']',
                      'green'), colored('Setup wallpaper done', 'green'))
    else:
        print(colored('[' + str(datetime.datetime.now()) + ']',
                      'red'), colored('Setup wallpaper error!', 'red'))
    print(colored('[' + str(datetime.datetime.now()) + ']',
                  'green'), colored('Remove xml file...', 'green'))
    if os.path.isfile(imagedir + 'bing.xml'):
        os.remove(imagedir + 'bing.xml')
        print(colored('[' + str(datetime.datetime.now()) + ']',
                      'green'), colored('Remove xml file done', 'green'))
    else:
        print(colored('[' + str(datetime.datetime.now()) + ']',
                      'red'), colored('Remove xml file eror!', 'red'))
