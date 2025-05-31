# SQL Visualizations

Visualizations for SQL `INNER JOIN` and `LEFT JOIN`.

## Generating the Videos

```
# create videos (pql for low quality, pqh for high quality)
uv run manim -pql sqlviz/main.py InnerJoin
uv run manim -pql sqlviz/main.py LeftJoin

fswatch -o sqlviz/main.py | xargs -n1 -I{} uv run manim -pql sqlviz/main.py SqlTable
```