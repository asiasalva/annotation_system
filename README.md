# Video Annotation System

This repository is aimed to keep the project for the course "Fundamentals of Image and Video Processing" held in University of Trento for the Computer Science Master Degree. 
The developer team is composed of two students, Federico Brugiolo and Asia Salvaterra.

# Environment

The project was created using Visual Studio and Python.

## Project Libraries
The following libraries are needed in order to make the project work:

- PyQt5 (https://pypi.org/project/PyQt5/)
- OpenCV (https://pypi.org/project/opencv-python/)
- K-Lite Codec Pack Basic (https://codecguide.com/download_k-lite_codec_pack_basic.htm)
- FFMPEG (both https://ffmpeg.org/ and https://pypi.org/project/ffmpeg-python/)

# Usage

The GUI we created is a video editor that takes in input a video or an existing project and allow to annotate the video in many ways.
The project the user will work on is composed by a video file and an XML file in which will be saved all the info about the annotations.

## Using the GUI

From the **file** command at the top left the user can choose to upload the video creating a new project, open an existing one and save the one he is working on.
Then there will be two sides of the interface: the video and the annotation one.
In the video side there is the box in which the video will be played and all the commands that a classical video player needs:
- Play: starts the video;
- Pause: pause the video and abilitate the annotation section;
- Stop: stop the video;
- Go ahead: jump ahead by 10 seconds;
- Go back: go back for 10 seconds;
- Slow down the video;
- Speed up the video;
- Go to next breakpoint: move between different breakpoints.


## Types of Annotations
The implemented annotations are the following: 
- TextBox: enable the user to write some text on the screen. Also, the user can change color of the text and of box's background, change dimensions of the box or of the characters. The box can be moved and resized as needed.
- Line: creates a line on the screen, resizable and colorable by user's preferences.
- Arrow: creates an arrow on the screen with same attributes as the line annotation. 
- BreakPoint: appears like a little circle. When a breakoint is encountered, the video pauses. The user can add breakpoints to play the video and instantly go to that position.
- Drawing: user can use the video player as a blackboard on which he can draw something, changing brush color and size, eliminate drawings with the rubber. This annotation type was thought as a blackboard because the user may need to explain something on the fly without really creating an annotation.

## Extra
Some structures were integrated in our code in order to create some functionalities. Here are the credits:
- TContainer used to insert annotations, move and resize them: https://github.com/korabelnikov/moveable-and-resize-qt-widget-on-python
- For the creation of the drawings on screen: https://stackoverflow.com/questions/62023019/how-to-draw-line-with-brush-on-image-with-pyqt5
- For the rubber: https://stackoverflow.com/questions/53515295/erasing-pen-on-a-canvas
- To make the color picker for the interface: http://www.blackbeltcoder.com/Articles/controls/creating-a-color-picker-with-an-owner-draw-combobox
