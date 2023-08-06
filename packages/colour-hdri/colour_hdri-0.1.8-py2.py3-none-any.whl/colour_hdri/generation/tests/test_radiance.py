# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Defines unit tests for :mod:`colour_hdri.generation.radiance` module.
"""

from __future__ import division, unicode_literals

import numpy as np
import os
import unittest

from colour import RGB_COLOURSPACES

from colour_hdri import TESTS_RESOURCES_DIRECTORY
from colour_hdri.generation import image_stack_to_radiance_image
from colour_hdri.calibration import camera_response_functions_Debevec1997
from colour_hdri.utilities import ImageStack, filter_files

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2015-2020 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = [
    'FROBISHER_001_DIRECTORY', 'GENERATION_DIRECTORY', 'JPG_IMAGES',
    'TestRadianceImage'
]

FROBISHER_001_DIRECTORY = os.path.join(TESTS_RESOURCES_DIRECTORY,
                                       'frobisher_001')

GENERATION_DIRECTORY = os.path.join(TESTS_RESOURCES_DIRECTORY, 'colour_hdri',
                                    'generation')

JPG_IMAGES = filter_files(FROBISHER_001_DIRECTORY, ('jpg', ))


class TestRadianceImage(unittest.TestCase):
    """
    Defines :func:`colour_hdri.generation.radiance.\
image_stack_to_radiance_image` definition unit tests methods.
    """

    def test_radiance_image(self):
        """
        Tests :func:`colour_hdri.generation.\
radiance.image_stack_to_radiance_image` definition.
        """

        image_stack = ImageStack.from_files(JPG_IMAGES)
        image_stack.data = RGB_COLOURSPACES['sRGB'].cctf_decoding(
            image_stack.data)

        # Lower precision for unit tests under *travis-ci*.
        np.testing.assert_allclose(
            image_stack_to_radiance_image(image_stack),
            np.load(
                os.path.join(GENERATION_DIRECTORY,
                             'test_radiance_image_linear.npy')),
            rtol=0.0001,
            atol=0.0001)

        # Lower precision for unit tests under *travis-ci*.
        image_stack = ImageStack.from_files(JPG_IMAGES)
        np.testing.assert_allclose(
            image_stack_to_radiance_image(
                image_stack,
                camera_response_functions=(
                    camera_response_functions_Debevec1997(image_stack))),
            np.load(
                os.path.join(GENERATION_DIRECTORY,
                             'test_radiance_image_crfs.npy')),
            rtol=0.0001,
            atol=0.0001)


if __name__ == '__main__':
    unittest.main()
