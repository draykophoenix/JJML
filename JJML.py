import graphviz
import regex as re

dot = graphviz.Digraph(comment='Jiu Jitsu')

MAJOR = {
    'shape':'house',
    'fontcolor':'white',
    'style':'filled',
    }

MINOR = {
    'shape':'hexagon',
    'style':'filled',
}

FNAME = "sample.jjml"
lines = []
with open(FNAME) as f:   
    for line in f:
        lines.append(line)

i = 0
nodes = {}
def position_parsing(lines, type):
    global i
    while lines[i] != "}\n":
        i += 1

def tech_regex(line):
    style_regex = r"([\^\-!#*?$])"
    name_regex = r"((?:[a-z]+)|(?:\[[a-z ]+\]))"
    tip_regex = r"(?:{([a-z,;'\"\-\n<> ]+)})?"
    return re.findall(f"{style_regex}{name_regex}{tip_regex} -> {style_regex}{name_regex}{tip_regex}", line, overlapped=True, flags=re.IGNORECASE)

def tech_parsing(lines):
    global i
    m = re.match(r"tech \(([a-z_]+)\) {", lines[i])
    print(m.group(1))
    i += 1
    while (lines[i] != "}\n") and (lines[i] != "}"):
        chain = tech_regex(lines[i])
        for step in chain:
            print(step)
        i += 1

while i < len(lines):
    m = re.match(r"major|minor|tech", lines[i])
    if m:
        match m.group(0):
            case "major":
                i += 1
                position_parsing(lines, "major")
            case "minor": 
                i += 1
                position_parsing(lines, "minor")
            case "tech":
                tech_parsing(lines)
    i += 1

print(nodes)
print(dot.source)
