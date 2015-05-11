# variety_reddit_title
Script to add title to reddit sourced images when using Peter Levi's Variety wallpaper changer

This script can be used to add a title to images downloaded with [Variety](http://peterlevi.com/variety/) taken from a Reddit source.
I'm putting this up as pretty much a 'use it or leave it' type script, but I'm willing to help if anyone has issues getting it to work.

Requirements
------------
At the very least, this script will require Python 2.X (script was written with 2.7.9), `exiftool`, `fc-match`, and `imagemagick` installed on your system.

Installation
------------
On my system (Arch linux running KDE 4.X desktop environment, with 1920x1080 resolution), 
I have this script working by doing the following:
 
 * Set only reddit sources for your Variety setup. I'm sure this script could be hacked into other sources, but 
 right now it's only for wallpaper subreddits. In particular, I have only tested it with [EarthPorn](https://www.reddit.com/r/earthporn/)
 as a source. Using other sources may work since I think the script will just silently crash for other images, but I haven't tested it.
 I also have Variety set to only download wallpapers that are at least as wide as my monitor.
 * Save the script `title_reddit_image.py` somewhere on your system and make sure it's executable.
 * Edit a few lines to make sure it fits your system. Namely, you'll probably want to change the following things:
  * `resize = True` (line 13) Change this to false if you do not want to resize the image before it's set as a wallpaper. Letting the script resize 
    for you helps with reliable placement of the image title, especially since certain desktop environments like to center, tile, scale, etc. images before making them the wallpaper.
  * in function `set_image_title()` (~line 70), you can change the font used for the title, the font size, and the location of both the text and the shadow.
    These options are supplied in the default `ImageMagick` format. The offsets provided will place the title near the top
    of the desktop for a 1080p display.
  * in function `resize_image()` (~line 90), you can change the size desired for for the image. This is useful 
    because if the image is too large, when KDE (or whatever environment) resizes it for the desktop, the text might 
    get skewed or not shown, since it is too high. Since images coming from reddit are all different resolutions,
    it is easiest to just resize them first, and then add the text.
  * **Important:** Add a call to this script to `~/.config/variety/scripts/set_wallpaper`. Since I am using KDE, 
    I have the following section in my file:
    
    ```bash
    # KDE - User will have to manually choose ~/Pictures/variety-wallpaper/ as a slideshow folder with a short iterval.
    # Afterwards, with the command below, Variety will just overwrite the single file there when changing the wallpaper
    # and KDE will refresh it
    if [ "`env | grep KDE_FULL_SESSION | tail -c +18`" == "true" ]; then
      mkdir -p "$(xdg-user-dir PICTURES)/variety-wallpaper"
      python2 /home/josh/scripts/variety_reddit_title/title_reddit_image.py "$WP"
      cp "$WP" "$(xdg-user-dir PICTURES)/variety-wallpaper/wallpaper-kde.jpg"
      exit 0
    fi
    ```
    
Again, this is what it took to get the script working on my system, but yours may be different, so good luck! 
And if you want to post in the [Wiki](https://github.com/jat255/variety_reddit_title/wiki) how you got it working
on your system, that would probably be helpful to others!
