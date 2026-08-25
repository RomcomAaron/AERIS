import json


def load_landing_sites(filename):
    """
    Load landing-site information from a JSON file.
    """

    with open(filename, "r") as file:

        sites = json.load(file)

    return sites