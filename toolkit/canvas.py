"""Canvas persistente y control de diapositivas.

Provee `SlidesControl`, una clase base que hereda de `Slide` y `ZoomedScene`,
ofreciendo:
- Un canvas con título y número de diapositiva persistentes.
- Métodos para limpiar contenido entre diapositivas.
- Animación de título de sección.

Uso:
    from toolkit import SlidesControl

    class MiSeccion(SlidesControl):
        def construct(self):
            self.counter = 0
            titulo = Title("Mi sección").to_corner(UL)
            num = Text("1").to_corner(DL)
            self.add_to_canvas(title=titulo, slide_number=num)
            self.play(Write(titulo))
            self.next_slide()
"""

from manim import (
    FadeIn,
    FadeOut,
    Group,
    LEFT,
    Tex,
    Text,
    Title,
    Transform,
    ZoomedScene,
)
from manim_slides import Slide

TINY_SIZE = 17
TITLE_SIZE = 50
NORMAL_SIZE = 30

HOME = "figures"


class SlidesControl(Slide, ZoomedScene):
    """Clase base para presentaciones con canvas persistente."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slide_canvas = {}
        self.slide_counter = 0

    def add_to_canvas(self, title=None, slide_number=None):
        """Registra objetos persistentes en el canvas.

        Args:
            title: Mobject que se mantiene visible entre diapositivas
                   (normalmente un título).
            slide_number: Mobject que se actualiza con `update_canvas`.
        """
        if title is not None:
            self.slide_canvas["title"] = title
        if slide_number is not None:
            self.slide_canvas["slide_number"] = slide_number

    def update_canvas(self):
        """Incrementa el contador y transforma el número visible."""
        self.slide_counter += 1
        old_slide_number = self.slide_canvas["slide_number"]
        new_slide_number = Text(f"{self.slide_counter}").move_to(old_slide_number)
        self.play(Transform(old_slide_number, new_slide_number))

    def clear_slide_content(self):
        """Hace fade out de todo excepto título y número de diapositiva."""
        trash_can = [
            mobj
            for mobj in self.mobjects
            if mobj
            not in [
                self.slide_canvas.get("title"),
                self.slide_canvas.get("slide_number"),
            ]
        ]
        self.play(FadeOut(*trash_can))

    def clear_allSlide_wipe(self, next_slide_content):
        """Limpia todo excepto el número de diapositiva con animación wipe."""
        trash_can = [
            mobj
            for mobj in self.mobjects
            if mobj is not self.slide_canvas.get("slide_number")
        ]
        self.wipe(Group(*trash_can), next_slide_content, run_time=1.2)

    def clear_allSlide_fade(self):
        """Limpia todo excepto el número de diapositiva con fade out."""
        trash_can = [
            FadeOut(mob)
            for mob in self.mobjects
            if mob is not self.slide_canvas.get("slide_number")
        ]
        self.play(*trash_can)

    def section_title_animation(self, str_title):
        """Muestra un título grande a la izquierda y lo quita tras la pausa."""
        section_title = Tex(
            str_title,
            tex_environment="flushleft",
            font_size=TITLE_SIZE + 15,
        ).to_edge(LEFT)

        self.play(FadeIn(section_title))
        self.next_slide()
        self.play(FadeOut(section_title))
