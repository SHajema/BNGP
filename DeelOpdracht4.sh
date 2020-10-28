#!/usr/bin/env bash

usage() {
echo "Function: $0 script is used to index the reference Genome and the Align reads onto that indexed Genome."
echo "$0 usage:" && grep "[[:space:]].)\ #" $0 | sed 's/#//' | sed -r 's/([a-z])\)/-\1/';
echo ""
echo "Example:"
echo "$0 -r lclav_genome.fa -d Results/Genome/bngsa_sample -t 4 -1 sample1_R1_trimmed.fastq -2 sample1_R2_trimmed.fastq"
exit 0;
}
[ $# -eq 0 ] && usage

while getopts hr:d:t:s:1:2: flag
do
    case "${flag}" in
        r) # Specify the location of the Reference genome. In Fasta Format
          ref_location=${OPTARG};;
        d) # Specify the location + basename of the output files
          dir_location=${OPTARG};;
        t) # Specify the amount of threads to use
          threads=${OPTARG};;
        s) # Specify the path of the SAM output file
          SAM_FILE=${OPTARG};;
        1) # The R1 file to use for Alignment
          read1=${OPTARG};;
        2) # The R2 file to use for Alignment
          read2=${OPTARG};;
        h | *) # Show help information
          usage
          exit 0
          ;;
    esac
done

echo ""
echo "Using ${ref_location} to create index files..."

#Indexing Reference genome
bowtie2-build ${ref_location} ${dir_location} --threads ${threads}

echo ""
echo "Building index files completed!"
echo ""
echo "Creating a Alignment file at ${dir_location}_Aligned.SAM..."

#Aligning reads to indexed Genome
bowtie2 -x ${dir_location} --threads ${threads} -1 ${read1} -2 ${read2} -S ${SAM_FILE}

echo ""