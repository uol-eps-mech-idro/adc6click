# Make file for AD7124 driver.

default: all

CC=gcc
CXX=g++
RM=rm -f
CPPFLAGS=-g $(shell root-config --cflags)
LDFLAGS=-g $(shell root-config --ldflags)
LDLIBS=$(shell root-config --libs)

SRCS=ad7124.c ad7124_regs.c
OBJS=$(subst .cc,.o,$(SRCS))

all: ad7124

ad7124: $(OBJS)
	$(CXX) $(LDFLAGS) -o ad7124 $(OBJS) $(LDLIBS)

depend: .depend

.depend: $(SRCS)
	$(RM) ./.depend
	$(CXX) $(CPPFLAGS) -MM $^>>./.depend;

clean:
	$(RM) $(OBJS)

distclean: clean
	$(RM) *~ .depend

include .depend
