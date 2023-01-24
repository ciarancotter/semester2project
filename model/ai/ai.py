import openai


def configure_openai():
    openai.api_key = "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"


def generate_monolith(emotion: str, theme: str) -> list:

    prompt: str = """
    Suppose that you are writing a short dramatic narration,
    which is composed of a series of inscriptions. 
    Each line should be in the first person perspective.
    The story should have a beginning, middle and end.
    Each inscription should be a single, vividly descriptive line.
    Do not write anything except the lines, no more than 10 lines long.
    Do not number each line.
    Consider the above instructions and set the protagonist to be a hero where the theme is {theme}
    and the story has a {emotion} ending.
    """.format(emotion=emotion, theme=theme)

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=512,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        result = response['choices'][0]["text"]
        narration = result.split("\n")[1:-1]

        for line in narration:
            line = line.rstrip()
        
    except Exception as e:
        narration = []
        print("OpenAI Error: " + str(e))

    for line in narration:
        print(line)


configure_openai()
generate_monolith("tragic", "romans")
