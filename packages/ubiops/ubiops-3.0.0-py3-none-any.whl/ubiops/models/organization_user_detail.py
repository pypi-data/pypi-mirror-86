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


class OrganizationUserDetail(object):
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
        'email': 'str',
        'name': 'str',
        'surname': 'str',
        'status': 'str',
        'admin': 'bool'
    }

    attribute_map = {
        'id': 'id',
        'email': 'email',
        'name': 'name',
        'surname': 'surname',
        'status': 'status',
        'admin': 'admin'
    }

    def __init__(self, id=None, email=None, name=None, surname=None, status=None, admin=None, local_vars_configuration=None):  # noqa: E501
        """OrganizationUserDetail - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._email = None
        self._name = None
        self._surname = None
        self._status = None
        self._admin = None
        self.discriminator = None

        self.id = id
        self.email = email
        if name is not None:
            self.name = name
        if surname is not None:
            self.surname = surname
        if status is not None:
            self.status = status
        if admin is not None:
            self.admin = admin

    @property
    def id(self):
        """Gets the id of this OrganizationUserDetail.  # noqa: E501


        :return: The id of this OrganizationUserDetail.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this OrganizationUserDetail.


        :param id: The id of this OrganizationUserDetail.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                id is not None and len(id) < 1):
            raise ValueError("Invalid value for `id`, length must be greater than or equal to `1`")  # noqa: E501

        self._id = id

    @property
    def email(self):
        """Gets the email of this OrganizationUserDetail.  # noqa: E501


        :return: The email of this OrganizationUserDetail.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this OrganizationUserDetail.


        :param email: The email of this OrganizationUserDetail.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and email is None:  # noqa: E501
            raise ValueError("Invalid value for `email`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                email is not None and len(email) < 1):
            raise ValueError("Invalid value for `email`, length must be greater than or equal to `1`")  # noqa: E501

        self._email = email

    @property
    def name(self):
        """Gets the name of this OrganizationUserDetail.  # noqa: E501


        :return: The name of this OrganizationUserDetail.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this OrganizationUserDetail.


        :param name: The name of this OrganizationUserDetail.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def surname(self):
        """Gets the surname of this OrganizationUserDetail.  # noqa: E501


        :return: The surname of this OrganizationUserDetail.  # noqa: E501
        :rtype: str
        """
        return self._surname

    @surname.setter
    def surname(self, surname):
        """Sets the surname of this OrganizationUserDetail.


        :param surname: The surname of this OrganizationUserDetail.  # noqa: E501
        :type: str
        """

        self._surname = surname

    @property
    def status(self):
        """Gets the status of this OrganizationUserDetail.  # noqa: E501


        :return: The status of this OrganizationUserDetail.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this OrganizationUserDetail.


        :param status: The status of this OrganizationUserDetail.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def admin(self):
        """Gets the admin of this OrganizationUserDetail.  # noqa: E501


        :return: The admin of this OrganizationUserDetail.  # noqa: E501
        :rtype: bool
        """
        return self._admin

    @admin.setter
    def admin(self, admin):
        """Sets the admin of this OrganizationUserDetail.


        :param admin: The admin of this OrganizationUserDetail.  # noqa: E501
        :type: bool
        """

        self._admin = admin

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
        if not isinstance(other, OrganizationUserDetail):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrganizationUserDetail):
            return True

        return self.to_dict() != other.to_dict()
