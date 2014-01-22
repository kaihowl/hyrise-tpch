#!/bin/bash
TPCHTABLES=( customer lineitem nation orders part partsupp region supplier )
echo Set HYRISE_DB_PATH to hyrise-tpch/ folder.
for TABLE in "${TPCHTABLES[@]}"
do
  echo Loading $TABLE :
  curl -XPOST --data-urlencode "query@queries/load_$TABLE.json" http://localhost:5000/jsonQuery 
done
