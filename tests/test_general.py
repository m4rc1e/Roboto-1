from fontbakery.callable import check
from fontbakery.callable import condition
from fontbakery.checkrunner import Section, PASS, FAIL, WARN
from fontbakery.fonts_profile import profile_factory
from fontbakery.profiles.universal import UNIVERSAL_PROFILE_CHECKS


# These checks fail in V2. If we try and make these checks pass, we
# will cause regressions. This isn't acceptable for a family which is
# requested 40 billion times a week.
REMOVE_CHECKS = [
    "com.google.fonts/check/required_tables",
    "com.google.fonts/check/family/win_ascent_and_descent",
    "com.google.fonts/check/os2_metrics_match_hhea",
    "com.google.fonts/check/ftxvalidator_is_available",
    "com.google.fonts/check/dsig",
]


def filter_checks(_, check_id, __):
    if check_id in REMOVE_CHECKS:
        return False
    return True


ROBOTO_GENERAL_CHECKS = [c for c in UNIVERSAL_PROFILE_CHECKS
                         if c not in REMOVE_CHECKS]

ROBOTO_GENERAL_CHECKS += [
    "com.roboto.fonts/check/italic_angle",
    "com.roboto.fonts/check/meta_info",
    "com.roboto.fonts/check/charset_coverage",
    "com.roboto.fonts/check/digit_widths",
]
profile_imports = ('fontbakery.profiles.universal',)
profile = profile_factory(default_section=Section("Roboto v3 general"))


# Checks ported from https://github.com/googlefonts/roboto/blob/master/scripts/run_general_tests.py

@condition
def is_italic(ttFont):
    return True if "Italic" in ttFont.reader.file.name else False


@condition
def is_vf(ttFont):
    return True if "fvar" in ttFont else False


@check(
    id="com.roboto.fonts/check/italic_angle",
    conditions = ["is_italic"]
)
def com_roboto_fonts_check_italic_angle(ttFont):
    """Check italic fonts have correct italic angle"""
    failed = False
    if ttFont['post'].italicAngle != -12:
        yield FAIL, "post.italicAngle must be set to -12"
    else:
        yield PASS, "post.italicAngle is set correctly"


@check(
    id="com.roboto.fonts/check/meta_info",
)
def com_roboto_fonts_check_meta_info(ttFont):
    """Check metadata is correct"""
    failed = False
    if ttFont['OS/2'].fsType != 0:
        yield FAIL, "OS/2.fsType must be 0"
    else:
        yield PASS, "OS/2.fsType is set correctly"

    if ttFont["OS/2"].achVendID != "GOOG":
        yield FAIL, "OS/2.achVendID must be set to 'GOOG'"
    else:
        yield PASS, "OS/2.achVendID is set corrrectly"

# TODO TestNames

# Test Digit Widths
@check(
    id="com.roboto.fonts/check/digit_widths",
)
def com_roboto_fonts_check_digit_widths(ttFont):
    """Check that all digits have the same width"""
    widths = set()
    for glyph_name in ["zero", "one", "two", "three","four", "five", "six", "seven", "eight", "nine"]:
        widths.add(ttFont['hmtx'][glyph_name][0])
    if len(widths) != 1:
        yield FAIL, "Numerals 0-9 do not have the same width"
    else:
        yield PASS, "Numerals 0-9 have the same width"

    # TODO MF: Port https://github.com/googlefonts/nototools/blob/master/nototools/unittests/font_tests.py#L288-L297


@check(
    id="com.roboto.fonts/check/charset_coverage",
)
def com_roboto_fonts_check_charset_coverage(ttFont):
    """Check to make sure certain unicode encoded glyphs are included and excluded"""
    include = frozenset([
        0x2117,  # SOUND RECORDING COPYRIGHT
        0xEE01, 0xEE02, 0xF6C3])  # legacy PUA

    exclude = frozenset([
        0x2072, 0x2073, 0x208F] +  # unassigned characters
        list(range(0xE000, 0xF8FF + 1)) + list(range(0xF0000, 0x10FFFF + 1))  # other PUA
        ) - include  # don't exclude legacy PUA

    font_unicodes = set(ttFont.getBestCmap().keys())

    to_include = include - font_unicodes
    if to_include != set():
        yield FAIL, f"Font must include the following codepoints {list(map(hex, to_include))}"
    else:
        yield PASS, "Font includes correct encoded glyphs"

    to_exclude = exclude - font_unicodes
    if to_exclude != exclude:
        yield FAIL, f"Font must exclude the following codepoints {list(map(hex, to_exclude))}"
    else:
        yield PASS, "Font excludes correct encoded glyphs"

# TODO TestLigatures

# TODO TestFeatures

@check(
    id="com.roboto.fonts/check/vertical_metrics",
)
def com_roboto_fonts_check_vertical_metrics(ttFont):
    """Check vertical metrics are correct"""
    failed = []
    expected = {
        # android requires this, and web fonts expect this
        ("head", "yMin"): -555,
        ("head", "yMax"): 2163,
        # test hhea ascent, descent, and lineGap to be equal to Roboto v1 values
        ("hhea", "descent"): -500,
        ("hhea", "ascent"): 1900,
        ("hhea", "lineGap"): 0,
        # test OS/2 vertical metrics to be equal to old OS/2 win values
        # since fsSelection bit 7 is now enabled
        ("OS/2", "sTypoDescender"): -555,
        ("OS/2", "sTypoAscender"): 2146,
        ("OS/2", "sTypoLineGap"): 0,
        ("OS/2", "usWinDescent"): 555,
        ("OS/2", "usWinAscent"): 2146,
    }
    for (table, k), v in expected.items():
        font_val = getattr(ttFont[table], k)
        if font_val != v:
            failed.append((table, k, v, font_val))
    if not failed:
        yield PASS, "Fonts have correct vertical metrics"
    else:
        msg = "\n".join(
            [
                f"- {tbl}.{k} is {font_val} it should be {v}"
                for tbl, k, v, font_val in failed
            ]
        )
        yield FAIL, f"Fonts have incorrect vertical metrics:\n{msg}"


# TODO TestGlyphBounds


profile.auto_register(globals(), filter_func=filter_checks)
profile.test_expected_checks(ROBOTO_GENERAL_CHECKS, exclusive=False)

