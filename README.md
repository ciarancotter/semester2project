# Summary
- Welcome to Team 2's software development project. This is an experimental 2D roguelike platformer. The player controls the character using machine vision. This is achieved through the use of a Kinect. The text and parts of the art are generated using GPT-3 and DALL.E respectively. 

![pixil-frame-0_9](https://user-images.githubusercontent.com/61756898/216027732-d97a34fe-bbe5-4f2c-a74a-69e1aef42768.png)

## Setting
This game is set in Ancient Egypt. The player is an archaeology student from UCC who was locked into the Boole library by accident, and decided to lay in the sarcophagus in the basement. The sarcophagus teleports the player to the pyramids of Luxor in 4200BC. The player is tasked with exploring this pyramid to complete their thesis.

![pharaohRightWalk1](https://user-images.githubusercontent.com/61756898/216027277-6d29a0a9-0e7b-4670-ad06-e5405a8d6819.png)

## Supported devices
This software is designed to run on the Windows operating system that runs the Kinect For Windows SDK. An Xbox Kinect is also required to play, although keyboard controls are also supported.

https://user-images.githubusercontent.com/61756898/216026880-2fa1f54b-93ab-46f1-a24e-993282cabca8.mp4


## Installation
- Clone this repository.
- Install the dependencies using `requirements.txt`.
- Run the main game script.


## Project Style
- We are using [Google's Python Style Guide](https://google.github.io/styleguide/pyguide.html) for this project. This is enforced using the [pylint](https://pylint.readthedocs.io/en/latest/) linting system and the [YAPF](https://github.com/google/yapf) formatter. These run automatically on our Github repository using a Github Workflow, which is triggered by pushes and pull requests. Documentation is generated automatically using the [Sphinx](https://www.sphinx-doc.org/en/master/index.html) tool.

