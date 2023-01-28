import os
import argparse
from module import counting
from module import denoise

# Argument
parser = argparse.ArgumentParser()

parser.add_argument('-i',
                    '--images',
                    help='Path to images folder',
                    required=True)

parser.add_argument('-o',
                    '--output',
                    help='Path to output folder',
                    required=True)

parser.add_argument('-s',
                    '--opening_sign',
                    default=1,
                    help='opening sign to choose kernel')

args = parser.parse_args()

# Extract command line arguments
path_in = args.images
path_out = args.output
opening_sign = args.opening_sign

# Extract image name
name_list = path_in.split("/")
name_png = name_list[-1]

# Denoise
denoise_operation = denoise.Denoise(path_in)
denoise_operation.denoise()

# Counting operation
path_in_counting = 'denoise' + "/" + name_png
counting_operation = counting.Counting(path_in_counting, path_out, opening_sign)
counting_operation.counting_object()



