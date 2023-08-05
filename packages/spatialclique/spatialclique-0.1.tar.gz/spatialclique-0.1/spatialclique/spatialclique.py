from statistics import NormalDist
import numpy as np
import networkx as nx


def mc_hard(src, dst, threshold):
    """Find the largest set of source and destination points (2D or 3D) whose
    relative distances are the same. In other words, given a set of source 
    points, find the largest set of destination points that differ only by a 
    rigid 6-parameter transformation (no scale). The determination of sameness
    for the relative distances is controlled by the specified threshold value.

    The order of the source and destination point sets must match, i.e.,
    represent putative correspondences.

    Parameters
    ----------
    src : (M, 2) or (M, 3) array
        Source coordinates.
    dst : (M, 2) or (M, 3) array
        Destination coordinates.
    threshold : scalar
        Maximum difference in distance between the source and destination points
        for edge inclusion in adjacency matrix. Must be greater than 0.

    Returns
    -------
    maximum_clique : list with length = size of maximum clique
        Row indices of maximum clique coordinates. Set to False if no maximum
        clique is found.
    """

    src = np.asarray(src)
    dst = np.asarray(dst)

    if src.shape[1] < 2 or src.shape[1] > 3:
        raise ValueError("src coordinate array must have 2 or 3 columns (to "
                         "hold 2D or 3D coordinates).")
    if dst.shape[1] < 2 or dst.shape[1] > 3:
        raise ValueError("dst coordinate array must have 2 or 3 columns (to "
                         "hold 2D or 3D coordinates).")

    if src.shape[1] != dst.shape[1]:
        raise ValueError("src and dst coordinate arrays must have the same "
                         "number of columns (i.e., be of same dimension).")
    if src.shape[0] != dst.shape[0]:
        raise ValueError("src and dst coordinate arrays must have the same "
                         "number of rows (i.e., hold equal number of points).")

    if threshold <= 0:
        raise ValueError("threshold must be greater than 0.")

    adjacency = hard_adjacency(src, dst, threshold)

    return maximum_clique(adjacency)


def mc_soft(src, dst, src_cov, dst_cov, confidence):
    """Find the largest set of source and destination points (2D or 3D) whose
    relative distances are the same. In other words, given a set of source 
    points, find the largest set of destination points that differ only by a 
    rigid 6-parameter transformation (no scale). The determination of sameness
    for the relative distances is controlled by the specified confidence
    threshold and propagation of point covariances into the distances.
    
    The order of the source and destination point sets must match, i.e.,
    represent putative correspondences.
    
    Parameters
    ----------
    src : (M, 2) or (M, 3) array
        Source coordinates.
    dst : (M, 2) or (M, 3) array
        Destination coordinates.
    src_cov : (M, 2, 2) or (M, 3, 3) array
        Source covariance matrices.
    dst_cov : (M, 2, 2) or (M, 3, 3) array
        Destination covariance matrices.
    confidence : scalar
        Confidence level for edge inclusion in adjacency matrix. Must be in 
        (0 < confidence < 100) interval.
    
    Returns
    -------
    maximum_clique : list with length = size of maximum clique
        Row indices of maximum clique coordinates. Set to False if no maximum
        clique is found.
    """

    src = np.asarray(src)
    dst = np.asarray(dst)
    src_cov = np.asarray(src_cov)
    dst_cov = np.asarray(dst_cov)

    if src.shape[1] < 2 or src.shape[1] > 3:
        raise ValueError("src coordinate array must have 2 or 3 columns (to "
                         "hold 2D or 3D coordinates).")
    if dst.shape[1] < 2 or dst.shape[1] > 3:
        raise ValueError("dst coordinate array must have 2 or 3 columns (to "
                         "hold 2D or 3D coordinates).")

    if src.shape[1] != dst.shape[1]:
        raise ValueError("src and dst coordinate arrays must have the same "
                         "number of columns (i.e., be of same dimension).")
    if src.shape[0] != dst.shape[0]:
        raise ValueError("src and dst coordinate arrays must have the same "
                         "number of rows (i.e., hold equal number of points).")

    if src_cov.shape != (src.shape[0], src.shape[1], src.shape[1]):
        raise ValueError("Incorrect src_cov shape: src_cov must contain "
                         "corresponding covariance matrices for each src "
                         "point.")
    if dst_cov.shape != (dst.shape[0], dst.shape[1], dst.shape[1]):
        raise ValueError("Incorrect dst_cov shape: dst_cov must contain "
                         "corresponding covariance matrices for each dst "
                         "point.")

    if confidence <=0 or confidence >=100:
        raise ValueError("confidence must be greater than 0 and less than 100.")

    adjacency = soft_adjacency(src, dst, src_cov, dst_cov, confidence)

    return maximum_clique(adjacency)


