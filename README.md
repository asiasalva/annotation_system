# Video Annotation System

This repository is aimed to contain the project for the course "Fundamentals of Image and Video Processing" held in University of Trento for the Computer Science Master Degree. 
The developer team is composed of two students: Federico Brugiolo and Asia Salvaterra.


# Environment

The project was created using Visual Studio and Python.

## Project Libraries

- PyQt5
- OpenCV

# Usage

The GUI we created is a video editor that can take in input a video in order to start a new project or an existing project composed by a video and an annotation XML file. 

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
- Drawing: user can use the video player as a sort of blackboard on which he can draw something, changing brush color and size, eliminate drawings with the rubber and so on.