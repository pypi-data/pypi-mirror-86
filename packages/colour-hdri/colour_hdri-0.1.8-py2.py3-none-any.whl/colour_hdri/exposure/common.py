# -*- coding: utf-8 -*-
"""
Exposure Value Computation
==========================

Defines exposure value computation objects:

-   :func:`colour_hdri.average_luminance`
-   :func:`colour_hdri.average_illuminance`
-   :func:`colour_hdri.luminance_to_exposure_value`
-   :func:`colour_hdri.illuminance_to_exposure_value`
-   :func:`colour_hdri.adjust_exposure`

References
----------
-   :cite:`Wikipediabj` : Wikipedia. (n.d.). EV as a measure of luminance and
    illuminance. Retrieved November 14, 2015, from
    https://en.wikipedia.org/wiki/Exposure_value#\
EV_as_a_measure_of_luminance_and_illuminance
"""

from __future__ import division, unicode_literals

import numpy as np

from colour.utilities import as_float_array

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2015-2020 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = [
    'average_luminance', 'average_illuminance', 'luminance_to_exposure_value',
    'illuminance_to_exposure_value', 'adjust_exposure'
]


def average_luminance(N, t, S, k=12.5):
    """
    Computes the average luminance :math:`L` in :math:`cd\\cdot m^{-2}` from
    given relative aperture *F-Number* :math:`N`, *Exposure Time* :math:`t`,
    *ISO* arithmetic speed :math:`S` and *reflected light calibration constant*
    :math:`k`.

    Parameters
    ----------
    N : array_like
        Relative aperture *F-Number* :math:`N`.
    t : array_like
       *Exposure Time* :math:`t`.
    S : array_like
        *ISO* arithmetic speed :math:`S`.
    k : numeric, optional
        *Reflected light calibration constant* :math:`k`.
        *ISO 2720:1974* recommends a range for :math:`k` of 10.6 to 13.4 with
        luminance in :math:`cd\\cdot m^{-2}`. Two values for :math:`k` are in
        common use: 12.5 (Canon, Nikon, and Sekonic) and 14 (Minolta, Kenko,
        and Pentax).

    Returns
    -------
    ndarray
        Average luminance :math:`L` in :math:`cd\\cdot m^{-2}`.

    References
    ----------
    :cite:`Wikipediabj`

    Examples
    --------
    >>> average_luminance(8, 1, 100)
    8.0
    """

    N = as_float_array(N)
    t = as_float_array(t)
    S = as_float_array(S)

    L = N ** 2 / t / S * k

    return L


def average_illuminance(N, t, S, c=250):
    """
    Computes the average illuminance :math:`E` in :math:`Lux` from given
    relative aperture *F-Number* :math:`N`, *Exposure Time* :math:`t`, *ISO*
    arithmetic speed :math:`S` and *incident light calibration constant*
    :math:`c`.

    Parameters
    ----------
    N : array_like
        Relative aperture *F-Number* :math:`N`.
    t : array_like
       *Exposure Time* :math:`t`.
    S : array_like
        *ISO* arithmetic speed :math:`S`.
    c : numeric, optional
        *Incident light calibration constant* :math:`c`.
        With a flat receptor, *ISO 2720:1974* recommends a range for
        :math:`c`. of 240 to 400 with illuminance in :math:`Lux`; a value of
        250 is commonly used. With a hemispherical receptor, *ISO 2720:1974*
        recommends a range for :math:`c` of 320 to 540 with illuminance in
        :math:`Lux`; in practice, values typically are between 320 (Minolta)
        and 340 (Sekonic).

    Returns
    -------
    ndarray
        Average illuminance :math:`E` in :math:`Lux`.

    References
    ----------
    :cite:`Wikipediabj`

    Examples
    --------
    >>> average_illuminance(8, 1, 100)
    160.0
    """

    N = as_float_array(N)
    t = as_float_array(t)
    S = as_float_array(S)

    E = N ** 2 / t / S * c

    return E


def luminance_to_exposure_value(L, S, k=12.5):
    """
    Computes the exposure value :math:`EV` from given scene luminance
    :math:`L` in :math:`cd\\cdot m^{-2}`, *ISO* arithmetic speed :math:`S` and
    *reflected light calibration constant* :math:`k`.

    Parameters
    ----------
    L : array_like
        Scene luminance :math:`L` in :math:`cd\\cdot m^{-2}`.
    S : array_like
        *ISO* arithmetic speed :math:`S`.
    k : numeric, optional
        *Reflected light calibration constant* :math:`k`.
        *ISO 2720:1974* recommends a range for :math:`k` of 10.6 to 13.4 with
        luminance in :math:`cd\\cdot m^{-2}`. Two values for :math:`k` are in
        common use: 12.5 (Canon, Nikon, and Sekonic) and 14 (Minolta, Kenko,
        and Pentax).

    Returns
    -------
    ndarray
        Exposure value :math:`EV`.

    Notes
    -----
    -   The exposure value :math:`EV` indicates a combination of camera
        settings rather than the focal plane exposure, i.e. luminous exposure,
        photometric exposure, :math:`H`. The focal plane exposure is
        time-integrated illuminance.

    References
    ----------
    :cite:`Wikipediabj`

    Examples
    --------
    >>> luminance_to_exposure_value(0.125, 100)
    0.0
    """

    L = as_float_array(L)
    S = as_float_array(S)
    k = as_float_array(k)

    EV = np.log2(L * S / k)

    return EV


def illuminance_to_exposure_value(E, S, c=250):
    """
    Computes the exposure value :math:`EV` from given scene illuminance
    :math:`E` in :math:`Lux`, *ISO* arithmetic speed :math:`S` and
    *incident light calibration constant* :math:`c`.

    Parameters
    ----------
    E : array_like
        Scene illuminance :math:`E` in :math:`Lux`.
    S : array_like
        *ISO* arithmetic speed :math:`S`.
    c : numeric, optional
        *Incident light calibration constant* :math:`c`.
        With a flat receptor, *ISO 2720:1974* recommends a range for
        :math:`c`. of 240 to 400 with illuminance in :math:`Lux`; a value of
        250 is commonly used. With a hemispherical receptor, *ISO 2720:1974*
        recommends a range for :math:`c` of 320 to 540 with illuminance in
        :math:`Lux`; in practice, values typically are between 320 (Minolta)
        and 340 (Sekonic).

    Returns
    -------
    ndarray
        Exposure value :math:`EV`.

    Notes
    -----
    -   The exposure value :math:`EV` indicates a combination of camera
        settings rather than the focal plane exposure, i.e. luminous exposure,
        photometric exposure, :math:`H`. The focal plane exposure is
        time-integrated illuminance.

    References
    ----------
    :cite:`Wikipediabj`

    Examples
    --------
    >>> illuminance_to_exposure_value(2.5, 100)
    0.0
    """

    E = as_float_array(E)
    S = as_float_array(S)
    c = as_float_array(c)

    EV = np.log2(E * S / c)

    return EV


def adjust_exposure(a, EV):
    """
    Adjusts given array exposure using given :math:`EV` exposure value.

    Parameters
    ----------
    a : array_like
        Array to adjust the exposure.
    EV : numeric
        Exposure adjustment value.

    Returns
    -------
    ndarray
        Exposure adjusted array.

    Examples
    --------
    >>> adjust_exposure(np.array([0.25, 0.5, 0.75, 1]), 1)
    array([ 0.5,  1. ,  1.5,  2. ])
    """

    a = as_float_array(a)

    return a * pow(2, EV)