def combination_distances(pts):
    """Euclidean distance between all points.

    Parameters
    ----------
    pts : (M, 2) or (M, 3) array
        2D or 3D "from" coordinates.

    Returns
    -------
    d : (M, M) array
        Array of all Euclidean distances between the points. Rows can be thought
        of as "from" and columns as "to" in the sense of computing distance from
        one point and to another.
    """

    m = pts.shape[0]
    dim = pts.shape[1]

    d = np.empty((m, m), dtype=np.double)
    if dim == 2:
        for i in range(0, m):  # "from"
            for j in range(0, m):  # "to"
                d[i,j] = np.sqrt( (pts[j,0] - pts[i,0])**2
                                + (pts[j,1] - pts[i,1])**2 )
    else:
        for i in range(0, m):  # "from"
            for j in range(0, m):  # "to"
                d[i,j] = np.sqrt( (pts[j,0] - pts[i,0])**2
                                + (pts[j,1] - pts[i,1])**2
                                + (pts[j,3] - pts[i,3])**2 )

    return d


def distance_variance(pts, cov, d):
    """Propagate coordinate covariance matrices into distance variances.

    Parameters
    ----------
    pts : (M, 2) or (M, 3) array
        2D or 3D point coordinates.
    cov : (M, 2, 2) or (M, 3, 3) array
        Point covariance matrices.
    d : (M, M) array of distances between all points, where rows can be thought
        of as "from" and columns as "to" in the sense of a distance from one 
        point and to another.

    """
    m = pts.shape[0]
    dim = pts.shape[1]

    # Partial derivatives of distances with respect to the 'from' and 'to'
    # coordinate components
    fm_x = np.empty((m, m), dtype=np.double)
    fm_y = fm_x.copy()
    to_x = fm_x.copy()
    to_y = fm_x.copy()
    for i in range(0, m):  # from
        for j in range(0, m):  # to
            if i == j:  # divide by zero
                fm_x[i,j] = 0
                fm_y[i,j] = 0
                to_x[i,j] = 0
                to_y[i,j] = 0
            else:
                fm_x[i,j] = (pts[i,0] - pts[j,0]) / d[i,j]
                fm_y[i,j] = (pts[i,1] - pts[j,1]) / d[i,j]
                to_x[i,j] = (pts[j,0] - pts[i,0]) / d[i,j]
                to_y[i,j] = (pts[j,1] - pts[i,1]) / d[i,j]
    if dim == 3:
        fm_z = np.empty((m, m), dtype=np.double)
        to_z = fm_z.copy()
        for i in range(0, m):  # from
            for j in range(0, m):  # to
                if i == j:  # divide by zero
                    fm_z[i,j] = 0
                    to_z[i,j] = 0
                else:
                    fm_z[i,j] = (pts[i,2] - pts[j,2]) / d[i,j]
                    to_z[i,j] = (pts[j,2] - pts[i,2]) / d[i,j]

    # Propagate point covariances into distance variance
    d_var = np.empty((m, m), dtype=np.double)
    if dim == 2:
        J = np.empty((1,4), dtype=np.double)
        C = np.zeros((4,4), dtype=np.double)
        for i in range(0, m):  # fromc
            for j in range(0, m):  # to
                J[0,0] = fm_x[i,j]
                J[0,1] = fm_y[i,j]
                J[0,2] = to_x[i,j]
                J[0,3] = to_y[i,j]
                C[0:2,0:2] = cov[i]
                C[2:,2:] = cov[j]
                d_var[i,j] = J @ C @ J.T
    else:
        J = np.empty((1,6), dtype=np.double)
        C = np.zeros((6,6), dtype=np.double)
        for i in range(0, m):  # from
            for j in range(0, m):  # to
                J[0,0] = fm_x[i,j]
                J[0,1] = fm_y[i,j]
                J[0,2] = fm_z[i,j]
                J[0,3] = to_x[i,j]
                J[0,4] = to_y[i,j]
                J[0,5] = to_z[i,j]
                C[0:3,0:3] = cov[i]
                C[3:,3:] = cov[j]
                d_var[i,j] = J @ C @ J.T

    return d_var


