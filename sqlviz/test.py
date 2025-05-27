from manim import *
class Sandbox(Scene):
    def construct(self):
        query = "SELECT person_id, favorite_color, person_name FROM color INNER JOIN person ON colors.person_id = person.id"
        text = Text(query, font_size=24)
        self.play(Create(text))
        # self.play(text.animate.set_color(YELLOW))
        text2 = Text(query, font_size=24, t2c={"person_id": YELLOW}, t2w={'person_id':BOLD})
        self.play(Transform(text, text2))
