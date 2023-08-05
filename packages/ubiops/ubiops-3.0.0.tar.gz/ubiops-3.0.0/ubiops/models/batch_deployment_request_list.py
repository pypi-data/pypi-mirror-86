# coding: utf-8

"""
    UbiOps

    Client Library to interact with the UbiOps API.  # noqa: E501

    The version of the OpenAPI document: v2.1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from ubiops.configuration import Configuration


class BatchDeploymentRequestList(object):
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
        'id': 'str',
        'status': 'str',
        'success': 'bool',
        'time_created': 'datetime',
        'time_last_updated': 'datetime'
    }

    attribute_map = {
        'id': 'id',
        'status': 'status',
        'success': 'success',
        'time_created': 'time_created',
        'time_last_updated': 'time_last_updated'
    }

    def __init__(self, id=None, status=None, success=None, time_created=None, time_last_updated=None, local_vars_configuration=None):  # noqa: E501
        """BatchDeploymentRequestList - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._status = None
        self._success = None
        self._time_created = None
        self._time_last_updated = None
        self.discriminator = None

        self.id = id
        self.status = status
        self.success = success
        self.time_created = time_created
        self.time_last_updated = time_last_updated

    @property
    def id(self):
        """Gets the id of this BatchDeploymentRequestList.  # noqa: E501


        :return: The id of this BatchDeploymentRequestList.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this BatchDeploymentRequestList.


        :param id: The id of this BatchDeploymentRequestList.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def status(self):
        """Gets the status of this BatchDeploymentRequestList.  # noqa: E501


        :return: The status of this BatchDeploymentRequestList.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this BatchDeploymentRequestList.


        :param status: The status of this BatchDeploymentRequestList.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and status is None:  # noqa: E501
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501
        allowed_values = ["pending", "processing", "completed", "failed"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and status not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def success(self):
        """Gets the success of this BatchDeploymentRequestList.  # noqa: E501


        :return: The success of this BatchDeploymentRequestList.  # noqa: E501
        :rtype: bool
        """
        return self._success

    @success.setter
    def success(self, success):
        """Sets the success of this BatchDeploymentRequestList.


        :param success: The success of this BatchDeploymentRequestList.  # noqa: E501
        :type: bool
        """

        self._success = success

    @property
    def time_created(self):
        """Gets the time_created of this BatchDeploymentRequestList.  # noqa: E501


        :return: The time_created of this BatchDeploymentRequestList.  # noqa: E501
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """Sets the time_created of this BatchDeploymentRequestList.


        :param time_created: The time_created of this BatchDeploymentRequestList.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and time_created is None:  # noqa: E501
            raise ValueError("Invalid value for `time_created`, must not be `None`")  # noqa: E501

        self._time_created = time_created

    @property
    def time_last_updated(self):
        """Gets the time_last_updated of this BatchDeploymentRequestList.  # noqa: E501


        :return: The time_last_updated of this BatchDeploymentRequestList.  # noqa: E501
        :rtype: datetime
        """
        return self._time_last_updated

    @time_last_updated.setter
    def time_last_updated(self, time_last_updated):
        """Sets the time_last_updated of this BatchDeploymentRequestList.


        :param time_last_updated: The time_last_updated of this BatchDeploymentRequestList.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and time_last_updated is None:  # noqa: E501
            raise ValueError("Invalid value for `time_last_updated`, must not be `None`")  # noqa: E501

        self._time_last_updated = time_last_updated

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
        if not isinstance(other, BatchDeploymentRequestList):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BatchDeploymentRequestList):
            return True

        return self.to_dict() != other.to_dict()
