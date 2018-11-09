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

    DEFAULT_CONFIG = {}

    def __init__(self, varset, output_dir):
        self._vars = varset
        self._output_dir = output_dir
        self._display = Display()
        self._display.v('Loading plugin %s' % self.NAME)
        self._template = Template()
        self._site_config = SiteConfig()
        self.build_config()

    def build_config(self):
        '''
        Build the plugin config
        '''
        self._plugin_config = self.DEFAULT_CONFIG.copy()
        # Helper var to tidy up the code
        self._fields = self._plugin_config['fields']
        # Convert field definitions into PluginField objects
        for section in self._fields:
            section_fields = self._fields[section]
            for k, v in section_fields.items():
                section_fields[k] = PluginField(k, v)
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
                            # Update existing field config or create new
                            if field_name in self._fields[section]:
                                self._fields[section][field_name].update_config(field)
                            else:
                                self._fields[section][field_name] = PluginField(field_name, field)
                else:
                    if k in self._plugin_config:
                        if isinstance(v, (list, dict)):
                            self._plugin_config[k] = v.copy()
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
        if self._section in self._fields and field in self._fields[self._section]:
            return True
        return False

    def get_required_fields(self):
        ret = []
        if self._section in self._fields:
            for k, v in self._fields[self._section].items():
                if v.required and v.default is None:
                    ret.append(k)
        return ret

    def is_field_locked(self, field):
        if self._section in self._fields and field in self._fields[self._section]:
            if self._fields[self._section][field].locked:
                return True
        return False

    def is_needed(self, app):
        # We aren't needed if we're marked as disabled (enabled: False)
        if self._plugin_config.get('enabled', True) is False:
            return False
        # We aren't needed if we have no fields for the current section
        if self._section not in self._fields:
            return False
        # We are needed if we're the configured default plugin
        if self._site_config.default_output == self.NAME:
            return True
        return True

    def merge_with_field_defaults(self, app):
        '''
        Merge user-provided values with configured field defaults
        '''
        ret = {}
        # Apply defaults
        for field, value in self._fields[self._section].items():
            ret[field] = value.apply_default(app.get(field, None))
        return ret

    def validate_fields(self, app):
        # Check that all required fields are provided
        req_fields = self.get_required_fields()
        for field in req_fields:
            if field not in app:
                raise DeployConfigError("required field '%s' not defined" % field)
        # Check field/subfield types and if field is locked
        for field, value in app.items():
            if self.has_field(field):
                if self.is_field_locked(field):
                    raise DeployConfigError("the field '%s' has been locked by the plugin config and cannot be overridden" % field)
                self._fields[self._section][field].validate(value)

    def generate(self, app, index):
        try:
            path = os.path.join(self._output_dir, '%s-%03d%s' % (self.NAME, index, self.FILE_EXT))
            # Build vars for template
            # changes
            app_vars = {
                'PLUGIN_NAME': self.NAME,
                'APP_INDEX': index,
                'OUTPUT_FILE': os.path.basename(path),
                'OUTPUT_PATH': path,
                # Plugin config
                'CONFIG': self._plugin_config.copy(),
                # App config
                'APP': self.merge_with_field_defaults(app),
                # Parsed vars
                'VARS': dict(self._vars),
            }
            output = self.generate_output(app_vars)
            self._display.v('Writing output file %s' % path)
            with open(path, 'w') as f:
                f.write(output)
        except Exception as e:
            show_traceback(self._display.get_verbosity())
            raise DeployConfigGenerationError(str(e))

    def generate_output(self, app_vars):
        output = self._template.render_template(inspect.cleandoc(self.TEMPLATE), app_vars)
        return output


class PluginField(object):

    _name = None
    _config = None
    _parent = None

    BASE_CONFIG = {
        # Whether field is required
        'required': False,
        # Default value
        'default': None,
        # Whether field is locked (value cannot be provided by user)
        'locked': False,
        # Expected type for field
        'type': None,
        # Expected type for sub-items (for lists)
        'subtype': None,
        # How to combine defaults (for lists)
        # * None - no combining, user value replaces default
        # * 'append' - default value is included at end of list
        # * 'prepend' - default value is included at beginning of list
        'default_action': None,
        # Field definitions (for dicts)
        'fields': None,
    }

    def __init__(self, name, config, parent=None):
        self._name = name
        self._parent = parent
        self._config = self.BASE_CONFIG.copy()
        self._config.update(config)
        self.convert_fields()

    def __getattr__(self, key, default=None):
        return self._config.get(key, default)

    __getitem__ = __getattr__
    get = __getattr__

    def __contains__(self, key):
        return (key in self._config)

    def __str__(self):
        return '<PluginField name=%s config=%s>' % (self._name, self._config)

    __repr__ = __str__

    def convert_fields(self):
        if self._config['fields'] is not None:
            for k, v in self._config['fields'].items():
                self._config['fields'][k] = PluginField(k, v, parent=self)

    def update_config(self, config):
        '''
        Deep merge field attributes from site config with current config
        '''
        for k, v in config.items():
            if k == 'fields':
                for field_name, field in v.items():
                    # Update existing field config or create new
                    if field_name in self.fields:
                        self.fields[field_name].update_config(field)
                    else:
                        self.fields[field_name] = PluginField(field_name, field, parent=self)
            else:
                if isinstance(v, dict):
                    if self._config[k] is None:
                        self._config[k] = {}
                    self._config[k].update(v)
                elif isinstance(v, list):
                    self._config[k] = v.copy()
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

    def validate_check_type(self, value):
        '''
        Determine the type of the passed value
        '''
        if isinstance(value, six.string_types):
            return 'str'
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
        raise DeployConfigError('unsupported type: %s' % type(value))

    def validate(self, value, use_subtype=False):
        '''
        Validate passed value against field config
        '''
        value_type = self.validate_check_type(value)
        field_type = self.type
        if use_subtype:
            # Use the field subtype
            field_type = self.subtype
        # Nothing to validate if no field type is specified
        if field_type is None:
            return
        if value_type != field_type:
            raise DeployConfigError("value for field '%s' is wrong type, expected '%s' and got: %s" % (self.get_full_name(), field_type, value_type))
        if field_type == 'list' and self.subtype is not None:
            # Validate each list item separately if a field subtype is specified
            for value_item in value:
                # Use field's subtype for list items
                self.validate(value_item, use_subtype=True)
        else:
            # Recursively validate sub-field values
            if field_type == 'dict' and self.fields is not None:
                for k, v in value.items():
                    if k not in self.fields:
                        raise DeployConfigError("unknown key in field '%s': %s" % (self.get_full_name(), k))
                    self.fields[k].validate(v)

    def apply_default_list(self, value, field_type):
        '''
        Apply default values for a list
        '''
        ret = []
        if self.subtype is not None:
            if value:
                for value_item in value:
                    new_val = self.apply_default(value_item, use_subtype=True)
                    if new_val is not None:
                        ret.append(new_val)
        if self.default is not None:
            # User values go after default value
            if self.default_action == 'prepend':
                ret.insert(0, self.default)
            # User values go before default value
            elif self.default_action == 'append':
                ret.append(self.default)
        return ret

    def apply_default(self, value, use_subtype=False):
        '''
        Apply default values
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
            for field in self.fields:
                ret[field] = self.fields[field].apply_default(value.get(field, None))
        else:
            # Use default if no value was provided
            if value is None:
                ret = self.default
            else:
                ret = value
        return ret
