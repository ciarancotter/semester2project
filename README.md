<p align="center">
<img src="src/view/assets/logo.png">
</p>

<p align="center"> •
  <a href="#summary">Summary</a> •
  <a href="#installation">Installation</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#game-plot">Game Plot</a> •
  <a href="#supported-devices">Supported Devices</a> •
  <a href="#style-and-the-github-workflow">Style/Github</a> •
  <a href="#faq">FAQ</a> •
</p>

---

# Summary
**Boole Raider** is an experimental 2D roguelike platformer that uses a Kinect with MV (machine vision) to control the player character and generates image assets as well a
parts of the story with OpenAI's AI software. This game represents the amalgamation of several cutting-edge technologies in a format that is fun to interact with.

![pixil-frame-0_9](https://user-images.githubusercontent.com/61756898/216027732-d97a34fe-bbe5-4f2c-a74a-69e1aef42768.png)

# Installation
- Clone this repository.
- Install the dependencies using `requirements.txt`.
- Run the game using `run.sh`.

# Architecture
This game was developed using [Pygame](https://pypi.org/project/pygame/). Pygame is a popular game development package for Python that supports up to Python 3.10. The game is structured in the **Model-View-Controller (MVC)** pattern. The UI interactions, such as the main menu and the game window, are handled by `view`. The game state is handled by the `model` directory.

# Game Plot
The player is an archaeology student from UCC, who was locked into the Boole library by accident. They decide to lay in the sarcophagus located in the basement. The sarcophagus teleports the player to the pyramids of Luxor, Egypt in 4200BC. The player is tasked with exploring this pyramid to complete their thesis by reading a series of monoliths located in each room.

![pharaohRightWalk1](https://user-images.githubusercontent.com/61756898/216027277-6d29a0a9-0e7b-4670-ad06-e5405a8d6819.png)

# Supported Devices
This software is designed to run on the Windows operating system that runs the Kinect For Windows SDK. An Xbox Kinect is also required to play, although keyboard controls are also supported.

https://user-images.githubusercontent.com/61756898/216026880-2fa1f54b-93ab-46f1-a24e-993282cabca8.mp4

# Style and the Github Workflow
- We are using [Google's Python Style Guide](https://google.github.io/styleguide/pyguide.html) for this project. This is enforced using the [pylint](https://pylint.readthedocs.io/en/latest/) linting system and the [YAPF](https://github.com/google/yapf) formatter. These run automatically on our Github repository using a Github Workflow, which is triggered by pushes and pull requests. Documentation is generated automatically using the [Sphinx](https://www.sphinx-doc.org/en/master/index.html) tool.

# FAQ
Nobody asks us any questions :(
