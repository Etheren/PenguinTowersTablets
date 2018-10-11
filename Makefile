#
#  Makefile for Pengium Tower
#

SHELL=/bin/bash

DISTFILES = COPYING       Makefile     sounds   version.c \
            ChangeLog     Makefile.in  penguin-tower.in   src \
            configure	  data	maps   penguin-tower.py   testscript \
            configure.in  doc   new    README   troff

DOCUMENTATION = doc/ptower.info doc/ptower.pdf \
                doc/ptower.html

IMAGES = data/wallv.png data/wallh.png data/doorv.png data/doorh.png \
         data/hingeh.png data/hingev.png \
         data/mann.png data/mane.png data/mans.png data/manw.png \
         data/manN.png data/manE.png data/manS.png data/manW.png \
         data/treasure.png data/arrown.png data/arrows.png \
         data/arrowe.png data/arroww.png \
         doc/initial.jpg doc/second.jpg doc/penguin-tower.jpg \
         doc/corridor.jpg

prefix= /usr/local
srcdir= .
mandir= ${datarootdir}/man
exec_prefix=${prefix}
bindir= ${exec_prefix}/bin
datarootdir= ${prefix}/share
ptowerdir= $(datarootdir)/ptower

GM2FLAGS=-g -flibs=pim-coroutine
GCCFLAGS=-g

GM2=gm2
GCC=gcc

OBJECTS= advflex.o AdvParse.o hack.o Dungeon.o AdvIntroduction.o \
         SysVec.o AdvUtil.o AdvSystem.o  \
         Lock.o ProcArgs.o Screen.o AdvMap.o AdvSound.o AdvMath.o  \
         DrawL.o Window.o DrawG.o AdvTreasure.o AdvCmd.o

all: data doc $(IMAGES) ptower-server $(DOCUMENTATION)

advflex.c: $(srcdir)/src/adv.flex
	flex -t $< > $@

advflex.o: advflex.c
	$(GCC) $(GCCFLAGS) -c $< -o $@

%.o: $(srcdir)/src/%.c
	$(GCC) $(GCCFLAGS) -c $< -o $@

%.o: $(srcdir)/src/%.mod
	$(GM2) $(GM2FLAGS) -c -I$(srcdir)/src $< -o $@

doc/%.jpg: $(srcdir)/doc/%.png
	pngtopnm $< | pnmtojpeg > $@

%.pdf: %.ps
	ps2pdf $< $@

ptower-server: $(OBJECTS)
	gm2 -g -flibs=pim-coroutine -I$(srcdir)/src:. $(srcdir)/src/Dungeon.mod -lpth
	mv a.out $@

data: force
	mkdir -p data

