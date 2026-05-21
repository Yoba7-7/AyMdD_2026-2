# Proyectos y Tareas para Almacenes y Minerias de Datos 26-2

| Alumnos                     | No. de Cuenta |
| --------------------------- | ------------- |
| Méndez Ávila Luis Geovanni  | 317143980     |
| Paredes Zamudio Luis Daniel | 318159926     |

<br/>

## Dependencias

### Python

Se usa [uv](https://docs.astral.sh/uv/) como manejador de paquetes, entorno virtual y de ejecución.

Para sincronizar la configuración se hace lo siguiente:

```bash
# En Mac y/o Linux:
source .venv/bin/activate
# o el equivalente en Windows:
source .venv/Scripts/activate
uv sync
```

### Jupyter Notebooks

Parten de las dependencias anteriores de Python y uv. Para ejecutarlos de manera más práctica
y más rápida, se ejecuta el siguiente comando:

```bash
uv run --with jupyter jupyter lab
```

Esto abrirá la interfaz web en el puerto 8888. Favor de referirse al documento de cada tarea para más detalles sobre los notebooks (archivo con extensión `.ipynb`).

### pre-commit

Se usa una configuración de pre-commit que se ejecuta antes de cada commit de manera automática. Esto para prevenir incluir archivos `.env`, archivos pesados, ejecución de linter (`ruff`), etc.

Para activarla se hace lo siguiente:

```bash
pre-commit install
```
Se activa de manera automática tras cada `git commit`.

> [!NOTE]
> Es posible la instalación y ejecución de las dependencias y configuraciones usando métodos tradicionales como `pip`, simplemente se recomienda usar las configuraciones mencionadas para mayor velocidad.

### Quarto

Posterior a la instalación del programa en su página oficial, el comando de ejecución para las presentaciones (partiendo de la carpeta /presentation de cada tarea) es el siguiente:

```bash
quarto render presentation.qmd --to revealjs --self-contained
# O, si se quiere ver un preview en vivo:
quarto preview presentation.qmd
```

> [!NOTE]
> La presentación y archivos que se encuentran en la carpeta raiz de este repositorio para revisar
> alguna en particular es necesario entrar a la carpeta de cada tarea y ejecutar el comando mencionado.
