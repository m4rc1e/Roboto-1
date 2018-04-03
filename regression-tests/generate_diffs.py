"""
Compare TN's Roboto visually against the official version.


Use fonttool's varLib mutator to generate the static instances
for comparison.

Script relies on Browserstack. Its very slow.
"""
import os
import json
from glob import glob

from fontTools.varLib import mutator
from fontTools.ttLib import TTFont
from diffbrowsers.utils import load_browserstack_credentials
from diffbrowsers.diffbrowsers import DiffBrowsers


AXIS = {
    'Thin': {'wght': 100, 'wdth': 100},
    'Regular': {'wght': 400, 'wdth': 100},
    'Black': {'wght': 900, 'wdth': 100},
    # TODO Add all instances
}


def generate_ttf_instances(vf_font, dst):
    """Generate instances from a variable font"""

    vf_font = TTFont(vf_font)
    for style in AXIS:
        font = mutator.instantiateVariableFont(vf_font, AXIS[style])

        filename = "Roboto-{}.ttf".format(style)
        file_dst = os.path.join(dst, filename)
        if os.path.isfile(file_dst):
            os.remove(file_dst)
        font.save(file_dst)


def main():
    c_dir = os.path.dirname(__file__)
    vf_font = os.path.join(c_dir, 'roboto-tn', 'src', 'Roboto-VF.ttf')
    instances_dir = os.path.join(c_dir, 'roboto-tn')
    generate_ttf_instances(vf_font, instances_dir)

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
