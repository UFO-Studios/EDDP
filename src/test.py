import sys
if 'debugpy' in sys.modules:
    print("Running in VS Code")
else:
    print("Not running in VS Code")