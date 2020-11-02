#!/bin/bash

# Create temporary dir
TMPDIR=`mktemp -d`
trap "{ rm -rf $TMPDIR; }" EXIT

EPSILON=1e-12
NHID=500
RUN="randomHeat"

# for ETA in 1e-3 5e-4 1e-4 5e-3 ;
for ETA in 1e-3 ;
do
	OUTPUTDIR=../output/symfb/$RUN/eta$ETA
	mkdir -p $OUTPUTDIR
	make && ./sim_symfb --nin 243 --nout 243 --grid 30.08 --eta $ETA --input ../themes/${RUN}-input.ras --target ../themes/${RUN}-target.ras --simtime 300.8 --nhid $NHID --epsilon $EPSILON --delay 0.0e-3 --block 40 --w0 0.05 --layer 1 --dir $TMPDIR
	cp $TMPDIR/*.stats $TMPDIR/*.spk $OUTPUTDIR
done

