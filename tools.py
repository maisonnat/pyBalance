from pathlib import Path


def copy(self, target):
    import shutil
    shutil.copy2(self, target)


# A�ade el m�todo a la clase Path
Path.copy = copy
