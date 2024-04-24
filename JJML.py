import graphviz
import regex as re

# GLOBALS
i = 0
position_to_name = {}
position_nodes = set()
step_nodes = set()
dot = graphviz.Digraph(comment='Jiu Jitsu')

MAJOR = {
    'shape':'house',
    'fontcolor':'white',
    'style':'filled',
    }
# ^
MAJOR_TOP = "#27AE60"
# !
MAJOR_BOTTOM = "#E74C3C"
# ~
MAJOR_NEUTRAL = "#F1C40F"

MINOR = {
    'shape':'hexagon',
    'style':'filled',
}
# ^
MINOR_TOP = "#58D68D"
# !
MINOR_BOTTOM = "#EC7063"
# ~
MINOR_NEUTRAL = "#F4D03F"

# #
CHECKPOINT = {
    'color': "#E59866",
    'shape': 'box'
}
# *
MOVE = {
    'color': "#76D7C4"
}
# ?
CONDITION = {
    'color': "#7FB3D5",
    'shape': 'diamond'
}
# $
SUBMISSION = {
    'color': "#BB8FCE",
    'shape': 'triangle'
}

symbol_to_key = {
    '^': "TOP",
    '!': "BOT",
    '~': "NEU"
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
        position_to_name[position[0]] = (position[1], type)
        i += 1

def add_position_if_not_exists(id, style, code, tip):
    if code not in position_nodes:
        if position_to_name[code][1] == "major":
            style_dict = MAJOR
            style_dict['color'] = MAJOR_TOP if style == '^' else MAJOR_BOTTOM if style == '!'else MAJOR_NEUTRAL
        elif position_to_name[code][1] == "minor":
            style_dict = MINOR
            style_dict['color'] = MINOR_TOP if style == '^' else MINOR_BOTTOM if style == '!'else MINOR_NEUTRAL
        dot.node(id, position_to_name[code][0] , style_dict, tooltip= tip)
        position_nodes.add(id)

def add_step_if_not_exists(id, style, name, tip):
    name = name[1:-1] # Remove the brackets
    if name not in step_nodes:
        match style:
            case "#":
                style_dict = CHECKPOINT
            case "*":
                style_dict = MOVE
            case "?":
                style_dict = CONDITION
            case "$":
                style_dict = SUBMISSION

        dot.node(id, name, style_dict, tooltip= tip)
        step_nodes.add(id)

def tech_regex(line):
    style_regex = r"([\^!~#*?$])"
    name_regex = r"((?:[a-z]+)|(?:\[[a-z ]+\]))"
    tip_regex = r"(?:{([a-z,;'\"\-\n<> ]+)})?"
    return re.findall(f"{style_regex}{name_regex}{tip_regex} -{tip_regex}> {style_regex}{name_regex}{tip_regex}", line, overlapped=True, flags=re.IGNORECASE)

def tech_parsing(lines):
    global i
    m = re.match(r"tech \(([a-z_]+)\) {", lines[i])
    tech_name = m.group(1)
    i += 1
    while (lines[i] != "}\n") and (lines[i] != "}"):
        chain = tech_regex(lines[i])
        for step in chain:
            position_id = lambda name, style: f"{symbol_to_key[style]}__{name}"
            step_id = lambda name, tech_name: f"{tech_name}__{name}"

            id_a, id_b = ("","")

            style_a, name_a, tip_a, edge_tip, style_b, name_b, tip_b = step
            # Check if named
            if style_a in ['^', '!', '~']:
                id_a = position_id(name_a, style_a)
                add_position_if_not_exists(id_a, style_a, name_a, tip_a)
            elif style_a in ['#', '*', '?', '$']:
                id_a = step_id(name_a, tech_name)
                add_step_if_not_exists(id_a, style_a, name_a, tip_a)

            if style_b in ['^', '!', '~']:
                id_b = position_id(name_b, style_b)
                add_position_if_not_exists(id_b, style_b, name_b, tip_b)
            elif style_b in ['#', '*', '?', '$']:
                id_b = step_id(name_b, tech_name)
                add_step_if_not_exists(id_b, style_b, name_b, tip_b)
            dot.edge(id_a, id_b)
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

print(dot.source)
