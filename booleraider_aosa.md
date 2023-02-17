# Boole Raider by Team 2
Boole Raider is...
*Summary here*

# Architecture & Design

## Design Overview
![](https://notes.monke.ie/uploads/2d620e05-cae3-4db8-a8cd-385e0e522032.png)

This project uses a Model View Controller (MVC) software architecture. 

- The **Model** will consist of modules dealing with the game state and logic of the game as well as communicating with outside resources.
- The **View** deals with drawing the UI and all the functionality that is distinct from the logic of the game.
- The **Controller** deals with the user input and calls the view to display the gamestate on the screen.

A concrete  example of this interaction is:
1. The Controller records the image and sends it to the model for classification.
2. The Model sends back a response containing whether or not the image was classified as a movement that is recognised by the program.
3. If it is a valid command such as “move right” then the Controller calls the Model's API, instructing it to change the player's position.
4. The Controller makes more calls relating to game state.
5. The Controller subsequently calls the view.
6. The View then calls the Model to check what it should be drawing.
7. The View displays the frame to the user.

## Programming Reasoning
We made the decision to use **Python** for this project for three main reasons.
- It supports game development via the Pygame module.
- Machine Vision supports integration with Python.
- OpenAI provide a module in Python that acts as a wrapper for their REST API, providing an easy-to-use interface for using their technology.

## Dataflow Diagrams

### Level 0
![](https://notes.monke.ie/uploads/ccbaf166-1289-4ed7-aa1d-49fb18b61f42.png)
*Fig 1. The level 0 dataflow diagram.*

Fig.1 gives an overview of the system at a high level, showing where the data is sent between each component. The user interacts with the machine vision controlling system to provide inputs to Pygame, which are used to control the player. Pygame fetches various types of assets for the game from OpenAI. The completed Pygame environment is returned to the user.

### Level 1
![](https://notes.monke.ie/uploads/4825ccb5-9500-4f0c-b6fd-eff89da33a4c.png)
*Fig 1.1 The level 1 dataflow diagram.*

Fig 1.1 shows a more detailed version of Fig 1. This figure includes the input type for each component.
- **Machine Vision** takes the user's physical motion as an input. The result of this is a series of vectors.
- **OpenAI** receives a prompt from Pygame, such as "forest" or "dungeon". The result of this is sent back to Pygame.
- **Pygame** takes two inputs.
- It receives the output vectors from the Machine Vision component.
- The resulting *Completion Object* from OpenAI, which is a class defined in the OpenAI Python module.
- The **User** interacts with the loaded Pygame interface.


# Interfaces

## Machine Vision
We wish to be able to control the game using machine vision like the games for the Xbox Kinect. After some exploration into OpenCV libraries such as OpenPose and the Nvidia libraries for the Jetson Nano, we concluded that the [Kineck SDK](https://learn.microsoft.com/en-us/previous-versions/windows/kinect/dn799271(v=ieb.10)) for Windows was the best option. 
To encourage development into machine vision, Microsoft made the tools to develop applications with the Kinect easy to access in C and Python via [PyKinect2](https://github.com/Kinect/PyKinect2). By getting the coordinate positions for each joint on the human body in the frame, we can interpret movements that can be used to control the game.
The PyKinect translation layer is old (2014) and only operable with Python 3.6. As we are using Python 3.10 work was put in to bring this library up to the modern standard. 

## Pygame
Pygame is a module in Python that is used to build video games. Pygame is one of the most well-known and stable libraries for this type of development, with over [5,000 stars on Github](https://github.com/pygame/pygame).
 
#### Background Generation
The background will be generated using DALL.E, the image generation deep learning model built by OpenAI. This image is saved to the user's local directory and Pygame reads from this location to set the game background.

## AI
[OpenAI](https://openai.com/) is a leading AI research company that is best known for its well-publicised deep learning models. In light of this technology's potential, we made the decision to integrate the models provided by OpenAI into our game.

### GPT-3
We decided to use GPT-3 to generate the storyline and in-game text. The cost of using this model for this purpose was minimal, and so the only necessity to use this for our game was to engineer a prompt that returned a consistently formatted response for Pygame to ingest.

### DALL.E 
We decided, at least preliminarily, to use DALL.E only for background image generation and for certain, regularly-shaped assets such as crates. There were two main reasons for this:
- Deep learning models do not handle asset background transparency very well, and we did not want to perform any image post-processing in a v1 of this project.
- Spritesheets may not be very consistent or regular, and we wanted to do a small amount of art ourselves, by hand.


# Game Design

## Theme 
- The Player is an Archaeology student, currently working on their thesis in Boole library into the night.
- The Boole library closes, and the player gets locked in.
- The player starts panicking, not knowing what to do. They end up bored and give up hope, knowing well that there is no way out.
- They have the whole library to themselves, and start exploring. They find the infamous UCC boole basement Egyptian mummy sarcophagus. 
- They decide that this is where they will sleep for the night.
- After a long nights sleep, they wake up in Ancient Egypt, in 4200 BC, Luxor.
- Stranded in a pyramid, they think of nothing other than the thesis. This is a perfect opportunity for them to have the best thesis known to man. The adventure begins.

## UI Interfaces

### Start Menu
- Egypt-themed background.
- Fixed canvas for game in the middle.
- Egyptian-style border for canvas.
- Drawing of team members beneath the canvas.
- Title and logo of game.
- Buttons: PLAY, LEADERBOARD, HELP, ABOUT (maybe animated).
- Ancient Egypt/ desert colour scheme.

### Leaderboard
- Same external layout excluding team members.
- User name column, Score column.

### About
- Info on team members
- Info on what they worked on 
- When the game was created
- Member drawings with mini paragraphs

### Help
- Game instructions
- Pictures of human and player showing same movement
- Descriptions of whats happening
- Describe of what to do in the game, what the levels are like.
    
## During Gameplay
- Treasure amount
- Chatbox at the bottom
- Healthbar at top middle
- Level number at corner top
- Camera with toggle button
- Every level health regains


## Level System
The level, or the "room" in the dungeon, is composed of a tilemap of entities that we refer to as *Blocks*. A single Block is a 32x32px tile on the 1024x1024px canvas. The canvas is this size due to the nature of DALL.E - DALL.E can only generate canvases that are either 256x256, 512x512, or 1024x1024 pixels.

Each instance of the Block class has an *Entity* attribute, which denotes what type of object, if any, occupies its space on the canvas.

A *Layout* is an array of blocks that creates a design of entities for a particular level.


## Movement
We anticipate that at the pygame stage of movement processing, we may need to use an asynchronous loop if the pygame event loop is not fast enough.

# Development Utilities
## Collaboration/Version control

- We used [git](https://git-scm.com/) as our version control and we used [Github](https://github.com/) for code centralisation and management. 
- We used [Github Actions](https://docs.github.com/en/actions) scripts to automate the checking formatting and documentation of our project.
- We used [Google's Python Style Guide](https://google.github.io/styleguide/pyguide.html) for our project. This was enforced using the [pylint](https://pylint.readthedocs.io/en/latest/) lint and the [YAPF](https://github.com/google/yapf) formatter. These ran automatically on our Github on pushes and pull requests to enforce the style guide.
- We automatically generated documentation using the [sphinx](https://www.sphinx-doc.org/en/master/index.html) tool.

## Testing
- We used the [*unittest*](https://docs.python.org/3/library/unittest.html) library that comes with python for our unittests.
- These tests ran automatically in the manner described above during the development process to stop breakages. 

# Deployment

## Supported Devices
This project is meant to run on a windows machine that runs the Kinect for windows SDK, connected to the Xbox kinect.

## Installation
- Blah blah blah.

