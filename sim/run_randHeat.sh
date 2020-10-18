#!/bin/bash

# Create temporary dir
TMPDIR=`mktemp -d`
trap "{ rm -rf $TMPDIR; }" EXIT

EPSILON=1e-12
NHID=256
RUN="randHeat"

# for ETA in 1e-3 5e-4 1e-4 5e-3 ;
for ETA in 1e-3 ;
do
	OUTPUTDIR=../output/symfb/$RUN/eta$ETA
	mkdir -p $OUTPUTDIR
	make && ./sim_symfb --nin 51 --nout 51 --grid 20.099 --eta $ETA --input ../themes/${RUN}-input.ras --target ../themes/${RUN}-target.ras --simtime 200.99 --nhid $NHID --epsilon $EPSILON --delay 0.0e-3 --block 40 --w0 0.05 --layer 1 --dir $TMPDIR
	cp $TMPDIR/*.stats $TMPDIR/*.spk $OUTPUTDIR
done

