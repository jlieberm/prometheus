#!/bin/bash

for file in $(find . -iname "*.py")
do
  echo "--> File: $file";
  cython $file;
  if [ $? -eq 0 ]
  then
    echo " - Successfully built file!";
  else
    echo -e "\e[5mBlink \e[101m X Could not build file" >&2;
    exit 1;
  fi
done
