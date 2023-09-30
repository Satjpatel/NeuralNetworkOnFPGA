from cocotb_test.simulator import run
def test_sigmoid():
    run(
        verilog_sources=["sigmoid.sv"], # sources
        toplevel="sigmoid",            # top level HDL
        module="tb_sigmoid"        # name of cocotb test module
    )