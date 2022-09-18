#!/usr/bin/env python
# coding: utf-8

# Import required libraries
import pandas as pd
import numpy as np
import time
import os
import random
from progressbar import progressbar
from moviepy.editor import *

import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


# Import configuration file
from config import CONFIG


# Parse the configuration file and make sure it's valid
def parse_config():

    # Input traits must be placed in the assets folder. Change this value if you want to name it something else.
    assets_path = "assets"

    # Loop through all layers defined in CONFIG
    for layer in CONFIG:

        # Go into assets/ to look for layer folders
        layer_path = os.path.join(assets_path, layer["directory"])

        # Get trait array in sorted order
        traits = sorted([trait for trait in os.listdir(layer_path) if trait[0] != "."])

        # If layer is not required, add a None to the start of the traits array
        if not layer["required"]:
            traits = [None] + traits

        # Generate final rarity weights
        if layer["rarity_weights"] is None:
            rarities = [1 for x in traits]
        elif layer["rarity_weights"] == "random":
            rarities = [random.random() for x in traits]
        elif type(layer["rarity_weights"] == "list"):
            assert len(traits) == len(
                layer["rarity_weights"]
            ), "Make sure you have the current number of rarity weights"
            rarities = layer["rarity_weights"]
        else:
            raise ValueError("Rarity weights is invalid")

        rarities = get_weighted_rarities(rarities)

        # Re-assign final values to main CONFIG
        layer["rarity_weights"] = rarities
        layer["cum_rarity_weights"] = np.cumsum(rarities)
        layer["traits"] = traits


# Weight rarities and return a numpy array that sums up to 1
def get_weighted_rarities(arr):
    return np.array(arr) / sum(arr)


# Generate a Deity NFT
def generate_single_deity(filepaths, output_filename=None):

    deity_clip = VideoFileClip(
        os.path.join("assets", filepaths[1]), True, False
    ).set_position("center")
    duration = deity_clip.duration

    if filepaths[0][-3:] == "mp4":
        bg_clip = VideoFileClip(os.path.join("assets", filepaths[0]), True, False)
    else:
        bg_clip = ImageClip(os.path.join("assets", filepaths[0])).set_duration(duration)

    video = CompositeVideoClip([bg_clip, deity_clip])

    # Save the final image into desired location
    if output_filename is not None:
        video.write_videofile(output_filename, codec="libx264", audio=False)
    else:
        # If output filename is not specified, use timestamp to name the image and save it in output/single_images
        if not os.path.exists(os.path.join("output", "single_images")):
            os.makedirs(os.path.join("output", "single_images"))
        video.write_videofile(
            os.path.join("output", "single_images", str(int(time.time())) + ".mp4")
        )


# Generate a single image with all possible traits
# generate_single_deity(["REALM/Mountain_Grid_1.png", "DEITY/Black.mov"])


# Get total number of distinct possible combinations
def get_total_combinations():

    total = 1
    for layer in CONFIG:
        total = total * len(layer["traits"])
    return total


# Select an index based on rarity weights
def select_index(cum_rarities, rand):

    cum_rarities = [0] + list(cum_rarities)
    for i in range(len(cum_rarities) - 1):
        if rand >= cum_rarities[i] and rand <= cum_rarities[i + 1]:
            return i

    # Should not reach here if everything works okay
    return None


# Generate a set of traits given rarities
def generate_trait_set_from_config():

    trait_set = []
    trait_paths = []

    for layer in CONFIG:
        # Extract list of traits and cumulative rarity weights
        traits, cum_rarities = layer["traits"], layer["cum_rarity_weights"]

        # Generate a random number
        rand_num = random.random()

        # Select an element index based on random number and cumulative rarity weights
        idx = select_index(cum_rarities, rand_num)

        # Add selected trait to trait set
        trait_set.append(traits[idx])

        # Add trait path to trait paths if the trait has been selected
        if traits[idx] is not None:
            trait_path = os.path.join(layer["directory"], traits[idx])
            trait_paths.append(trait_path)

    return trait_set, trait_paths


