
import gzip
import json

with gzip.open(input('path to file'), 'rt') as f:
    count = 0
    for line in f:
        if "id" in line:
                count += 1
        data = json.loads(line)
        print(data)
print(count)
