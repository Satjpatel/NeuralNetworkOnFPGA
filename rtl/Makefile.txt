# Makefile

TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(shell pwd)/fix_point_adder.sv
TOPLEVEL = fix_point_adder
MODULE = fix_point_adder_tb

include $(shell cocotb-config --makefiles)/Makefile.sim