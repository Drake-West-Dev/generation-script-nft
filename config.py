# This file MUST be configured in order for the code to run properly

# Make sure you put all your input images into an 'assets' folder.
# Each layer (or category) of images must be put in a folder of its own.

# CONFIG is an array of objects where each object represents a layer
# THESE LAYERS MUST BE ORDERED.

# Each layer needs to specify the following
# 1. id: A number representing a particular layer
# 2. name: The name of the layer. Does not necessarily have to be the same as the directory name containing the layer images.
# 3. directory: The folder inside assets that contain traits for the particular layer
# 4. required: If the particular layer is required (True) or optional (False). The first layer must always be set to true.
# 5. rarity_weights: Denotes the rarity distribution of traits. It can take on three types of values.
#       - None: This makes all the traits defined in the layer equally rare (or common)
#       - "random": Assigns rarity weights at random.
#       - array: An array of numbers where each number represents a weight.
#                If required is True, this array must be equal to the number of images in the layer directory. The first number is  the weight of the first image (in alphabetical order) and so on...
#                If required is False, this array must be equal to one plus the number of images in the layer directory. The first number is the weight of having no image at all for this layer. The second number is the weight of the first image and so on...

# Be sure to check out the tutorial in the README for more details.

realmWeights = [
    0.0125,
    0.0125,
    0.0125,
    0.0125,
    0.0125,
    0.0125,
    0.0125,
    0.0125,
    0.025,
    0.025,
    0.025,
    0.025,
    0.025,
    0.025,
    0.025,
    0.025,
    0.00625,
    0.00625,
    0.00625,
    0.00625,
    0.00625,
    0.00625,
    0.00625,
    0.00625,
    0.0222222222222222,
    0.0222222222222222,
    0.0222222222222222,
    0.0222222222222222,
    0.0222222222222222,
    0.0222222222222222,
    0.0222222222222222,
    0.0222222222222222,
    0.0222222222222222,
    0.0277777777777778,
    0.0277777777777778,
    0.0277777777777778,
    0.0277777777777778,
    0.0277777777777778,
    0.0277777777777778,
    0.0277777777777778,
    0.0277777777777778,
    0.0277777777777778,
    0.0125,
    0.0125,
    0.0125,
    0.0125,
    0.0125,
    0.0125,
    0.0125,
    0.0125,
    0.00625,
    0.00625,
    0.00625,
    0.00625,
    0.00625,
    0.00625,
    0.00625,
    0.00625,
    0.0125,
    0.0125,
    0.0125,
    0.0125,
]

deityWeights = [
    0.0072,  # black glitch reverse
    0.0048,  # black glitch
    0.0032,  # black reverse
    0.0048,  # black
    0.15,  # bronze
    0.0036,
    0.0024,
    0.004,
    0.072,
    0.048,
    0.032,
    0.048,
    0.0648,
    0.0432,
    0.0288,
    0.0432,
    0.0072,
    0.0048,
    0.0032,
    0.0048,
    0.03,
    0.03,
    0.03,
    0.03,
    0.11,
    0.0684,
    0.0456,
    0.0304,
    0.0456,
]

CONFIG = [
    {
        "id": 1,
        "name": "REALM",
        "directory": "REALM",
        "required": True,
        "rarity_weights": realmWeights,
    },
    {
        "id": 2,
        "name": "DEITY",
        "directory": "DEITY",
        "required": True,
        "rarity_weights": None,
    },
]
