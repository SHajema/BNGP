#!/usr/bin/env bash

usage() { echo "$0 usage: " && grep "[[:space:]].)\ #" $0 | sed 's/#//' | sed -r 's/([a-z])\)/-\1/'; exit 0; }

while getopts r:d:t:h flag
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

bowtie2-build ${ref_location} ${dir_location} -t ${threads}
