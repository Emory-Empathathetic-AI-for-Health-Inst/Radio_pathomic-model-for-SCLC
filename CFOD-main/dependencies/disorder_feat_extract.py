import numpy as np
from scipy.special import comb
from dependencies.haralick_no_img_v2 import haralick_no_img_v2
from itertools import combinations

# orient_cooccur_scheme: 1 for weighted (with area) co-occurrence matrix, 2 for unweighted co-occurrence matrix (only count)
def contrast_entropy(orients, areas, orient_num, orient_cooccur_scheme):
    # 19*19 co-occurrence matrix (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18)
    p_orient_occur = np.zeros((orient_num, orient_num))
    # as 0 and 18 are same orientation, so change the orientation of 0 to 18
    # hajoia's way also ignores the 0th bin and 18th bin
    orients[orients == 0] = 18
    for pair1 in range(1, orient_num):  
        for pair2 in range(pair1, orient_num):  
            if np.any(orients == pair1) and np.any(orients == pair2):
                if pair1 != pair2:
                    if orient_cooccur_scheme == 1:
                        p_orient_occur[pair1, pair2] = np.sum(areas[orients == pair1]) * np.sum(areas[orients == pair2])
                    elif orient_cooccur_scheme == 2:
                        p_orient_occur[pair1, pair2] = np.sum(orients == pair1) * np.sum(orients == pair2)
                else:
                    iden_angle_num = np.sum(orients == pair1)
                    if iden_angle_num == 1:
                        # p_orient_occur[pair1, pair2] = 0
                        # we start from zeros so no need to set it to zero
                        continue
                    else:
                        if orient_cooccur_scheme == 1:
                            indices = np.where(orients == pair1)[0]

                            # Generating all 2-element combinations of these indices
                            ind_permutation = np.array(list(combinations(indices, 2)))
                            p_orient_occur[pair1, pair2] = np.sum(areas[ind_permutation[:, 0]] * areas[ind_permutation[:, 1]])
                        elif orient_cooccur_scheme == 2:
                            p_orient_occur[pair1, pair2] = comb(iden_angle_num, 2, exact=True)
    # Normalize co-occurrence matrix
    orient_occur_matrix = p_orient_occur / np.sum(p_orient_occur)
    orient_occur_feats = haralick_no_img_v2(orient_occur_matrix)
    
    return orient_occur_feats


