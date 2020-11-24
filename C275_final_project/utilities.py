import time, math

'''
This file contains a Timer class and a euclid distance function.
'''
class Timer():
    '''
    A helper class which allows a function to be periodically executed.

    If the preset time has elapsed since init/'function' was called,
    call function and reset start time.
    '''
    def __init__(self, preset, function):
        '''
        Args:
        preset: desired period of function call
        function: desired function to call
        '''
        self.preset = preset
        self.function = function
        self.start = time.time()

    def update(self, *args):
        # passes args to function call
        if time.time() - self.start > self.preset:
            self.start = time.time()
            self.function(*args)

def euclidD(point1, point2):
    '''
    Computes the euclidean distance between two points and 
    returns this distance.
    '''
    sum = 0
    for index in range(len(point1)):
        diff = (point1[index]-point2[index]) ** 2
        sum = sum + diff

    return math.sqrt(sum)
