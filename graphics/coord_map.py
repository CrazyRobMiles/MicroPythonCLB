class CoordMap:

    def __init__(self, panel_width=8,panel_height=8,x_panels = 3,y_panels = 2):
        self.panel_row_pixels = (panel_width*panel_height)*x_panels
        self.top_left = self.panel_row_pixels*(y_panels-1) + panel_height-1  
        self.panel_height=panel_height
        self.panel_width=panel_width
        self.x_panels=x_panels
        self.y_panels=y_panels
        self.width=panel_width*x_panels
        self.height=panel_height*y_panels
        self.pixels = self.width*self.height

    def get_offset(self,x, y):
        row_no = y//self.panel_height
        p = self.top_left - (row_no*self.panel_row_pixels)
        y = y - (row_no*self.panel_height)
        p=p+(self.panel_width*x)-y
        return p