# Generate the image set. Don't change drop_dup
def generate_images(edition, count):

    # Initialize an empty rarity table
    rarity_table = {}
    for layer in CONFIG:
        rarity_table[layer["name"]] = []

    # Define output path to output/edition {edition_num}
    op_path = os.path.join("output", "edition " + str(edition), "images")

    # Will require this to name final images as 000, 001,...
    zfill_count = len(str(count - 1))

    # Create output directory if it doesn't exist
    if not os.path.exists(op_path):
        os.makedirs(op_path)

    # Create the images
    for n in progressbar(range(count)):

        # Set image name
        image_name = str(n).zfill(zfill_count) + ".mp4"

        # Get a random set of valid traits based on rarity weights
        trait_sets, trait_paths = generate_trait_set_from_config()

        # Generate the actual image
        generate_single_deity(trait_paths, os.path.join(op_path, image_name))

        # Populate the rarity table with metadata of newly created image
        for idx, trait in enumerate(trait_sets):
            if trait is not None:
                rarity_table[CONFIG[idx]["name"]].append(trait[: -1 * len(".mp4")])
            else:
                rarity_table[CONFIG[idx]["name"]].append("none")

    # Create the final rarity table by removing duplicate creat
    rarity_table_pd = pd.DataFrame(rarity_table)

    return rarity_table_pd, zfill_count


def drop_duplicates(edition, count, zfill_count, rarity_table_no_dups):
    # Get list of duplicate images
    img_tb_removed = sorted(list(set(range(count)) - set(rarity_table_no_dups.index)))

    # Remove duplicate images
    print("Removing %i images..." % (len(img_tb_removed)))

    op_path = os.path.join("output", "edition " + str(edition), "images")
    for i in img_tb_removed:
        os.remove(os.path.join(op_path, str(i).zfill(zfill_count) + ".mp4"))

    # Rename images such that it is sequentialluy numbered
    for idx, img in enumerate(sorted(os.listdir(op_path))):
        os.rename(
            os.path.join(op_path, img),
            os.path.join(op_path, str(idx).zfill(zfill_count) + ".mp4"),
        )

    # Modify rarity table to reflect removals
    rarity_table_no_dups = rarity_table_no_dups.reset_index()
    rarity_table_no_dups = rarity_table_no_dups.drop("index", axis=1)
    return rarity_table_no_dups


# Main function. Point of entry
def main(num_nfts, nft_name):

    print("Checking assets...")
    parse_config()
    print("Assets look great! We are good to go!")
    print()

    tot_comb = get_total_combinations()
    print("You can create a total of %i distinct avatars" % (tot_comb))
    print()

    while True:
        if num_nfts > 0:
            break

    print("Starting task...")
    rarity_table, zfill_count = generate_images(nft_name, num_nfts)
    print("Saving metadata...")
    rarity_table.to_csv(
        os.path.join("output", "edition " + str(nft_name), "metadata.csv")
    )

    rarity_table_no_dups = rarity_table.drop_duplicates()
    print(
        "Generated %i images, %i are distinct"
        % (num_nfts, rarity_table_no_dups.shape[0])
    )

    drop_duplicates(nft_name, num_nfts, zfill_count, rarity_table_no_dups)
    rarity_table_no_dups.to_csv(
        os.path.join("output", "edition " + str(nft_name), "metadata_no_dups.csv")
    )

    print("Task complete!")


# Run the main function
main(1250, "Deity-final")

# Traceback (most recent call last):
#   File "/Users/nathandrake/code/generation-script-nft/nft.py", line 237, in <module>
#     main(1150, "Deity")
#   File "/Users/nathandrake/code/generation-script-nft/nft.py", line 228, in main
#     rt = generate_images(nft_name, num_nfts)
#   File "/Users/nathandrake/code/generation-script-nft/nft.py", line 196, in generate_images
#     os.remove(os.path.join(op_path, str(i).zfill(zfill_count) + ".mp4"))
# FileNotFoundError: [Errno 2] No such file or directory: 'output/edition Deity/0061.mp4'
# (generation-script-nft)
