
## Index
- [Summary](#summary)
- [Game Plot](#game-plot)
- [Supported Devices](#supported-devices)
- [Installation](#installation)
- [Style/Github](#style-and-the-github-workflow)

## Summary
**Boole Raider** is an experimental 2D roguelike platformer that uses a Kinect with MV (machine vision) to control the player character and generates image assets as well a
parts of the story with OpenAI's AI software. This game represents the amalgamation of several cutting-edge technologies in a format that is fun to interact with.

![pixil-frame-0_9](https://user-images.githubusercontent.com/61756898/216027732-d97a34fe-bbe5-4f2c-a74a-69e1aef42768.png)

## Game Plot
The player is an archaeology student from UCC, who was locked into the Boole library by accident. They decide to lay in the sarcophagus located in the basement. The sarcophagus teleports the player to the pyramids of Luxor, Egypt in 4200BC. The player is tasked with exploring this pyramid to complete their thesis by reading a series of monoliths located in each room.

![pharaohRightWalk1](https://user-images.githubusercontent.com/61756898/216027277-6d29a0a9-0e7b-4670-ad06-e5405a8d6819.png)

## Supported Devices
This software is designed to run on the Windows operating system that runs the Kinect For Windows SDK. An Xbox Kinect is also required to play, although keyboard controls are also supported.

https://user-images.githubusercontent.com/61756898/216026880-2fa1f54b-93ab-46f1-a24e-993282cabca8.mp4


## Installation
- Clone this repository.
- Install the dependencies using `requirements.txt`.
- Run the game using `run.sh`.


## Style and the Github Workflow
- We are using [Google's Python Style Guide](https://google.github.io/styleguide/pyguide.html) for this project. This is enforced using the [pylint](https://pylint.readthedocs.io/en/latest/) linting system and the [YAPF](https://github.com/google/yapf) formatter. These run automatically on our Github repository using a Github Workflow, which is triggered by pushes and pull requests. Documentation is generated automatically using the [Sphinx](https://www.sphinx-doc.org/en/master/index.html) tool.

