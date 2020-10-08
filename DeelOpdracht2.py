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


def run_thread(pos, lines):
    for x in range(0, len(lines), 3):
        lines[x:x+3] = trim_read(lines[x:x+3])
    return [pos, lines]


def seperate_reads(read_list):
    good_reads, bad_reads = '', ''

    for x in range(0, len(read_list), 3):
        if len(read_list[x+1]) > 19:
            good_reads += read_list[x] + '\n'
            good_reads += read_list[x+1] + '\n'
            good_reads += '+\n'
            good_reads += read_list[x+2] + '\n'
        else:
            bad_reads += read_list[x] + '\n'
            bad_reads += read_list[x+1] + '\n'
            bad_reads += '+\n'
            bad_reads += read_list[x+2] + '\n'

    return good_reads, bad_reads


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfiles', metavar='File', type=str, nargs=2, required=False,
                        help='The file you wish to use as input for the program.')
    parser.add_argument('-o', '--outputdir', metavar='Directory', type=str, default=None,
                        help='Use this to select an output directory for the output files')
    parser.add_argument('-t', '--threads', metavar='number of threads', type=int, default=1,
                        help='Give the number of threads you would like to use.')
    parser.add_argument('-c', '--chunks', metavar='number of reads to load into RAM', type=int,
                        default=10_000_000, help='Give the number of reads you wish to process at the same time.')
    args = parser.parse_args()
    return args


def main_processing(args, reads):
    reads_num = len(reads)

    intlist = [int(x * (reads_num/3 // args.threads))*3 for x in range(args.threads)]
    intlist.append(int(reads_num))
    final_results = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(run_thread, x, reads[intlist[x]:intlist[x + 1]]) for x in range(args.threads)]
    for r in concurrent.futures.as_completed(results):
        final_results.append(r.result())
    final_results.sort()
    for result in final_results:
        good_reads, bad_reads = seperate_reads(result[1])
        print(good_reads.count('\n'))


def main(args):
    count, reads, result_list, lines = 0, [], [], []
    with open(args.inputfiles[0], 'r') as f:
        for line in f:
            count += 1
            lines.append(line.rstrip())
            if count != 0 and count % args.chunks*4 == 0:
                result_list.append(main_processing(args, reads))
                reads = []
            if count != 0 and count % 4 == 0:
                reads += lines[0], lines[1], lines[3]
                lines = []
    if len(reads) != 0:
        result_list.append(main_processing(args, reads))
        print(len(result_list))

    return True


if __name__ == '__main__':
    start = time.perf_counter()
    args = parse_args()
    args.inputfiles = ['/home/steen/Desktop/BNGP/Input/testbestand_paired_fw.fastq', '/home/steen/Desktop/BNGP/Input/testbestand_paired_rv.fastq']
    main(args)

    final = time.perf_counter()

    print(f'Program finished in {final-start:.2f} second(s)')
