from numpy import array, zeros, argmin, inf
from numpy.linalg import norm

def dtw(x, y, dist=lambda x, y: norm(x - y, ord=1), w=None):
    """ Computes the DTW of two sequences.

    :param array x: N1*M array
    :param array y: N2*M array
    :param func dist: distance used as cost measure (default L1 norm)

    Returns the minimum distance, the accumulated cost matrix and the wrap path.

    """
    x = array(x)
    if len(x.shape) == 1:
        x = x.reshape(-1, 1)
    y = array(y)
    if len(y.shape) == 1:
        y = y.reshape(-1, 1)

    r, c = len(x), len(y)

    D = zeros((r + 1, c + 1))
    if w:
        w = max(w, abs(r - c))
        D[:, :] = inf
        D[0, 0] = 0.
    else:
        D[0, 1:] = inf
        D[1:, 0] = inf
        for i in range(r):
            for j in range(c):
                D[i+1, j+1] = dist(x[i], y[j])

    for i in range(r):
        if w:
            for j in range(max(0, i - w), min(c, i + w)):
                d = dist(x[i], y[j])
                D[i+1, j+1] = d + min(D[i, j], D[i, j+1], D[i+1, j])
        else:
            for j in range(c):
                D[i+1, j+1] += min(D[i, j], D[i, j+1], D[i+1, j])

    D = D[1:, 1:]

    # divides by sum(D.shape) so that the distance is normalized by the number of points in both series combined
    dist = D[-1, -1] / sum(D.shape)

    return dist, D, _trackeback(D)


def _trackeback(D):
    i, j = array(D.shape) - 1
    p, q = [i], [j]
    while (i > 0 and j > 0):
        tb = argmin((D[i-1, j-1], D[i-1, j], D[i, j-1]))

        if (tb == 0):
            i = i - 1
            j = j - 1
        elif (tb == 1):
            i = i - 1
        elif (tb == 2):
            j = j - 1

        p.insert(0, i)
        q.insert(0, j)

    p.insert(0, 0)
    q.insert(0, 0)
    return (array(p), array(q))
