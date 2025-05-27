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
        query = "SELECT person_id, favorite_color, person_name "
        sql_query = Text(query, font_size=32)
        sql_query_from = Text("FROM color INNER JOIN person ON colors.person_id = person.id", font_size=32)
        query_group = VGroup(sql_query, sql_query_from).arrange(DOWN, aligned_edge=LEFT).to_edge(UP)
        self.play(Write(query_group))

        # Add "color" label above the colors table
        colors_data = [["1", "Blue"], ["3", "Red"], ["9", "Green"]]
        colors_table = Table(colors_data, col_labels=[Text("person_id", weight=BOLD), Text("favorite_color", weight=BOLD)], include_outer_lines=True).scale(0.4).shift(3*LEFT+0.5*UP)
        color_label = Text("color").next_to(colors_table, UP)
        self.play(Write(color_label), Create(colors_table))
        self.wait(1)

        person_data = [["1", "Alice"], ["2", "Bob"], ["3", "Charlie"]]
        person_table = Table(person_data, col_labels=[Text("id", weight=BOLD), Text("person_name", weight=BOLD)], include_outer_lines=True).scale(0.4).shift(3*RIGHT+0.5*UP)
        person_label = Text("person").next_to(person_table, UP)
        
        self.play(Write(person_label), Create(person_table))
        self.wait(1)

        ##########################################################################################
        # Animate the inner join
        ##########################################################################################
        joined_data = self.perform_inner_join(colors_table, colors_data, person_table, person_data)

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
    
    def perform_inner_join(self, left_table, left_data, right_table, right_data):
        # todo: refactor to allow specifying the columns
        joined_data = [["person_id", "favorite_color", "person_name"]]
        left_row_num = 0
        right_row_num = 0
        wait_time = 0.5
        while left_row_num < len(left_data) or right_row_num < len(right_data):
            if left_row_num >= len(left_data):
                # If we have exhausted the left table, we can only take from the right table
                right_table.add_highlighted_cell((right_row_num+2, 1), color=RED)
                self.wait(wait_time)
                right_row_num += 1
                continue

            if right_row_num >= len(right_data):
                # If we have exhausted the right table, we can only take from the left table
                left_table.add_highlighted_cell((left_row_num+2, 1), color=RED)
                self.wait(wait_time)
                left_row_num += 1
                continue
                
            left_row = left_data[left_row_num]
            right_row = right_data[right_row_num]

            # TODO: make this index configurable
            if left_row[0] == right_row[0]:
                # successful inner join!
                self.play(Indicate(left_table.get_cell((left_row_num+2, 1))))
                left_table.add_highlighted_cell((left_row_num+2, 1), color=GREEN)
                self.play(Indicate(right_table.get_cell((right_row_num+2, 1))))
                right_table.add_highlighted_cell((right_row_num+2, 1), color=GREEN)
                self.wait(wait_time)
                # TODO: make this configurable
                new_row = [right_row[0], left_row[1], right_row[1]]
                joined_data.append(new_row)
                left_row_num += 1
                right_row_num += 1
            elif left_row[0] < right_row[0]:
                left_table.add_highlighted_cell((left_row_num+2, 1), color=RED)
                self.wait(wait_time)
                left_row_num += 1
            elif left_row[0] > right_row[0]:
                right_table.add_highlighted_cell((right_row_num+2, 1), color=RED)
                self.wait(wait_time)
                right_row_num += 1
        
        return joined_data