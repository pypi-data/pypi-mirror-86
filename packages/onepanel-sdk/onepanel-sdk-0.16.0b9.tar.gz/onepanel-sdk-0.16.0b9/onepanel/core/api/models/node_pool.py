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


class NodePool(object):
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
        'label': 'str',
        'options': 'list[NodePoolOption]'
    }

    attribute_map = {
        'label': 'label',
        'options': 'options'
    }

    def __init__(self, label=None, options=None, local_vars_configuration=None):  # noqa: E501
        """NodePool - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._label = None
        self._options = None
        self.discriminator = None

        if label is not None:
            self.label = label
        if options is not None:
            self.options = options

    @property
    def label(self):
        """Gets the label of this NodePool.  # noqa: E501


        :return: The label of this NodePool.  # noqa: E501
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this NodePool.


        :param label: The label of this NodePool.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def options(self):
        """Gets the options of this NodePool.  # noqa: E501


        :return: The options of this NodePool.  # noqa: E501
        :rtype: list[NodePoolOption]
        """
        return self._options

    @options.setter
    def options(self, options):
        """Sets the options of this NodePool.


        :param options: The options of this NodePool.  # noqa: E501
        :type: list[NodePoolOption]
        """

        self._options = options

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
        if not isinstance(other, NodePool):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NodePool):
            return True

        return self.to_dict() != other.to_dict()
