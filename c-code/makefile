# Make file for AD7124 driver.

default: all

CC=gcc
CXX=g++
RM=rm -f
CPPFLAGS=-g
LDFLAGS=-g
LDLIBS=

SRCS=ad7124.c ad7124_regs.c ad7124_test.c platform_drivers.c
OBJS=$(subst .cc,.o,$(SRCS))

all: ad7124

ad7124: $(OBJS)
	$(CC) $(LDFLAGS) -o ad7124 $(OBJS) $(LDLIBS)

depend: .depend

.depend: $(SRCS)
	$(RM) ./.depend
	$(CXX) $(CPPFLAGS) -MM $^>>./.depend;

clean:
	$(RM) $(OBJS)

distclean: clean
	$(RM) *~ .depend

include .depend
