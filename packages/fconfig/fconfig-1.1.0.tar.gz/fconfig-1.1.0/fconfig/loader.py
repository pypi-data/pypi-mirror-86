import logging
import sys
import pkgutil
import fconfig.merger as merger

from typing import Tuple, List, TypeVar
from fconfig.config_data_object import ConfigDataObject
from fconfig.config_property import ConfigProperty
from fconfig.resolver import Resolver
from fconfig.config import Config
from fconfig.parser import Parser, Reference
from fconfig.common import ConfigException

DEFAULT_CONFIG_NAME = "config"
DEFAULT_CONFIG_FILE_NAME = "config.cfg"
DEFAULT_CONFIG_PACKAGE = "resources"
DEFAULT_GENERATED_CONFIG_PACKAGE = "config"

C = TypeVar('P', bound=Config)


class ConfigSource:

	def __init__(self, source: str, path_in_config: str=None):
		self.source = source
		self.path_in_config = path_in_config


def load_config_data(*config_source_definitions: ConfigSource, use_builder_directives=False) -> ConfigDataObject:

	config_data_list = []

	for config_source_definition in config_source_definitions:
		source = config_source_definition.source
		config_map_from_source = Parser(use_builder_directives).parse_config_source(source)

		if config_source_definition.path_in_config:
			config_map_from_source \
				= _change_config_context(config_map_from_source, config_source_definition.path_in_config)

		config_data_list.append(config_map_from_source)

	config_root = Resolver(merger.merge(config_data_list)).resolve_values()

	logging.info(config_root.get_string_for_print())

	return config_root


def get_config_sources_from_def(parent_config: List[Tuple[C, str]]) -> List[ConfigSource]:
	config_sources: List[ConfigSource] = []
	for config_info in parent_config:
		config_source = get_master_config_content(generated_config=config_info[0], path_in_config=config_info[1])
		config_sources.append(config_source)

	return config_sources


def get_master_config_content(package: str=None, generated_config: C=None, path_in_config: str=None) -> ConfigSource:
	if not package:
		class_module: str = generated_config.__module__
		class_package = '.'.join(class_module.split('.')[:-1])
		package = class_package.replace(DEFAULT_GENERATED_CONFIG_PACKAGE, DEFAULT_CONFIG_PACKAGE)
	content = get_config_content_from_resource(package, DEFAULT_CONFIG_NAME, path_in_config)
	return content


def get_config_content_from_resource(package: str, config_name: str = DEFAULT_CONFIG_FILE_NAME, path_in_config: str=None) -> ConfigSource:
	"""
	Load config from project resources. The location is determined by the package param
	@param package: Determines the location where the config file is stored starting with the root package
	@param config_name: The name of the config file. Defaults to config.cfg
	@param path_in_config: The name of this config  inside the top level config
	@return:
	"""

	config_filename = "{}.cfg".format(config_name)

	try:
		resource = pkgutil.get_data(package, config_filename)
		if resource:
			content = resource.decode("utf-8").split("\n")
		else:
			logging.critical("Config file %s cannot be loaded from resource path: %s", config_filename, package)
			raise ConfigException("Config file cannot be loaded", "{}/{}".format(package, config_filename))

		config_source = ConfigSource(content, path_in_config)
		return config_source
	except FileNotFoundError as e:
		logging.critical("Config file %s cannot be found in resource path: %s", config_filename, package)
		raise ConfigException("Config file not found", "{}/{}".format(package, config_filename))


def _change_config_context(config_map_from_source: ConfigDataObject, path: str):

	def add_prefix(config_property: ConfigProperty, object_name: str):
		for token in config_property.value:
			if isinstance(token, Reference):
				token.add_prefix(object_name)

	for object_name in reversed(path.split(".")):

		# add prefix to all variables path_in_config
		config_map_from_source.iterate_properties(lambda x: len(x) > 1, add_prefix, object_name)

		# move object to new parent
		parent_map = ConfigDataObject(False)
		parent_map.put(object_name, ConfigDataObject(config_map_from_source.is_array, parent_map, object_name,
													 config_map_from_source.config_object))
		config_map_from_source = parent_map

	return config_map_from_source


def get_local_config_content(source: str):
	try:
		with open(source) as f:
			content = f.readlines()
	except FileNotFoundError as e:
		logging.critical("Specified file does not exist: %s", source)
		sys.exit(1)
	return content


