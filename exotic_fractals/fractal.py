def generate_fractal(a, b, initial_color_hue, color_scale=10, 
                     zoom_level=1, center_point = (0,0), max_iter = 250, 
                     job = None, directory = None, image_size = (1920, 1080), 
                     image_save = True, x_max=2.3, aspect_ratio = 16/9, verbose = True,
                     m_style = True, j_style = False):

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
            if j_style:
                nsmooth = math.exp(-abs(z_curr))
            
            while pixel[x,y] == (0,0,0) and l < max_iter:
                # if coloring like we would for a julia set
                if j_style:
                    nsmooth += math.exp(-abs(z_curr))
                
                if abs(z_curr) > 1:
                    if m_style:
                        nsmooth = (l + 1 - math.log10(math.log2(abs(z_curr)))/math.log10(2))/max_iter
                        pixel[x,y] = hsv2rgb(h = nsmooth, s = 0.79, v = 0.59)
                    elif j_style:

                        pixel[x,y] = hsv2rgb(h = initial_color_hue + color_scale * (nsmooth/max_iter), s = 0.79, v = 0.59) 
                    else:
                        pixel[x,y] = (255, 255, 255)
                
                # generation function
                z_curr = z_curr**(1/z_curr) + c
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
    slightly modified from https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a
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
    print('\r{0} |{1}| {2}% {3}'.format(prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

if __name__=="__main__":
    generate_fractal(a = 0, b = 0, initial_color_hue = 0.41, color_scale = 10,
                    zoom_level=1, center_point = (0,0),
                    max_iter = 250, directory = "generated_images",
                    image_size = (int(1920/2), int(1080/2)), image_save = True,
                    x_max=2.3, aspect_ratio = 16/9, verbose = True)