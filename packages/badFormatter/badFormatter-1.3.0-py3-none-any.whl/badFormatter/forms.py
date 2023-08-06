def read_file(filename):
    return [line.replace('\n', '') for line in open(filename, 'r')]


def formatter(text):
    result = ''
    form = '{:<' + str(max([len(line) for line in text]) + 5) + '}'
    for idx, line in enumerate(text):
        to_add = []
        for cidx,char in list(enumerate(line))[::-1]:
            if char not in '{}; ':
                break
            else:
                to_add.append(char)
        try:
            to_add = to_add[::-1].remove(' ')
        except:
            to_add = to_add[::-1]
        if not to_add:
            to_add = []
        newline = ''.join( list(form.format(line.replace('{','').replace('}','').replace(';',''))) + to_add)
        if not len(set(newline)) == 1 or len(set(newline)) == 0:
            result += (newline+'\n')



    return result



'''
def formatter(text):
    form = '{:<' + str(max([len(line) for line in text]) + 5) + '}'
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
'''

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

shitify_print_text('''#include <stdio.h>
int main() {
    int n1, n2, max;
    printf("Enter two positive integers: ");
    scanf("%d %d", &n1, &n2);{}

    // maximum number between n1 and n2 is stored in min
    max = (n1 > n2) ? n1 : n2;

    while (1) {
        if (max % n1 == 0 && max % n2 == 0) {
            printf("The LCM of %d and %d is %d.", n1, n2, max);
            break;
        }
        ++max;
    }
    return 0;
}
''')