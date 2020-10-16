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

while getopts hs:b:t:1:2: flag
do
    case "${flag}" in
        s) # Specify the location of the SAM file
          SAMFILE=${OPTARG};;
        b) # Specify the path + name of the output BAM file
          BAMFILE=${OPTARG};;
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

BAMFILE = echo "${}"

echo ""
echo "Creating BAM file from ${SAMFILE}"

#Indexing Reference genome
samtools view -bT ${SAM_FILE} > ${BAMFILE}

echo ""
echo "${BAMFILE} created!"

echo ""
echo "Creating a Alignment file at ${dir_location}_Aligned.SAM..."

#Aligning reads to indexed Genome
bowtie2 -x ${dir_location} --threads ${threads} -1 ${read1} -2 ${read2} -S ${dir_location}"_Aligned.SAM"

echo ""