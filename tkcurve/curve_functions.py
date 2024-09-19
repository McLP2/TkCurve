import numpy as np
from scipy.interpolate import CubicSpline, Akima1DInterpolator, KroghInterpolator, PchipInterpolator


def scipy_interpolation(interpolator, points, cache, at=None):
    if 'points' in cache.keys() and cache['points'] == points:
        if at is None:
            return cache['results']
        else:
            spline = cache['interpolation']
            return spline(at)
    else:
        in_xs, in_ys = map(list, zip(*points))
        for i in range(len(in_xs) - 2, -1, -1):
            if in_xs[i] == in_xs[i + 1]:
                del in_xs[i]
                del in_ys[i]
        spline = interpolator(in_xs, in_ys)
        cache['interpolation'] = spline
        out_xs = np.linspace(0, 1, 100)
        results = list(zip(out_xs, spline(out_xs)))
        cache['results'] = results
        cache['points'] = points.copy()
        if at is None:
            return results
        else:
            return spline(at)


def cubic_spline_interpolation(points, cache, at=None):
    return scipy_interpolation(CubicSpline, points, cache, at)


def akima_interpolation(points, cache, at=None):
    return scipy_interpolation(Akima1DInterpolator, points, cache, at)


def krogh_interpolation(points, cache, at=None):
    return scipy_interpolation(KroghInterpolator, points, cache, at)


def pchip_interpolation(points, cache, at=None):
    return scipy_interpolation(PchipInterpolator, points, cache, at)
