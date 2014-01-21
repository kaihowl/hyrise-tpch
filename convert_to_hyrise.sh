#!/bin/bash
TPCHTABLES=( customer lineitem nation orders part partsupp region supplier )
for TABLE in "${TPCHTABLES[@]}"
do
  echo $TABLE :
  echo Concatenating header and data...
  cat headers/$TABLE.head rawdata/$TABLE.tbl > $TABLE_tmp.tbl
  echo Stripping trailing pipes...
  sed "s/|$//g" $TABLE_tmp.tbl > hyrise/$TABLE.tbl
  echo Cleaning up...
  rm $TABLE_tmp.tbl
  echo Creating the load query file...
  sed "s/{{tablename}}/$TABLE/g" load_template.json > queries/load_$TABLE.json
  echo Done!
done
