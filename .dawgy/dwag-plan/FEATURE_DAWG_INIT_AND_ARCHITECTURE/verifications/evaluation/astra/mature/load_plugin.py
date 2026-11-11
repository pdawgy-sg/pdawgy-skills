from importlib import import_module

plugin = import_module("ledgerbox.plugins")
print(plugin.label())
