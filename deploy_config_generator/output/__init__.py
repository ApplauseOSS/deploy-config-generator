import copy
import inspect
import os.path
import six

from deploy_config_generator.site_config import SiteConfig
from deploy_config_generator.display import Display
from deploy_config_generator.template import Template
from deploy_config_generator.errors import DeployConfigGenerationError, DeployConfigError, ConfigError
from deploy_config_generator.utils import show_traceback


class OutputPluginBase(object):

    '''
    Base class for output plugins
    '''

    _vars = None
    _output_dir = None
    _display = None
    _section = None
    _plugin_config = None
    _fields = None
    _config_version = None

    COMMON_DEFAULT_CONFIG = dict(
        enabled=True,
    )
    PRIORITY = 1

    def __init__(self, varset, output_dir, config_version):
        self._vars = varset
        self._output_dir = output_dir
        self._display = Display()
        self._template = Template()
        self._site_config = SiteConfig()
        self._config_version = config_version
        self.build_config()

    # Comparison functions for sorting plugins
    # Sort first by priority and then by name (for consistency)
    def __lt__(self, other):
        return (self.PRIORITY < other.PRIORITY or (self.PRIORITY == other.PRIORITY and self.NAME < other.NAME))

    def __gt__(self, other):
        return (self.PRIORITY > other.PRIORITY or (self.PRIORITY == other.PRIORITY and self.NAME > other.NAME))

    def __le__(self, other):
        return (self.PRIORITY <= other.PRIORITY or (self.PRIORITY == other.PRIORITY and self.NAME <= other.NAME))

    def __ge__(self, other):
        return (self.PRIORITY >= other.PRIORITY or (self.PRIORITY == other.PRIORITY and self.NAME >= other.NAME))

    def __eq__(self, other):
        return (self.PRIORITY == other.PRIORITY or (self.PRIORITY == other.PRIORITY and self.NAME == other.NAME))

    def __ne__(self, other):
        return (self.PRIORITY != other.PRIORITY or (self.PRIORITY == other.PRIORITY and self.NAME != other.NAME))

    def build_config(self):
        '''
        Build the plugin config
        '''
        self._plugin_config = self.COMMON_DEFAULT_CONFIG.copy()
        self._plugin_config.update(self.DEFAULT_CONFIG)
        # Helper var to tidy up the code
        self._fields = copy.deepcopy(self._plugin_config['fields'])
        # Convert field definitions into PluginField objects
        for section in self._fields:
            section_fields = self._fields[section]
            for k, v in section_fields.items():
                section_fields[k] = PluginField(k, v, self._config_version, self._template)
        self.build_config_site()

    def build_config_site(self):
        '''
        Merge in plugin config values from site config
        This will also do a deep merge of deeply nested field definitions
        '''
        if self.NAME in self._site_config.plugins:
            for k, v in self._site_config['plugins'][self.NAME].items():
                if k == 'fields':
                    for section in v:
                        for field_name, field in v[section].items():
                            # Create section if it doesn't exist
                            if section not in self._fields:
                                self._fields[section] = {}
                            # Update existing field config or create new
                            if field_name in self._fields[section]:
                                self._fields[section][field_name].update_config(field)
                            else:
                                self._fields[section][field_name] = PluginField(field_name, field, self._config_version, self._template)
                else:
                    if k in self._plugin_config:
                        if isinstance(v, dict):
                            self._plugin_config[k] = v.copy()
                        elif isinstance(v, list):
                            self._plugin_config[k] = v[:]
                        else:
                            self._plugin_config[k] = v
                    else:
                        raise ConfigError('unrecognized config option: %s' % k)

    def set_section(self, section):
        '''
        Sets the active section of the deploy config

        This is used to figure out which set of fields to process
        '''
        self._section = section

    def has_field(self, field):
        '''
        Check if a field exists in the current section for this plugin
        '''
        if self._section in self._fields and field in self._fields[self._section]:
            if self._fields[self._section][field].is_valid_for_config_version():
                return True
        return False

    def get_required_fields(self):
        '''
        Return a list of fields in the current section with required=True
        '''
        ret = []
        if self._section in self._fields:
            for k, v in self._fields[self._section].items():
                if v.required and v.default is None and v.is_valid_for_config_version():
                    ret.append(k)
        return ret

    def is_field_locked(self, field):
        '''
        Check if a field has been marked as 'locked' (cannot be overridden by user)
        '''
        if self._section in self._fields and field in self._fields[self._section]:
            if self._fields[self._section][field].locked:
                return True
        return False

    def is_needed(self, app):
        '''
        Determine whether this plugin is needed based on the provided deploy config
        '''
        # We aren't needed if we're marked as disabled (enabled: False)
        if self._plugin_config.get('enabled', True) is False:
            return False
        # We aren't needed if we have no fields for the current section
        if self._section not in self._fields:
            return False
        # We are needed if we're the configured default plugin
        if self._site_config.default_output == self.NAME:
            return True
        # Check if any of our required top-level fields are provided
        for field in self.get_required_fields():
            if field in app:
                return True
        # If nothing above matched, then we're probably not needed
        return False

    def merge_with_field_defaults(self, app):
        '''
        Merge user-provided values with configured field defaults
        '''
        ret = {}
        # Apply defaults/transforms
        for field, value in self._fields[self._section].items():
            ret[field] = value.apply_default(app.get(field, None))
            ret[field] = value.apply_transform(ret.get(field, None))
        return ret

    def validate_fields(self, app):
        '''
        Validate the provided app config against plugin field definitions
        '''
        # Check that all required top-level fields are provided
        req_fields = self.get_required_fields()
        for field in req_fields:
            if field not in app:
                raise DeployConfigError("required field '%s' not defined" % field)
        # Check field/subfield types, required, and if field is locked
        unmatched = []
        for field, value in app.items():
            if self.has_field(field):
                if self.is_field_locked(field):
                    raise DeployConfigError("the field '%s' has been locked by the plugin config and cannot be overridden" % field)
                field_unmatched = self._fields[self._section][field].validate(value)
                unmatched.extend(field_unmatched)
            else:
                unmatched.append(field)
        return unmatched

    def generate(self, config):
        '''
        Write out the generated config to disk
        '''
        try:
            for section in config:
                if section in self._fields:
                    self.set_section(section)
                    for idx, app in enumerate(config[section]):
                        # We want a 1-based index for the output files
                        index = idx + 1
                        if self.is_needed(app):
                            path = os.path.join(self._output_dir, '%s-%03d%s' % (self.NAME, index, self.FILE_EXT))
                            # Build vars for template
                            app_vars = {
                                'PLUGIN_NAME': self.NAME,
                                'APP_INDEX': index,
                                'OUTPUT_FILE': os.path.basename(path),
                                'OUTPUT_PATH': path,
                                # App config
                                'APP': self.merge_with_field_defaults(app),
                                # Parsed vars
                                'VARS': dict(self._vars),
                            }
                            # Check conditionals
                            for field, value in self._fields[self._section].items():
                                app_vars['APP'][field] = value.check_conditionals(app_vars['APP'].get(field, None), app_vars)
                            # Generate output
                            output = self.generate_output(app_vars)
                            self._display.v('Writing output file %s' % path)
                            with open(path, 'w') as f:
                                f.write(output)
        except Exception as e:
            show_traceback(self._display.get_verbosity())
            raise DeployConfigGenerationError(str(e))

    def generate_output(self, app_vars):
        '''
        Generate output content

        By default, this renders the Jinja template defined in the 'TEMPLATE'
        class var. However, it can be overridden by an output plugin to provide
        a custom method for generating the output.
        '''
        output = self._template.render_template(inspect.cleandoc(self.TEMPLATE), app_vars)
        return output


