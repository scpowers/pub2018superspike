#!/bin/bash

# Create temporary dir
TMPDIR=`mktemp -d`
trap "{ rm -rf $TMPDIR; }" EXIT

EPSILON=1e-12
#ETA=1e-5
NHID=500
RUN="simpleHeat"

# for ETA in 1e-5 5e-5 1e-4;
for ETA in 1e-3 ;
# for EPSILON in 1e-11 5e-10 1e-13;
do
	OUTPUTDIR=../output/symfb/$RUN/eta$ETA
	mkdir -p $OUTPUTDIR
	make && ./sim_symfb --nin 243 --nout 243 --grid 2.99 --eta $ETA --input ../themes/${RUN}-input.ras --target ../themes/${RUN}-target.ras --simtime 29.9 --nhid $NHID --epsilon $EPSILON --delay 0.0e-3 --block 40 --w0 0.05 --layer 1 --dir $TMPDIR
	cp $TMPDIR/*.stats $TMPDIR/*.spk $OUTPUTDIR
done

