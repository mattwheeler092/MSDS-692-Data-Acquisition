from mycsv import getdata, readcsv

# Helper functions to create HMTL string
json_data = lambda data, header: f'"{header}":"{data}"'
json_line = lambda line: ", ".join(json_data(data, header) for data, header in line)

# Load csv file passed as terminal argument
headers, data = readcsv(getdata())

# Create JSON string to return
json = "{\n"
header_str = '", "'.join(headers)
json += f'\t"headers":["{header_str}"],\n'
json += '\t"data":[\n'
for i, record in enumerate(data):
    json += "\t\t{\n"
    json += f"\t\t\t{json_line(zip(record, headers))}\n"
    json += "\t\t}"
    if i != len(data) - 1:
        json += ",\n"
    else:
        json += "\n"
json += "\t]\n}"

# Return the XML string to the terminal
print(json)
