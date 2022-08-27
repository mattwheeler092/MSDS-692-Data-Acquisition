from mycsv import getdata, readcsv

# Helper functions to create HMTL string
add_tag = lambda data, tag: f"<{tag}>{data}</{tag}>"
add_data = lambda data, tag: "".join([add_tag(d, tag) for d in data])
create_line = lambda data, tag: f"<tr>{add_data(data, tag)}</tr>\n"

# Load csv file passed as terminal argument
headers, data = readcsv(getdata())

# Create HTML string to return
html = "<html>\n<body>\n<table>\n"
html += create_line(headers, tag="th")
for line in data:
    html += create_line(line, tag="td")
html += "</table>\n</body>\n</html>"

# Return the string to the terminal
print(html)