class PluginField(object):

    '''
    Class representing a field from a deploy config that's supported by an output
    plugin
    '''

    _name = None
    _config = None
    _parent = None
    _config_version = None

    BASE_CONFIG = {
        # Whether field is required
        'required': False,
        # Default value
        'default': None,
        # Whether field is locked (value cannot be provided by user)
        'locked': False,
        # Expected type for field
        'type': None,
        # Transformation (for strings)
        # This should be a dict containing one of the following keys:
        # * prefix - prefix to add to value
        # * suffix - suffix to add to value
        'transform': None,
        # Expected type for sub-items (for lists)
        'subtype': None,
        # How to combine defaults
        # * None - no combining, user value replaces default
        # * 'append' - default value is included at end of list
        # * 'prepend' - default value is included at beginning of list
        # * 'merge' - user value is merged with default value (for lists/dicts)
        'default_action': None,
        # Key to use for merging (for lists of dicts)
        'merge_key': None,
        # Minimum/maximum config version that field is valid for
        'min_version': None,
        'max_version': None,
        # Field definitions (for dicts)
        'fields': None,
        # Whether the field supports a conditional (for dicts)
        'conditional': False,
        # Field name to use for conditional
        'conditional_key': 'condition',
        # Loop var (for use in conditionals)
        'loop_var': 'item',
    }

    def __init__(self, name, config, config_version, template, parent=None):
        self._name = name
        self._parent = parent
        self._config_version = config_version
        self._template = template
        self._config = self.BASE_CONFIG.copy()
        if config is not None:
            self._config.update(copy.deepcopy(config))
        self.convert_fields()

    def __getattr__(self, key, default=None):
        return self._config.get(key, default)

    __getitem__ = __getattr__
    get = __getattr__

    def __setattr__(self, key, value):
        if self._config is not None and key in self._config:
            self._config[key] = value
        else:
            super(PluginField, self).__setattr__(key, value)

    def __contains__(self, key):
        return (key in self._config)

    def __str__(self):
        return '<PluginField name=%s config=%s>' % (self._name, self._config)

    __repr__ = __str__

    def is_valid_for_config_version(self):
        '''
        Compare min/max version for field to config version
        '''
        if self._config_version is None:
            return True
        if self._config['min_version'] is not None:
            if float(self._config_version) < float(self._config['min_version']):
                return False
        if self._config['max_version'] is not None:
            if float(self._config_version) > float(self._config['max_version']):
                return False
        return True

    def convert_fields(self):
        '''
        Replace items in 'fields' dict with PluginField objects
        '''
        if self._config['fields'] is not None:
            for k, v in self._config['fields'].items():
                self._config['fields'][k] = PluginField(k, v, self._config_version, self._template, parent=self)

    def update_config(self, config):
        '''
        Deep merge field attributes from site config with current config
        '''
        for k, v in config.items():
            if k == 'fields':
                for field_name, field in v.items():
                    # Update existing field config or create new
                    if self.fields is not None and field_name in self.fields:
                        self.fields[field_name].update_config(field)
                    else:
                        if self.fields is None:
                            self.fields = {}
                        self.fields[field_name] = PluginField(field_name, field, self._config_version, self._template, parent=self)
            else:
                if isinstance(v, dict):
                    if self._config[k] is None:
                        self._config[k] = {}
                    self._config[k].update(v)
                elif isinstance(v, list):
                    self._config[k] = v[:]
                else:
                    self._config[k] = v

    def get_full_name(self):
        '''
        Construct full name of field from parent(s)

        This is used when generating exceptions
        '''
        field_name = self._name
        parent = self._parent
        while parent is not None:
            field_name = '%s.%s' % (parent._name, field_name)
            parent = parent._parent
        return field_name

    def convert_bool(self, value):
        if value in ('true', 'True', 'yes', 'on'):
            return True
        if value in ('false', 'False', 'no', 'off'):
            return False
        return None

    def validate_check_type(self, value, expected_type=None):
        '''
        Determine the type of the passed value
        '''
        if isinstance(value, list):
            return 'list'
        if isinstance(value, dict):
            return 'dict'
        if isinstance(value, bool):
            return 'bool'
        if isinstance(value, six.integer_types):
            return 'int'
        if isinstance(value, float):
            return 'float'
        if isinstance(value, six.string_types):
            # Values from variables always come in as a string, so we need special
            # logic to determine their actual type based on the field type
            try:
                if expected_type == 'float' and float(value) is not None:
                    return 'float'
                if expected_type == 'int' and int(value) is not None:
                    return 'int'
                if expected_type == 'bool' and self.convert_bool(value) is not None:
                    return 'bool'
            except Exception:
                pass
            return 'str'
        raise DeployConfigError('unsupported type: %s' % type(value))

    def validate(self, value, use_subtype=False):
        '''
        Validate passed value against field config
        '''
        unmatched = []
        if value is None:
            return unmatched
        field_type = self.type
        if use_subtype:
            # Use the field subtype
            field_type = self.subtype
        # Nothing to validate if no field type is specified
        if field_type is None:
            return unmatched
        value_type = self.validate_check_type(value, field_type)
        if value_type != field_type:
            # TODO: replace this with the ability to specify multiple types for a field
            # Hack to allow an int value to satisfy a float
            if field_type == 'float' and value_type == 'int':
                pass
            else:
                raise DeployConfigError("value for field '%s' is wrong type, expected '%s' and got: %s" % (self.get_full_name(), field_type, value_type))
        if field_type == 'list' and self.subtype is not None:
            # Validate each list item separately if a field subtype is specified
            for value_item in value:
                # Use field's subtype for list items
                item_unmatched = self.validate(value_item, use_subtype=True)
                unmatched.extend(item_unmatched)
        else:
            # Recursively validate sub-field values
            if field_type == 'dict' and self.fields is not None:
                for k, v in value.items():
                    if k not in self.fields or not self.fields[k].is_valid_for_config_version():
                        unmatched.append('%s.%s' % (self.get_full_name(), k))
                        continue
                    field_unmatched = self.fields[k].validate(v)
                    unmatched.extend(field_unmatched)
                # Check for required and locked sub-fields
                for tmp_field_name, tmp_field in self.fields.items():
                    if tmp_field.required and value.get(tmp_field_name, None) is None and tmp_field.default is None:
                        raise DeployConfigError("field '%s' is required, but no value provided" % tmp_field.get_full_name())
                    if tmp_field.locked and value.get(tmp_field_name, None) is not None:
                        raise DeployConfigError("field '%s' is locked, but a value was provided" % tmp_field.get_full_name())

        return unmatched

    def apply_transform(self, value, use_subtype=False):
        '''
        Apply transformations to string values
        '''
        if value is None:
            return value
        field_type = self.type
        if use_subtype:
            field_type = self.subtype
        value_type = self.validate_check_type(value)
        ret = None
        if value_type == 'list':
            # Apply transformations to all items in the list
            ret = []
            for value_item in value:
                ret.append(self.apply_transform(value_item, use_subtype=True))
        elif value_type == 'dict':
            ret = {}
            if self.fields is not None:
                # Recursively apply transformations to sub-fields
                for field in self.fields:
                    if field in value:
                        ret[field] = self.fields[field].apply_transform(value[field])
            else:
                ret = value
        elif value_type == 'str':
            # Convert types for values that came in from a variable (which always
            # produces a string)
            if field_type == 'bool':
                # Convert values to boolean if they're expected to be boolean
                ret = self.convert_bool(value)
            elif field_type == 'float':
                ret = float(value)
            elif field_type == 'int':
                ret = int(value)
            elif isinstance(self.transform, dict):
                if 'prefix' in self.transform:
                    ret = self.transform['prefix'] + value
                elif 'suffix' in self.transform:
                    ret = value + self.transform['suffix']
            else:
                ret = value
        else:
            if field_type == 'float' and value_type == 'int':
                # An int can satisfy a 'float' field, but we want to make sure
                # that it's a float for output
                ret = float(value)
            else:
                ret = value
        return ret

    def apply_default_list(self, value, field_type):
        '''
        Apply default values for a list (helper function)
        '''
        ret = []
        if self.subtype is not None:
            if value:
                for value_item in value:
                    new_val = self.apply_default(value_item, use_subtype=True)
                    if new_val is not None:
                        ret.append(new_val)
        else:
            if value:
                ret = value[:]
        if self.default is not None:
            def_val = self.default
            if not isinstance(def_val, list):
                def_val = [def_val]
            # User values are merged with default values
            if self.default_action == 'merge':
                # Create a copy of the default values, since we'll be modifying it
                def_val = def_val[:]
                # Iterate over user values and compare against default values
                for tmp_value in ret:
                    for idx, tmp_def_val in enumerate(def_val):
                        if self.subtype == 'dict' and self.merge_key is not None:
                            # Delete default value if the merge key value matches the current value
                            if tmp_value.get(self.merge_key, "MERGE_KEY_USER") == tmp_def_val.get(self.merge_key, "MERGE_KEY_DEFAULT"):
                                del def_val[idx]
                                break
                        else:
                            # Delete default value if it matches the current value
                            if tmp_value == tmp_def_val:
                                del def_val[idx]
                                break
                # Prepend remaining defaults to user values
                ret = def_val + ret
            # User values go after default value
            elif self.default_action == 'prepend':
                ret = def_val + ret
            # User values go before default value
            elif self.default_action == 'append':
                ret = ret + def_val
            elif not ret:
                ret = self.default
        return ret

    def apply_default(self, value, use_subtype=False):
        '''
        Apply default values from the field config
        '''
        ret = None
        field_type = self.type
        if use_subtype:
            # Use the field subtype
            field_type = self.subtype
        if field_type == 'list':
            ret = self.apply_default_list(value, field_type)
        elif field_type == 'dict':
            # Recursively apply defaults for sub-fields
            ret = {}
            if self.fields is not None:
                if value is None:
                    value = {}
                for field in self.fields:
                    ret[field] = self.fields[field].apply_default(value.get(field, None))
            else:
                # Don't apply defaults for subtype
                if use_subtype:
                    ret = value
                else:
                    if value is None:
                        ret = self.default
                    else:
                        if self.default_action == 'merge':
                            ret = self.default.copy()
                            ret.update(value)
                        else:
                            ret = value.copy()
        else:
            # Use default if no value was provided
            if value is None:
                ret = self.default
            else:
                ret = value
        return ret

    def check_conditionals(self, value, app_vars, use_subtype=False):
        '''
        Check conditionals and filter value
        '''
        ret = None
        field_type = self.type
        if use_subtype:
            # Use the field subtype
            field_type = self.subtype
        if field_type == 'list':
            ret = []
            for idx, item in enumerate(value):
                if self.loop_var:
                    # Add loop item and index vars
                    app_vars = app_vars.copy()
                    app_vars.update({self.loop_var: item, ('%s_index' % self.loop_var): idx})
                tmp_value = self.check_conditionals(item, app_vars, use_subtype=True)
                # Don't add item to returned data if its condition evaluated to False
                if tmp_value is not None:
                    ret.append(tmp_value)
        elif field_type == 'dict':
            ret = {}
            if self.fields is not None:
                if value is None:
                    value = {}
                for field in self.fields:
                    ret[field] = self.fields[field].check_conditionals(value.get(field, None), app_vars)
            else:
                ret = value
            if self.conditional and self.conditional_key in ret:
                if ret[self.conditional_key] is not None:
                    if not self._template.evaluate_condition(ret[self.conditional_key], app_vars):
                        return None
                # Remove the conditional key from the returned data
                del ret[self.conditional_key]
        else:
            ret = value
        return ret
