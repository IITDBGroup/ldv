#!/bin/sh

cp single query
oldpath=`pwd`
if [ "$PERM" = "" ]
then
	if [ `hostname` = "qpc" ]
	then
	  PERM=/home/quanpt/myapps/perm
	else
	  PERM=/var/tmp/quanpt/froot/perm
	fi
fi

# prepare minimal database
cd cde-package/cde-root/$PERM
bin/pg_ctl stop -D data >/dev/null 2>&1
rm -rf data
$PERM/bin/initdb -D data >/dev/null 2>&1
cd $oldpath

####
#~ remember to add to cde.options
#~ ignore_environment_var=PTU_DB_MODE
#~ ignore_environment_var=PTU_DBSESSION_ID
#~ ignore_environment_var=PTU_DB_REPLAY

### start
export PTU_DB_REPLAY=/dblog.txt
export PTU_DB_MODE=22

# real re-run
cd cde-package
time -p -a -o ../time.run.txt sh cde.log
echo time.exp.txt
tail -n 9 cde-root/$oldpath/time.exp.txt | grep real
