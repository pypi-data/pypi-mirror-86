# Spatial Clique

Applies the concept of a maximum clique to two sets of *corresponding* 2D or 3D points in order to find the largest group of points whose *relative* positions are the same in both sets. Sameness is defined via either a *hard* threshold (a Euclidean distance) or a *soft* threshold (a confidence level) applied to the differences between the intra-set distances. Soft thresholds require point covariance information.

The point sets can be thought of as "source" and "destination" in the sense that the "source" point set has been subjected to some type of transformation or deformation to produce the "destination" point set. The maximum clique will identify the largest group of points that exists in both point sets and differs by only a 6-parameter rigid-body transformation (translation and rotation). It cannot handle scale. Alternatively, the "source" and "destination" point sets could be putative correspondences, perhaps determined by a nearest neighbor metric in a descriptive feature space, generated from data obtained from two different observations of a common spatial scene.

The current implementation emphasizes clarity (for the creator, at least) and is deliberately inefficient. There are multiple nested `for` loops that could be replaced with more efficient mechanisms, e.g., scipy's `cdist` function could be used to compute all intra-point set distances.


## Installation

- Source: clone the repo and `pip install .`
- PyPI: `pip install spatialclique`
- Conda: perhaps in the future


## Usage

Not much to see here:

    from spatialclique import mc_hard
    max_clique_indices = mc_hard(src, dst, 0.2)

Of course, you must create the (M, 2) or (M, 3) sized `src` and `dst` arrays of 2D or 3D points first. The distance threshold is set to 0.2 in this example. 

For a soft threshold, you also need (M, 2, 2) or (M, 3, 3) sized arrays of covariance matrices (one for each point in the `src` and `dst` arrays):

    from spatialclique import mc_soft
    max_clique_indices = mc_soft(src, dst, src_cov, dst_cov, 95)

Here, we have set the confidence level to 95%. The covariance data is propagated through the distance and difference computations, and only those differences statistically equal to zero (at 95% confidence in this example) are included in the adjacency matrix that is fed to the maximum clique algorithm.


## Reference

None of this make sense? This [reference](https://arxiv.org/pdf/1902.01534.pdf) might help:

A. Parra, T. Chin, F. Neumann, T. Friedrich, and M. Katzmann, “A Practical Maximum Clique Algorithm for matching with Pairwise Constraints,” arXiv:1902.01534v2 \[cs.CV\], Feb. 2020.







