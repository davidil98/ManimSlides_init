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
egofets/
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
├── egofets_test.ipynb       # Experimentación libre
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

```bash
conda activate manim

# Dependencias del visor interactivo
conda install -c conda-forge pyside6 qt6-multimedia -y

# Manim Slides + soporte Jupyter
pip install "manim-slides[magic]"
```

Requiere `manim>=0.19` y `manimpango>=0.6.1`.

## Galería

Notebooks de ejemplo en `gallery/`:

- `01_canvas_y_zoom.ipynb`: `SlidesControl` con `ZoomedScene`.
- `02_video_en_escena.ipynb`: `VideoMobject` insertando un video.
- `03_graficos_espectros.ipynb`: `ManimGraph` graficando datos.
- `04_estructuras_quimicas.ipynb`: pendiente de poblar.
