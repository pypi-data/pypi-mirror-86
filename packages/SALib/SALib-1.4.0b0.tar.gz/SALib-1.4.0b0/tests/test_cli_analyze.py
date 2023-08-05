"""Test CLI usage.

These tests only ensure input/outputs from the CLI.
Results are compared against previously obtained results.
"""

import sys
import subprocess
from SALib.test_functions import Ishigami
import numpy as np
import pandas as pd
from io import StringIO

import re
import os
from os.path import join as pth_join

salib_cli = "./src/SALib/scripts/salib.py"
ishigami_fp = "./src/SALib/test_functions/params/Ishigami.txt"
test_dir = 'tests/data'
input_file = 'model_input.txt'
output_file = 'model_output.txt'
input_path = pth_join(test_dir, input_file) 
output_path =  pth_join(test_dir, output_file)

if sys.version_info[0] == 2:
    subprocess.run = subprocess.call


def teardown_function(func):
    # Removes the test file if it was created.
    files = os.listdir(test_dir)
    if input_file in files:
        os.remove(input_path)

    if output_file in files:
        os.remove(output_path)


def test_delta():
    cmd = f"python {salib_cli} sample saltelli -p {ishigami_fp} -o {input_path} -n 1000 \
    --precision 8 --max-order 2 --seed=100"
    subprocess.run(cmd.split())

    # Run model and save output
    np.savetxt(output_path, Ishigami.evaluate(
        np.loadtxt(input_path)))

    analyze_cmd = f"python {salib_cli} analyze delta -p {ishigami_fp} -X {input_path} \
    -Y {output_path} -c 0 -r 10 --seed=100".split()

    result = subprocess.check_output(analyze_cmd, universal_newlines=True)

    delta_expected = [0.210478, 0.354023, 0.160986]
    sobol_expected = [0.311362, 0.428365, 0.001111]

    test = pd.read_csv(StringIO(result), index_col=0, sep=r'\s+')
    test['expected'] = delta_expected

    lower = (test['delta'] - test['delta_conf'])
    upper = (test['delta'] + test['delta_conf'])
    comparison = test['expected'].between(lower, upper)
    assert comparison.all(), \
        "Expected Delta results not within confidence bounds"

    test['expected'] = sobol_expected
    lower = (test['S1'] - test['S1_conf'])
    upper = (test['S1'] + test['S1_conf'])
    comparison = test['expected'].between(lower, upper)
    assert comparison.all(), \
        "Expected Sobol results not within confidence bounds"


def test_dgsm():
    # Generate inputs
    cmd = f"python {salib_cli} sample finite_diff -p {ishigami_fp} -o {input_path} -d 0.001\
    --precision=8 -n 1000 --seed=100".split()
    subprocess.run(cmd)

    # Run model and save output
    np.savetxt(output_path, Ishigami.evaluate(
        np.loadtxt(input_path)))

    analyze_cmd = f"python {salib_cli} analyze dgsm -p {ishigami_fp} -X {input_path}\
    -Y {output_path} -c 0 -r 1000 --seed=100".split()

    # run analysis and use regex to strip all whitespace from result
    result = subprocess.check_output(analyze_cmd, universal_newlines=True)

    dgsm_expected = [2.207554, 7.092019, 3.238259]

    test = pd.read_csv(StringIO(result), index_col=0, sep=r'\s+')
    test['expected'] = dgsm_expected

    lower = (test['dgsm'] - test['dgsm_conf'])
    upper = (test['dgsm'] + test['dgsm_conf'])
    comparison = test['expected'].between(lower, upper)
    assert comparison.all(), \
        "Expected DGSM results not within confidence bounds"


def test_fast():
    # Generate inputs
    cmd = f"python {salib_cli} sample fast_sampler -p {ishigami_fp} -o {input_path} \
    --precision=8 -n 1000 -M 4 --seed=100".split()
    subprocess.run(cmd)

    # Run model and save output
    np.savetxt(output_path, Ishigami.evaluate(
        np.loadtxt(input_path)))

    analyze_cmd = f"python {salib_cli} analyze fast -p {ishigami_fp} \
    -Y {output_path} -c 0 --seed=100".split()

    # run analysis and use regex to strip all whitespace from result
    result = subprocess.check_output(analyze_cmd, universal_newlines=True)

    expected = """              S1        ST   S1_conf   ST_conf
x1  3.104027e-01  0.555603  0.007016  0.027110
x2  4.425532e-01  0.469546  0.006901  0.026395
x3  1.921394e-28  0.239155  0.007892  0.026510"""

    col_names = ["Name", "S1", "ST", "S1_conf", "ST_conf"]

    data = StringIO(expected)
    df1 = pd.read_csv(data, sep="\t")

    df1 = df1.iloc[:, 0].str.split(expand=True)
    df1.columns = col_names
    df1 = df1.iloc[:, 1:].values.astype('float64')

    data = StringIO(result)
    df2 = pd.read_csv(data, sep="\t")

    df2 = df2.iloc[:, 0].str.split(expand=True)
    df2.columns = col_names
    df2 = df2.iloc[:, 1:].values.astype('float64')

    assert np.allclose(df1, df2), \
        "Unexpected FAST results.\n\nExpected:\n{}\n\nGot:{}"\
        .format(expected, result)


