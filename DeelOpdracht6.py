

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
                    print(line)
    return deletions, insertions


def calc_mutations(lines):
    mut_dict = create_mut_dict()
    for key in lines.keys():
        line = lines[key]
        print(line)


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


if __name__ == '__main__':
    file_data = read_file('Input\\Ref_Genome.VCF')
    lines = categorize_data(file_data)
    deletions, insertions = calc_indel(lines)
    calc_mutations(lines)
