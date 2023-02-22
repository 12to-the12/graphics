import tomli

with open('config.toml', 'rb') as file:
    try: config = tomli.load(file)
    except tomli.TOMLDecodeError:
        raise Exception('invalid TOML config file')
    


individual = config['raster']['individual']
if individual:
    config['window']['scaling'] = 1