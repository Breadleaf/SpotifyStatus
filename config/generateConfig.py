import sys
import os

# TODO: implement a updateConfigFile() to fix invalid config or missing config fields

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = f"{FILE_PATH}/config.py"

DEBUG = os.environ.get("DEBUG", None) is not None
STRICT = os.environ.get("STRICT", None) is not None
EXPECTED_FIELDS = [
    "CLIENT_ID",
    "CLIENT_SECRET",
    "REDIRECT_URI",
    "SCOPE",
    "CACHE_PATH",
    "DATA_PATH",
    "DEFAULT_DATA_PATH",
    "POLLING_DELAY",
    # "IMAGE_WIDTH",
    # "IMAGE_HEIGHT",
]

def validateConfigFields(configFields, errorMessage):
    if STRICT and not all(key in configFields.keys() for key in EXPECTED_FIELDS):
        print("-" * 40, file=sys.stderr)
        print(f"STRICT MODE: {errorMessage}", file=sys.stderr)
        print("DETAILS:", file=sys.stderr)
        print("- EXPECTED_FIELDS", EXPECTED_FIELDS, sep="\n", file=sys.stderr)
        print("- list(configFields.keys())", list(configFields.keys()), sep="\n", file=sys.stderr)
        print("-" * 40, file=sys.stderr)
        sys.exit(1)


def generateConfigFields():
    print("CLIENT_ID, CLIENT_SECRET, and REDIRECT_URI must be the exact same from the spotify dev portal")

    fields = {
        "CLIENT_ID" : lambda: input("CLIENT_ID: ").strip() \
            or None,

        "CLIENT_SECRET" : lambda: input("CLIENT_SECRET: ").strip() \
            or None,

        # NOTE: rewrite section in the README.md, it only needs to match spotify, doesn't even need to exist
        # tldr, user shouldn't try to make an endpoint unless they are doing too much <3
        "REDIRECT_URI" : lambda: input("REDIRECT_URI: ").strip() \
            or None,

        # TODO: this should be hard coded, spotify weird
        "SCOPE" : lambda: input("[user-read-playback-state user-read-currently-playing] SCOPE: ").strip() \
            or "user-read-playback-state user-read-currently-playing",

        "CACHE_PATH" : lambda: input("[./.cache] CACHE_PATH: ").strip() \
            or "./.cache",

        "DATA_PATH" : lambda: input("[./.data] Relative from project root! DATA_PATH: ").strip() \
            or "./.data",

        "DEFAULT_DATA_PATH" : lambda: input("[./.defaults] Relative from project root! DEFAULT_DATA_PATH: ").strip() \
            or "./.defaults",

        "POLLING_DELAY": lambda: float(
            input("[0.6] POLLING_DELAY").strip() \
                or 0.7
        ),

        # "IMAGE_WIDTH" : lambda: int(
        #     input("[300] IMAGE_WIDTH: ").strip() \
        #         or 300
        # ),

        # "IMAGE_HEIGHT" : lambda: int(
        #     input("[300] IMAGE_HEIGHT: ").strip() \
        #         or 300
        # ),
    }

    validateConfigFields(fields, "generateConfigFields() is out of date.")

    try:
        for field, func in fields.items():
            fields[field] = func()
    except Exception as ex:
        print(ex, type(ex), file=sys.stderr)
        sys.exit(1)

    return fields


def generateConfigFile(configFields):
    validateConfigFields(
        configFields,
        "generateConfigFile(configFields): configFields is missing fields."
    )

    try:
        configFile = open(CONFIG_PATH, "w", encoding="utf-8")
    except Exception as ex:
        print(ex, type(ex), file=sys.stderr)
        sys.exit(1)

    for field, value in configFields.items():
        if isinstance(value, str): value = f"\"{value}\""
        configFile.write("{0} = {1}\n".format(field, value))

    configFile.close()


if __name__ == "__main__":
    print("THIS SCRIPT USES `[]` TO DENOTE A DEFAULT PARAMETER!")

    overwrite = not os.path.exists(CONFIG_PATH)
    overwrite = overwrite \
        or input("[No] Overwrite existing config? ").strip().lower() in ["yes", "y"]
    if overwrite:
        gcf = generateConfigFields()
        if DEBUG: print("DEBUG", gcf, sep="\n")
        generateConfigFile(gcf)
