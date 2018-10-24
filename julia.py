def generate_julia(a, b, initial_color_hue, color_scale=10, zoom_level=1, center_point = (0,0),
                   max_iter = 250, job = None, directory = None,
                   image_size = (1920, 1080), image_save = True,
                   x_max=2.3, aspect_ratio = 16/9, verbose = True):

    '''
    Generate a Julia Set using z = z^2 + c, where c is a + ib

        Parameters:
            a: number between -2 and 2
            b: number between -2 and 2
            initial_color_hue: number between 0 and 1. Specifies the initial coloring based on HSV color model. Corresponds with H
            color_scale: how rapidly colors change while rendering the julia set
            zoom_level: any number from 1 to inf. 
            center_point: point at which the image is centered. bounded by ((-2, -2), (2, 2))
            max_iter: number of iterations to run on a pixel
            job: helpful for when generating multiple julia sets. First number that shows up in the image name.
            directory: directory to save image in. Must be relative to current working directory.
            image_size: Image size in pixels (tuple)
            image_save: boolean of whether or not to save the image
            x_max: don't change this number (2.3)
            aspect_ratio: ratio between sides of image
            verbose: whether or not to print information about generation of image
    '''
    
    from PIL import Image
    import math
    from datetime import datetime
    
    start_time = datetime.now()
    
    if image_size[0]/image_size[1] != aspect_ratio:
        print('Warning: resolution does not match aspect ratio. Resolution: ' + str(image_size))
    
    # Find the boundaries of the complex plane in which the fractal will be generated based on the aspect ratio.
    #    calculate image bounds like normal
    if aspect_ratio > 1:
        y_max = x_max / aspect_ratio
    else:
        y_max = x_max * aspect_ratio
    x_min = -x_max
    y_min = -y_max
    
    #    zooming, if desired
    x_max = center_point[0] + x_max * 1/zoom_level
    y_max = center_point[1] + y_max * 1/zoom_level
    x_min = center_point[0] + x_min * 1/zoom_level
    y_min = center_point[1] + y_min * 1/zoom_level
        
    # Initialize a black image, load in the pixels of the image to an array 'pixel'
    image = Image.new('RGB', image_size, 'black')
    pixel = image.load()
    
    # Set the scaling factor - the mandelbrot set is defined between -2 and 2, not the pixel size of the image
    x_size = (x_max - x_min)/image.size[0]
    y_size = (y_max - y_min)/image.size[1]
    
    # HSV to RGB conversion
    def hsv2rgb(h,s,v):
        import colorsys
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

    # For each pixel in the image, iterate z_next = z^2 + c, 
    #   where z is imaginary and c is the complex coordinate value of that specific pixel
    for x in range(image.size[0]):
    
    # Print the progress bar
        if verbose: print_progress_bar(x+1, image.size[0], 'Percentage complete:', 'Finished.')
    
        for y in range(image.size[1]):
            l = 0 # Initialize the while loop counter
            z = complex((x_min + x * x_size), (y_min + y * y_size))
            z_curr = z
            c = complex(a, b)
            nsmooth = math.exp(-abs(z_curr))
            while pixel[x,y] == (0,0,0) and l < max_iter:
                nsmooth += math.exp(-abs(z_curr))
                if abs(z_curr) > 2:
                    # hue, saturation, value/brightness
                    pixel[x,y] = hsv2rgb(h = initial_color_hue + color_scale * (nsmooth/max_iter), s = 0.79, v = 0.59) 
                z_curr = z_curr**2 + c
                l += 1
    
    # calculate total time in minutes
    total_time = (datetime.now() - start_time).total_seconds()/60
    if verbose: print('fractal created in', round(total_time, 3), 'minutes')

    # Name of this image:
    if job != None:
        save_name_list = ['job_' + str(job), '_a_' + str(a) + '_b_' + str(b),
                          '_inithue_scale_' + str(initial_color_hue) + '_' + str(color_scale),
                          '.png']
    else:
        save_name_list = ['a_' + str(a) + '_b_' + str(b),
                          '_inithue_scale_' + str(initial_color_hue) + '_' + str(color_scale),
                          '.png']

    # Save the image
    save_name = ''.join(save_name_list)
    if image_save:
        if directory == None:
            if verbose: print('saved as:', save_name)
            image.save(save_name)
        else:
            if verbose: print('saved as:', save_name, 'in the directory:', directory)
            image.save(directory + '/' + save_name)
    else:
        if verbose: print('Will not save the image.')

def print_progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 25, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

if __name__=="__main__":
    import random as rn
    for i in range(25):
        print(i)
        hue = rn.random()
        scale = rn.random()*10
        generate_julia(-0.834, -0.171, initial_color_hue = hue, color_scale = scale, 
               zoom_level=1, center_point = (0,0),
               max_iter = 250, job = i+1, directory = "testing_hue_scale",
               image_size = (int(1920/2), int(1080/2)), image_save = True,
               x_max=2.3, aspect_ratio = 16/9, verbose = False)
    # generate_julia(a = -0.834, b = -0.171, initial_color_hue = 0.41, color_scale = 20,
    #                zoom_level=1, center_point = (0,0),
    #                max_iter = 250, job = 13, directory = "testing_hue_scale",
    #                image_size = (int(1920/2), int(1080/2)), image_save = True,
    #                x_max=2.3, aspect_ratio = 16/9, verbose = True)