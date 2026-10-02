from pathlib import Path
from process_mg_data import read_mgfile, config

import re

pattern = re.compile(r'^([A-Za-z]+)_(\d{12})(?:-(mod(?:ified)?))?\.csv$')

def _update_name(filename):
    m = pattern.match(filename)
    if not m:
        return filename  # unexpected format, leave alone
    prefix, timestamp, suffix = m.groups()
    if suffix:
        return f"{prefix}_{timestamp}-{suffix}-new.csv"
    return f"{prefix}_{timestamp}-mod.csv"


def preprocess_mgfile(filename, config):
    """
    Ensures that all numerical columns (e.g. gas concentrations, ratios, gps
    coordinates are in proper numeric format and rewrites the csv file.
    """

    sep   = config.get('DEFAULT', 'sep')
    dtfmt = config.get('DEFAULT', 'dtfmt')

    regex = re.compile(r'.*[-_](?:mod(?:ified)?)?\.csv')
    fn    = Path(filename)
    outfn = _update_name(fn.name)
    data  = read_mgfile(filename, config)
    
    data.to_csv(outfn, sep=sep, date_format=dtfmt, index=False)

    return data


if __name__ == '__main__':
    regex     = re.compile(r'(OPGC|OVSG|guada).*\.csv$')
    filenames = sorted(p for p in Path('.').rglob('*.csv')
                       if regex.search(p.name) is not None)

    for filename in filenames:
        preprocess_mgfile(filename)
