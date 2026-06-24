# Toolkit de presentaciones Manim Slides

Estructura base para crear presentaciones tipo RevealJS con animaciones de Manim.

## Inicio rápido

```bash
conda activate manim

# 1. Renderizar todas las escenas (calidad baja para iterar)
python scripts/workflow.py render-all -q l

# 2. Visualizar interactivamente
python scripts/workflow.py present Introduccion Estructura

# 3. Exportar producto final
python scripts/workflow.py export html salida.html --open
```

## Estructura del proyecto

```
ManimSlides_init/
├── presentacion.py          # Clases Slide de la presentación
├── scripts/workflow.py      # CLI para render/present/export
├── toolkit/                 # Utilidades reutilizables
│   ├── canvas.py            # SlidesControl, constantes
│   ├── video.py             # VideoMobject
│   ├── graphs.py            # ManimGraph
│   └── chemistry.py         # (pendiente) estructuras químicas
├── gallery/                 # Notebooks demo de cada herramienta
│   ├── 01_canvas_y_zoom.ipynb
│   ├── 02_video_en_escena.ipynb
│   ├── 03_graficos_espectros.ipynb
│   └── 04_estructuras_quimicas.ipynb  # pendiente
├── test.ipynb       # Experimentación libre
├── slides/                  # Generado, ignorado por git
└── media/                   # Generado, ignorado por git
```

## Flujo de trabajo

### 1. Diseñar escenas en `presentacion.py`

Cada sección es una clase `Slide` (simple) o `SlidesControl` (con canvas persistente).

```python
from manim_slides import Slide
from toolkit import SlidesControl, NORMAL_SIZE, TITLE_SIZE

class Introduccion(Slide):
    def construct(self):
        titulo = Text("Mi sección")
        self.play(Write(titulo))
        self.next_slide()  # Pausa: usuario presiona ->

class ConCanvas(SlidesControl):
    def construct(self):
        titulo = Title("Sección", font_size=TITLE_SIZE).to_corner(UL)
        num = Text("1").to_corner(DL)
        self.add_to_canvas(title=titulo, slide_number=num)
        # ...
```

### 2. Probar selectivamente

```bash
# Solo la escena en la que estás trabajando
manim-slides render presentacion.py Introduccion -ql
manim-slides Introduccion

# O desde el script
python scripts/workflow.py render-all -q l
```

### 3. Ensamblar sin re-renderizar

```bash
manim-slides Introduccion Estructura Funcionamiento Conclusion
```

### 4. Exportar producto final

```bash
# HTML (RevealJS)
manim-slides convert Introduccion Estructura Conclusion salida.html --open

# PowerPoint
manim-slides convert Introduccion Estructura Conclusion salida.pptx

# PDF / ZIP
manim-slides convert Introduccion Conclusion salida.pdf
manim-slides convert Introduccion Conclusion salida.zip
```

## Toolkit

Re-exportado en `toolkit/__init__.py` para import simple:

```python
from toolkit import (
    SlidesControl,    # Slide + ZoomedScene con canvas persistente
    VideoMobject,     # Reproducir video como ImageMobject animado
    ManimGraph,       # Wrapper para Axes + plot_spectrum + create_legend
    TINY_SIZE,        # 17
    TITLE_SIZE,       # 50
    NORMAL_SIZE,      # 30
    HOME,             # "figures"
)
```

### Cuándo usar cada cosa

| Herramienta | Caso de uso |
|-------------|-------------|
| `Slide` | Diapositiva simple sin canvas persistente. |
| `SlidesControl` | Presentación larga con número visible y título entre slides. |
| `VideoMobject` | Incrustar un `.mp4` en la escena. |
| `ManimGraph` | Graficar datos espectroscópicos desde archivos de 2 columnas. |
| `chemistry.py` | (Pendiente) dibujar estructuras moleculares. |

## Tips

### `self.next_slide()` vs `self.wait()`

- `self.next_slide()`: pausa que el presentador controla con la flecha `→`.
- `self.wait()`: pausa fija (en segundos o hasta fin de animaciones).
- `self.next_slide(loop=True)`: la animación se repite hasta presionar `→`.
  Útil para procesos cíclicos o cuando quieres hablar mientras se mueve algo.

### Renderizado selectivo

Cada `Slide` se renderiza a un archivo `.json` independiente en `slides/`.
Si modificas una escena, solo re-renderiza esa:

```bash
manim-slides render presentacion.py Estructura
```

Las demás escenas siguen listas para presentar.

### Atajos del visor interactivo

| Tecla | Acción |
|-------|--------|
| `→` / `Space` | Siguiente diapositiva |
| `←` | Diapositiva anterior |
| `Esc` / `Q` | Salir |
| `F` | Pantalla completa |
| `G` | Ir a escena específica |

### Calidad

| Flag | Resolución | FPS | Uso |
|------|-----------|-----|-----|
| `-ql` | 480p | 15 | Iteración rápida |
| `-qm` | 720p | 30 | Previsualización |
| `-qh` | 1080p | 60 | Producto final |
| `-qp` | 1440p | 60 | Alta calidad |
| `-qk` | 2160p | 60 | 4K |

