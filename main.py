"""Entry program for make.fun news-image-20261124.

Copies the rendered front page (entry.png, drawn by render.py from the
verified story set in stories.json) to /output/entry.png.

Standard library only, no network, no clock, no randomness: every run
writes exactly the same bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"), "/output/entry.png")


if __name__ == "__main__":
    main()
