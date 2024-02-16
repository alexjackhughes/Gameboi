# Gameboi

This is a little messaround with getting OpenAI's vision model to play Pokemon, and really, any Gameboy game.

It works like so:

1. We take a screenshot of the current screen where Pokemon is visible
2. We give that image to GPT-V, asking it to describe the image and allowing it to submit one of a specific set of moves
3. We extract that key, and press that key programatically
4. We repeat the steps again

This is really a fun little experiment, and I'm sure there are many ways to improve it. I just wanted to see how "smart" GPT-4 is, and whether it could play pokemon without any intervention.

You should be able to just change a few lines on the prompt, and get this to work with any Gameboy game.

I've tested it with `gpt-4-vision-preview`, and it worked pretty well. It'll be interesting to see how it works with the next model.

Inspired by Charlie's wonderful narrator AI:

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
