import numpy as np

def haralick_no_img_v2(SGLD):

    # pi is the orientation of the first CF, pj is the orientation of the second CF
    pi, pj = np.nonzero(SGLD)
    p = SGLD[pi, pj]

    if len(p) <= 1:
        return None

    # Normalize the co-occurrence matrix and readjust the angles
    # it was already normalized in contrast_entropy function but this wont change as np.sum(p) is going to be 1
    p = p / np.sum(p)
    # need not to subtract 1 from pi and pj (probably haojia did this to mitigate for 1-based indexing in p_orient_occur's calculation) NEED HELP
    # this wont have any effect on only contrast_entropy feature
    # pi -= 1
    # pj -= 1

    # Marginals
    px_all = np.sum(SGLD, axis=1)
    pxi = np.nonzero(px_all)
    px = px_all[pxi]
    px = px / np.sum(px)
    # probably this should not be done as well
    # pxi = pxi[0] - 1

    py_all = np.sum(SGLD, axis=0).T
    pyi = np.nonzero(py_all)
    py = py_all[pyi]
    py = py / np.sum(py)
    # probably this should not be done as well
    # pyi = pyi[0] - 1

    epsilon = 1e-10  # Small value to replace zero
    px_all = np.maximum(px_all, epsilon)
    py_all = np.maximum(py_all, epsilon)
    

    # all_contrast are the angle between pairs of  CFs
    all_contrast = np.abs(pi - pj)

    # difference between two orientation of CF like x degrees and 180-x degrees is the same
    all_contrast[all_contrast > 9] = 18 - all_contrast[all_contrast > 9]

    # sort the angles between the pairs of CFs 
    sorted_indices = np.argsort(all_contrast)
    sorted_contrast = all_contrast[sorted_indices]
    p_sorted = p[sorted_indices]

    # only keep the CFs which have different angles between them as you can get the same angle between two CFs from different pairs of CFS
    # the np.diff(...) line will add the probabilites of same pairs of CFs (same pair as in same angle between them)
    ind = np.concatenate([np.where(np.diff(sorted_contrast) != 0)[0], [len(all_contrast) - 1]])
    contrast = sorted_contrast[ind]
    pcontrast = np.diff(np.concatenate(([0], np.cumsum(p_sorted)[ind])))

    contrast_energy = np.sum(contrast**2 * pcontrast)
    contrast_inverse_moment = np.sum((1 / (1 + contrast**2)) * pcontrast)
    contrast_ave = np.sum(contrast * pcontrast)
    contrast_var = np.sum((contrast - contrast_ave)**2 * pcontrast)
    contrast_entropy = -np.sum(pcontrast * np.log(pcontrast))

    # making the pairs of CFs as a single CF (orientation wise)
    # then accumlating the probabilities of the same new single CFs (orientation wise)
    all_intensity = (pi + pj) / 2
    sorted_intensity = np.sort(all_intensity)
    sind = np.argsort(all_intensity)
    ind = np.concatenate([np.where(np.diff(sorted_intensity) != 0)[0], [len(all_intensity)-1]])
    intensity = sorted_intensity[ind]
    pintensity = np.cumsum(p[sind])
    pintensity = np.diff(np.concatenate(([0], pintensity[ind])))

    intensity_ave = np.sum(intensity * pintensity)
    intensity_variance = np.sum((intensity - intensity_ave)**2 * pintensity)
    intensity_entropy = -np.sum(pintensity * np.log(pintensity))

    # Calculate probability features
    entropy = -np.sum(p * np.log(p))
    energy = np.sum(p**2)

    # Calculate correlation features
    mu_x = np.sum(pxi * px)
    sigma_x = np.sqrt(np.sum((pxi - mu_x)**2 * px))
    mu_y = np.sum(pyi * py)
    sigma_y = np.sqrt(np.sum((pyi - mu_y)**2 * py))

    correlation = np.sum((pi - mu_x) * (pj - mu_y) * p) / (sigma_x * sigma_y) if sigma_x != 0 and sigma_y != 0 else 0

    px_grid, py_grid = np.meshgrid(px, py)
    log_px_grid, log_py_grid = np.meshgrid(np.log(px), np.log(py))



    h1 = -np.sum(p * np.log(px_all[pj] * py_all[pi]))
    h2 = -np.sum(px_grid.flatten() * py_grid.flatten() * (log_px_grid.flatten() + log_py_grid.flatten()))
    hx = -np.sum(px * np.log(px))
    hy = -np.sum(py * np.log(py))

    information_measure1 = (entropy - h1) / max(hx, hy)
    information_measure2 = np.sqrt(1 - np.exp(-2 * (h2 - entropy)))


    # i have only fully understood contrast_entropy, intensity_entropy and entropy
    feats = {
        'contrast_energy': contrast_energy,
        'contrast_inverse_moment': contrast_inverse_moment,
        'contrast_ave': contrast_ave,
        'contrast_var': contrast_var,
        'contrast_entropy': contrast_entropy,
        'intensity_ave': intensity_ave,
        'intensity_variance': intensity_variance,
        'intensity_entropy': intensity_entropy,
        'entropy': entropy,
        'energy': energy,
        'correlation': correlation,
        'information_measure1': information_measure1,
        'information_measure2': information_measure2
    }
    return feats

