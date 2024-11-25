#!/bin/bash

# util to test, make submit file
# require:
#		docker
#		
# usage:
#		./util.sh test
#		./util.sh submit

# please provide info
STUDENT_ID="2114278"

# python or java
PROJ_P_LANG="python"

# DO NOT CHANGE BELOW VARIABLES
S_OUT="`pwd`/$STUDENT_ID/output"
S_IN="`pwd`/input"

# default: do nothing
function run_ { echo "Please give either command submit/test" ; }

function run_test {
	# run and make output, similar when grading your assignment
	# make sure ./input folder exits
	# check results in $S_OUT
	echo "run test your assignment"
	
	cur=`pwd`
	cd $PROJ_P_LANG
	docker build --network=host -t nlp222 .

	docker run --rm -v $S_OUT:/src/nlp/output -v $S_IN:/src/nlp/input nlp222

	cd $cur
	echo "please check output in $S_OUT"
}


function run_submit {
	# make submit file, just needed directories/files
	# require: zip
	echo "make submit file $STUDENT_ID.zip"
	# zip PROJ_P_LANG -o $STUDENT_ID.zip
	docker run --rm -ti -v `pwd`:/data thanhhungqb/images:zip-2023  zip -r /data/$STUDENT_ID.zip python java util.sh
	echo "Please check file $STUDENT_ID.zip to make sure all correct directories/files included"
}

run_$1 "${@:2}"