## Instalación

Este proyecto requiere **LaTeX**, **FFmpeg** y dependencias gráficas.

### Dependencias del sistema (Linux)

`manimpango` (necesario para manim) no tiene wheels pre-compiladas para Linux.
Antes de instalar los paquetes Python, necesitas:

```bash
# Ubuntu/Debian
sudo apt install libpango1.0-dev pkg-config python3-dev

# Arch Linux
sudo pacman -S python-pip python-setuptools pkg-config cairo pango

# Fedora
sudo dnf install pango-devel pkg-config python3-devel redhat-rpm-config
```

Luego puedes instalar `manimpango` con:

```bash
pip install manimpango
# o con conda:
conda install -c conda-forge manimpango
```

### Opción 1: Conda (sin LaTeX, ya lo tienes instalado)

Si ya tienes LaTeX por separado y prefieres conda solo para las dependencias Python:

```bash
conda env create -f environment.yml
conda activate manim
```

### Opción 2: Conda (con LaTeX incluido)

Si prefieres que conda maneje todo, incluyendo LaTeX:

```bash
conda env create -f environment.yml
conda install -c conda-forge texlive-core -y
conda activate manim
```

### Opción 3: uv + pyproject.toml

Si prefieres un entorno más ligero con uv:

```bash
# 1. Instalar uv (si no lo tienes)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Crear entorno virtual e instalar dependencias
uv venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Instalar manimpango primero (requiere las dependencias del sistema, ver arriba)
pip install manimpango

# 4. Instalar el resto desde pyproject.toml
uv pip install -e .

# 5. Dependencias del sistema (LaTeX, FFmpeg, etc.):
#    - Con conda:
conda install -c conda-forge ffmpeg texlive-core pycairo pango cairo pyside6 qt6-multimedia -y
#    - En Arch:
sudo pacman -S ffmpeg texlive-most pycairo pango cairo qt6-multimedia
#    - En Ubuntu/Debian:
sudo apt install ffmpeg texlive texlive-latex-extra pycairo libcairo2-dev libpango1.0-dev qt6-multimedia-dev
```

### Opción 4: Solo pip

Si prefieres pip sin gestores de entorno:

```bash
# 1. Instalar manimpango primero (requiere las dependencias del sistema, ver arriba)
pip install manimpango

# 2. Instalar el resto
pip install manim "manim-slides[magic]" opencv-python scipy pillow jupyter notebook ipykernel
```

### Verificar instalación

```bash
manim --version
manim-slides --version
jupyter --version
```

## Usar como template

Puedes usar este repositorio como base para nuevas presentaciones de dos formas:

### Opción A: "Use this template" (proyectos independientes)

En GitHub, haz click en **"Use this template"** para crear un repositorio nuevo independiente. Recibirás una copia limpia sin historial git.

### Opción B: git clone (para recibir actualizaciones)

Si quieres poder recibir actualizaciones de este repositorio original:

```bash
# 1. Clonar tu fork o el repositorio original
git clone https://github.com/tu-user/tu-presentacion.git
cd tu-presentacion

# 2. Agregar este repositorio como upstream
git remote add upstream https://github.com/david-ibarra/ManimSlides_init.git

# 3. (Opcional) Verificar los remotes
git remote -v

# Para recibir actualizaciones futuras:
git fetch upstream
git merge upstream/main
# Resuelve conflictos manualmente si los hay

# 4. (Opcional) Mantener tu fork actualizado
git push origin main
```

## Galería

Ejemplos en `gallery/`. Cada demo tiene **dos versiones**:

- `.ipynb`: notebook con `%%manim_slides` (solo funciona en Jupyter).
- `.py`: script ejecutable con `manim-slides render` (funciona siempre).

| Demo | Notebook | Script | Qué muestra |
|------|----------|--------|-------------|
| Canvas y zoom | `01_canvas_y_zoom.ipynb` | `01_canvas_y_zoom.py` | `SlidesControl` con `wipe()` y `ZoomedScene` |
| Video | `02_video_en_escena.ipynb` | `02_video_en_escena.py` | `VideoMobject` reproduciendo un .mp4 |
| Espectros | `03_graficos_espectros.ipynb` | `03_graficos_espectros.py` | `ManimGraph` con suavizado Savitzky-Golay |
| Química | `04_estructuras_quimicas.ipynb` | `04_estructuras_quimicas.py` | RDKit/Datamol generando imágenes 2D |

### Ejecutar un demo como script

```bash
manim-slides render gallery/01_canvas_y_zoom.py DemoCanvasZoom -ql
manim-slides DemoCanvasZoom
```

### Ejecutar un demo en Jupyter

Abre el notebook, ejecuta la celda de imports, y la celda con `%%manim_slides`.
La celda mágica **solo produce el iframe con la presentación** dentro del navegador de Jupyter.
