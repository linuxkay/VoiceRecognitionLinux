#!/bin/bash
terminator -e "julius -C ~/dictation-kit-v4.4/custom.jconf -module -lv 20000 " &
gnome-terminal -e "python /home/user/Workspace/sound-rec.py" &
notify-send 'Julius Started'
