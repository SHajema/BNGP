#!/usr/bin/env bash

usage() { echo "$0 usage:" && grep " .)\ #" $0; exit 0; }
[ $# -eq 0 ] && usage

while getopts hr:d:t: flag
do
    case "${flag}" in
        r) ref_location=${OPTARG};;
        d) dir_location=${OPTARG};;
        t) threads=${OPTARG};;
        h | *)
          usage
          exit 0
          ;;
    esac
done

echo "ref_location = ${ref_location}"
echo "dir_location = ${dir_location}"
echo "threads = ${threads}"

bowtie2-build ${ref_location} ${dir_location} --threads ${threads}
