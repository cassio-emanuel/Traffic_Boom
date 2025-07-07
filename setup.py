from cx_Freeze import setup, Executable

executables = [Executable("main.py")]

setup(
    name="TrafficBoom",
    version="1.0",
    description="Traffic Boom app",
    options={"build_exe": {"packages": ["pygame"]}},
    executables=executables

)
