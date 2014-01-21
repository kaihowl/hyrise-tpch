#!/bin/bash
if [ "$#" -eq 0 ];then
  echo 'Please supply the table name.'
else
  echo Concatenating header and data...
  cat headers/$1.head rawdata/$1.tbl > $1_tmp.tbl
  echo Stripping trailing pipes...
  sed "s/|$//g" $1_tmp.tbl > hyrise/$1.tbl
  echo Cleaning up...
  rm $1_tmp.tbl
  echo Done!
fi
