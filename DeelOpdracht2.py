import concurrent.futures
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfile', type=str, required=False,
                        help='The file you wish to use as input for the program.')
    parser.add_argument('-o', '--outputfile', type=str, default="Trimmed_file.txt",
                        help='Use this to select an name for the output file')
    parser.add_argument('-t', '--threads', type=int, default=4,
                        help='Give the number of threads you would like to use.')
    parser.add_argument('-c', '--chunks', type=int, default=2_000,
                        help='Give the number of reads you wish to process at the same time.')
    args = parser.parse_args()
    return args


def trim_read(read):
    sequence = read[1]
    quality = read[2]
    length = len(quality)//2

    pos = split_seq(quality[length::])
    read[1] = sequence[0:pos+length]
    read[2] = quality[0:pos+length]

    pos = split_seq(read[2][::-1])
    read[1] = read[1][-pos::]
    read[2] = read[2][-pos::]
    return read


def split_seq(quality):
    for x in range(len(quality)-4):
        if calc_quality_score(quality[x:x + 5]):
            return x+4
    return len(quality)


def calc_quality_score(values):
    score_num = 0
    for x in range(len(values)):
        score_num += ord(values[x])-33
    if score_num >= 100:
        return False
    elif score_num < 100:
        return True


def seperate_reads(read_list):
    good_reads, bad_reads = [], []

    for x in range(0, len(read_list), 3):
        if len(read_list[x+1]) > 19:
            good_reads += read_list[x:x+3]
        else:
            bad_reads.append(read_list[x].split()[0])
    return good_reads, bad_reads


def write_out_bad(path, data):
    print(f"Writing bad sequence IDs to: {path}...")
    write_string = ""

    with open(path, 'a+') as f:
        for x in range(0, len(data), 1):
            write_string += f'{data[x]}\n'
            if x % 1_000_000 == 0 and x != 0:
                f.write(write_string)
                write_string = ""
                print(f"Wrote {x}   bad read IDs to: {path}.")
        if write_string != "":
            f.write(write_string)

    return f"Completed! Wrote {len(data)} bad Read IDs to: {path}"


def write_file(path, data):
    print(f"Writing correct sequences to: {path}...")
    write_string = ""

    with open(path, 'a+') as f:
        for x in range(0, len(data), 3):
            write_string += f'{data[x]}\n{data[x+1]}\n+\n{data[x+2]}\n'
            if x % (1_000_000 * 3) == 0 and x != 0:
                f.write(write_string)
                write_string = ""
                print(f"Wrote {x//3} good reads to: {path}.")
        if write_string != "":
            f.write(write_string)
    return f"Completed! Wrote {len(data)//3} sequences to: {path}\n"


def create_intlist(reads_num, threads):
    intlist = [int(x * (reads_num / 3 // threads)) * 3 for x in range(threads)]
    intlist.append(int(reads_num))
    return intlist


def multi_process(function, intlist, reads):
    final_results = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(function, x, reads[intlist[x]:intlist[x + 1]]) for x in range(args.threads)]
    for r in concurrent.futures.as_completed(results):
        final_results.append(r.result())
    final_results.sort()
    return final_results


def process_results(final_results):
    good, bad = [], []

    for result in final_results:
        if len(result[1]) != 0:
            good += result[1]
        if len(result[2]) != 0:
            bad += result[2]
    return good, bad


def run_thread(pos, lines):
    for x in range(0, len(lines), 3):
        lines[x:x+3] = trim_read(lines[x:x+3])
    good_reads, bad_reads = seperate_reads(lines)
    return [pos, good_reads, bad_reads]


def main_processing(args, reads):
    reads_num = len(reads)

    intlist = create_intlist(reads_num, args.threads)
    final_results = multi_process(run_thread, intlist, reads)
    final_results = process_results(final_results)

    print(write_file((args.outputfile.split('.')[0]+"_good.fastq"), final_results[0]))
    print(write_out_bad((args.outputfile.split('.')[0]+"_bad.fastq"), final_results[1]))


def file_processing(file):
    print(f'Trimming File: {file}')
    reads, lines = [], []

    with open(file, 'r') as f:
        for count, line in enumerate(f):
            if count != 0 and count % 4 == 0:
                reads += lines[0], lines[1], lines[3]
                lines = []
            if count != 0 and count % (args.chunks * 4) == 0:
                main_processing(args, reads)
                print(f'\nProcessed {count // 4} reads\n')
                reads = []
            lines.append(line.rstrip())

    if len(reads) != 0:
        count += 1
        reads += lines[0], lines[1], lines[3]
        main_processing(args, reads)
        print(f'\nProcessed {count // 4} reads\n')
    return


def clean_file(path):
    with open(path, 'w') as f:
        f.write("")
    return f"Removed content from file: {path}"


def main(args):
    print(clean_file(args.outputfile.split('.')[0] + "_good.fastq"))
    print(clean_file(args.outputfile.split('.')[0] + "_bad.fastq"))
    file_processing(args.inputfile)


if __name__ == '__main__':
    args = parse_args()
    if not args.inputfile:
        args.inputfile = 'Input/testbestand_paired_rv.fastq'

    main(args)

