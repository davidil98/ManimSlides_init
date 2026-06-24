"""Template de presentación con Manim Slides.

Define cada sección como una clase `Slide` (versión simple) o
`SlidesControl` (versión con canvas persistente y número de diapositiva).
Renderiza selectivamente y ensambla al final con `manim-slides`.

Render individual:
    manim-slides render presentacion.py Introduccion

Ensamblado final:
    manim-slides convert Introduccion Estructura Funcionamiento Conclusion salida.html
"""

from manim import *
from manim_slides import Slide

from toolkit import NORMAL_SIZE, SlidesControl, TITLE_SIZE

config.verbosity = "WARNING"


class Introduccion(Slide):
    """Ejemplo simple: hereda de Slide sin canvas persistente."""

    def construct(self):
        titulo = Text("Canales Iónicos en EGOFETs")
        titulo.scale(1.2)
        self.play(Write(titulo))
        self.next_slide()

        subtitulo = Text("Mecanismos de transporte y sensado").scale(0.6)
        subtitulo.next_to(titulo, DOWN, buff=0.5)
        self.play(FadeIn(subtitulo))
        self.next_slide()
        self.wait()


class Estructura(Slide):
    def construct(self):
        canal = Circle(radius=2, color=BLUE)
        self.play(Write(canal))
        self.next_slide()

        membrana = Rectangle(width=6, height=0.2, color=WHITE, fill_opacity=0.5)
        membrana.move_to(canal.get_center())
        self.play(FadeIn(membrana))
        self.next_slide()

        label_mem = Text("Membrana lipídica").scale(0.4).next_to(membrana, DOWN, buff=0.3)
        label_can = Text("Canal iónico").scale(0.4).next_to(canal, RIGHT, buff=0.5)
        self.play(Write(label_mem), Write(label_can))
        self.next_slide()
        self.wait()


class Funcionamiento(Slide):
    def construct(self):
        canal = Circle(radius=2, color=BLUE)
        self.add(canal)

        ion = Dot(color=YELLOW, radius=0.2)
        ion.move_to(canal.get_top())

        self.play(FadeIn(ion))
        self.next_slide(loop=True)
        self.play(ion.animate.move_to(canal.get_bottom()), run_time=1.5)
        self.next_slide()

        explicacion = Text("Flujo de iones a través del canal").scale(0.5)
        explicacion.to_edge(DOWN)
        self.play(Write(explicacion))
        self.next_slide()
        self.wait()


class Conclusion(Slide):
    def construct(self):
        puntos = BulletedList(
            "Canales iónicos: sensado químico",
            "EGOFETs: transducción eléctrica",
            "Aplicaciones en biosensores",
            font_size=NORMAL_SIZE - 6,
        )
        self.play(Write(puntos))
        self.next_slide()

        cierre = Text("Gracias").scale(1.5)
        self.play(FadeOut(puntos), FadeIn(cierre))
        self.next_slide()
        self.wait()


class DemoCanvas(SlidesControl):
    """Ejemplo avanzado: usa SlidesControl con título y número persistentes."""

    def construct(self):
        # Inicializar canvas persistente
        titulo = Title("Sección con Canvas", font_size=TITLE_SIZE).to_corner(UL)
        num = Text("1").to_corner(DL)
        self.add_to_canvas(title=titulo, slide_number=num)

        self.play(Write(titulo), Write(num))
        self.next_slide()

        contenido = Text(
            "Esta escena usa SlidesControl.\n"
            "El número de slide se actualiza con self.update_canvas()."
        )
        contenido.scale(0.6)
        self.play(Write(contenido))
        self.next_slide()

        # Cambiar el título de la siguiente "sub-sección" sin perder el número
        self.update_canvas()
        nuevo_titulo = Title("Sub-sección", font_size=TITLE_SIZE).to_corner(UL)
        self.play(titulo.animate.become(nuevo_titulo))
        self.next_slide()

        self.clear_slide_content()
        self.wait()
