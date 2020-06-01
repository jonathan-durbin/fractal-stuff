#! /usr/bin/env python3
# gif.py
"""Function to generate a gif from a numbered list of files in a directory."""


def generate_gif(directory: ("Folder name", "positional"),
                 image_format: ('Image format', 'positional') = '.png',
                 print_file_names=False):
    """Generate a gif from a numbered list of files in a directory."""
    import imageio
    from glob import glob
    from natsort import natsorted

    images = []
    # Create a list of file names in the specified directory
    filenames = glob(directory + '/*' + image_format)

    filenames = natsorted(filenames, key=lambda y: y.lower())
    # Sort the list 'filenames' using the traditional method.
    # Traditional method -
    #   isolate the entire first number in the string, then sort by that number
    # If this step is not included,
    #   files will be sorted like so: 0, 100, 110, 200, 3, 420, etc...

    if print_file_names:  # For troubleshooting
        for i in filenames:
            print(i)

    for filename in filenames:
        images.append(imageio.imread(filename))
    # Append each file to the list that will become the gif

    imageio.mimsave(directory + '.gif', images)
    # Save the gif as the name of the directory
    #   that the images were generated from
    return


if __name__ == "__main__":
    import plac
    plac.call(generate_gif)
