import graphviz
import regex as re

# GLOBALS
i = 0
position_dict = {}
position_nodes = set()
step_nodes = set()
dot = graphviz.Digraph(comment='Jiu Jitsu')

MAJOR = {
    'shape':'house',
    'fontcolor':'white',
    'style':'filled',
    }
MAJOR_TOP = "#27AE60"
MAJOR_BOTTOM = "#E74C3C"
MAJOR_NEUTRAL = "#F1C40F"

MINOR = {
    'shape':'hexagon',
    'style':'filled',
}
MINOR_TOP = "#58D68D"
MINOR_BOTTOM = "#EC7063"
MINOR_NEUTRAL = "#F4D03F"

symbol_to_key = {
    '^': "TOP_",
    '!': "BOT_",
    '~': "NEU_"
}

FNAME = "sample.jjml"
lines = []
with open(FNAME) as f:   
    for line in f:
        lines.append(line)


def position_parsing(lines, type):
    global i
    while lines[i] != "}\n":
        position = lines[i].strip().split(": ")
        position_dict[position[0]] = (position[1], type)
        i += 1

def add_position_if_not_exists(style, name, tip):
    if name not in position_nodes:
        if position_dict[name][1] == "major":
            style_dict = MAJOR
            style_dict['color'] = MAJOR_TOP if style == '^' else MAJOR_BOTTOM if style == '!'else MAJOR_NEUTRAL
        elif position_dict[name][1] == "minor":
            style_dict = MINOR
            style_dict['color'] = MINOR_TOP if style == '^' else MINOR_BOTTOM if style == '!'else MINOR_NEUTRAL
        dot.node(f"{symbol_to_key[style]}{name}", position_dict[name][0] , style_dict, tooltip= tip)
        position_nodes.add(name)

def add_step_if_not_exists(style, name, tip):
    if name not in position_nodes:
        if position_dict[name][1] == "major":
            style_dict = MAJOR
            style_dict['color'] = MAJOR_TOP if style == '^' else MAJOR_BOTTOM if style == '!'else MAJOR_NEUTRAL
        elif position_dict[name][1] == "minor":
            style_dict = MINOR
            style_dict['color'] = MINOR_TOP if style == '^' else MINOR_BOTTOM if style == '!'else MINOR_NEUTRAL
        dot.node(f"{symbol_to_key[style]}{name}", position_dict[name][0], style_dict)
        position_nodes.add(name)

def tech_regex(line):
    style_regex = r"([\^!~#*?$])"
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
            style_a, name_a, tip_a, style_b, name_b, tip_b = step
            # Check if named
            if style_a in ['^', '!', '~']:
                add_position_if_not_exists(style_a, name_a, tip_a)
            elif style_a in ['#', '*', '?', '$']:
                pass
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

print(position_nodes)
print(dot.source)
