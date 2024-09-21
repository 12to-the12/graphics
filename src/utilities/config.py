import tomli
import types

with open("config.toml", "rb") as file:
    try:
        config_dict = tomli.load(file)
    except tomli.TOMLDecodeError:
        raise Exception("invalid TOML config file")


# Define a function to recursively convert nested dictionaries to SimpleNamespace objects
def to_namespace(obj):
    if isinstance(obj, dict):
        for key, val in obj.items():
            obj[key] = to_namespace(val)
        return types.SimpleNamespace(**obj)
    elif isinstance(obj, list):
        return [to_namespace(val) for val in obj]
    else:
        return obj


# Convert the dictionary into a namespace object
config = to_namespace(config_dict)


if config.raster.individual:
    config.window.scaling = 1


if __name__ == "__main__":
    print(type(config_dict))
