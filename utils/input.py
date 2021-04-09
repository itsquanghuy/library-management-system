from datetime import date


def date_input(text):
    return date(*list(map(int, input(text).split("-"))))


def multiline_input(text):
    print(text)
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    return '\n'.join(lines)
