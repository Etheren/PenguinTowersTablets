#
#
# GM2_TREE=/home/gaius/GM2/gm2-harness-0.96/sources/gcc-3.3.6/gcc/gm2
# GM2_BUILD=/home/gaius/GM2/gm2-harness-0.96/build
#
# guenevere
#
GM2_TREE=/home/gaius/GM2/graft-4.1.2/gcc-4.1.2/gcc/gm2
GM2_BUILD=/home/gaius/GM2/graft-4.1.2/build-4.1.0
PPG=$(GM2_BUILD)/gcc/gm2/ppg

LIBRARIES=-I.:$(GM2_TREE)/examples/server

all: force advflex.o AdvParse.o sckt.o hack.o
	gm2 -g -Wmakeall -Wlibs=pim-coroutine $(LIBRARIES) Dungeon.mod sckt.o -lpth

hack.o: hack.c
	gcc -c -g $<

sckt.o: $(GM2_TREE)/examples/server/sckt.c
	gcc -c -g $<

advflex.o: advflex.c
	gcc -g -c -o $@ $<

advflex.c: adv.flex
	flex -t $< > $@

AdvParse.o: AdvParse.mod
	gm2 -g -c $<

AdvParse.mod: AdvParse.bnf
	$(PPG) $< > $@

clean: force
	$(RM) *.o dungeon advflex.c a.out

force:
