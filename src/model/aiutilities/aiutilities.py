"""Utilities to interact with OpenAI's models.

This includes the generation of text via GPT-3, and the generation of images using DALLE.
The background is saved to view/assets as "gamebg.png".
Usage:

configure_openai()
generate_monolith("tragic", "Roman")
generate_background("jungle")
"""

import os
import openai
import asyncio
import requests


def configure_openai() -> None:
    """Configures the OpenAI module with the API key from environment variables.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_monolith(emotion: str, theme: str) -> list:
    """Generates a list containing a story to be written on monoliths as inscriptions.

    Args:
      emotion:
        The emotion of the story's ending.
      theme:
        The theme of the story.

    Returns:
        A list containing individual lines in the story. Each item is one sentence.
    """

    prompt: str = """
    Suppose that you are writing a short dramatic narration,
    which is composed of a series of inscriptions. 
    Each line should be in the first person perspective.
    The story should have a beginning, middle and end.
    Each inscription should be a single, vividly descriptive line.
    Do not write anything except the lines, no more than 11 lines long.
    Do not number each line.
    Each line must be no more than 7 words long and must end in a full stop.
    Consider the above instructions and set the protagonist to be a hero where the theme is {theme}
    and the story has a {emotion} ending.
    """.format(emotion=emotion, theme=theme)

    try:
        response = openai.Completion.create(engine="text-davinci-003",
                                            prompt=prompt,
                                            temperature=0.5,
                                            max_tokens=512,
                                            top_p=1.0,
                                            frequency_penalty=0.0,
                                            presence_penalty=0.0)

        result = response['choices'][0]["text"]
        narration = result.split("\n")[1:-1]

        for line in narration:
            line = line.rstrip()

    except Exception as e:
        narration = []
        print("OpenAI Error: " + str(e))

    return narration


def generate_background(theme: str) -> None:
    """Generates a PNG file to be used as the game's background, one-time.

        Args:
          theme:
            The theme of the background.
    """
    prompt_template = theme + "style caves in a dungeon, clean looking pixel art, detailed, vibrant"
    response = openai.Image.create(
        prompt=prompt_template,
        n=1,
        size="512x512",
    )
    image_url = response["data"][0]["url"]
    img_data = requests.get(image_url).content
    save_path = './src/view/assets/gamebg1.png'
    with open(save_path, 'wb') as handler:
        handler.write(img_data)


async def generate_background_async(theme: str, index: int) -> None:
    g_bg_event = asyncio.Event()
    """Generates a PNG file to be used as the game's background asynchronously.

        Args:
          theme:
            The theme of the background.
          index: 
            The level that the background is generated for.
        """
    prompt_template = theme + "style caves in a dungeon, clean looking pixel art, detailed, vibrant"
    response = openai.Image.create(
        prompt=prompt_template,
        n=1,
        size="512x512",
    )
    image_url = response["data"][0]["url"]
    img_data = requests.get(image_url).content
    save_path = './src/view/assets/gamebg' + str(index) + '.png'
    with open(save_path, 'wb') as handler:
        handler.write(img_data)
        g_bg_event.set()
    await g_bg_event.wait()
