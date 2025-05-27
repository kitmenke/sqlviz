uv run manim -pql sqlviz/main.py SqlTable

fswatch -o sqlviz/main.py | xargs -n1 -I{} uv run manim -pql sqlviz/main.py SqlTable