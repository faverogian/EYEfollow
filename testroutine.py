'''
EYEfollow 1.0
Ball Class 
Gian Favero and Steven Caro
2022
'''

import tkinter as tk
from enum import Enum, auto
from math import pi, sin, cos
from time import time, time_ns

# TODO: Hide mouse

# Constants to control behaviour of the tests
routine_duration    = 15      # s
frequency           = 0.4     # Hz
draw_refresh_rate   = 10      # ms
countdown_duration  = 3       # s
state_machine_cycle = 100     # ms

class Routine_State(Enum):
    '''
    Enum class for state of Ball object
    '''
    countdown   = auto()
    update_test = auto()
    drawing     = auto()
    idle        = auto()

class Test_Routine:
    '''
    Class that handles all eye-test routine related activity
    ''' 
    def __init__(self, master, canvas):
        self.master = master
        self.canvas: tk.Canvas = canvas

        # Initialize the ball (oval) shape
        self.ball_radius = 50
        self.ball = self.canvas.create_oval(0, 0, self.ball_radius, self.ball_radius, fill="white")
        self.canvas.itemconfig(self.ball, state='hidden')

        # Initialize the countdown text items
        self.count = countdown_duration
        self.countdown_text = self.canvas.create_text(self.master.width/2, self.master.height/2, text=self.count, 
                                                      font=("Arial", 50, "bold"), fill="white")
        self.canvas.itemconfig(self.countdown_text, state='hidden')

        # Initialize the state machine variables
        self.state = Routine_State.idle
        self.current_test = None
        self.start_countdown = 0
        self.start_drawing = 0
        self.drawing_finished = 0

        # Call 'main loop' of the class
        self.move_ball()
    
    def move_ball(self):
        '''
        Main loop for the class. Handles and transitions main state machine
        '''
        if self.state == Routine_State.update_test:
            self.current_test = next(self.test_names, "Done")
            if self.current_test == "Done":
                self.master.routine_finished()
                self.cancel()
            else:
                self.time_ref = time()
                self.start_countdown = 1
                self.state = Routine_State.countdown

        elif self.state == Routine_State.countdown:
            if self.start_countdown:
                self.update_countdown()
            else:
                self.start_drawing = 1
                self.state = Routine_State.drawing

        elif self.state == Routine_State.drawing:
            if self.start_drawing:
                self.start_drawing = 0
                self.time_ref = time()
                self.canvas.itemconfig(self.ball, state='normal')
                self.draw()
            elif not self.start_drawing and self.drawing_finished:
                self.drawing_finished = 0
                self.state = Routine_State.update_test

        elif self.state == Routine_State.idle:
            pass

        self.move_ball_ref = self.canvas.after(state_machine_cycle, self.move_ball)
        
    def draw(self):
        '''
        Draws/moves the ball (oval) on the screen
        '''
        t = time_ns()/1e9 - self.time_ref
        x, y = self.get_coords(self.current_test, t)
        self.canvas.moveto(self.ball, x, y)

        if t < routine_duration:
            self.draw_ref = self.canvas.after(draw_refresh_rate, self.draw)
        else:
            self.drawing_finished = 1
            self.canvas.moveto(self.ball, 0, 0)
            self.canvas.itemconfig(self.ball, state='hidden')

    def update_countdown(self):
        '''
        A function called to provide a countdown on the screen (prior to a test)
        '''
        self.canvas.itemconfig(self.countdown_text, text=self.count,state='normal')
        
        if time() - self.time_ref >= 1:  
            self.count -= 1
            self.time_ref = time()

        if self.count <= -1:
            self.start_countdown = 0
            self.canvas.itemconfig(self.countdown_text,state='hidden')
            self.count = countdown_duration
        
    def get_coords(self, test, t):
        '''
        Prescribes the coordinates of where the ball (oval) should be drawn according to test as a function of time
        test: test_name
        t: time
        '''
        if test == "Vertical_Saccade":
            f = self.vertical_saccade()
        elif test == "Horizontal_Saccade":
            f = self.horizontal_saccade()
        elif test == "Smooth_Vertical":
            f = self.smooth_vertical()
        elif test == "Smooth_Horizontal":
            f = self.smooth_horizontal()
        elif test == "Smooth_Circle":
            f = self.smooth_circle()

        x = self.master.width / 2 + self.master.height*(f(t)[0]/2) - self.ball_radius / 2
        y = self.master.height*(1/2 + f(t)[1]/2) - self.ball_radius / 2
        
        return x, y 

    def vertical_saccade(self):
        return lambda t: (0, (int(frequency * t * 2) % 2 == 0) * 1.5 - 0.75)

    def horizontal_saccade(self):
        return lambda t: ((int(frequency * t * 2) % 2 == 0) * 1.5 - 0.75, 0)

    def smooth_vertical(self):
        return lambda t: (0, 0.75 * cos(2 * pi * frequency * t))

    def smooth_horizontal(self):
        return lambda t: (0.75 * cos(2 * pi * frequency * t), 0)

    def smooth_circle(self):
        return lambda t: (0.75 * sin(2 * pi * frequency * t), 0.75 * cos(2 * pi * frequency * t))

    def cancel(self):
        '''
        Cancel all test routines being run and reset variables
        '''
        try:
            self.draw_ref = self.canvas.after_cancel(self.draw_ref)
        except:
            pass

        self.canvas.itemconfig(self.ball, state='hidden')
        self.canvas.itemconfig(self.countdown_text, state='hidden')

        self.state = Routine_State.idle
        self.current_test = None
        self.count = countdown_duration
        self.start_countdown = 0
        self.start_drawing = 0
        self.drawing_finished = 0
    
