from manim import *

select_query = "SELECT favorite_color.person_id, favorite_color.color_name, person.first_name"
font_size = 24
colors_data = [["1", "Blue"], ["3", "Red"], ["3", "Purple"], ["9", "Green"]]
person_data = [["1", "Alice"], ["2", "Bob"], ["3", "Charlie"]]

def create_data_tables(self):
    self.colors_table = Table(colors_data, col_labels=[Text("person_id", weight=BOLD), Text("color_name", weight=BOLD)], include_outer_lines=True).scale(0.4).shift(3*LEFT+0.5*UP)
    color_label = Text("favorite_color").next_to(self.colors_table, UP)
    self.play(Write(color_label), Create(self.colors_table))
    self.wait(1)

    self.person_table = Table(person_data, col_labels=[Text("person_id", weight=BOLD), Text("first_name", weight=BOLD)], include_outer_lines=True).scale(0.4).shift(3*RIGHT+0.5*UP)
    person_label = Text("person").next_to(self.person_table, UP)
    
    self.play(Write(person_label), Create(self.person_table))
    self.wait(1)

def highlight_select_columns(self):
    # Highlight the columns in the colors and joined tables
    sql_query2 = Text(select_query, font_size=font_size, t2c={"person_id": YELLOW}, t2w={'person_id': BOLD}).move_to(self.sql_query.get_center())
    self.play(Transform(self.sql_query, sql_query2))
    rect1 = SurroundingRectangle(self.colors_table.get_columns()[0], color=YELLOW)
    self.colors_table.add(rect1)
    self.play(Create(rect1))
    self.wait(0.5)        
    rect2 = SurroundingRectangle(self.joined_table.get_columns()[0], color=YELLOW)
    self.joined_table.add(rect2)
    self.play(Create(rect2))
    self.wait(0.5)
    self.colors_table.remove(rect1)
    self.joined_table.remove(rect2)
    self.play(Uncreate(rect1), Uncreate(rect2))

    sql_query3 = Text(select_query, font_size=font_size, t2c={"color_name": YELLOW}, t2w={'color_name': BOLD}).move_to(self.sql_query.get_center())
    self.play(Transform(self.sql_query, sql_query3))
    rect1 = SurroundingRectangle(self.colors_table.get_columns()[1], color=YELLOW)
    self.colors_table.add(rect1)
    self.play(Create(rect1))
    self.wait(0.5)        
    rect2 = SurroundingRectangle(self.joined_table.get_columns()[1], color=YELLOW)
    self.joined_table.add(rect2)
    self.play(Create(rect2))
    self.wait(0.5)
    self.colors_table.remove(rect1)
    self.joined_table.remove(rect2)
    self.play(Uncreate(rect1), Uncreate(rect2))
    
    sql_query4 = Text(select_query, font_size=font_size, t2c={"first_name": YELLOW}, t2w={'first_name': BOLD}).move_to(self.sql_query.get_center())
    self.play(Transform(self.sql_query, sql_query4))
    rect1 = SurroundingRectangle(self.person_table.get_columns()[1], color=YELLOW)
    self.person_table.add(rect1)
    self.play(Create(rect1))
    self.wait(0.5)        
    rect2 = SurroundingRectangle(self.joined_table.get_columns()[2], color=YELLOW)
    self.joined_table.add(rect2)
    self.play(Create(rect2))
    self.wait(0.5)
    self.person_table.remove(rect1)
    self.joined_table.remove(rect2)
    self.play(Uncreate(rect1), Uncreate(rect2))

