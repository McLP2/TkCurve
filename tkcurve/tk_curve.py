import tkinter as tk

class CurveWidget(tk.Canvas):
    """
    Curve line widget for tkinter
    Author: Akascape
    """
    def __init__(self,
                 parent,
                 points=[],
                 width=300,
                 height=300,
                 point_color="black",
                 point_size=8,
                 line_width=5,
                 line_color="orange",
                 outline="white",
                 grid_color="grey20",
                 bg="grey12",
                 smooth=True,
                 function=True,
                 allow_swapping=True,
                 **kwargs):

        super().__init__(parent, width=width, height=height, bg=bg, borderwidth=0, highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self.line_color = line_color
        self.point_size = point_size
        self.line_width = line_width
        self.point_color = point_color
        self.outline_color = outline
        self.grid_color = grid_color
        self.smooth = smooth
        self.function = function
        
        self.allow_swapping = allow_swapping
        self.points = points
        self.point_ids = []
        self.create_grid()
        self.create_curve()
        self.bind_events()

        self.sort_points_if_required()

    def create_grid(self):
        for i in range(0, self.winfo_screenwidth(), 30):
            self.create_line([(i, 0), (i, self.winfo_screenheight())], tag='grid_line', fill=self.grid_color)
        for i in range(0, self.winfo_screenheight(), 30):
            self.create_line([(0, i), (self.winfo_screenwidth(), i)], tag='grid_line', fill=self.grid_color)

    def create_curve(self):
        if self.points==[]:
            self.points.append((0,0))
       
        if len(self.points)==1:
            self.points.append(self.points[0])
        
        self.create_line(self.points, tag='curve', fill=self.line_color, smooth=self.smooth, width=self.line_width,
                         capstyle=tk.ROUND, joinstyle=tk.BEVEL)

        for point in self.points:
            point_id = self.create_oval(point[0]-self.point_size, point[1]-self.point_size,
                                        point[0]+self.point_size, point[1]+self.point_size,
                                        fill=self.point_color, outline=self.outline_color, tags='point')
            self.point_ids.append(point_id)
            
    def bind_events(self):
        for point_id in self.point_ids:
            self.tag_bind(point_id, '<ButtonPress-1>', self.on_point_press)
            self.tag_bind(point_id, '<ButtonRelease-1>', self.on_point_release)
            self.tag_bind(point_id, '<B1-Motion>', self.on_point_move)

    def on_point_press(self, event):
        self.drag_data = {'x': event.x, 'y': event.y}

    def on_point_release(self, event):
        self.drag_data = {}
        current_id = self.find_withtag('current')[0]
        index = self.point_ids.index(current_id)

    def constrain_to_bounds(self, index, new_pos):
        dx = 0
        dy = 0
        top_boundary = self.winfo_height()
        right_boundary = self.winfo_width()
        bottom_boundary = 0
        left_boundary = 0
        if self.function and not self.allow_swapping:
            if index > 0:
                left_boundary = self.points[index - 1][0] + 1
            if index < len(self.points) - 1:
                right_boundary = self.points[index + 1][0] - 1
        if new_pos[1] > top_boundary:
            dy = top_boundary - new_pos[1]
        if new_pos[0] > right_boundary:
            dx = right_boundary - new_pos[0]
        if new_pos[1] < bottom_boundary:
            dy = bottom_boundary - new_pos[1]
        if new_pos[0] < left_boundary:
            dx = left_boundary - new_pos[0]
        return dx, dy

    def on_point_move(self, event):
        dx = event.x - self.drag_data['x']
        dy = event.y - self.drag_data['y']
        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y
        current_id = self.find_withtag('current')[0]
        self.move(current_id, dx, dy)
        index = self.point_ids.index(current_id)
        new_pos = (self.points[index][0] + dx, self.points[index][1] + dy)
        constrain_dx, constrain_dy = self.constrain_to_bounds(index, new_pos)
        self.move(current_id, constrain_dx, constrain_dy)
        self.points[index] = (new_pos[0] + constrain_dx, new_pos[1] + constrain_dy)
        self.sort_points_if_required()
        self.update_curve()

    def update_curve(self):
        if len(self.points) == 1:
            self.coords('curve', self.points[0][0], self.points[0][1],
                        self.points[0][0], self.points[0][1])
        else:
            self.coords('curve', sum(self.points, ()))

    def fix(self, point):
        if point in self.points:
            index = self.points.index(point)
            point_id = self.point_ids[index]
            self.tag_unbind(point_id, '<ButtonPress-1>')
            self.tag_unbind(point_id, '<ButtonRelease-1>')
            self.tag_unbind(point_id, '<B1-Motion>')

    def get(self):
        return self.points
    
    def add_point(self, point):
        if point in self.points:
            return
        self.points.append(point)
        self.sort_points_if_required()
        point_id = self.create_oval(point[0]-self.point_size, point[1]-self.point_size,
                                        point[0]+self.point_size, point[1]+self.point_size,
                                        fill=self.point_color, outline=self.outline_color, tags='point')
        self.point_ids.append(point_id)
        self.tag_bind(point_id, '<ButtonPress-1>', self.on_point_press)
        self.tag_bind(point_id, '<ButtonRelease-1>', self.on_point_release)
        self.tag_bind(point_id, '<B1-Motion>', self.on_point_move)
        self.update_curve()
        
    def delete_point(self, point):
        if point not in self.points:
            return
    
        point_id = self.point_ids[self.points.index(point)]
        self.points.remove(point)
        self.delete(point_id)
        if len(self.points)<=0:
            return
        self.update_curve()
       
    def config(self, **kwargs):
        if "point_color" in kwargs:
            self.point_color = kwargs.pop("point_color")
        if "outline" in kwargs:
            self.outline_color = kwargs.pop("outline")
        if "line_color" in kwargs:
            self.line_color = kwargs.pop("line_color")
        if "grid_color" in kwargs:
            self.grid_color = kwargs.pop("grid_color")
            self.itemconfig('grid_line', fill=self.grid_color)
        if "smooth" in kwargs:
            self.smooth = kwargs.pop("smooth")
        if "point_size" in kwargs:
            self.point_size = kwargs.pop("point_size")
        if "line_width" in kwargs:
            self.line_width = kwargs.pop("line_width")
        if "points" in kwargs:
            self.points = kwargs.pop("points")
            self.sort_points_if_required()
            for i in self.point_ids:
                self.delete(i)
            self.point_ids = []
            
            for point in self.points:
                point_id = self.create_oval(point[0]-self.point_size, point[1]-self.point_size,
                                        point[0]+self.point_size, point[1]+self.point_size,
                                        fill=self.point_color, outline=self.outline_color, tags='point')
                self.point_ids.append(point_id)
            self.bind_events()
            
        for point_id in self.point_ids:
            self.itemconfig(point_id, fill=self.point_color, outline=self.outline_color)
            point = self.points[self.point_ids.index(point_id)]
            self.coords(point_id, point[0]-self.point_size, point[1]-self.point_size,
                        point[0]+self.point_size, point[1]+self.point_size)
            
        self.itemconfig('curve', fill=self.line_color, smooth=self.smooth, width=self.line_width)
        self.update_curve()
        
        super().config(**kwargs)

    def cget(self, param):
        if param=="point_color":
            return self.point_color
        if param=="outline":
            return self.outline_color
        if param=="line_color":
            return self.line_color
        if param=="grid_color":
            return self.grid_color
        if param=="smooth":
            return self.smooth
        if param=="point_size":
            return self.point_size
        if param=="line_width":
            return self.line_width
        if param=="points":
            return self.points
        return super().cget(param)

    def sort_points_if_required(self):
        if self.function:
            self.points, self.point_ids = map(list, zip(*sorted(zip(self.points, self.point_ids),
                                                                key=lambda point: point[0][0])))