def soft_adjacency(src, dst, src_cov, dst_cov, confidence):
    """Adjacency matrix based on whether the confidence intervals of the 
    inter-set distance differences contain zero at the specified confidence
    level.

    Parameters
    ----------
    src : (M, 2) or (M, 3) array
        Source coordinates.
    dst : (M, 2) or (M, 3) array
        Destination coordinates.
    src_cov : (M, 2, 2) or (M, 3, 3) array
        Source covariance matrices.
    dst_cov : (M, 2, 2) or (M, 3, 3) array
        Destination covariance matrices.
    confidence : scalar
        Confidence level for edge inclusion in adjacency matrix. Must be in 
        (0 < confidence < 100) interval.

    Returns
    -------
    adjacency : (M, M) array
        Standard adjacency matrix: 1 = edge, 0 - no edge.
    """

    # Intra-set distance arrays
    src_d = combination_distances(src)
    dst_d = combination_distances(dst)

    # Propagated variances for all intra-set distances between points in the 
    # source and destination point sets
    src_d_var = distance_variance(src, src_cov, src_d)
    dst_d_var = distance_variance(dst, dst_cov, dst_d)

    # Inter-set distance differencesa and variances
    difference = dst_d - src_d
    difference_var = src_d_var + dst_d_var
    difference_std = np.sqrt(difference_var)

    # Confidence multiplier
    p = (1 + confidence/100) / 2
    multiplier = NormalDist().inv_cdf(p)

    # Adjacency matrix
    adjacency = np.logical_and(difference + multiplier*difference_std >= 0,
                              difference - multiplier*difference_std <= 0)

    return adjacency.astype(np.int)


def hard_adjacency(src, dst, threshold):
    """Adjacency matrix based on whether the inter-set distance differences
    exceed the specified threshold.

    Parameters
    ----------
    src : (M, 2) or (M, 3) array
        Source coordinates.
    dst : (M, 2) or (M, 3) array
        Destination coordinates.
    threshold : scalar
        Maximum difference in distance between the source and destination points
        for edge inclusion in adjacency matrix. Must be greater than 0.

    Returns
    -------
    adjacency : (M, M) array
        Standard adjacency matrix: 1 = edge, 0 - no edge.
    """

    # Intra-set distance arrays
    src_d = combination_distances(src)
    dst_d = combination_distances(dst)

    difference = dst_d - src_d

    adjacency = np.abs(difference) < threshold

    return adjacency.astype(np.int)


def maximum_clique(adjacency):
    """Maximum clique of an adjacency matrix.

    Parameters
    ----------
    adjacency : (M, M) array
        Adjacency matrix.

    Returns
    -------
    maximum_clique : list with length = size of maximum clique
        Row indices of maximum clique coordinates. Set to False if no maximum
        clique is found.
    """

    G = nx.Graph(adjacency)
    cliques = list(nx.find_cliques(G))
    if len(cliques) < 1:
        print('No maximal cliques found.')
        return False

    clique_sizes = [len(i) for i in cliques]
    maximum_clique = cliques[np.argmax(np.array(clique_sizes))]

    return maximum_clique


