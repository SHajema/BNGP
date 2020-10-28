import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfile', type=str, required=False,
                        help='The file you wish to use as input for the program.')
    parser.add_argument('-o', '--outputfile', type=str, default="Variants.txt",
                        help='Use this to select an name for the output file')
    args = parser.parse_args()
    return args


def read_file(file_path):
    with open(file_path, 'r') as f:
        file_data = f.read().splitlines()
    return file_data


def categorize_data(file_data):
    lines = {}
    for num, line in enumerate(file_data):
        if not line.startswith('#'):
            split_line = line.split('\t')
            if ',' in split_line[3]:
                split_line[3]  = split_line[3].split(',')
            else:
                split_line[3] = [split_line[3]]
            if ',' in split_line[4]:
                split_line[4] = split_line[4].split(',')
            else:
                split_line[4] = [split_line[4]]
            lines[num] = {'CHROM': split_line[0],
                          'POS': split_line[1],
                          'REF': split_line[3],
                          'ALT': split_line[4],
                          'QUAL': split_line[5],
                          'INFO': split_line[7].split(';'),
                          }
    return lines


def calc_indel(lines):
    mut_dict = create_mut_dict()
    insertions, deletions = 0, 0
    for key in lines.keys():
        line = lines[key]
        if line['INFO'][0] == 'INDEL':
            for seq in line['ALT']:
                if len(line['REF'][0]) > len(seq):
                    deletions += 1
                elif len(line['REF'][0]) < len(seq):
                    insertions += 1
        else:
            base = line['REF'][0]
            for alt_base in line['ALT']:
                mut_dict[(base+alt_base).upper()] += 1
    return deletions, insertions, mut_dict


def create_mut_dict():
    mut_dict = {
        'AT': 0,
        'AC': 0,
        'AG': 0,
        'TA': 0,
        'TC': 0,
        'TG': 0,
        'CA': 0,
        'CG': 0,
        'CT': 0,
        'GA': 0,
        'GC': 0,
        'GT': 0,
    }
    return mut_dict


def create_result_string(inputfile, insertions, deletions, mut_dict):
    result_string = f'The Variants of : {inputfile}\n\n'
    result_string += f'The number of Deletions: {deletions}\n'
    result_string += f'The number of Insertions: {insertions}\n'
    result_string += f'The ratio of Deletions/Insertions: ' \
        f'{deletions} ({(insertions/(deletions+insertions)*100):.2f}%) ' \
        f'{insertions} ({(deletions/(deletions+insertions)*100):.2f}%)\n\n'
    for base_combination in sorted(mut_dict.keys()):
        result_string += f'Number of {base_combination[0]} -> {base_combination[1]} mutations: {mut_dict[base_combination]}\n'
    return result_string


def write_out(file, out):
    with open(file, 'w') as f:
        f.write(out)
    return f'Output written to: {file}'


def main(inputfile, outputfile):
    file_data = read_file(inputfile)
    lines = categorize_data(file_data)
    deletions, insertions, mut_dict = calc_indel(lines)
    result_string = create_result_string(inputfile, insertions, deletions, mut_dict)
    write_out(outputfile, result_string)
    print(result_string)


if __name__ == '__main__':
    args = parse_args()

    main(args.inputfile, args.outputfile)
