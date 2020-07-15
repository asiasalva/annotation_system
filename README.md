# Video Annotation System

This repository is aimed to contain the project for the course "Fundamentals of Image and Video Processing" held in University of Trento for the Computer Science Master Degree. 
The developer team is composed of two students: Federico Brugiolo and Asia Salvaterra.
In this read me there will be basic info about the project. To discover more just look at the Wiki page.


# Environment

The project was created using Visual Studio and Python.

## Project Libraries
The following libraries are needed in order to make the project work:

- PyQt5 (https://pypi.org/project/PyQt5/)
- OpenCV (https://pypi.org/project/opencv-python/)
- K-Lite Codec Pack Basic (https://codecguide.com/download_k-lite_codec_pack_basic.htm)
- FFMPEG (both https://ffmpeg.org/ and https://pypi.org/project/ffmpeg-python/)

# Usage

The GUI we created is a video editor that can take in input a video in order to start a new project or an existing project composed by a video and an annotations XML file. 

## Using the GUI

From the **file** command on the left the user can choose to upload the video or the project and also can save the project he is working on.
Then there will be two sides of the interface: the video one and the annotation one.
In the video side there is the box in which the video will be played and then all the commands that a video player needs:
- Play: starts the video;
- Pause: pause the video and abilitate the annotation section;
- Stop: stop the video;
- Go ahead: jump ahead by 10 seconds;
- Go back: go back for 10 seconds;
- Move forward of one frame
- Move backword for one frame
- Go to next breakpoint: move between different breakpoints


## Types of Annotations

- TextBox: the TextBox annotation enable the user to write some text on the screen. Also, the user can change color of the text and the background of the box, or change dimensions of the box or the characters, and also change the font.
- Line: creates a line on the screen, resizable and colorable by user's preferences.
- Arrow: same as the line but it is an arrow.
- BreakPoint: when a breakoint is encountered, the video pauses. Also, the user can add breakpoints to play the video and instantly go to that position.
- BlackBoard: user can use the video player as a sort of blackboard on which he can draw something, changing brush color and size, eliminate drawings with the rubber and so on.
- Drawings: user can create drawing in specified positions of the screen that will have the same behaviour as textbox, arrow and line annotations.

## Extra
Some structures were used in order to create some functionalities and understand how pyqt5 library work:
- TContainer used to insert annotations, move and resize them: https://github.com/korabelnikov/moveable-and-resize-qt-widget-on-python
- For the creation of the drawings on screen: https://stackoverflow.com/questions/62023019/how-to-draw-line-with-brush-on-image-with-pyqt5
- For the rubber: https://stackoverflow.com/questions/53515295/erasing-pen-on-a-canvas
- To make the color picker for the interface: http://www.blackbeltcoder.com/Articles/controls/creating-a-color-picker-with-an-owner-draw-combobox
