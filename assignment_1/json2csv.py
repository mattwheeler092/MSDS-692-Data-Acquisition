import json

from mycsv import getdata

# Helper functions to create CSV string
add_line = lambda line: ",".join(line) + "\n"

# Load JSON file passed as terminal argument
data = json.loads(getdata())

# Extract headers and data from JSON dictionary
headers = data["headers"]
data = [list(record.values()) for record in data["data"]]

# Create csv output string
csv = add_line(headers)
for line in data:
    csv += add_line(line)
csv = csv.strip('\n')

# Return the string to the terminal
print(csv)
