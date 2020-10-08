import time
import concurrent.futures
import argparse


def read_file(file):
    with open(file, 'r') as f:
        inp = f.read().splitlines()
    return inp

# def write_out(Dir, file, out):
#     filedir = "/".join(file.split('/')[:-1])+'/'
#     file = '_fqc.'.join(file.split('/')[-1].split('.'))
#
#     if Dir:
#         if Dir[-1] != '/':
#             Dir += '/'
#         return write_to_file(Dir+file, out)
#     else:
#         return write_to_file(filedir+file, out)
#
#
# def write_to_file(path, out, stop=False):
#     try:
#         with open(path, 'w') as f:
#             f.write(out)
#     except PermissionError:
#         if stop:
#             return 'No permission to write to: '+path
#         else:
#             print('No permission to write to Directory, trying current directory instead instead')
#             return write_to_file(path.split('/')[-1], out, stop=True)
#     return 'Output written to file: '+path


def write_out(file, out):
    with open(file, 'w') as f:
        f.write(out)
    return f'Output written to: {file}'


def run_thread(lines):
    total = 0
    maximum_len = len(max(lines, key=len))
    minimum_len = len(min(lines, key=len))
    pos_dict = create_pos_dict(maximum_len)

    for line in lines:
        length = len(line)
        total += length
        pos_dict = base_calc(line, pos_dict)

    gc_count = calc_gc(pos_dict)
    return maximum_len, minimum_len, total, gc_count, pos_dict


def base_calc(read, pos_dict):
    for x in range(len(read)):
        pos_dict[x] = base_dict_count(read[x], pos_dict[x])
    return pos_dict


def base_dict_count(base, list):
    if base == 'A':
        list[0] += 1
    elif base == 'C':
        list[1] += 1
    elif base == 'G':
        list[2] += 1
    elif base == 'T':
        list[3] += 1
    elif base == 'N':
        list[4] += 1
    else:
        print('error, base is:', base)
    return list


def create_pos_dict(maxi):
    dict_pos = {}
    for i in range(maxi):
        dict_pos[i] = [0, 0, 0, 0, 0]  # A, C, G, T, N
    return dict_pos


def calc_gc(pos_dict):
    gc_count = 0
    for value in pos_dict.values():
        gc_count += (value[1]+value[2])
    return gc_count


def results_mapper(results):
    results.sort(reverse=True)
    final_list = list(results[0])

    for x in range(len(results)-1):
        if results[x + 1][0] > final_list[0]:
            final_list[0] = results[x + 1][0]
        if results[x + 1][1] < final_list[1]:
            final_list[1] = results[x + 1][1]
        final_list[2] += results[x + 1][2]
        final_list[3] += results[x + 1][3]
        final_list[4] = dict_combine(final_list[4], results[x+1][4])
    return final_list


def dict_combine(final_dict, new_dict):
    for key in new_dict.keys():
        final_dict[key] = [x + y for x, y in zip(final_dict[key], new_dict[key])]
    return final_dict


def create_result_string(reads_num, result_list):
    result_string = f'The number of reads is: {reads_num}\n'
    result_string += f'\nThe average read length is: {result_list[2]/reads_num:.2f}\n'
    result_string += f'\nThe maximum read length is: {result_list[0]}\n'
    result_string += f'\nThe minimum read length is: {result_list[1]}\n'
    result_string += f'\nThe GC percentage is:  {result_list[3]/result_list[2]*100:.2f}%\n'
    result_string += f'\nThe GC percentage per position:\n'
    for x in range(result_list[0]):
        result_string += f'Position {x+1}: ' \
            f'{(result_list[4][x][1]+result_list[4][x][2])/sum(result_list[4][x])*100:.2f}%\n'

    return result_string


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfile', metavar='File', type=str, required=True,
                        help='The file you wish to use as input for the program.')
    parser.add_argument('-o', '--outputfile', metavar='String', type=str, default=None,
                        help='Give the name of the outputfile')
    parser.add_argument('-t', '--threads', metavar='number of threads', type=int, default=4,
                        help='Give the number of threads you would like to use.')
    parser.add_argument('-c', '--chunks', metavar='number of reads to load into ram to process', type=int,
                        default=10_000_000, help='Give the number of reads you wish to process at the same time.')
    args = parser.parse_args()
    return args


def main_processing(args, reads):
    reads_num = len(reads)

    intlist = [int(x * reads_num // args.threads) for x in range(args.threads)]
    intlist.append(int(reads_num))
    final_results = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(run_thread, reads[intlist[x]:intlist[x + 1]]) for x in range(args.threads)]
    for r in concurrent.futures.as_completed(results):
        final_results.append(r.result())

    final_results = results_mapper(final_results)
    return final_results


def main():
    args = parse_args()
    count, reads, result_list = 0, [], []
    with open(args.inputfile, 'r') as f:
        for line in f:
            count += 1
            if count % args.chunks*4 == 0:
                result_list.append(main_processing(args, reads))
                reads = []
            if count % 4 == 0:
                reads.append(line.rstrip())
                print(reads)

    if len(reads) != 0:
        result_list.append(main_processing(args, reads))
    final_results = results_mapper(result_list)

    result_string = create_result_string((count-3)//4, final_results)
    print(result_string)
    print("\n\n\n\n")
    print(write_out(args.outputfile, result_string))


if __name__ == '__main__':
    start = time.perf_counter()

    main()

    final = time.perf_counter()

    print(f'\n\n\nProgram finished in {final-start:2} second(s)')
