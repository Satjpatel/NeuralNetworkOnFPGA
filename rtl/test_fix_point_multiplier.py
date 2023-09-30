from cocotb_test.simulator import run
def test_fix_point_adder():
    run(
        verilog_sources=["fix_point_multiplier.sv"], # sources
        toplevel="fix_point_multiplier",            # top level HDL
        module="tb_fix_point_multiplier"        # name of cocotb test module
    )