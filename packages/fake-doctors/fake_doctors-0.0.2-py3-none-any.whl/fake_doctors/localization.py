import numpy as np
import skimage


def non_maximal_suppression(heatmap_path_in: str, coords_path_out: str,
                            wsi_level: int = 6, radius: int = 12, 
                            threshold: float = 0.5, sigma: float = 0.) -> None:

    '''Perform localization using non-maximal suppression.

    - Args
        heatmap_path_in: Path to the heatmap(.npy) file
        coord_path_out: Path to the coordinates list file
        wsi_level: Level of wsi
        radius: 

    - Returns
        None
    '''

    heatmap = np.load(heatmap_path_in)
    heatmap_width, heatmap_height = heatmap.shape
    resolution = 2 ** wsi_level

    if sigma > 0:
        heatmap = skimage.filters.gaussian(heatmap, sigma=sigma)

    with open(coords_path_out, 'w') as f:
        while np.max(heatmap) > threshold:
            max_prob = heatmap.max()
            max_prob_coords = np.where(heatmap == max_prob)

            mask_x_coord, mask_y_coord = max_prob_coords[0][0], max_prob_coords[1][0] # Use the first coordinate only
            # Scale coordinates because the level of wsi and heatmap can be different
            wsi_x_coord = mask_x_coord * resolution
            wsi_y_coord = mask_y_coord * resolution

            f.write(f'{max_prob}, {wsi_x_coord}, {wsi_y_coord}\n')

            start_x = mask_x_coord - radius if (mask_x_coord - radius) > 0 else 0
            end_x = mask_x_coord + radius if (mask_x_coord + radius) <= heatmap_width else heatmap_width
            start_y = mask_y_coord - radius if (mask_y_coord - radius) > 0 else 0
            end_y = mask_y_coord + radius if (mask_y_coord + radius) <= heatmap_height else heatmap_height

            for x in range(start_x, end_x):
                for y in range(start_y, end_y):
                    heatmap[x, y] = 0