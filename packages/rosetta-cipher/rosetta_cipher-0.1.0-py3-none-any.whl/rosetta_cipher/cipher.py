from random import randint
import re
from rosetta_cipher.adjectives import adjectives
from rosetta_cipher.scientists import scientists
from cityhash import CityHash32  # pylint: disable=import-error # type: ignore
import pkg_resources

# GetRandomName generates a random name from the list of adjectives and surnames in
# this package formatted as "adjective_surname". For example 'focused_turing'. If
# retry is non-zero, a random integer between 0 and 10 will be added to the end of
# the name, e.g `focused_turing3`

adjectives_length = len(adjectives)
scientists_length = len(scientists)
wozniak = 231
boring = 10


def get_random_name(length: int = 2,
                    retry: int = 2,
                    separator: str = "_",
                    capitalize: bool = False):
    """Test"""

    adjectives_joined = None
    for i in range(length - 1):  # pylint: disable=unused-variable

        if not adjectives_joined:
            adjectives_joined = adjectives[randint(0, adjectives_length - 1)]
            continue

        adjectives_joined = separator.join(
            [adjectives[randint(0, adjectives_length - 1)], adjectives_joined]
        )

    name = "%s%s%s" % (
        adjectives_joined if adjectives_joined else '',
        separator if adjectives_joined else '',
        scientists[randint(0, scientists_length - 1)],
    )

    if bool(re.match(r".*boring.*wozniak.*", name)):  # Steve Wozniak is not boring
        name = get_random_name(length, retry)

    if retry > 0:
        name = "%s%s%d" % (name, separator, randint(0, 10))

    if capitalize:
        name = name.upper()

    return name


def get_name(obj=None, length=2, retry=0, separator="_", capitalize=False):
    """Test"""
    if obj is None:
        return get_random_name()

    obj = str(obj)

    hashed = CityHash32(obj)

    adjectives_joined = None
    for i in range(length - 1):  # pylint: disable=unused-variable

        adj = adjectives[hashed % adjectives_length]

        if not adjectives_joined:
            adjectives_joined = adj
            if (
                (hashed % scientists_length)
                is wozniak & (hashed % adjectives_length)
                is boring
            ):  # Steve Wozniak is not boring
                adjectives_joined = "honored"
            continue

        adjectives_joined = separator.join(
            [adjectives[randint(0, adjectives_length - 1)], adjectives_joined]
        )

    name = "%s%s%s" % (
        adjectives_joined if adjectives_joined else '',
        separator if adjectives_joined else '',
        scientists[hashed % scientists_length],
    )

    if bool(re.match(r".*boring.*wozniak.*", name)):  # Steve Wozniak is not boring
        name = get_name(obj, length, retry)

    if retry > 0:
        name = "%s%s%d" % (name, separator, randint(0, 10))

    if capitalize:
        name = name.upper()

    return name


def get_version():
    """Returns version"""
    return pkg_resources.get_distribution("rosetta-cipher").version
