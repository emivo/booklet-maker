#!/bin/bash
# Author: Emil Airta 
# 2024:
# MIT Licence
# This is an earlier version of processing the files. It can be used for updating the abstracts but it does not contain any updating of the schedules

echo "This is a simple script to make latex booklet of given files please see the README for the instructions for setting up the files."


process_files() {
  local dir=$1
  local output_file=$2
ls "${dir}"/*.tex | awk '{
beg = match($0, /\//)
str=substr($0,beg,match($0,/.tex/)-beg)
split(str,arr,"_")
if (arr[2]) {
	printf "\\filbreak \n"
      printf "\\hypertarget{" arr[2] "}{\\input{%s}}\n", $0
    }}' | tee "$output_file"
    }
# Process input files. 
# Take TeX file names from folders "Abstracts_*" and create files inputs_*.tex 
# where we have latex code inputting these tex files with hypertargets keyed by filename_{key}.tex
echo "Processing abstracts"
process_files "Abstracts_short" "inputs_shorts.tex"
process_files "Abstracts_invited" "inputs_invited.tex"

echo "Initiating latexmk with pdflatex and minimal output"
# Compile the booklet using latexmk
latexmk -pdf -pdflatex="pdflatex -file-line-error -interaction=nonstopmode" booklet.tex | grep "^.*:[0-9]*: .*$"



  

  
