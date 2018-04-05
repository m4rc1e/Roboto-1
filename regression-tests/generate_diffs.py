"""
Compare TN's Roboto visually against the official version.

Script relies on Browserstack. Its very slow.
"""
import os
import json
from glob import glob

from diffbrowsers.utils import load_browserstack_credentials
from diffbrowsers.diffbrowsers import DiffBrowsers


def main():
    c_dir = os.path.dirname(__file__)

    imgs_dir = os.path.join(c_dir, 'imgs')

    auth = load_browserstack_credentials()

    fonts_before = {os.path.basename(f): f for f in
                    glob(os.path.join('roboto-2.138', '*.ttf'))}
    fonts_after = {os.path.basename(f): f for f in
                   glob(os.path.join('roboto-tn', '*.ttf'))}
    shared_fonts = set(fonts_before.keys()) & set(fonts_after.keys())

    for font in shared_fonts:
        img_dir = os.path.join(imgs_dir, font[:-4])

        diffbrowsers = DiffBrowsers(
            auth,
            [fonts_before[font]],
            [fonts_after[font]],
            img_dir
        )
        diffbrowsers.diff_view('glyphs-all', 20, gen_gifs=True)

        stats_path = os.path.join(img_dir, 'stats.json')
        with open(stats_path, 'w') as doc:
            json.dump(diffbrowsers.stats, doc)


if __name__ == '__main__':
    main()
