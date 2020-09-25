#!/bin/bash

# Create temporary dir
TMPDIR=`mktemp -d`
trap "{ rm -rf $TMPDIR; }" EXIT

EPSILON=1e-12
NHID=500
RUN="wine"

# for ETA in 1e-3 5e-4 1e-4 5e-3 ;
for ETA in 1e-3 ;
do
	OUTPUTDIR=../output/symfb/$RUN/eta$ETA
	mkdir -p $OUTPUTDIR
	make && ./sim_symfb --nin 561 --nout 11 --grid 159.9 --eta $ETA --input ../themes/${RUN}-input.ras --target ../themes/${RUN}-target.ras --simtime 1599 --nhid $NHID --epsilon $EPSILON --delay 0.0e-3 --block 40 --w0 0.05 --layer 0 --dir $TMPDIR
	cp $TMPDIR/*.stats $TMPDIR/*.spk $OUTPUTDIR
done

