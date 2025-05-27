from manim import *

def scan(data, id):
    """
    Scan the data for a specific ID and return the corresponding row.
    """
    i = 0
    for row in data:
        if row[0] == id:
            return i
        i += 1
    return None


class InnerJoin(Scene):
    def construct(self):
        # Visual representation of the inner join operation
        # Show the SQL query at the top of the screen
        query = "SELECT person_id, favorite_color, person_name\nFROM color INNER JOIN person ON colors.person_id = person.id"
        sql_query = Text(query, font_size=32)

        sql_query.to_edge(UP)
        self.play(Write(sql_query))

        # Add "color" label above the colors table
        colors_data = [["1", "Blue"], ["3", "Red"], ["9", "Green"]]
        colors_table = Table(colors_data, col_labels=[Text("person_id", weight=BOLD), Text("favorite_color", weight=BOLD)], include_outer_lines=True).scale(0.4).shift(3*LEFT+0.5*UP)
        color_label = Text("color").next_to(colors_table, UP)
        self.play(Write(color_label), Create(colors_table))
        self.wait(1)

        person_data = [["1", "Alice"], ["2", "Bob"], ["3", "Charlie"]]
        person_table = Table(person_data, col_labels=[Text("id", weight=BOLD), Text("person_name", weight=BOLD)], include_outer_lines=True).scale(0.4).shift(3*RIGHT+0.5*UP)
        person_label = Text("person").next_to(person_table, UP)
        
        # person_table.add(SurroundingRectangle(person_table.get_columns()[0], color=YELLOW))
        self.play(Write(person_label), Create(person_table))
        self.wait(1)


        joined_data = [["person_id", "favorite_color", "person_name",]]
        row_num = 0
        for colors_row in colors_data:
            person_id = colors_row[0]
            found = scan(person_data, person_id)
            if found is not None:
                person_row = person_data[found]
                colors_table.add_highlighted_cell((row_num+2, 1), color=GREEN)
                self.wait(0.2)
                self.play(Indicate(person_table.get_cell((found+2, 1))))  # animate the highlighting
                person_table.add_highlighted_cell((found+2, 1), color=GREEN)
                self.wait(0.2)
                new_row = [person_row[0], colors_row[1], person_row[1]]
                joined_data.append(new_row)
            else:
                colors_table.add_highlighted_cell((row_num+2, 1), color=RED)
                self.wait(0.2)
            
            self.wait(1)
            row_num += 1

        joined_table = Table(joined_data, include_outer_lines=True).scale(0.4).to_edge(DOWN)
        joined_label = Text("Result").next_to(joined_table, UP)
        # joined_table.add(SurroundingRectangle(joined_table.get_columns()[0], color=YELLOW))
        self.play(Write(joined_label), Create(joined_table))
        self.wait(2)

        # Highlight the columns in the colors and joined tables
        sql_query2 = Text(query, font_size=32, t2c={"person_id": YELLOW}, t2w={'person_id': BOLD}).move_to(sql_query.get_center())
        self.play(Transform(sql_query, sql_query2))
        rect1 = SurroundingRectangle(colors_table.get_columns()[0], color=YELLOW)
        colors_table.add(rect1)
        self.play(Create(rect1))
        self.wait(0.5)        
        rect2 = SurroundingRectangle(joined_table.get_columns()[0], color=YELLOW)
        joined_table.add(rect2)
        self.play(Create(rect2))
        self.wait(0.5)
        colors_table.remove(rect1)
        joined_table.remove(rect2)
        self.play(Uncreate(rect1), Uncreate(rect2))

        sql_query3 = Text(query, font_size=32, t2c={"favorite_color": YELLOW}, t2w={'favorite_color': BOLD}).move_to(sql_query.get_center())
        self.play(Transform(sql_query, sql_query3))
        rect1 = SurroundingRectangle(colors_table.get_columns()[1], color=YELLOW)
        colors_table.add(rect1)
        self.play(Create(rect1))
        self.wait(0.5)        
        rect2 = SurroundingRectangle(joined_table.get_columns()[1], color=YELLOW)
        joined_table.add(rect2)
        self.play(Create(rect2))
        self.wait(0.5)
        colors_table.remove(rect1)
        joined_table.remove(rect2)
        self.play(Uncreate(rect1), Uncreate(rect2))
        
        sql_query4 = Text(query, font_size=32, t2c={"person_name": YELLOW}, t2w={'person_name': BOLD}).move_to(sql_query.get_center())
        self.play(Transform(sql_query, sql_query4))
        rect1 = SurroundingRectangle(person_table.get_columns()[1], color=YELLOW)
        person_table.add(rect1)
        self.play(Create(rect1))
        self.wait(0.5)        
        rect2 = SurroundingRectangle(joined_table.get_columns()[2], color=YELLOW)
        joined_table.add(rect2)
        self.play(Create(rect2))
        self.wait(0.5)
        person_table.remove(rect1)
        joined_table.remove(rect2)
        self.play(Uncreate(rect1), Uncreate(rect2))
        