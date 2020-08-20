# Gamelist Addon

Gamelist Addon is a graphical desktop app for Linux with the capability to add new custom entries into a gamelist.xml file used by EmulationStation.

- Author: Tuncay D.
- License: [MIT License](LICENSE)
- Website: [https://thingsiplay.game.blog/gamelist-addon](https://thingsiplay.game.blog/gamelist-addon) 
- Source: [https://github.com/thingsiplay/gamelistaddon](https://github.com/thingsiplay/gamelistaddon) 

![Screenshot addgame state](img/screen_addgame-thumb.png  "screen-addgame")

## Introduction

[gamelist.xml](https://retropie.org.uk/docs/EmulationStation/#gamelistxml-edits) files are databases for the use in [EmulationStation](https://retropie.org.uk/docs/EmulationStation/), in example in RetroPie. They contain all paths and meta information for each system. Usually those files are created by some sort of [scraper tools](https://retropie.org.uk/docs/Scraper/) and do not require any manual editing. However sometimes there are cases when manually editing is required. Editing such files in a text editor has some traps and is just a pain.

This app will check for existing game entries and make sure the file is written in correct format. It is not a replacement for a rom manager or full fledged gamelist.xml editor. Entries are added as they are and no additional rom, image or video files are copied or checked for existence. It is the users responsibility to manage those things separately.

I started this project because there was no application on Linux that fulfill my needs. Also this is a good exercise to me learning more about programming.

## Usage

Once unpacked and the requirements are met, it is easy as running **GamelistAddon.py** or the run script. The app provides two main functionality modes: *Add Game* and *Merge Gamelists*.

In **Add Game**-mode only the fields with content will be written to the file, but *path* is required. The game entry can be added to an existing gamelist.xml or saved as a new file created from scratch. When overwriting to an existing file, a check if the game is already existing will be made. The comparison is done at basename level of the path field, ignoring the directory portion. This allows for detecting any game, regardless of how the path is noted (in example relative notion). In example:

	./game.gb
	/home/pi/RetroPie/roms/gb/game.gb
	
is treated as identical game. Currently if a dublication is detected, the user action is limited to ignoring or replacing the whole game entry.

The **import** button will load up the first found entry from a selected gamelist.xml file. Any of the edit fields in the GUI act as af filter for searching. Only one of the active filters need to match, in order to read the entire game entry. A new added game with this function will have an attribute "source" with the content "gamelistaddon", just like a scraper does. Note: Currently the favorite, hidden and kidgame do not work as filter, but work correctly otherwise.

In the **Merge Gamelists**-mode two XML files must be selected. The first one act as base content to compare against and second file should have new content to add. The order is important. When saving a new output XML file, both input files game entries are compared at basename level (described above). The selected output file will be created from scratch with the content of the input files. The update log view will be populated with all newly added game entries only. 

There are two merge modes: **Ignore** and **Update**. Ignore mode will only add new games which do not exist in base content, basically ignoring duplicates. In Update mode all games from both files are included and every single tag is compared individually. The tags from add content have higher priority. Any merging operation is considered to be an update and listed in the log. It will copy non updated games in its entirety too.

Once Update mode is activated, a new tab **Settings Merge Update** will appear. In this view every single tag like *name* or *lastplayed* can be individually selected. Only those selected tags will be compared between base content data and add content data when using the update functionality. That means, if the tag lastplayed is found in add content, then it will be used in new file. Otherwise it defaults to lastplayed from base content. Any unchecked tag will be taken from base content without any changes.

In the app folder is a separate commandline tool **merge.py** with merge functionality from the main app. It does not require PyQt5 and could be used for automation or testing. Currently if there is any error, then the program will stop and output *ERROR* on screen. On success the paths of each newly added game entries are output. Important: On default no files are saved and the original XML files are untouched. Check the options and how to specify an output file with

	./merge.py -h.

## How duplicates are identified

This program uses an unique way of identifying duplicates. It assumes that a rom is appearing only once in the gamelist file. When comparing two different files, one might have a different notation of the directory part in the path. The comparison is done at *basename* only, means the file itself and ignoring that directory part. Here is an example what this means. 

gamelist.xml from user 1:

	<path>./Aero the Acro-Bat 2 (U).smc</path>

gamelist.xml from user 2:

	<path>./roms/snes/Aero the Acro-Bat 2 (U).smc</path>

This game is considered to be a duplicate. *Warning*: If the other file is using an unusual folder, this might cause problems when merging them.

## Known bugs, limitations and quirks

In certain situations or parts of the program it behaves unexpected or in a very specific way. All unsolved mysteries are collected and described here.

### Non critical

- Add Game view: When using the import function/button, then the checkboxes *favorite*, *hidden* and *kidgame* do not work as filters and are ignored. But they are fully functional otherwise and will be read and written. Only the ability to use them as filters like in name or desc is not possible.

- Merge Gamelists view: When using the Duplicate Mode: Update with Custom tag settings enabled, then the log will only list games with individually updated tags. These are marked as "udpated". When a tag is copied from one of the contents without overwriting it, then it's not considered to be an update. This really applies only when using Custom tag settings and only what is seen in the log.

## Requirements

When running Python version directly:

- Python: 3.6.x
- PyQt5: 5.15.x

Additional requirements when building standalone distribution:

- Nuitka: 0.6.8.x
- Qt Designer: 5.9.x
- Pandoc: 1.19.2.x
- Linux compatible operating system

### GNU / Linux

Download the Python release build. You need Python 3 and PyQt 5 installed on your system to run the application. Source code is saved on Github and contains additional files and building scripts. The standalone release build is a compiled executable binary for Linux. It eliminates the need for any of the requirements listed above, besides the operating system.

### Windows and MacOS

Currently only Linux is tested and supported. There are no standalone builds for Windows or Mac. The Make script from source code is designed around the tools and scripting capabilities in Linux. The main release build do not need all these stuff and is a pure Python program. You need to install Python 3 and PyQt5 in order to use Gamelist Addon.

## Make

	usage: merge.py [-h] [--version] --base file --add file [--output file] [--log file] [--duplicate mode]

	
make.py is the script to build all release packages and is only relevant to the source code. It is a custom script written in Python. Running it without arguments will execute all routines. Using at least one argument will disable all other routines and just execute what is defined. All distribution related files are found in a sub folder "dist". In example:

	./make.py --ui --package

will only generate the .ui files and the distribution packages for Python only. No binary compilation is created and temporary files are not cleaned up.

## Feedback

If you want report a bug or have any questions, head over to the [project's forum thread](https://retropie.org.uk/forum/topic/27466/gamelist-addon-an-assist-tool-to-manually-add-new-game-entries)  in RetroPie or [leave me a message](https://thingsiplay.game.blog/contact/) on my contact page.

## Changelog

Version 0.3:

- new dedicated settings for Merge Update mode, limit updates to selected Tags only
- few missing Tags support added, previously they were ignored, namely *sortname*, *thumbnail*, *favorite*, *hidden* and *kidgame*
- layout of main Add Game view redesigned, to reflect the new additions

Version 0.2:

- new update feature in merge mode
- bug fixes

Version 0.1:

- initial release
