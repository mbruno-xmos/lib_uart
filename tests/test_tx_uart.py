import xmostest
import os
from xmostest.xmostest_subprocess import call
from uart_tx_checker import UARTTxChecker, Parity


def do_test(baud):
    myenv = {'baud':baud}
    path = "app_uart_test_tx"
    resources = xmostest.request_resource("xsim")

    checker = UARTTxChecker("tile[0]:XS1_PORT_1A", "tile[0]:XS1_PORT_1B", Parity['UART_PARITY_NONE'], baud, 256, 1, 8)
    tester  = xmostest.ComparisonTester(open('test_tx_uart.expect'),
                                        "lib_uart", "sim_regression", "tx", myenv,
                                        regexp=True)

    # Only want no parity @ 230400 baud for smoke tests
    if baud != 230400:
        tester.set_min_testlevel('nightly')
    if tester.test_required() != True:
        return

    xmostest.build(path, env = myenv, do_clean = True)

    xmostest.run_on_simulator(resources['xsim'],
        'app_uart_test_tx/bin/smoke/app_uart_test_tx_smoke.xe',
        simthreads = [checker],
        xscope_io=True,
        tester = tester)

def runtests():
    for baud in [57600, 115200, 230400]:
        do_test(baud)