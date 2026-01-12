import pygame
import sys
import json

# Read HTML file
with open("index.html", "r") as f:
    html = f.read()

stack = []
root = None
i = 0
length = len(html)

branch = []
name = ""
open = False

tree = {}

while i < length:
    print("\n")
    if html[i] == "<" and html[i+1] != "/":
        close = 1
        while html[close + i] != ">":
            name += html[close + i]
            close += 1

        i += close + 1

        if not open:
            open = True

        branch.append(name)

        treemaker = tree
        if len(branch) == 1:
            tree[name] = { "name": name, "children": {} }
        else:
            for b in branch:
                if b == "body":
                    treemaker = tree["body"]
                else:
                    treemaker["children"][b] = { "name": b, "children": {} }
                    treemaker = treemaker["children"][b]
        
        name = ""

    elif html[i] == "<" and html[i+1] == "/":
        if open and len(branch) > 0:
            print(branch)
            del branch[-1]
            i += 1
    else:
        i += 1

print("branch: ", branch)
print(tree)