doc: force
	mkdir -p doc
	cp $(srcdir)/doc/*.{png,eps} doc

install: force
	install -m 755 penguin-tower $(bindir)/penguin-tower
	install -m 755 ptower-server $(bindir)/ptower-server
	install -d data $(ptowerdir)/data
	install -d data $(ptowerdir)/sounds
	install -d data $(ptowerdir)/maps
	install -d data $(ptowerdir)/doc
	for i in x data/* ; do \
	    if [ -f $$i ] ; then \
		install $$i $(ptowerdir)/$$i ; \
	    fi ; \
	done
	for i in x $(srcdir)/sounds/* ; do \
	    if [ -f $$i ] ; then \
		install -m 644 $$i $(ptowerdir)/sounds ; \
	    fi ; \
	done
	for i in x $(srcdir)/maps/* ; do \
	    if [ -f $$i ] ; then \
		install -m 644 $$i $(ptowerdir)/maps ; \
	    fi ; \
	done
	for i in x doc/* ; do \
	    if [ -f $$i ] ; then \
		install $$i $(ptowerdir)/$$i ; \
	    fi ; \
	done
	install -m 644 $(srcdir)/penguin-tower.py $(ptowerdir)/penguin-tower.py

clean: force
	$(RM) config.log config.cache config.status
	$(RM) data/*.png data/*.pnm doc/*.{pdf,html,aux,ps,jpg}
	$(RM) *.o dungeon advflex.c a.out

distclean: clean force
	$(RM) Makefile penguin-tower

doc/ptower.info: $(srcdir)/doc/ptower.texi
	cd doc ; makeinfo ../$(srcdir)/doc/ptower.texi

doc/ptower.html: $(srcdir)/doc/ptower.texi
	cd doc ; texi2html ../$(srcdir)/doc/ptower.texi

doc/ptower.ps: $(srcdir)/doc/ptower.texi
	cd doc ; texi2dvi ../$(srcdir)/doc/ptower.texi
	cd doc ; dvips ptower.dvi -o ptower.ps

data/%.png: data/%.pnm
	pnmscale -xsize=20 -ysize=20 $< > t.pnm
	pnmtopng t.pnm > $@
	$(RM) t.pnm

data/wallh.pnm: $(srcdir)/troff/wallh.n
	groff -I$(srcdir)/troff < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

data/wallv.pnm: $(srcdir)/troff/wallv.n
	groff -I$(srcdir)/troff < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

data/doorh.pnm: $(srcdir)/troff/doorh.n
	groff -I$(srcdir)/troff < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

data/doorv.pnm: $(srcdir)/troff/doorv.n
	groff -I$(srcdir)/troff < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

data/hingeh.pnm: $(srcdir)/troff/hingeh.n
	groff -I$(srcdir)/troff < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

data/hingev.pnm: $(srcdir)/troff/hingeh.n
	groff -I$(srcdir)/troff < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm | pnmrotate 90 > $@
	$(RM) t.ps t.pnm

data/mann.pnm: $(srcdir)/troff/mane.n
	groff -I$(srcdir)/troff < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm | pnmrotate 90 > $@
	$(RM) t.ps t.pnm

data/mane.pnm: $(srcdir)/troff/mane.n
	groff -I$(srcdir)/troff < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

data/mans.pnm: $(srcdir)/troff/manw.n
	groff -I$(srcdir)/troff < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm | pnmrotate 90 > $@
	$(RM) t.ps t.pnm

data/manw.pnm: $(srcdir)/troff/manw.n
	groff -I$(srcdir)/troff < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

data/manN.pnm: $(srcdir)/troff/manE.n
	groff -I$(srcdir)/troff < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm | pnmrotate 90 > $@
	$(RM) t.ps t.pnm

data/manE.pnm: $(srcdir)/troff/manE.n
	groff -I$(srcdir)/troff < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

data/manS.pnm: $(srcdir)/troff/manW.n
	groff -I$(srcdir)/troff < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm | pnmrotate 90 > $@
	$(RM) t.ps t.pnm

data/manW.pnm: $(srcdir)/troff/manW.n
	groff -I$(srcdir)/troff < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

data/treasure.pnm: $(srcdir)/troff/treasure.n
	groff -I$(srcdir)/troff < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

data/arrown.pnm: $(srcdir)/troff/arrown.n
	groff -I$(srcdir)/troff < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

data/arrowe.pnm: $(srcdir)/troff/arrowe.n
	groff -I$(srcdir)/troff < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

data/arrows.pnm: $(srcdir)/troff/arrows.n
	groff -I$(srcdir)/troff < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

data/arroww.pnm: $(srcdir)/troff/arroww.n
	groff -I$(srcdir)/troff < $< > t.ps
	echo "" | gs -q -dBATCH -dSAFER -sDEVICE=pnmraw -r100 -sOutputFile=t.pnm t.ps
	pnmcrop t.pnm > $@
	$(RM) t.ps t.pnm

release: force
	echo penguin-tower-`sed -e '/version_string/!d' \
          -e 's/[^0-9.]*\([0-9.]*\).*/\1/' -e q version.c` > .fname
	-rm -rf `cat .fname`
	mkdir `cat .fname`
	dst=`cat .fname`; for f in $(DISTFILES); do \
           cp -rp $(srcdir)/$$f $$dst/$$f ; \
        done
	tar --gzip -chf `cat .fname`.tar.gz `cat .fname`
	uuencode `cat .fname`.tar.gz `cat .fname`.tar.gz > `cat .fname`.uue
	-rm -rf `cat .fname` .fname

force:
