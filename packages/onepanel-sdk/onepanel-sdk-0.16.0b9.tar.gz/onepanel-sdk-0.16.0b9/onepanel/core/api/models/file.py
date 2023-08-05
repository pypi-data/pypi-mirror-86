# coding: utf-8

"""
    Onepanel

    Onepanel API  # noqa: E501

    The version of the OpenAPI document: 0.16.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from onepanel.core.api.configuration import Configuration


class File(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'path': 'str',
        'name': 'str',
        'extension': 'str',
        'size': 'str',
        'content_type': 'str',
        'last_modified': 'str',
        'directory': 'bool'
    }

    attribute_map = {
        'path': 'path',
        'name': 'name',
        'extension': 'extension',
        'size': 'size',
        'content_type': 'contentType',
        'last_modified': 'lastModified',
        'directory': 'directory'
    }

    def __init__(self, path=None, name=None, extension=None, size=None, content_type=None, last_modified=None, directory=None, local_vars_configuration=None):  # noqa: E501
        """File - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._path = None
        self._name = None
        self._extension = None
        self._size = None
        self._content_type = None
        self._last_modified = None
        self._directory = None
        self.discriminator = None

        if path is not None:
            self.path = path
        if name is not None:
            self.name = name
        if extension is not None:
            self.extension = extension
        if size is not None:
            self.size = size
        if content_type is not None:
            self.content_type = content_type
        if last_modified is not None:
            self.last_modified = last_modified
        if directory is not None:
            self.directory = directory

    @property
    def path(self):
        """Gets the path of this File.  # noqa: E501


        :return: The path of this File.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this File.


        :param path: The path of this File.  # noqa: E501
        :type: str
        """

        self._path = path

    @property
    def name(self):
        """Gets the name of this File.  # noqa: E501


        :return: The name of this File.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this File.


        :param name: The name of this File.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def extension(self):
        """Gets the extension of this File.  # noqa: E501


        :return: The extension of this File.  # noqa: E501
        :rtype: str
        """
        return self._extension

    @extension.setter
    def extension(self, extension):
        """Sets the extension of this File.


        :param extension: The extension of this File.  # noqa: E501
        :type: str
        """

        self._extension = extension

    @property
    def size(self):
        """Gets the size of this File.  # noqa: E501


        :return: The size of this File.  # noqa: E501
        :rtype: str
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this File.


        :param size: The size of this File.  # noqa: E501
        :type: str
        """

        self._size = size

    @property
    def content_type(self):
        """Gets the content_type of this File.  # noqa: E501


        :return: The content_type of this File.  # noqa: E501
        :rtype: str
        """
        return self._content_type

    @content_type.setter
    def content_type(self, content_type):
        """Sets the content_type of this File.


        :param content_type: The content_type of this File.  # noqa: E501
        :type: str
        """

        self._content_type = content_type

    @property
    def last_modified(self):
        """Gets the last_modified of this File.  # noqa: E501


        :return: The last_modified of this File.  # noqa: E501
        :rtype: str
        """
        return self._last_modified

    @last_modified.setter
    def last_modified(self, last_modified):
        """Sets the last_modified of this File.


        :param last_modified: The last_modified of this File.  # noqa: E501
        :type: str
        """

        self._last_modified = last_modified

    @property
    def directory(self):
        """Gets the directory of this File.  # noqa: E501


        :return: The directory of this File.  # noqa: E501
        :rtype: bool
        """
        return self._directory

    @directory.setter
    def directory(self, directory):
        """Sets the directory of this File.


        :param directory: The directory of this File.  # noqa: E501
        :type: bool
        """

        self._directory = directory

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, File):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, File):
            return True

        return self.to_dict() != other.to_dict()