def test_ff():
    # Generate inputs
    cmd = f"python {salib_cli} sample ff -p {ishigami_fp} -o {input_path} \
    --precision=8 -n 1000 --seed=100".split()
    subprocess.run(cmd)

    # Run model and save output
    np.savetxt(output_path, Ishigami.evaluate(
        np.loadtxt(input_path)))

    analyze_cmd = f"python {salib_cli} analyze ff -p {ishigami_fp} -X {input_path} \
    -Y {output_path} -c 0 --seed=100".split()

    # run analysis and use regex to strip all whitespace from result
    result = subprocess.check_output(analyze_cmd, universal_newlines=True)
    result = re.sub(r'[\n\t\s]*', '', result)

    expected = "MEx13.855764e-08x20.000000e+00x30.000000e+00dummy_00.000000e+00IE(x1,x2)0.0(x1,x3)0.0(x2,x3)0.0(x1,dummy_0)0.0(x2,dummy_0)0.0(x3,dummy_0)0.0"
    assert len(result) > 0 and result == expected, \
        f"Unexpected FF results.\n\nExpected:\n{expected}\n\nGot:{result}"


def test_morris():

    # Generate inputs
    cmd = f"python {salib_cli} sample morris -p {ishigami_fp} -o {input_path} -n 100\
    --precision=8 --levels=10 --seed=100 -lo False".split()

    subprocess.run(cmd)

    # Run model and save output
    np.savetxt(output_path, Ishigami.evaluate(np.loadtxt(input_path)))

    # run analysis
    analyze_cmd = f"python {salib_cli} analyze morris -p {ishigami_fp} -X {input_path}\
    -Y {output_path} -c 0 -r 1000 -l 10 --seed=100".split()

    result = subprocess.check_output(analyze_cmd, universal_newlines=True)
    result = re.sub(r'[\n\t\s]*', '', result)

    expected_output = "mumu_starsigmamu_star_confx17.4989307.4989309.3304601.801208x2-0.4703942.2152432.7759250.347972x30.8640155.4238337.8621281.147559"

    assert len(result) > 0 and result == expected_output, \
        "Results did not match expected values:\n\n Expected: \n{} \n\n Got: \n{}".format(
            expected_output, result)


def test_rbd_fast():
    # Generate inputs
    cmd = f"python {salib_cli} sample latin -p {ishigami_fp} -o {input_path} \
    --precision=8 -n 1000 --seed=100".split()

    subprocess.run(cmd)

    # Run model and save output
    np.savetxt(output_path, Ishigami.evaluate(
        np.loadtxt(input_path)))

    analyze_cmd = f"python {salib_cli} analyze rbd_fast -p {ishigami_fp} -X {input_path}\
    -Y {output_path} --seed=100".split()

    # run analysis and use regex to strip all whitespace from result
    result = subprocess.check_output(analyze_cmd, universal_newlines=True)

    expected = [0.351277, 0.468170, -0.005864]

    test = pd.read_csv(StringIO(result), index_col=0, sep=r'\s+')
    test['expected'] = expected

    lower = (test['S1'] - test['S1_conf'])
    upper = (test['S1'] + test['S1_conf'])
    comparison = test['expected'].between(lower, upper)

    assert comparison.all(), \
        "RBD-FAST results +/- CI not in line with expected results."


def test_sobol():
    # Generate inputs
    cmd = f"python {salib_cli} sample saltelli -p {ishigami_fp} -o {input_path} -n 1000\
    --precision 8 --max-order 2 --seed=100"
    cmd = cmd.split()

    result = subprocess.check_output(cmd, universal_newlines=True)
    np.savetxt(output_path, Ishigami.evaluate(
        np.loadtxt(input_path)))

    analyze_cmd = f"python {salib_cli} analyze sobol -p {ishigami_fp}\
    -Y {output_path} -c 0 --max-order 2\
    -r 1000 --seed=100".split()

    result = subprocess.check_output(analyze_cmd, universal_newlines=True)
    result = re.sub(r'[\n\t\s]*', '', result)

    expected_output = 'STST_confx10.5601370.091908x20.4387220.040634x30.2428450.026578S1S1_confx10.3079750.063047x20.4477670.053323x3-0.0042550.059667S2S2_conf(x1,x2)0.0122050.086177(x1,x3)0.2515260.108147(x2,x3)-0.0099540.065569'
    assert len(result) > 0 and result == expected_output, \
        "Results did not match expected values:\n\n Expected: \n{} \n\n Got: \n{}".format(
            expected_output, result)


if __name__ == '__main__':
    test_delta()
    test_dgsm()
    test_fast()
    test_ff()
    test_morris()
    test_rbd_fast()
    test_sobol()
