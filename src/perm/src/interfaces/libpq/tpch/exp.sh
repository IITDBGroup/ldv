#!/bin/sh
N=100
#~ export TPCH=3

# start perm
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
cd $PERM
rm logfile
bin/pg_ctl start -D $PGDATA -l logfile
# > /dev/null 2>&1
cd $oldpath
sleep 6
# start clients
#./single "host=localhost dbname=single" 100 2>100.log &
#~ time ./single "host=localhost dbname=single" 99 1000 2>/dev/null &

# make one db conn then exit (to restore db if needed)
time -p -a -o time.exp.txt ./single "host=localhost dbname=$DBNAME" 95 1

# insert
time -p -a -o time.exp.txt ./single "host=localhost dbname=$DBNAME" 91 $N

# select heavy
time -p -a -o time.exp.txt ./single "host=localhost dbname=$DBNAME" 92 1 $TPCH

# select light
time -p -a -o time.exp.txt ./single "host=localhost dbname=$DBNAME" 92 $N $TPCH
#wc -l *.dblog

# update
time -p -a -o time.exp.txt ./single "host=localhost dbname=$DBNAME" 93 $N

#time -p -a -o time.exp.txt ./single "host=localhost dbname=$DBNAME" 94 $N

# stop perm
cd $PERM
bin/pg_ctl stop > /dev/null 2>&1
