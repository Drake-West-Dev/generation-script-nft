import os
import pandas as pd


def drop_duplicates(edition, count):
    rarity_table = pd.read_csv(
        "./output/edition Deity-full-run-2/metadata.csv", index_col=0
    )
    rarity_table_dicts = rarity_table.to_dict("records")
    rarity_table_no_dups = pd.DataFrame(rarity_table_dicts).drop_duplicates()
    # print(rarity_table_no_dups)

    print("Generated %i images, %i are distinct" % (count, rarity_table.shape[0]))
    # Get list of duplicate images
    img_tb_removed = sorted(list(set(range(count)) - set(rarity_table_no_dups.index)))

    # Remove duplicate images
    print("Removing %i images..." % (len(img_tb_removed)))

    zfill_count = len(str(count - 1))

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

    rarity_table_no_dups.to_csv(
        os.path.join("output", "edition " + str(edition), "metadata_new.csv")
    )


drop_duplicates("Deity-full-run-2", 1250)
