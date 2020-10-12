from time import sleep

def load_file(path):
    lines = []
    with open(path, 'r') as f:
        for line in f:
            lines.append(line.rstrip())
    return lines


if __name__ == '__main__':
    data = load_file('/exports/bngsa_nietinfected_1.fastq')
    sleep(60)