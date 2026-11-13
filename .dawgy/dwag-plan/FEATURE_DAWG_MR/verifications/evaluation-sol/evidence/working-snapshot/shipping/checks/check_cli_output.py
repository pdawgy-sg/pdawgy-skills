import subprocess
import sys
result = subprocess.run([sys.executable, "-B", "cli.py", "1.2"], capture_output=True, text=True, check=True)
assert result.stdout == "Shipping: 10\n", repr(result.stdout)
