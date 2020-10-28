import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfiles', metavar='', type=str, nargs=2, required=False,
                        help='The file you wish to use as input for the program.')
    args = parser.parse_args()
    return args


def read_bad_file(file):
    bad_dict = {}
    with open(file, "r") as f:
        for line in f:
            bad_dict[line.rstrip()] = False
    return bad_dict


def read_file(file, bad_dict):
    reads, lines = [], []
    with open(file, 'r') as f:
        for count, line in enumerate(f):

            if count != 0 and count % 4 == 0:
                if bad_dict.get(lines[0].split(' ')[0], True):
                    reads += lines[0], lines[1], lines[3]

                lines = []
            lines.append(line.rstrip())

    if len(reads) != 0:
        count += 1
        reads += lines[0], lines[1], lines[3]
    return reads


def write_out(path, data):
    write_string = ""

    with open(path, 'a+') as f:
        for x in range(0, len(data), 3):
            write_string += f'{data[x]}\n{data[x + 1]}\n+\n{data[x + 2]}\n'
            if x % (1_000_000 * 3) == 0 and x != 0:
                f.write(write_string)
                write_string = ""
        if write_string != "":
            f.write(write_string)
    return f"Completed! Wrote {len(data) / 3} sequences to: {path}\n"


def create_complete_dict(inputfiles):
    bad_dict1 = read_bad_file(inputfiles[0])
    bad_dict2 = read_bad_file(inputfiles[1])
    complete_dict = {**bad_dict1, **bad_dict2}
    return complete_dict


def clean_file(path):
    with open(path, 'w') as f:
        f.write("")
    return f"Removed content from file: {path}"


def main_process(inputfiles):
    for file in inputfiles:
        print(clean_file(file.split('_bad.fastq')[0] + '_trimmed.fastq'))
    complete_dict = create_complete_dict(inputfiles)

    data = read_file(inputfiles[0].split("_bad.fastq")[0] + '_good.fastq', complete_dict)
    print(write_out(inputfiles[0].split("_bad.fastq")[0]+"_trimmed.fastq", data))
    del data
    data = read_file(inputfiles[1].split("_bad.fastq")[0] + '_good.fastq', complete_dict)
    print(write_out(inputfiles[1].split("_bad.fastq")[0]+"_trimmed.fastq", data))
    del data

    print("Removing old files")
    for item in inputfiles:
        os.remove(item)
        os.remove(item.split("_bad.fastq")[0] + '_good.fastq')


if __name__ == '__main__':
    args = parse_args()
    if not args.inputfiles:
        args.inputfiles = ['testbestand_paired_fw_bad.fastq', 'testbestand_paired_rv_bad.fastq']

    main_process(args.inputfiles)
