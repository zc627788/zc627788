# Rebuilding the profile

Run from the repository root with Python 3:

```sh
python -m pip install fonttools
python tools/build_profile.py
```

The generator builds the English profile and its SVG assets. Chinese text stays
in `README.zh-CN.md`. The current orbital data-station artwork lives in
`tools/hyperspace.py` (a projected 4D sculpture with a seamless CSS path animation).
Panel machinery and the previous orbital hero live in `tools/observatory.py`;
the earlier hero layout is retained in `tools/sources`.

Space Grotesk and Manrope are bundled under their SIL Open Font Licenses in
`assets/fonts`. Text is outlined to preserve typography in GitHub image rendering;
it does not download web fonts or require JavaScript. Every panel has alt text
and SVG accessibility labels. The text edition remains available from the footer.

All animation is decorative CSS inside SVGs, with a reduced-motion override.
Images of project evidence are embedded unchanged from the existing PNGs.
Historical output counts are not live crawl metrics. Do not replace these counts
with estimates or imply a fresh run without new verification evidence.

Links wrap the images in the README because image-internal SVG links are not
interactive in GitHub's profile rendering. The surrounding GitHub layout remains
controlled by GitHub. Assets are served from this repository, with no external
stats-card service.
