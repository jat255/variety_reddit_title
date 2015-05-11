#!/usr/bin/env python2

# Josh Taillon - jat255@gmail.com
# uses a fair bit of code from the wallpaper-reddit script by http://www.reddit.com/u/MarcusTheGreat7 available at https://github.com/markubiak/wallpaper-reddit

import lxml.html
import sys
import subprocess
import re
from distutils import spawn
import platform

resize = True   # Flag to determine if we want to resize image or not. Helps with placement of title

try:
  im_path = sys.argv[1]
except:
  print("Could not read command line option. Please supply path of image as only argument.\n")
  
opsys = platform.system()

#in - string - path to image (from variety) that will be checked for title
#out - string - url of reddit post  
def get_reddit_post(image):
  o = subprocess.check_output([spawn.find_executable("exiftool"), '-sourceurl', image,])
  url = o.split()[3]
  return url

#in - string - the url of the reddit post to get the title of
#out - string - title if reddit post
def get_title(url):
  t = lxml.html.parse(url)
  title = t.find(".//title").text
  return title

#checks that all required commands can be found
def check_requirements():
  for cmd in (('convert','imagemagick'),('identify','imagemagick'),('mogrify','imagemagick')):
    if not spawn.find_executable(cmd[0]):
      print("Missing required program '%s'." %cmd[1])
      if opsys == "Linux":
        print("Please install from the package manager and try again")
      else:
        print("Please install the imagemagick suite from http://imagemagick.org/script/binary-releases.php#windows and try again")
      sys.exit(1)
  for cmd in (('exiftool','exiftool'),):
    if not spawn.find_executable(cmd[0]):
      print("Missing required program '%s'." %cmd[1])
      if opsys == "Linux":
        print("Please install from the package manager and try again")
      else:
        print("Please install exiftool from http://www.sno.phy.queensu.ca/~phil/exiftool/ and try again")
      sys.exit(1)
  for cmd in (('awk','awk'),):
    if not spawn.find_executable(cmd[0]):
      print("Missing required program '%s'." %cmd[1])
      if opsys == "Linux":
        print("Please install from the package manager and try again")
      else:
        print("Please install awk from http://gnuwin32.sourceforge.net/packages/gawk.htm and try again")
      sys.exit(1)
      
#in - string - title of the picture
#out - string - title without any annoying tags
#removes the [tags] throughout the image
def remove_tags(str):
  return re.sub(' +', ' ', re.sub("[\[\(\<].*?[\]\)\>]", "", str)).split(':')[0].strip()

#in - string, string - path of the image to set title on, title for image
def set_image_title(path, 
                    newtitle, 
                    titlefont="Ubuntu Condensed",
                    titlesize=42,
                    titlegravity="south",
                    text_offset='+5+1007',
                    shadow_offset='+7+1005'):
  if titlefont == "":
    subprocess.call([spawn.find_executable("convert"), path, "-pointsize", str(titlesize), "-gravity", titlegravity,
                     "-fill", "#00000080", "-annotate", shadow_offset, newtitle,
                     "-fill", "white", "-annotate", text_offset, newtitle, path])
  else:
    font = subprocess.check_output([spawn.find_executable("fc-match"), "-f '%{file[0]}'", titlefont]).replace("'","").strip()
    o = subprocess.check_output([spawn.find_executable("convert"), path, "-pointsize", str(titlesize), "-gravity", titlegravity, "-font", font,
                     "-fill", "#00000080", "-annotate", shadow_offset, newtitle,
                     "-fill", "white", "-annotate", text_offset, newtitle, path])
    
#in - path: image path
#   - minwidth: desired image width
#   - minheigh: desire image height
def resize_image(path, minwidth, minheight):
  command = [spawn.find_executable("convert"), path, "-resize", str(minwidth) + "x" + str(minheight) + "^",
               "-gravity", "center", "-extent", str(minwidth) + "x" + str(minheight), path]
  subprocess.call(command)
    
check_requirements()
url = get_reddit_post(im_path)
t = remove_tags(get_title(url))

if resize:
  resize_image(im_path,1920,1080)

set_image_title(im_path,t)