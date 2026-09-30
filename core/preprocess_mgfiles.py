from pathlib import Path
from .mg_common import read_mgfile, mg_fmt_conf

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


def preprocess_mgfile(filename, mg_fmt_conf=mg_fmt_conf):
    """
    Ensures that all numerical columns (e.g. gas concentrations, ratios, gps
    coordinates are in proper numeric format and rewrites the csv file.
    """

    sep, _, date_format = mg_fmt_conf.values()

    regex = re.compile(r'.*[-_](?:mod(?:ified)?)?\.csv')
    fn    = Path(filename)
    outfn = _update_name(fn.name)
    data  = read_mgfile(filename, mg_fmt_conf)
    
    data.to_csv(outfn, sep=sep, date_format=date_format, index=False)

    return data


if __name__ == '__main__':
    regex     = re.compile(r'(OPGC|OVSG|guada).*\.csv$')
    filenames = sorted(p for p in Path('.').rglob('*.csv')
                       if regex.search(p.name) is not None)

    for filename in filenames:
        preprocess_mgfile(filename)
