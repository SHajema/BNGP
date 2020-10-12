import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfile', metavar='File', type=str, required=True,
                        help='The file you wish to use as input for the program.')
    parser.add_argument('-o', '--outputfile', metavar='Directory', type=str, default="Trimmed_file.txt",
                        help='Use this to select an name for the output file')
    args = parser.parse_args()
    return args


def read_bad_file(file):
    bad_dict = {}
    with open(file, "r") as f:
        for line in f:
            bad_dict[line] = True
    return bad_dict


def read_file(file, bad_dict):
    reads = []
    with open(file, 'r') as f:
        for count, line in enumerate(f):
            if count != 0 and count % 4 == 0:
                if bad_dict.get(lines[0].split(' ')[0], False):
                    reads += lines[0], lines[1], lines[3]
                lines = []

    if len(reads) != 0:
        count += 1
        reads += lines[0], lines[1], lines[3]
        print(f'Processed {count // 4} reads')
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


def main_process(inputfiles, outputfiles):
    bad_dict1 = read_bad_file(inputfiles[0])
    bad_dict2 = read_bad_file(inputfiles[1])
    complete_dict = {**bad_dict1, **bad_dict2}
    bad_dict1, bad_dict2 = {}, {}

    read_file(inputfiles[0].split("_good.fastq"), complete_dict)
    write_out(inputfiles[0].split("_bad.fastq")[1]+"_trimmed.fastq", data)
    write_out(inputfiles[0].split("_bad.fastq")[1]+"_trimmed.fastq", data)

if __name__ == '__main__':
    bad_dict1 = read_bad_file(inputfile)
    bad_dict2 = read_bad_file()
    complete_dict = {**bad_dict1, **bad_dict2}
    bad_dict1, bad_dict2 = {}, {}

    write_out(args.outputfile, complete_dict)
