import argparse


GB_QUAL_DICT = {}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfile', metavar='File', type=str, nargs=1, required=False,
                        help='The file you wish to use as input for the program.')
    parser.add_argument('-o', '--outputfile', metavar='Directory', type=str, default="Trimmed_file.txt",
                        help='Use this to select an name for the output file')
    parser.add_argument('-t', '--threads', metavar='number of threads', type=int, default=4,
                        help='Give the number of threads you would like to use.')
    parser.add_argument('-c', '--chunks', metavar='number of reads to load into RAM', type=int,
                        default=2_000, help='Give the number of reads you wish to process at the same time.')
    args = parser.parse_args()
    return args


def trim_read(read):
    length = len(read["qual"])//2

    pos = split_seq(read['qual'][length::])
    read['seq'] = read["seq"][0:pos+length]
    read['qual'] = read["qual"][0:pos+length]

    pos = split_seq(read["qual"][::-1])
    read["seq"] = read["seq"][-pos::]
    read["qual"] = read["qual"][-pos::]
    return read


def split_seq(quality):
    for x in range(len(quality)-4):
        if GB_QUAL_DICT.get(quality[x:x+5], calc_quality_score(quality[x:x + 5])):
            return x+4
    return len(quality)


def calc_quality_score(values):
    score_num = 0
    for x in range(len(values)):
        score_num += ord(values[x])-33
    if score_num >= 100:
        GB_QUAL_DICT[values] = False
        return False
    elif score_num < 100:
        GB_QUAL_DICT[values] = True
        return True


def load_file(path):
    read_dict, lines = {}, []
    with open(path, 'r') as f:
        for count, line in enumerate(f, 1):
            lines.append(line.rstrip())
            if count % 4 == 0:
                read_dict[int(count/4)] = {
                    "id" : lines[0],
                    "seq": lines[1],
                    "qual": lines[3]
                }
                lines = []
        if lines:
            print(count+1 / 4)
            read_dict[int(count+1 / 4)] = {
                "id": lines[0],
                "seq": lines[1],
                "qual": lines[3]
            }
    return read_dict


def write_file(path, data):
    write_string = ""

    with open(path, 'a+') as f:
        for x in range(1, len(data.keys())+1, 1):
            write_string += f'{data[x]["id"]}\n{data[x]["seq"]}\n+\n{data[x]["qual"]}\n'
            if x % 1_000_000 == 0:
                f.write(write_string)
                write_string = ""
                print(f"Wrote {x} reads.")
        if write_string != "":
            f.write(write_string)


def clean_file(path):
    with open(path, 'w') as f:
        f.write("")
    return f"Removed content from file: {path}"


def main_process(inputfile, outputfile):
    data = load_file(inputfile)
    print(clean_file(outputfile))
    for x in range(1, len(data.keys()) + 1, 1):
        data[x] = trim_read(data[x])
        if x % 1_000_000 == 0:
            print(f"Trimmed {x} reads.")
    write_file(outputfile, data)


if __name__ == '__main__':
    args = parse_args()
    main_process(args.inputfile, args.outputfile)