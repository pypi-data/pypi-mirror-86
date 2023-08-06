# -*- coding: utf-8 -*-
"""
EXIF Data Manipulation
======================

Exif data manipulation routines based on *exiftool*:

-   :func:`colour_hdri.parse_exif_data`
-   :func:`colour_hdri.read_exif_tags`
-   :func:`colour_hdri.copy_exif_tags`
-   :func:`colour_hdri.update_exif_tags`
-   :func:`colour_hdri.delete_exif_tags`
-   :func:`colour_hdri.read_exif_tag`
-   :func:`colour_hdri.write_exif_tag`
"""

from __future__ import division, unicode_literals

import logging
import numpy as np
import re
import subprocess  # nosec
from collections import namedtuple
from fractions import Fraction
from six import text_type

from colour.utilities.documentation import (DocstringText,
                                            is_documentation_building)

from colour_hdri.utilities import vivification

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2015-2020 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = [
    'EXIF_EXECUTABLE', 'ExifTag', 'parse_exif_string', 'parse_exif_numeric',
    'parse_exif_fraction', 'parse_exif_array', 'parse_exif_data',
    'read_exif_tags', 'copy_exif_tags', 'update_exif_tags', 'delete_exif_tags',
    'read_exif_tag', 'write_exif_tag'
]

EXIF_EXECUTABLE = 'exiftool'
if is_documentation_building():  # pragma: no cover
    EXIF_EXECUTABLE = DocstringText(EXIF_EXECUTABLE)
    EXIF_EXECUTABLE.__doc__ = """
Command line exif manipulation application, usually Phil Harvey's *ExifTool*.

EXIF_EXECUTABLE : unicode
"""


class ExifTag(namedtuple('ExifTag', ('group', 'name', 'value', 'identifier'))):
    """
    Hunt colour appearance model induction factors.

    Parameters
    ----------
    group : unicode, optional
        Exif tag group name.
    name : unicode, optional
        Exif tag name.
    value : object, optional
        Exif tag value.
    identifier : numeric, optional
        Exif tag identifier.
    """

    def __new__(cls, group=None, name=None, value=None, identifier=None):
        """
        Returns a new instance of the :class:`colour_hdri.ExifTag` class.
        """

        return super(ExifTag, cls).__new__(cls, group, name, value, identifier)


def parse_exif_string(exif_tag):
    """
    Parses given exif tag assuming it is a string and return its value.

    Parameters
    ----------
    exif_tag : ExifTag
        Exif tag to parse.

    Returns
    -------
    unicode
        Parsed exif tag value.
    """

    return text_type(exif_tag.value)


def parse_exif_numeric(exif_tag, dtype=np.float_):
    """
    Parses given exif tag assuming it is a numeric type and return its value.

    Parameters
    ----------
    exif_tag : ExifTag
        Exif tag to parse.
    dtype : object, optional
        Return value data type.

    Returns
    -------
    numeric
        Parsed exif tag value.
    """

    return dtype(exif_tag.value)


def parse_exif_fraction(exif_tag, dtype=np.float_):
    """
    Parses given exif tag assuming it is a fraction and return its value.

    Parameters
    ----------
    exif_tag : ExifTag
        Exif tag to parse.
    dtype : object, optional
        Return value data type.

    Returns
    -------
    numeric
        Parsed exif tag value.
    """

    return dtype(Fraction(exif_tag.value))


def parse_exif_array(exif_tag, dtype=np.float_, shape=None):
    """
    Parses given exif tag assuming it is an array and return its value.

    Parameters
    ----------
    exif_tag : ExifTag
        Exif tag to parse.
    dtype : object, optional
        Return value data type.
    shape : array_like, optional
        Shape of

    Returns
    -------
    ndarray
        Parsed exif tag value.
    """

    return np.array(exif_tag.value.split()).astype(dtype).reshape(shape)


def parse_exif_data(data):
    """
    Parses given exif data output from *exiftool*.

    Parameters
    ----------
    data : unicode
        Exif data.

    Returns
    -------
    list
        Parsed exif data.
    """

    search = re.search(
        r'\[(?P<group>\w+)\]\s*(?P<id>(\d+|-))?(?P<tag>.*?):(?P<value>.*$)',
        data)

    return [
        group.strip() if group is not None else group
        for group in (search.group('group'), search.group('id'),
                      search.group('tag'), search.group('value'))
    ]


def read_exif_tags(image):
    """
    Returns given image exif image tags.

    Parameters
    ----------
    image : unicode
        Image file.

    Returns
    -------
    defaultdict
        Exif tags.
    """

    logging.info("Reading '{0}' image exif data.".format(image))

    exif_tags = vivification()
    lines = text_type(
        subprocess.check_output(  # nosec
            [EXIF_EXECUTABLE, '-D', '-G', '-a', '-u', '-n', image]),
        'utf-8',
        'ignore').split('\n')

    for line in lines:
        if not line.strip():
            continue

        group, identifier, tag, value = parse_exif_data(line)

        if not exif_tags[group][tag]:
            exif_tags[group][tag] = []

        exif_tags[group][tag].append(ExifTag(group, tag, value, identifier))

    return exif_tags


def copy_exif_tags(source, target):
    """
    Copies given source image file exif tag to given image target.

    Parameters
    ----------
    source : unicode
        Source image file.
    target : unicode
        Target image file.

    Returns
    -------
    bool
        Definition success.
    """

    logging.info("Copying '{0}' file exif data to '{1}' file.".format(
        source, target))

    arguments = [EXIF_EXECUTABLE, '-overwrite_original', '-TagsFromFile']
    arguments += [source, target]
    subprocess.check_output(arguments)  # nosec

    return True


def update_exif_tags(images):
    """
    Updates given images siblings images pairs exif tags.

    Parameters
    ----------
    images : list
        Image files to update.

    Returns
    -------
    bool
        Definition success.
    """

    success = True
    for (source, target) in images:
        success *= copy_exif_tags(source, target)

    return success


def delete_exif_tags(image):
    """
    Deletes all given image exif tags.

    Parameters
    ----------
    image : unicode
        Image file.

    Returns
    -------
    bool
        Definition success.
    """

    logging.info("Deleting '{0}' image exif tags.".format(image))

    subprocess.check_output(  # nosec
        [EXIF_EXECUTABLE, '-overwrite_original', '-all=', image])

    return True


def read_exif_tag(image, tag):
    """
    Returns given image exif tag value.

    Parameters
    ----------
    image : unicode
        Image file.
    tag : unicode
        Tag.

    Returns
    -------
    unicode
        Tag value.
    """

    value = text_type(
        subprocess.check_output(  # nosec
            [EXIF_EXECUTABLE, '-{0}'.format(tag), image]),
        'utf-8',
        'ignore').split(':').pop().strip()

    logging.info("Reading '{0}' image '{1}' exif tag value: '{2}'".format(
        image, tag, value))

    return value


def write_exif_tag(image, tag, value):
    """
    Sets given image exif tag value.

    Parameters
    ----------
    image : unicode
        Image file.
    tag : unicode
        Tag.
    value : unicode
        Value.

    Returns
    -------
    bool
        Definition success.
    """

    logging.info("Writing '{0}' image '{1}' exif tag with '{2}' value.".format(
        image, tag, value))

    arguments = [EXIF_EXECUTABLE, '-overwrite_original']
    arguments += ['-{0}={1}'.format(tag, value), image]
    subprocess.check_output(arguments)  # nosec

    return True
