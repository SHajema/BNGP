#!/usr/bin/env bash

usage() {
echo "$0 script is used to index the reference Genome and the Align reads onto that indexed Genome."
echo "$0 usage:" && grep "[[:space:]].)\ #" $0 | sed 's/#//' | sed -r 's/([a-z])\)/-\1/';
echo ""
echo "Example:"
echo "$0 -r <path to reference genome> -d <path to directory + basename> -t <number of threads as integer> -1 <path to Read1 file> -2 <path to Read2 file>"
exit 0;
}
[ $# -eq 0 ] && usage

while getopts hr:d:t:1:2: flag
do
    case "${flag}" in
        r) # Specify the location of the Reference genome
          ref_location=${OPTARG};;
        d) # Specify the location + basename of the output files
          dir_location=${OPTARG};;
        t) # Specify the amount of threads to use
          threads=${OPTARG};;
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
bowtie2 -x ${dir_location} --threads ${threads} -1 ${read1} -2 ${read2} -S ${dir_location}".SAM"

echo ""