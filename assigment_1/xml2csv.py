import untangle

from mycsv import getdata

# Helper functions to create CSV string
add_line = lambda line: ",".join(line) + "\n"

# Load xml file passed as terminal argument
xmldata = untangle.parse(getdata())

# Extract headers and data from raw XML string
headers = xmldata.file.headers.cdata.split(",")
data = {header: [] for header in headers}
for record in xmldata.file.data.record:
    for element in record.children:
        data[element._name].append(element.cdata)
data = list(map(list, zip(*data.values())))

# Create csv output string
csv = add_line(headers)
for line in data:
    csv += add_line(line)

# Return the string to the terminal
print(csv)

