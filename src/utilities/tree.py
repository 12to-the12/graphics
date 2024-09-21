import functools
from utilities.clear_terminal import clear_terminal

# from clipboard import copy


def tree(funct):
    """wrapper
    adds the function's time taken  to the buffer"""
    global indent

    @functools.wraps(funct)
    def out_funct(*args, **kwargs):
        global indent, prev_indent

        # escalate
        indent += 1
        if prev_indent != indent:
            blocks.append(">")

        # add to lists
        blocks.append(funct.__name__)
        prefix = "|  " * indent

        push(prefix + funct.__name__)

        # execute function
        prev_indent = indent
        out = funct(*args, **kwargs)

        if prev_indent != indent:
            blocks.append("<")
        # deescalate
        indent -= 1

        return out

    return out_funct


buffer = ""
blocks = []
indent = -1
prev_indent = indent


def push(message, end="\n"):
    """pushes message to the message heap"""
    global buffer
    buffer += end + message


def dump():
    global buffer, blocks
    # clear_terminal()

    # print(buffer)

    # print('\n')
    blocks = blocks[1:]
    for index, block in enumerate(blocks):
        try:
            if block == "<" and blocks[index + 1] == ">":
                del blocks[index + 1]
        except:
            pass
    indent = 0
    for block in blocks:
        if block == ">":
            indent += 1
        elif block == "<":
            indent -= 1
        else:
            ind = indent * 4 * " "
            print(ind + block)

    print("\nblocks:", blocks)

    header = """\n:::mermaid\ngraph TB\n    start((start)) -->\n"""
    footer = """End((end))\n:::"""
    # x = header + render(blocks) + footer
    # with open('mermaid.md', 'w') as mermaid:
    #    mermaid.write(x)
    # print(x)
    print(render(blocks))

    buffer = ""
    blocks = []


counter = -1


# build nested dict first
def render(blocks, level=0, root="root"):
    print(f"<building {root}>")
    global counter
    assert type(root) is str
    structure = {}
    level = 0
    if counter == len(blocks):
        print("breaking")
        print(f"returning out{structure}")
        return "xxx"
    while 1:
        counter += 1
        block = blocks[counter]
        # print('\ncounter:',counter, 'len:',len(blocks))

        if block == ">":
            level += 1
            parent = blocks[counter - 1]
            structure[parent] = render(blocks, root=parent)
        elif block == "<":
            level -= 1
            print(f"<returning {structure} to {root}>")
            return structure
        else:
            print(f"{block}@{counter}/{len(blocks)}")
            structure[str(block)] = block
