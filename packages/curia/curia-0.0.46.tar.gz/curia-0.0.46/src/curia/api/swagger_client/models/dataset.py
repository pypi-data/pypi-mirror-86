# coding: utf-8

"""
    Curia Platform API

    These are the docs for the curia platform API. To test, generate an authorization token first.  # noqa: E501

    OpenAPI spec version: 0.0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Dataset(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'name': 'str',
        'description': 'str',
        'type': 'str',
        'location': 'str',
        'file_content_type': 'str',
        'file_size': 'str',
        'athena_execution_id': 'str',
        'dataset_results': 'object',
        'organization_id': 'str',
        'model_datasets': 'list[ModelDataset]',
        'model_jobs': 'list[ModelJob]',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'version': 'float'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'description': 'description',
        'type': 'type',
        'location': 'location',
        'file_content_type': 'fileContentType',
        'file_size': 'fileSize',
        'athena_execution_id': 'athenaExecutionId',
        'dataset_results': 'datasetResults',
        'organization_id': 'organizationId',
        'model_datasets': 'modelDatasets',
        'model_jobs': 'modelJobs',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'version': 'version'
    }

    def __init__(self, id=None, name=None, description=None, type=None, location=None, file_content_type=None, file_size=None, athena_execution_id=None, dataset_results=None, organization_id=None, model_datasets=None, model_jobs=None, created_at=None, updated_at=None, version=None):  # noqa: E501
        """Dataset - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._name = None
        self._description = None
        self._type = None
        self._location = None
        self._file_content_type = None
        self._file_size = None
        self._athena_execution_id = None
        self._dataset_results = None
        self._organization_id = None
        self._model_datasets = None
        self._model_jobs = None
        self._created_at = None
        self._updated_at = None
        self._version = None
        self.discriminator = None
        if id is not None:
            self.id = id
        self.name = name
        self.description = description
        self.type = type
        if location is not None:
            self.location = location
        if file_content_type is not None:
            self.file_content_type = file_content_type
        self.file_size = file_size
        if athena_execution_id is not None:
            self.athena_execution_id = athena_execution_id
        self.dataset_results = dataset_results
        if organization_id is not None:
            self.organization_id = organization_id
        if model_datasets is not None:
            self.model_datasets = model_datasets
        if model_jobs is not None:
            self.model_jobs = model_jobs
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        if version is not None:
            self.version = version

    @property
    def id(self):
        """Gets the id of this Dataset.  # noqa: E501


        :return: The id of this Dataset.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Dataset.


        :param id: The id of this Dataset.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Dataset.  # noqa: E501


        :return: The name of this Dataset.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Dataset.


        :param name: The name of this Dataset.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this Dataset.  # noqa: E501


        :return: The description of this Dataset.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Dataset.


        :param description: The description of this Dataset.  # noqa: E501
        :type: str
        """
        if description is None:
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501

        self._description = description

    @property
    def type(self):
        """Gets the type of this Dataset.  # noqa: E501


        :return: The type of this Dataset.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Dataset.


        :param type: The type of this Dataset.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def location(self):
        """Gets the location of this Dataset.  # noqa: E501


        :return: The location of this Dataset.  # noqa: E501
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """Sets the location of this Dataset.


        :param location: The location of this Dataset.  # noqa: E501
        :type: str
        """

        self._location = location

    @property
    def file_content_type(self):
        """Gets the file_content_type of this Dataset.  # noqa: E501


        :return: The file_content_type of this Dataset.  # noqa: E501
        :rtype: str
        """
        return self._file_content_type

    @file_content_type.setter
    def file_content_type(self, file_content_type):
        """Sets the file_content_type of this Dataset.


        :param file_content_type: The file_content_type of this Dataset.  # noqa: E501
        :type: str
        """

        self._file_content_type = file_content_type

    @property
    def file_size(self):
        """Gets the file_size of this Dataset.  # noqa: E501


        :return: The file_size of this Dataset.  # noqa: E501
        :rtype: str
        """
        return self._file_size

    @file_size.setter
    def file_size(self, file_size):
        """Sets the file_size of this Dataset.


        :param file_size: The file_size of this Dataset.  # noqa: E501
        :type: str
        """
        if file_size is None:
            raise ValueError("Invalid value for `file_size`, must not be `None`")  # noqa: E501

        self._file_size = file_size

    @property
    def athena_execution_id(self):
        """Gets the athena_execution_id of this Dataset.  # noqa: E501


        :return: The athena_execution_id of this Dataset.  # noqa: E501
        :rtype: str
        """
        return self._athena_execution_id

    @athena_execution_id.setter
    def athena_execution_id(self, athena_execution_id):
        """Sets the athena_execution_id of this Dataset.


        :param athena_execution_id: The athena_execution_id of this Dataset.  # noqa: E501
        :type: str
        """

        self._athena_execution_id = athena_execution_id

    @property
    def dataset_results(self):
        """Gets the dataset_results of this Dataset.  # noqa: E501


        :return: The dataset_results of this Dataset.  # noqa: E501
        :rtype: object
        """
        return self._dataset_results

    @dataset_results.setter
    def dataset_results(self, dataset_results):
        """Sets the dataset_results of this Dataset.


        :param dataset_results: The dataset_results of this Dataset.  # noqa: E501
        :type: object
        """
        if dataset_results is None:
            raise ValueError("Invalid value for `dataset_results`, must not be `None`")  # noqa: E501

        self._dataset_results = dataset_results

    @property
    def organization_id(self):
        """Gets the organization_id of this Dataset.  # noqa: E501


        :return: The organization_id of this Dataset.  # noqa: E501
        :rtype: str
        """
        return self._organization_id

    @organization_id.setter
    def organization_id(self, organization_id):
        """Sets the organization_id of this Dataset.


        :param organization_id: The organization_id of this Dataset.  # noqa: E501
        :type: str
        """

        self._organization_id = organization_id

    @property
    def model_datasets(self):
        """Gets the model_datasets of this Dataset.  # noqa: E501


        :return: The model_datasets of this Dataset.  # noqa: E501
        :rtype: list[ModelDataset]
        """
        return self._model_datasets

    @model_datasets.setter
    def model_datasets(self, model_datasets):
        """Sets the model_datasets of this Dataset.


        :param model_datasets: The model_datasets of this Dataset.  # noqa: E501
        :type: list[ModelDataset]
        """

        self._model_datasets = model_datasets

    @property
    def model_jobs(self):
        """Gets the model_jobs of this Dataset.  # noqa: E501


        :return: The model_jobs of this Dataset.  # noqa: E501
        :rtype: list[ModelJob]
        """
        return self._model_jobs

    @model_jobs.setter
    def model_jobs(self, model_jobs):
        """Sets the model_jobs of this Dataset.


        :param model_jobs: The model_jobs of this Dataset.  # noqa: E501
        :type: list[ModelJob]
        """

        self._model_jobs = model_jobs

    @property
    def created_at(self):
        """Gets the created_at of this Dataset.  # noqa: E501


        :return: The created_at of this Dataset.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Dataset.


        :param created_at: The created_at of this Dataset.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this Dataset.  # noqa: E501


        :return: The updated_at of this Dataset.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this Dataset.


        :param updated_at: The updated_at of this Dataset.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def version(self):
        """Gets the version of this Dataset.  # noqa: E501


        :return: The version of this Dataset.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Dataset.


        :param version: The version of this Dataset.  # noqa: E501
        :type: float
        """

        self._version = version

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(Dataset, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Dataset):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
