#!/usr/bin/env bash

usage() {
echo "This script "
echo "$0 usage:" && grep "[[:space:]].)\ #" $0 | sed 's/#//' | sed -r 's/([a-z])\)/-\1/'; exit 0;
}
[ $# -eq 0 ] && usage

while getopts hr:d:t: flag
do
    case "${flag}" in
        r) # Specify the location of the Reference genome
          ref_location=${OPTARG};;
        d) # Specify the location + basename of the output files
          dir_location=${OPTARG};;
        t) # Specify the amount of threads to use
          threads=${OPTARG};;
        h | *) # Show help information
          usage
          exit 0
          ;;
    esac
done

echo "ref_location = ${ref_location}"
echo "dir_location = ${dir_location}"
echo "threads = ${threads}"

bowtie2-build ${ref_location} ${dir_location} --threads ${threads}
