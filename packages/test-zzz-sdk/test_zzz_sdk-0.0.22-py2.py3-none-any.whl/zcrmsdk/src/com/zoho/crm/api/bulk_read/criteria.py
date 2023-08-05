try:
	from zcrmsdk.src.com.zoho.crm.api.exception import SDKException
	from zcrmsdk.src.com.zoho.crm.api.util import Choice, Constants
except Exception:
	from ..exception import SDKException
	from ..util import Choice, Constants


class Criteria(object):
	def __init__(self):
		"""Creates an instance of Criteria"""

		self.__api_name = None
		self.__value = None
		self.__group_operator = None
		self.__group = None
		self.__comparator = None
		self.__key_modified = dict()

	def get_api_name(self):
		"""
		The method to get the api_name

		Returns:
			string: A string representing the api_name
		"""

		return self.__api_name

	def set_api_name(self, api_name):
		"""
		The method to set the value to api_name

		Parameters:
			api_name (string) : A string representing the api_name
		"""

		if api_name is not None and not isinstance(api_name, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: api_name EXPECTED TYPE: str', None, None)
		
		self.__api_name = api_name
		self.__key_modified['api_name'] = 1

	def get_value(self):
		"""
		The method to get the value

		Returns:
			Object: A Object representing the value
		"""

		return self.__value

	def set_value(self, value):
		"""
		The method to set the value to value

		Parameters:
			value (Object) : A Object representing the value
		"""

		self.__value = value
		self.__key_modified['value'] = 1

	def get_group_operator(self):
		"""
		The method to get the group_operator

		Returns:
			Choice: An instance of Choice
		"""

		return self.__group_operator

	def set_group_operator(self, group_operator):
		"""
		The method to set the value to group_operator

		Parameters:
			group_operator (Choice) : An instance of Choice
		"""

		if group_operator is not None and not isinstance(group_operator, Choice):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: group_operator EXPECTED TYPE: Choice', None, None)
		
		self.__group_operator = group_operator
		self.__key_modified['group_operator'] = 1

	def get_group(self):
		"""
		The method to get the group

		Returns:
			list: An instance of list
		"""

		return self.__group

	def set_group(self, group):
		"""
		The method to set the value to group

		Parameters:
			group (list) : An instance of list
		"""

		if group is not None and not isinstance(group, list):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: group EXPECTED TYPE: list', None, None)
		
		self.__group = group
		self.__key_modified['group'] = 1

	def get_comparator(self):
		"""
		The method to get the comparator

		Returns:
			Choice: An instance of Choice
		"""

		return self.__comparator

	def set_comparator(self, comparator):
		"""
		The method to set the value to comparator

		Parameters:
			comparator (Choice) : An instance of Choice
		"""

		if comparator is not None and not isinstance(comparator, Choice):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: comparator EXPECTED TYPE: Choice', None, None)
		
		self.__comparator = comparator
		self.__key_modified['comparator'] = 1

	def is_key_modified(self, key):
		"""
		The method to check if the user has modified the given key

		Parameters:
			key (string) : A string representing the key

		Returns:
			int: An int representing the modification
		"""

		if key is not None and not isinstance(key, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: key EXPECTED TYPE: str', None, None)
		
		if key in self.__key_modified:
			return self.__key_modified.get(key)
		
		return None

	def set_key_modified(self, key, modification):
		"""
		The method to mark the given key as modified

		Parameters:
			key (string) : A string representing the key
			modification (int) : An int representing the modification
		"""

		if key is not None and not isinstance(key, str):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: key EXPECTED TYPE: str', None, None)
		
		if modification is not None and not isinstance(modification, int):
			raise SDKException(Constants.DATA_TYPE_ERROR, 'KEY: modification EXPECTED TYPE: int', None, None)
		
		self.__key_modified[key] = modification
