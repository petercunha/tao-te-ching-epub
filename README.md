# Tao Te Ching — EPUB

An EPUB edition of Lao Tzu's *Tao Te Ching: The Book of the Way* (Sam Torode translation, Ancient Renewal 2021), built from the post at <https://vialogue.wordpress.com/2021/12/14/tao-te-ching/>.

**Download:** [`Tao Te Ching.epub`](Tao%20Te%20Ching.epub)

## Contents
- Cover and title page
- Reflections (the blogger's essay)
- Chapters 1–81, one per page, with the original line breaks and emphasis
- A preview of Epictetus's *The Manual*
- A table of contents that links to every chapter

Typos in the source post are corrected in `build.py` (see `CORRECTIONS`).

## Rebuilding
```sh
curl -sL https://vialogue.wordpress.com/2021/12/14/tao-te-ching/ -o page.html
pip install beautifulsoup4
python3 build.py
```
