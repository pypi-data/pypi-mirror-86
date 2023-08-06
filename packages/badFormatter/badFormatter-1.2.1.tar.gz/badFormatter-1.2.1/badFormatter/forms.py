def read_file(filename):
    return [line.replace('\n', '') for line in open(filename, 'r')]


def formatter(text):
    form = '{:<' + str(max([len(line) for line in text]) + 1) + '}'
    for idx, line in enumerate(text):
        line = form.format(line)
        to_add = []
        new_line = []
        for charidx, char in enumerate(line):
            if char in '{}':
                to_add.append(char)
                new_line.append(' ')
            elif char == ';' and len(set(line[charidx:])) == 2:
                to_add.append(char)
                new_line.append(' ')
            else:
                new_line.append(char)

        if len(set(new_line)) == 1 or len(set(new_line)) == 0:
            found, i = False, 1
            while not found:
                if len(text[idx - i]) > 1:
                    break
                i += 1
            text[idx - i] = ''.join(list(text[idx - i]) + to_add)
            text[idx] = ''
        else:
            new_line += to_add
            text[idx] = ''.join(new_line)

    result = ''
    for line in text:
        if line:
            result += line + '\n' if line else ''
    return result


def shitify_print(filename):
    print(formatter(read_file(filename)))


def shitify_return(filename):
    return formatter(read_file(filename))


def shitify_print_text(text):
    text = [line.replace('\n', '') for line in text.split('\n')]
    print(formatter(text))


def shitify_return_text(text):
    text = [line.replace('\n', '') for line in text.split('\n')]
    return formatter(text)

