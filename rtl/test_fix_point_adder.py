from cocotb_test.simulator import run
def test_fix_point_adder():
    run(
        verilog_sources=["fix_point_adder.sv"], # sources
        toplevel="fix_point_adder",            # top level HDL
        module="tb_fix_point_adder"        # name of cocotb test module
    )