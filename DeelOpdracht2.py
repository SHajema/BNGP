import time
import concurrent.futures
import argparse


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


def seperate_reads(read_list, bad_qual):
    good_reads, bad_reads = [], []

    for x in range(0, len(read_list), 3):
        if len(read_list[x+1]) > 19 and bad_qual.get(read_list[x].split()[0], True):
            good_reads += read_list[x:x+3]
        else:
            bad_reads.append(read_list[x].split()[0])
    return good_reads, bad_reads


def run_thread(pos, lines, bad_qual):
    for x in range(0, len(lines), 3):
        lines[x:x+3] = trim_read(lines[x:x+3])
    good_reads, bad_reads = seperate_reads(lines, bad_qual)
    return [pos, good_reads, bad_reads]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfiles', metavar='File', type=str, nargs=2, required=False,
                        help='The file you wish to use as input for the program.')
    parser.add_argument('-o', '--outputfile', metavar='Directory', type=str, default="Trimmed_file.txt",
                        help='Use this to select an name for the output file')
    parser.add_argument('-t', '--threads', metavar='number of threads', type=int, default=4,
                        help='Give the number of threads you would like to use.')
    parser.add_argument('-c', '--chunks', metavar='number of reads to load into RAM', type=int,
                        default=2_000, help='Give the number of reads you wish to process at the same time.')
    args = parser.parse_args()
    return args


def write_out(file, data):
    with open(file, "a+") as f:
        for pos in range(0, len(data), 3):
            f.write(f'{data[pos]}\n{data[pos + 1]}\n+\n{data[pos + 2]}\n')
    return f"Wrote {len(data)//3} sequences to {file}"


def temp_write(file, data):
    with open(file, "a+") as f:
        for pos in range(0, len(data), 3):
            f.write(f'{data[pos]}\n{data[pos + 1]}\n+\n{data[pos + 2]}\n')
    return f"Wrote {len(data) // 3} sequences to {file}"


def create_intlist(reads_num, threads):
    intlist = [int(x * (reads_num / 3 // threads)) * 3 for x in range(threads)]
    intlist.append(int(reads_num))
    return intlist


def process_results(final_results):
    good, bad = [], []
    for result in final_results:
        if len(result[1]) != 0:
            good += result[1]
        if len(result[2]) != 0:
            bad += result[2]
    return good, bad


def multi_process(function, intlist, reads, bad_qual):
    final_results = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(function, x, reads[intlist[x]:intlist[x + 1]], bad_qual) for x in range(args.threads)]
    for r in concurrent.futures.as_completed(results):
        final_results.append(r.result())
    final_results.sort()
    return final_results


def main_processing(args, reads, piece, i, bad_qual):
    reads_num = len(reads)

    intlist = create_intlist(reads_num, args.threads)

    final_results = multi_process(run_thread, intlist, reads, bad_qual)
    good, bad = process_results(final_results)
    if i == 0:
        print(temp_write('temp.fastq', good))
        good = []
    if i == 1:
        print(write_out(args.outputfile, good))
        good = []
    return [piece, good, bad]


def file_processing(file, i, bad_qual):
    print('Trimming File: ' + file)
    count, reads, result_list, lines, piece = 0, [], [], [], 0

    with open(file, 'r') as f:
        for count, line in enumerate(f):
            if count != 0 and count % 4 == 0:
                reads += lines[0], lines[1], lines[3]
                lines = []
            if count != 0 and count % (args.chunks * 4) == 0:
                piece += 1
                result_list.append(main_processing(args, reads, piece, i, bad_qual))
                print(f'Processed {count // 4} reads')
                reads = []
            lines.append(line.rstrip())

    if len(reads) != 0:
        count += 1
        reads += lines[0], lines[1], lines[3]
        piece += 1
        result_list.append(main_processing(args, reads, piece, i, bad_qual))
        print(f'Processed {count // 4} reads')
    return process_results(result_list)


def main(args):
    bad_qual = {}
    result = file_processing(args.inputfiles[0], 0, bad_qual)

    for read in result[1]:
        bad_qual[read] = False
    print(f'{len(result[1])} reads removed because they were too short')

    result = file_processing(args.inputfiles[1], 1, bad_qual)
    for read in result[1]:
        bad_qual[read] = False
    print(f'{len(result[1])} reads removed because they were too short')
    
    return True


if __name__ == '__main__':
    start = time.perf_counter()
    args = parse_args()
    if not args.inputfiles:
        args.inputfiles = ['Input/testbestand_paired_fw.fastq', 'Input/testbestand_paired_rv.fastq']
    main(args)

    final = time.perf_counter()

    print(f'Program finished in {final-start:.2f} second(s)')
