import cx_Freeze
import sys

base = None

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name = "SeaofBTC-Client",
    options = {"build_exe": {"packages":["tkinter"], "include_files":[]}},
    version = "0.01",
    description = "Sea of BTC trading application",
    executables = executables
    )