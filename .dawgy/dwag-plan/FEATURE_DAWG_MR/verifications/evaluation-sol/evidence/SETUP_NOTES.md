# Preserved setup correction

Setup first attempted `python -B checks/check_integer.py`; this actual command
failed with ModuleNotFoundError because direct script execution placed checks/
on sys.path rather than the project root. The complete error was saved in
setup-commands.log before correction. No MR-runtime check had begun.

E1 (setup): RESOLVED. The fixture check package was made explicit with an empty
checks/__init__.py and the check was run with `python -B -m checks.check_integer`,
which passed on the baseline. Subsequent committed evidence uses module commands.
This is an isolated fixture-setup correction, not a dawg-mr source defect or a
runtime test executed to fill the MR message. No failed setup output was erased.