class InnerJoin(Scene):
    def construct(self):
        # Visual representation of the inner join operation
        # Show the SQL query at the top of the screen
        self.sql_query = Text(select_query, font_size=font_size)
        sql_query_from = Text("FROM favorite_color INNER JOIN person ON favorite_color.person_id = person.person_id", font_size=font_size, t2c={"INNER JOIN": YELLOW}, t2w={'INNER JOIN': BOLD})
        query_group = VGroup(self.sql_query, sql_query_from).arrange(DOWN, aligned_edge=LEFT).to_edge(UP)
        self.play(Write(query_group))

        create_data_tables(self)

        ##########################################################################################
        # Animate the inner join
        ##########################################################################################
        joined_data = self.perform_inner_join(self.colors_table, colors_data, self.person_table, person_data)

        self.joined_table = Table(joined_data, include_outer_lines=True).scale(0.4).to_edge(DOWN)
        joined_label = Text("Result").next_to(self.joined_table, UP)
        self.play(Write(joined_label), Create(self.joined_table))
        self.wait(2)
        highlight_select_columns(self)
        
    
    def perform_inner_join(self, left_table, left_data, right_table, right_data):
        # todo: refactor to allow specifying the columns
        joined_data = [["person_id", "color_name", "first_name"]]
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
                # right_row_num += 1
            elif left_row[0] < right_row[0]:
                left_table.add_highlighted_cell((left_row_num+2, 1), color=RED)
                self.wait(wait_time)
                left_row_num += 1
            elif left_row[0] > right_row[0]:
                right_table.add_highlighted_cell((right_row_num+2, 1), color=RED)
                self.wait(wait_time)
                right_row_num += 1
        
        return joined_data
    

class LeftJoin(Scene):
    def construct(self):
        # Visual representation of the inner join operation
        # Show the SQL query at the top of the screen
        query = "SELECT favorite_color.person_id, favorite_color.color_name, person.first_name"
        font_size = 24
        self.sql_query = Text(query, font_size=font_size)
        sql_query_from = Text("FROM favorite_color LEFT JOIN person ON favorite_color.person_id = person.person_id", font_size=font_size, t2c={"LEFT JOIN": YELLOW}, t2w={'LEFT JOIN': BOLD})
        query_group = VGroup(self.sql_query, sql_query_from).arrange(DOWN, aligned_edge=LEFT).to_edge(UP)
        self.play(Write(query_group))

        create_data_tables(self)

        ##########################################################################################
        # Animate the left join
        ##########################################################################################
        joined_data = self.perform_left_join(self.colors_table, colors_data, self.person_table, person_data)

        self.joined_table = Table(joined_data, include_outer_lines=True).scale(0.4).to_edge(DOWN)
        joined_label = Text("Result").next_to(self.joined_table, UP)
        self.play(Write(joined_label), Create(self.joined_table))
        self.wait(2)
        highlight_select_columns(self)
    

    def perform_left_join(self, left_table, left_data, right_table, right_data):
        # todo: refactor to allow specifying the columns
        joined_data = [["person_id", "color_name", "first_name"]]
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
                # left_table.add_highlighted_cell((left_row_num+2, 1), color=RED)
                # self.wait(wait_time)
                self.play(Indicate(left_table.get_cell((left_row_num+2, 1))))
                left_table.add_highlighted_cell((left_row_num+2, 1), color=GREEN)
                new_row = [right_row[0], left_row[1], "null"]
                joined_data.append(new_row)
                left_row_num += 1
                continue
                
            left_row = left_data[left_row_num]
            right_row = right_data[right_row_num]

            # TODO: make this index configurable
            if left_row[0] == right_row[0]:
                # successful left join!
                self.play(Indicate(left_table.get_cell((left_row_num+2, 1))))
                left_table.add_highlighted_cell((left_row_num+2, 1), color=GREEN)
                self.play(Indicate(right_table.get_cell((right_row_num+2, 1))))
                right_table.add_highlighted_cell((right_row_num+2, 1), color=GREEN)
                self.wait(wait_time)
                # TODO: make this configurable
                new_row = [right_row[0], left_row[1], right_row[1]]
                joined_data.append(new_row)
                left_row_num += 1
            elif left_row[0] < right_row[0]:
                # left_table.add_highlighted_cell((left_row_num+2, 1), color=RED)
                # self.wait(wait_time)
                self.play(Indicate(left_table.get_cell((left_row_num+2, 1))))
                left_table.add_highlighted_cell((left_row_num+2, 1), color=GREEN)
                new_row = [right_row[0], left_row[1], "null"]
                joined_data.append(new_row)
                left_row_num += 1
            elif left_row[0] > right_row[0]:
                right_table.add_highlighted_cell((right_row_num+2, 1), color=RED)
                self.wait(wait_time)
                right_row_num += 1
        
        return joined_data