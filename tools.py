from pathlib import Path


def copy(self, target):
    import shutil
    shutil.copy2(self, target)


# Añade el método a la clase Path
Path.copy = copy
