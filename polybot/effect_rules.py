"""
Rules for parsing the arguments for all the effects the user can request.
In EffectRules dict, all effect commands names must be entered with
identical names to the name of it method in Img class, when it's value
must be an EffectArgParser with all its Arg Rules instances.
"""

# pylint: disable=E0401
from polybot.effect_arg_parser import EffectArgParser
from polybot.effect_arg_rules import ArgRangeRule, ArgOptionRule, ArgPositiveInt, ArgColorRule
# pylint: enable=E0401

EffectRules = {
    'blur': EffectArgParser(0, 1, [
        ArgRangeRule(1, 32)
    ]),
    'contour': EffectArgParser(0, 0,[]),
    'rotate': EffectArgParser(0, 1, [
        ArgOptionRule([90, -90, 180, 270], int)
    ]),
    'salt_n_pepper': EffectArgParser(0, 3, [
        ArgRangeRule(0, 0.5, float),
        ArgColorRule(),
        ArgColorRule()
    ]),
    'color_noise': EffectArgParser(0, 1, [
        ArgRangeRule(0, 0.5, float)
    ]),
    'segment': EffectArgParser(0, 3, [
        ArgRangeRule(0, 255),
        ArgColorRule(),
        ArgColorRule()
    ]),
    'concat': EffectArgParser(0, 2, [
        ArgOptionRule(['horizontal', 'vertical']),
        ArgColorRule()
    ], True),
    'grayscale': EffectArgParser(0, 0, []),
    'canvas_resize': EffectArgParser(2, 3, [
        ArgPositiveInt(),
        ArgPositiveInt(),
        ArgColorRule()
    ]),
    'rgb_posterize': EffectArgParser(0, 1, [
        ArgRangeRule(0, 255)
    ]),
    'multiply': EffectArgParser(0, 0,[], True)
}
