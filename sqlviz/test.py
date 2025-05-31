from manim import *

def highlight_text(text, highlight_words, color=YELLOW):
    new_text = Text(text.original_text, font_size=text.font_size, t2c={highlight_words: color}, t2w={highlight_words:BOLD})\
        .move_to(text.get_center())
    return new_text

class Sandbox(Scene):
    def construct(self):
        query = "SELECT person_id, favorite_color, person_name FROM color INNER JOIN person ON colors.person_id = person.id"
        text = Text(query, font_size=24)
        self.play(Create(text))
        # new_text = text.copy()
        # new_text.__init()
        # new_text.t2c = {"person_id": YELLOW}
        # new_text.t2w = {"person_id": BOLD}
        # new_text._set_color_by_t2c(t2c={"person_id": YELLOW})
        # self.play(text.animate.set_color(YELLOW))
        # text2 = Text(query, font_size=24, t2c={"person_id": YELLOW}, t2w={'person_id':BOLD})
        self.play(Transform(text, highlight_text(text, "person_id")))
