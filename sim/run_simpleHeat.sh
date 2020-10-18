#!/bin/bash

# Create temporary dir
TMPDIR=`mktemp -d`
trap "{ rm -rf $TMPDIR; }" EXIT

EPSILON=1e-12
NHID=500
RUN="simpleHeat"

# for ETA in 1e-3 5e-4 1e-4 5e-3 ;
for ETA in 1e-3 ;
do
	OUTPUTDIR=../output/symfb/$RUN/eta$ETA
	mkdir -p $OUTPUTDIR
	make && ./sim_symfb --nin 205 --nout 205 --grid 0.2 --eta $ETA --input ../themes/${RUN}-input.ras --target ../themes/${RUN}-target.ras --simtime 2 --nhid $NHID --epsilon $EPSILON --delay 0.0e-3 --block 80 --w0 0.05 --layer 1 --dir $TMPDIR
	cp $TMPDIR/*.stats $TMPDIR/*.spk $OUTPUTDIR
done

