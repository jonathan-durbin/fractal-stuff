def generate_gif(directory, print_file_names = False):
    import imageio
    from glob import glob
    from natsort import natsorted
    
    images = []
    filenames = glob(directory + '/*.png') # Create a list of file names in the specified directory
    
    filenames = natsorted(filenames, key=lambda y: y.lower()) 
    # Sort the list 'filenames' using the traditional method.
    # Traditional method - isolate the entire first number in the string, then sort by that number. 
    # If this step is not included, files will be sorted like so: 0, 100, 110, 200, 3, 420, etc...
    
    if print_file_names: # For troubleshooting
        for i in filenames:
            print(i)
    
    for filename in filenames: 
        images.append(imageio.imread(filename)) 
    # Append each file to the list that will become the gif
    
    imageio.mimsave(directory + '.gif', images) 
    # Save the gif as the name of the directory that the images were generated from
    return

if __name__=="__main__":
    import sys
    generate_gif(directory=sys.argv[1])