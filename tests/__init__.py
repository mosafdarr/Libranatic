import os
import sys

test_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(test_dir)
lib_dir = os.path.join(root_dir, "src")

sys.path.append(lib_dir)
sys.path.append(os.path.join(lib_dir, "libintegration"))
