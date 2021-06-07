import numpy as np

def derivative(function,point,delta):
    return (function(point+delta)-function(point-delta))/(2*delta)

