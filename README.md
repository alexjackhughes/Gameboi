# Pokemon GPT

This is a little messaround with getting OpenAI's vision model to play Pokemon.

It works like so:

1. We take a screenshot of the screen
2. We give that to GPT, asking it to describe the image and allowing it to submit a specific move
3. We extract that key, and press it
4. We repeat

You should be able to just change a few lines on the prompt, and get this to work with any Gameboy game.

I've tested it with `gpt-4-vision-preview`, and it worked pretty well. It'll be interesting to see how it works with the next model.

Forked from Charlie's wonderful narrator AI:

https://twitter.com/charliebholtz/status/1724815159590293764

## Setup

Clone this repo, and install the dependencies:
`pip install -r requirements.txt`

Make an [OpenAI](https://beta.openai.com/) account and create an .env file:

```
OPENAI_API_KEY=<token>
OPENAI_ORGANIZATION=<organization>
```

## Run it!

```bash
python narrator.py
```
