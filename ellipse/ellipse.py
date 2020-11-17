#Widget use copied from https://kapernikov.com/ipywidgets-with-matplotlib/
    
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
import datetime

def make_box_layout():
    """define how the widget box looks"""
    return widgets.Layout(
        border='solid 1px black',
        margin='0px 10px 10px 0px',
        padding='5px 5px 5px 5px'
     )
 

class Ellipse(widgets.HBox):
    """
    Interactively display ellipse and its foci, defined by
        a -- semimajor axis
        b -- semiminor axis
        r -- rotation angle in degrees (stored as radians)
        x -- ellipse center in x
        y -- ellipse center in y
    
    Plot the ellipse and the location of the foci, an display the value of
    the eccentricity = sqrt(1 - (b/a)^2)
    
    Constrain input values so a >= b
    """ 
 
    def __init__(self):
        super().__init__()
        plt.close()
        output = widgets.Output()
 
        self.thetas = np.linspace(0, 2 * np.pi, num = 100000, endpoint=True)
        initial_color = '#AA0202'
        self.plotSize = 50
        with output:
            figTitle = "Interactive Ellipse"
            self.fig, self.ax = plt.subplots(
                constrained_layout=True, figsize=(5, 3.5), num=figTitle)
            self.ax.set_xlim(-self.plotSize,self.plotSize)
            self.ax.set_ylim(-self.plotSize,self.plotSize)
            self.ax.set_aspect('equal')
            self.xlabel = self.ax.set_xlabel("???")
            self.title = self.ax.set_title("????")
        self.a = 20
        self.b = 10
        self.radians = np.radians(0)
        self.x = 0
        self.y = 0
        
        self._defineWidgets()

        self.updateXY()
        self.line, = self.ax.plot(self.xs, self.ys, initial_color)
        self.foci,  = self.ax.plot(self.fxs, self.fys, "b+")
        self.fig.canvas.toolbar_position = 'bottom'
        self.ax.grid(True)
        self.updatePlot()
 
 
        controls = widgets.VBox([
            self.t_text,
            self.a_slider, 
            self.b_slider, 
            self.r_slider,
            self.x_slider,
            self.y_slider,
            self.e_text,
        ])
        controls.layout = make_box_layout()
         
        out_box = widgets.Box([output])
        output.layout = make_box_layout()
 
        # observe the slider values
        self.a_slider.observe(self.update_a, 'value')
        self.b_slider.observe(self.update_b, 'value')
        self.r_slider.observe(self.update_r, 'value')
        self.x_slider.observe(self.update_x, 'value')
        self.y_slider.observe(self.update_y, 'value')
               
        # add to children
        self.children = [controls, output]
        
    def _defineWidgets(self):
        """ convenient way to make all the widgets we need"""
        # define widgets
        
        self.instructions = [
            'Welcome to Interactive Ellipse.',
            'The ellipse is defined by 5 numbers.  Adjust values with sliders.',
            'Click on a slider, drag it to the new value, and release it.',
            'If you highlight a slider, the up, down, left, and right arrows',
            'make small changes to the values.'
            'Note that <b>a</b> must always be greater than or equal to <b>b</b>.',
            'The value of the ellipticity (<b>b/a</b>) is shown each time.'
            ' ',
            'Below the plot there are some controls to adjust the view.',
            'The first one (three horizontal lines) toggles them on and off.',
            'The next one returns you home to the full view if you get lost.',
            'The left and right arrows change you between views defined by',
            'the next two buttons:  pan and zoom.',
            'The final button is to save a snapshot of the ellipse.'
        ]
        iValue = ''
        for i,instruction in enumerate(self.instructions):
            if i == 0:
                iValue = instruction
            else:
                iValue += "<br>"+instruction
        
        self.t_text = widgets.HTML(value=iValue, description='')
        #self.t_text = widgets.Textarea(value=iValue, description='')
 
        #text = widgets.Textarea(value=iValue, description='',layout={'height': '100%'})
        #self.t_text = widgets.VBox([text], layout={'height': '500px'})
        
        self.a_slider = widgets.FloatSlider(
            value=self.a,
            min=0.1,
            max=30.01,
            step=0.001,
            description='a (semi-major axis):',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='.3f',
            style = {'description_width': 'initial'}
        )
        self.b_slider = widgets.FloatSlider(
            value=self.b,
            min=0.1,
            max=30.01,
            step=0.001,
            description='b (semi-minor axis):',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='.3f',
            style = {'description_width': 'initial'}
        )
        self.r_slider = widgets.FloatSlider(
            value=self.radians,
            min=0,
            max=180.0,
            step=0.1,
            description='rotation (degrees):',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='.1f',
            style = {'description_width': 'initial'}
        )
 
        self.x_slider = widgets.FloatSlider(
            value=self.x,
            min=-self.plotSize,
            max=self.plotSize,
            step=0.1,
            description='x center:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='.1f',
            style = {'description_width': 'initial'}
        )
 
        self.y_slider = widgets.FloatSlider(
            value=self.x,
            min=-self.plotSize,
            max=self.plotSize,
            step=0.1,
            description='y center:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='.1f',
            style = {'description_width': 'initial'}
        )
    
        self.e_text = widgets.Text(
            value='?',
            placeholder='',
            description='eccentricity:',
            disabled=True
        )
     
    def update_a(self, change):
        """update the value of a, semi-major axis  Snap the value so it is than or equal to b"""
        if change.new > self.b:
            self.a = change.new
        else:
            self.a = self.b
            self.a_slider.value = self.b
        self.updatePlot()
    def update_b(self, change):
        """update the value of b.  Snap the value so it is less than or equal to a"""
        if change.new < self.a:
            self.b = change.new
        else:
            self.b = self.a
            self.b_slider.value = self.a
        self.updatePlot()
    def update_r(self, change):
        """update the value of r, the rotation in degrees.  Store the value in radians"""
        self.radians = np.radians(change.new)
        self.updatePlot()
    def update_x(self, change):
        """update the value of x, the location of the center in x."""
        self.x = change.new
        self.updatePlot()
    def update_y(self, change):
        """update the value of y, the location of the center in y."""
        self.y = change.new
        self.updatePlot()
    def updatePlot(self): 
        """set plot data for the ellipse and foci"""
        self.updateXY()
        self.line.set_xdata(self.xs)
        self.line.set_ydata(self.ys)
        self.foci.set_xdata(self.fxs)
        self.foci.set_ydata(self.fys)
        self.xlabel.set_text("a=%.3f b=%.3f r=%.1f x=%.1f y=%.1f"%(self.a, self.b, np.degrees(self.radians), self.x, self.y))
        self.title.set_text(datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"))
        self.fig.canvas.draw()
    def updateXY(self):
        """calculte ellipse and foci data based on current values"""
        self.xs = self.a*np.cos(self.thetas)
        self.ys = self.b*np.sin(self.thetas)
        c, s = np.cos(-self.radians), np.sin(-self.radians)
        j = np.array([[c, s], [-s, c]])
        self.xs,self.ys = np.dot(j, [self.xs, self.ys])
        self.xs += self.x
        self.ys += self.y
        c = np.sqrt(self.a**2 - self.b**2)
        self.fxs,self.fys = np.dot(j,[np.array([-c,c]),np.array([0.0,0.0])])
        self.fxs += self.x
        self.fys += self.y
        eccentricity= np.sqrt(1-(self.b/self.a)**2)
        eText = "%.6f"%eccentricity
        self.e_text.value = eText
         
         
