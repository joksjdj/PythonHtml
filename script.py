import pygame
import sys
import json

class Node:
    def __init__(self, tag, parent=None):
        self.tag = tag
        self.parent = parent
        self.children = []

    def add_child(self, child):
        self.children.append(child)

# Read HTML file
with open("index.html", "r") as f:
    html = f.read()

stack = []
root = None
i = 0
length = len(html)



while i < length:
    if html[i] == "<":
        # closing tag
        if i+1 < length and html[i+1] == "/":
            j = i + 2
            while j < length and html[j] != ">":
                j += 1
            # pop current node
            stack.pop()
            i = j + 1
        else:
            # opening tag
            j = i + 1
            while j < length and html[j] != ">":
                j += 1
            tag_content = html[i+1:j]  # e.g., div id='box'
            
            # check for id attribute
            if "id=" in tag_content:
                # extract id value
                start = tag_content.find("id=") + 3
                quote = tag_content[start]
                if quote in "'\"":
                    start += 1
                    end = tag_content.find(quote, start)
                    tag_name = tag_content[start:end]

                el_type = tag_content.split()[0]
                tag_name = tag_name + f" id {el_type}"
            else:
                # no id, use tag name
                tag_name = tag_content.split()[0]  # div, body, etc.

            node = Node(tag_name, stack[-1] if stack else None)
            if stack:
                stack[-1].add_child(node)
            else:
                root = node

            stack.append(node)
            i = j + 1
    else:
        i += 1

pygame.init()

# Initial size
width, height = 800, 600

# Create resizable window
body = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Resizable Pygame Window")


set_style = {}
def set_style_f():
    global set_style
    with open("style.json", "r") as style:
        style_file = json.load(style)

        if parent != "none":
            print (set_style[parent])
            parent_width = set_style[parent]["rect"][2]
            parent_height = set_style[parent]["rect"][3]
            parent_x = set_style[parent]["rect"][0]
            parent_y = set_style[parent]["rect"][1]
        else:
            parent_width = width
            parent_height = height
            parent_x = 0
            parent_y = 0

        if tag in style_file:
            el = style_file[tag]
        else:
            el = style_file["defaults"]
        print(el)

        size = el["size"]

        draw_width = float(size["width"]["value"])
        draw_height = float(size["height"]["value"])
        if size["width"]["type"] == "%":
            draw_width = (draw_width / 100) * parent_width
        if size["height"]["type"] == "%":
            draw_height = (draw_height / 100) * parent_height

        color = tuple(map(int, el["color"].split(", ")))
        
        position = el["position"]
        pos_x = float(position["x"]["value"]) + parent_x
        pos_y = float(position["y"]["value"]) + parent_y
        if position["x"]["type"] == "%":
            pos_x = ((pos_x / 100) * parent_width) + parent_x
        if position["y"]["type"] == "%":
            pos_y = ((pos_y / 100) * parent_height) + parent_y

        set_style[tag] = {"color": color, "rect": (pos_x, pos_y, draw_width, draw_height), "percent": position, "parent": parent}

        print("set_style:", set_style)

        parent = tag

# Helper to print tree
def print_tree(node, indent=0):
    global set_style
    print("  " * indent + node.tag)

    set_parent = {}

    parent = "none"
    for child in node.children:

        if "id" in child.tag:
            type = child.tag.split(" id ")[1]
            tag = child.tag.split(" id ")[0]
        else:
            type = child.tag
            tag = child.tag

        print_tree(child, indent + 1)
        print(tag + "\n" + parent)

        set_parent[tag] = {"parent": parent, "type": type, "id": tag}

        
    print("parent and type:",set_parent)

print_tree(root)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detect window resize
        if event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            body = pygame.display.set_mode((width, height), pygame.RESIZABLE)

            for tag, style in set_style.items():
                pos = style["percent"]
                pos_x = float(pos["x"]["value"])
                pos_y = float(pos["y"]["value"])
                if pos["x"]["type"] == "%":
                    pos_x = (pos_x / 100) * width
                if pos["y"]["type"] == "%":
                    pos_y = (pos_y / 100) * height

                rect = style["rect"]
                draw_width = rect[2]
                draw_height = rect[3]

                set_style[tag]["rect"] = (pos_x, pos_y, draw_width, draw_height)

            print(f"Window resized to: {width}x{height}")

    body.fill((0, 0, 0))

    for tag, style in set_style.items():
        pygame.draw.rect(body, style["color"], style["rect"])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
