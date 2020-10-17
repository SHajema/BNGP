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

while getopts hs:b:t: flag
do
    case "${flag}" in
        s) # Specify the location of the SAM file
          SAMFILE=${OPTARG};;
        b) # Specify the path + name of the output BAM file
          BAMFILE=${OPTARG};;
        t) # Specify the amount of threads to use
          threads=${OPTARG};;
        h | *) # Show help information
          usage
          exit 0
          ;;
    esac
done

BASENAME=${SAMFILE%.SAM}
BAMFILE=${BASENAME}'.BAM'
SORTED_BAM=${BASENAME}'_sorted.BAM'
PILEUP=${BASENAME}'_pileup.mpileup'


echo ""
echo "Creating BAM file from ${SAMFILE}"

#Indexing Reference genome
samtools view --threads ${threads} -b ${SAM_FILE} > ${BAMFILE}

echo ""
echo "${BAMFILE} created!"

echo ""
echo "Creating sorted BAM file at ${SORTED_BAM}"

samtools sort --threads ${threads} ${BAMFILE} -o ${SORTED_BAM}

echo ""
echo "${SORTED_BAM} created!"

echo ""
echo "Creating Pileup file at ${PILEUP}"

samtools mpileup
