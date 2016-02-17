""" 
Serena Chen
"""

import random,math
from PIL import Image


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    if max_depth<0 or (min_depth<0 and random.random()<.5):
        return ['x'] if random.random()<.5 else ['y']
    #single input
    if random.random()<.5:
        return [random.choice(['cos_pi','sin_pi']),build_random_function(min_depth-1,max_depth-1)]
    #two inputs
    else:
        return [random.choice(['prod','avg','para','mem']),build_random_function(min_depth-1,max_depth-1),build_random_function(min_depth-1,max_depth-1)]

def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    if f[0]=='x':
        return x
    if f[0]=='y':
        return y
    if f[0]=='cos_pi':
        return math.cos(math.pi*evaluate_random_function(f[1],x,y))
    if f[0]=='sin_pi':
        return math.sin(math.pi*evaluate_random_function(f[1],x,y))
    if f[0]=='prod':
        return evaluate_random_function(f[1],x,y)*evaluate_random_function(f[2],x,y)
    if f[0]=='avg':
        return (evaluate_random_function(f[1],x,y)+evaluate_random_function(f[2],x,y))/2.0
    #evaluates a parabola
    if f[0]=='para':
        res = (evaluate_random_function(f[1],x,y)**2-evaluate_random_function(f[2],x,y))
        return res%math.copysign(1,res)#mod 1 or -1 for error correction

    #takes the last few digits of the memory address of the string representation of wither x or y
    #if we don't have random x or y, we get bars accross the screen
    if f[0]=='mem':
        numx = evaluate_random_function(f[1],x,y)
        numy = evaluate_random_function(f[2],x,y)
        return math.copysign((1000.0/(id(str(numx))%10000))%1,numx) if random.random()<.5 else math.copysign((1000.0/(id(str(numy))%10000))%1,numy)#mod for error correction
    raise ValueError('This function is invalid')


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    if val>input_interval_end or val <input_interval_start:
        raise ValueError('The value is not between the specified interval')
    val+=(0-input_interval_start)
    val*=((output_interval_end-output_interval_start)/float(input_interval_end-input_interval_start))
    val+=output_interval_start
    return val


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)

def build_random_function_lambda(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)
        
        Uses anonymous functions. It's so slow. And the syntax is weird and the
        internet is not the most helpful for nesting lambdas

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    if max_depth<0 or (min_depth<0 and random.random()<.5):
        if random.random()<.5:
            return lambda x,y:x 
        else: 
            return lambda x,y:y

    func1 = build_random_function_lambda(min_depth-1,max_depth-1)
    func2 = build_random_function_lambda(min_depth-1,max_depth-1)

    cos_pi = lambda x,y:math.cos(x*math.pi)
    sin_pi = lambda x,y:math.sin(x*math.pi)
    prod = lambda x,y:x*y
    avg = lambda x,y:(x+y)/2.0
    func = random.choice([cos_pi,sin_pi,prod,avg])

    res = lambda x,y:func(func1(x,y),func2(x,y))
    return res


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens
    # commented lines for lambda function testing 
    # red_function = build_random_function_lambda(5,7)
    # green_function = build_random_function_lambda(5,7)
    # blue_function = build_random_function_lambda(5,7)
    red_function = build_random_function(5,7)
    green_function = build_random_function(5,7)
    blue_function = build_random_function(5,7)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    # color_map(red_function(x, y)),
                    # color_map(green_function(x, y)),
                    # color_map(blue_function(x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart.png",500,500)
    generate_art("myart1.png",500,500)
    generate_art("myart2.png",500,500)
    generate_art("myart3.png",500,500)

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    # test_image("noise.png")
