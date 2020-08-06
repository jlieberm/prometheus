#!/bin/bash

EXIT_CODE=0

for file in $(find . -iname "*.py")
do
  echo "";
  echo "--> File: $file";
  cython $file;
  if [ $? -eq 0 ]
  then
    echo " - Success!";
  else
    echo -e "\e[5m \e[101m X Could not build file $file" >&2;
    echo -e "\e[5m \e[101m   Please check errors above" >&2;
    EXIT_CODE=1;
  fi
done

exit $EXIT_CODE;
