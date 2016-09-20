from collections import defaultdict
from fitparse import FitFile

def grab_data(filename, target_units=[]):
    fitfile = FitFile(filename)
    results = defaultdict(list)
    for record in fitfile.get_messages('record'):
        for record_data in record:
            if len(target_units) > 0 and record_data.name not in target_units:
                continue
            results[record_data.name].append(record_data.value)
    return results
