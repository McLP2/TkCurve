# TkCurve
A curve widget editor for tkinter, can be used in complex programs for better controls.

![image](https://github.com/Akascape/TkCurve/assets/89206401/b4cd7314-b899-4244-b4ee-1ff25355ba7c)

## Usage
```python
import tkinter as tk
from tkcurve import CurveWidget

root = tk.Tk()
root.config(bg="black")

values = [(300,0), (150,150), (0,300)]
curve_widget = CurveWidget(root, values, line_color="purple",
                           point_color="white", outline="black")
curve_widget.pack(side="left", padx=10, pady=10)

values2 = [(300,0), (150,150), (0,300)]
curve_widget2 = CurveWidget(root, values2)
curve_widget2.pack(side="left", padx=10, pady=10)

values3 = [(300,0), (200,200), (75, 75), (0,300)]
curve_widget3 = CurveWidget(root, values3, line_color="green")
curve_widget3.pack(side="left", padx=10, pady=10)

root.mainloop()
```

## Parameters
| Parameters | Details |
|--------|----------|
| master	| parent widget |
| width | width of the canvas |
| height | height of the canvas |
| points | the values of the points, example: [(x,y), (x,y)] |
| point_color | color of the points |
| point_size | radius of the points |
| line_color | color of the curve line |
| line_width | width of the line |
| bg | background color |
| smooth | enable/disable bezier curve |
| grid_color | color of the grid lines |

## Methods
- `.add_point((x,y))`: add a new point in the canvas
- `.delete_point((x,y))`: delete a point from canvas
- `.config`: change all the parameters
- `.cget`: get any parameter
- `.get()`: get the current points
  
Follow me for more stuff like this: [`Akascape`](https://github.com/Akascape/)
