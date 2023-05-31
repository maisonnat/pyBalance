import math
import re
from pathlib import Path
from datetime import datetime


def copy(self, target):
    import shutil
    shutil.copy2(self, target)


# Añade el método a la clase Path
Path.copy = copy


class LevelBalancer:
    def __init__(self, filename):
        self.filename = Path(filename)

    def backup_file(self):
        backup_filename = f"{str(self.filename.stem)}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}{str(self.filename.suffix)}"
        self.filename.copy(backup_filename)

    def balance(self):
        # Crea una copia de seguridad del archivo original.
        self.backup_file()

        # Lee el archivo.
        with open(self.filename, 'r') as file:
            data = file.read()

        # Encuentra la sección [INIT] en el archivo.
        init_section = re.search(r'\[INIT\][\s\S]*?(?=\[|\Z)', data).group(0)

        # Extrae los valores de Nivel y Experiencia del archivo.
        levels_and_exp = re.findall(r'Nivel(\d+)=(\d+)', init_section)

        # Crea una lista vacía para guardar los nuevos valores de experiencia.
        new_exp_values = []

        # Recorre cada par de nivel y experiencia.
        for level, exp in levels_and_exp:
            # Convierte los valores a enteros.
            level = int(level)
            exp = int(exp)

            # Elige una función para calcular la nueva experiencia según el nivel.
            # Puedes cambiar esta función por otra que prefieras.
            # En este caso usamos una función exponencial con base e y un multiplicador de 1000.
            new_exp = math.ceil(math.exp(level / 10) * 1000)

            # Añade el nuevo valor a la lista.
            new_exp_values.append(new_exp)

            # Reemplaza el valor antiguo por el nuevo en la sección [INIT].
            init_section = re.sub(f'Nivel{level}=\d+', f'Nivel{level}={new_exp}', init_section)

        # Replace the old init section with the new one
        data = re.sub(r'\[INIT\][\s\S]*?(?=\[|\Z)', init_section, data)

        # Write the data back to the file
        with open(self.filename, 'w') as file:
            file.write(data)
