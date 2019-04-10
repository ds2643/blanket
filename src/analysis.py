import ast
from operator import concat
from functools import reduce

import repository
import util


# NOTE: approach attributed to @jargnar
def get_fns_called(path):
    r = open(path, 'r')
    t = ast.parse(r.read())

    calls = []
    for node in ast.walk(t):
        if isinstance(node, ast.Call):
            vtr = util.FuncCallVisitor()
            vtr.visit(node.func)
            calls.append(vtr.name)

    # NOTE: module names associated with called functions dropped
    # as a simplication. for now, we ignore the case where two or
    # more functions of the same name are defined in two different
    # source files. Casting away this assumption should later help
    # when implementing tracing functionality.
    drop_module_name = (lambda fn_name: fn_name.split(".")[-1])

    calls_with_module_removed = list(map(drop_module_name, calls))
    return calls_with_module_removed


res2 = get_fns_called("./dev-resources/samplemod/tests/test_advanced.py")


def get_fns_defined(path):
    ''' Given a path to a python file, find the names of all functions
    defined therein.'''
    r = open(path, 'r')
    t = ast.parse(r.read())
    fs = [n.name for n in ast.walk(t) if isinstance(n, ast.FunctionDef)]
    return fs


def tally_function_calls(test_path):
    test_files = repository.find_python_files(test_path)
    # TODO: use fcalls vs fdef
    seen = reduce(concat, map(get_fns_called, test_files))
    return seen


res2 = tally_function_calls("./dev-resources/samplemod/tests/")


def report_coverage(source_path, test_path):
    report = dict()
    calls = tally_function_calls(test_path)
    source_files = repository.find_python_files(source_path)

    for f in source_files:
        module_name = repository.get_module_name(f)

        function_counts = {
            fn_name: calls.count(fn_name) for fn_name in get_fns_defined(f)
        }

        report[module_name] = {
            "source_path": f,
            "function_call_count": function_counts
        }

    return report


source_path = "./dev-resources/samplemod/sample/"
test_path = "./dev-resources/samplemod/tests/"
res = report_coverage(source_path, test_path)
