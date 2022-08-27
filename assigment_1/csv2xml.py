from mycsv import getdata, readcsv

# Helper functions to create HMTL string
xml_data = lambda data, header: f"<{header}>{data}</{header}>"
xml_line = lambda line: "".join(xml_data(data, header) for data, header in line)

# Load csv file passed as terminal argument
headers, data = readcsv(getdata())

# Create XML string to return
xml = '<?xml version="1.0"?>\n<file>\n'
xml += f"\t<headers>{','.join(headers)}</headers>\n"
xml += "\t<data>\n"
for record in data:
    xml += "\t\t<record>\n"
    xml += f"\t\t\t{xml_line(zip(record, headers))}\n"
    xml += "\t\t</record>\n"
xml += "\t</data>\n</file>"

# Return the XML string to the terminal
print(xml)
