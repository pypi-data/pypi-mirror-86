import os

def pytest_generate_tests(metafunc):
    script_dir = os.path.dirname(__file__) or "."
    os.chdir(script_dir)
    test_list = [x for x in os.listdir("./functional/") if os.path.isdir(x)]
    metafunc.parametrize("directory", test_list)
