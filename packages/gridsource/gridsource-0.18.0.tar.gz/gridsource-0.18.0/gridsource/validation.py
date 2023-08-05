# -*- coding: utf-8 -*-

"""Validator module.
"""

import logging
import os
import re
from collections import defaultdict
from io import StringIO
from pprint import pprint

import jsonschema
import numpy as np
import pandas as pd
import pint
import pint_pandas as pintpandas
import pkg_resources
import simplejson as json
import yaml


def yamlcat(*files):
    """concat YAML files and returns a StringIO object

    files is an iterable of posibly:
      * StringIO object
      * strings:
        - YAML content (shall begin with "---")
        - path to an existing valid YAML file

    >>> f1 = StringIO('''
    ... ---
    ... _length: &length
    ...   units: mm
    ...   default: 0
    ... key1: 5
    ... ''')
    >>> f2 = '''
    ... ---
    ... key2: 15
    ... key3:
    ...   <<: *length
    ... '''
    >>> print(yamlcat(f1, f2).getvalue())
    ---
    _length: &length
      units: mm
      default: 0
    key1: 5
    key2: 15
    key3:
      <<: *length
    """
    out = StringIO()
    out.write("---")
    for i, fh in enumerate(files):
        if isinstance(fh, str):
            if fh.strip().startswith("---"):
                # YAML was passed as a text string
                fh = StringIO(fh)
            else:
                fh = open(fh)  # assume we have a path to a YAML file
        out.write(fh.read().strip().strip("---"))
        fh.close()
    out.seek(0)
    return out


def load_yaml(*files, clean=True, debug=False):
    """concatenate and load yaml files
    Wrapper for:
    * yamlcat(*files)
    * yaml.load()

    if `debug` is True, return a tuple:
        (YAML dictionnary translation, YAML concatenated file)
    otherwise, return the YAML dictionnary translation

    >>> f1 = StringIO('''
    ... ---
    ... _length: &length
    ...   units: mm
    ...   default: 0
    ... key1: 5
    ... ''')
    >>> f2 = '''
    ... ---
    ... key2: 15
    ... key3:
    ...   <<: *length
    ... key4:
    ...   <<: *length
    ...   default: 1
    ... '''
    >>> load_yaml(f1, f2) == {'key1': 5,
    ...                       'key2': 15,
    ...                       'key3': {'units': 'mm', 'default': 0},
    ...                       'key4': {'units': 'mm', 'default': 1}}
    True
    """
    src = yamlcat(*files)
    specs = yaml.load(src, Loader=yaml.FullLoader)
    if clean:
        # clean keys beginning with "_" if required
        specs = {k: v for k, v in specs.items() if not k.startswith("_")}
    if debug:
        src.seek(0)
        return specs, src.getvalue()
    return specs


# use short units
pintpandas.PintType.ureg.default_format = "~P"


class DataFrameSchematizer:
    """
    utility class to build a schema (jsonschema) for a Pandas DataFrame

    Given a DataFrame like:

    >>> df = pd.DataFrame({ "id": {7: 0, 1: 1, 2:5},
    ...                    "name": {7: "Doe", 1: "Fante", 2: "Mercury"},
    ...                    "firstname": {7: "John", 2: "Freddy", 1:"Richard"},
    ...                    "age": {7: '42', 1: 22},
    ...                    "life_nb": {7: 5, 1: 'hg', 2: 15}})

    We can build a column-wise schema:

    >>> v = DataFrameSchematizer()
    >>> v.add_column(name='id', types='integer', unique=True, mandatory=True)
    >>> v.add_column(name='name', types='string', mandatory=True)
    >>> v.add_column(name='firstname', types='string')
    >>> v.add_column(name='age', types='integer', mandatory=False, default=0)
    >>> v.add_column(name='life_nb', types='integer', mandatory=True, maximum=4)
    >>> v._is_units  # no units declared in any column
    False

    And validate the DataFrame:

    >>> df, is_valid, errors = v.validate_dataframe(df)
    >>> pprint(errors)
    {('age', 0): ["'42' is not valid under any of the given schemas",
                  "'42' is not of type 'integer'",
                  "'42' is not of type 'null'"],
     ('life_nb', 0): ['5 is greater than the maximum of 4'],
     ('life_nb', 1): ["'hg' is not of type 'integer'"],
     ('life_nb', 2): ['15 is greater than the maximum of 4']}

    The schema used for validation can be accessed by:

    >>> schema = v.build()
    >>> pprint(schema)
    {'$schema': 'http://json-schema.org/draft-07/schema#',
     'properties': {'age': {'items': {'anyOf': [{'type': 'integer'},
                                                {'type': 'null'}],
                                      'default': 0},
                            'type': 'array',
                            'uniqueItems': False},
                    'firstname': {'items': {'anyOf': [{'type': 'string'},
                                                      {'type': 'null'}]},
                                  'type': 'array',
                                  'uniqueItems': False},
                    'id': {'items': {'type': 'integer'},
                           'type': 'array',
                           'uniqueItems': True},
                    'life_nb': {'items': {'maximum': 4, 'type': 'integer'},
                                'type': 'array',
                                'uniqueItems': False},
                    'name': {'items': {'type': 'string'},
                             'type': 'array',
                             'uniqueItems': False}},
     'required': ['id', 'name', 'life_nb'],
     'type': 'object'}

    We can also build a basic schema and populate `DataFrameSchematizer` with it:

    >>> schema = {
    ...           'id': {'types': 'integer', 'unique': True, 'mandatory': True},
    ...           'name': {'types': 'string', 'mandatory': True},
    ...           'firstname': {'types': 'string'},
    ...           'age': {'types': 'integer', 'minimum': 0, 'default':0},
    ...           'life_nb': {'types': 'integer', 'mandatory': True, 'maximum': 4}
    ...           }

    >>> v = DataFrameSchematizer()
    >>> v.add_columns(schema)

    Or via a JSON string

    >>> schema = (
    ...   '{"id": {"types": "integer", "unique": true, "mandatory": true}, "name": '
    ...   '{"types": "string", "mandatory": true}, "firstname": {"types": "string"}, '
    ...   '"age": {"types": "integer", "minimum": 0, "default": 0}, "life_nb": {"types": "integer", '
    ...   '"mandatory": true, "maximum": 4}}')
    >>> v.add_columns(schema)
    >>> df, is_valid, errors = v.validate_dataframe(df)
    >>> pprint(errors)
    {('age', 0): ["'42' is not valid under any of the given schemas",
                  "'42' is not of type 'integer'",
                  "'42' is not of type 'null'"],
     ('life_nb', 0): ['5 is greater than the maximum of 4'],
     ('life_nb', 1): ["'hg' is not of type 'integer'"],
     ('life_nb', 2): ['15 is greater than the maximum of 4']}

    Or via a YAML string

    >>> schema = '''
    ... ---
    ... id:
    ...   types: integer
    ...   unique: true
    ...   mandatory: true
    ... name:
    ...   types: string
    ...   mandatory: true
    ... firstname:
    ...   types: string
    ... age:
    ...   types: integer
    ...   minimum: 0
    ...   default: 0
    ... life_nb:
    ...   types: integer
    ...   mandatory: true
    ...   maximum: 4
    ... '''
    >>> v.add_columns(schema)

    And validate the DataFrame:

    >>> df, is_valid, errors = v.validate_dataframe(df)
    >>> pprint(errors)
    {('age', 0): ["'42' is not valid under any of the given schemas",
                  "'42' is not of type 'integer'",
                  "'42' is not of type 'null'"],
     ('life_nb', 0): ['5 is greater than the maximum of 4'],
     ('life_nb', 1): ["'hg' is not of type 'integer'"],
     ('life_nb', 2): ['15 is greater than the maximum of 4']}
    """

    def __init__(self):
        self.columns_specs = {}
        self.required = []
        self._is_units = False
        self._source_units = None
        self._target_units = None

    def build(self):
        """build and return schema"""
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {},
            # "required": []
        }
        for colname, desc in self.columns_specs.items():
            schema["properties"][colname] = desc
        schema["required"] = self.required
        return schema

    def _add_columns_from_json(self, jsontxt):
        specs = json.loads(jsontxt)
        self.add_columns(specs)

    def _add_columns_from_yaml(self, yamltxt):
        specs = load_yaml(yamltxt)
        self.add_columns(specs)

    def add_columns_from_string(self, txt):
        """create columns checker from string. First test json, then yaml"""
        try:
            self._add_columns_from_json(jsontxt=txt)
        except:
            self._add_columns_from_yaml(yamltxt=txt)

    def add_columns(self, specs):
        if isinstance(specs, str):
            self.add_columns_from_string(specs)
            return
        # --------------------------------------------------------------------
        # specs is a dictionnary mapping DataFrame columns to its spec
        for colname, colspec in specs.items():
            self.add_column(name=colname, **colspec)

    def add_column(
        self,
        name,
        types=("integer",),
        unique=False,
        mandatory=False,
        units=None,
        **kwargs,
    ):
        """add a column to the schema"""
        if isinstance(types, str):
            types = (types,)
        types = list(types)
        if mandatory:
            self.required.append(name)
        else:
            types.append("null")
        # ---------------------------------------------------------
        if len(types) > 1:
            items = {"anyOf": [{"type": typ} for typ in types]}
        else:
            items = {"type": types[0]}
        items.update(kwargs)
        ref = {
            "type": "array",
            "items": items,
            "uniqueItems": unique,
        }
        # ---------------------------------------------------------------------
        # handle units specifications
        if units:
            ref["units"] = units
            self._is_units = True

        self.columns_specs[name] = ref

    def validate_dataframe(self, df):
        """validate dataframe against self.schema()"""
        schema = self.build()
        intermediate_report = defaultdict(list)  # what is not raised by jsonschema
        # =====================================================================
        # builds mult-header from dataframes if schemas are units-aware
        # =====================================================================
        if self._is_units:
            # -----------------------------------------------------------------
            # work on a copy:
            # so we can revert back to original `df` if something is failing
            _df = df.copy()
            # -----------------------------------------------------------------
            # create a multi-index columns such as pint-pandas can work
            _df.columns = pd.MultiIndex.from_tuples(
                zip(_df.columns, _df.iloc[0].fillna(""))
            )
            _df = _df.iloc[1:]
            # -----------------------------------------------------------------
            # collect defined units for later usage
            self._source_units = dict(
                _df.columns.tolist()
            )  #  {'id': '', 'distA': 'm',... }
            for i in range(len(_df.columns)):
                try:
                    _df.iloc[:, i] = pd.to_numeric(_df.iloc[:, i])
                except:
                    pass  # probably a column with strings
            try:
                # insert the correct to workaround this bug:
                # https://github.com/hgrecco/pint-pandas/issues/49
                _df = _df.pint.quantify(level=-1)
            except pint.errors.UndefinedUnitError as exc:
                self._is_units = False
                colnames = [
                    colname
                    for colname, unit in self._source_units.items()
                    if unit in exc.args
                ]
                for colname in colnames:
                    intermediate_report[(colname, "*")].append(
                        "undefined units '%s'" % self._source_units[colname]
                    )
                    df = df[1:]
            except Exception as exc:
                self._is_units = False
                intermediate_report["uncatched unit error"].extend(list(exc.args))
            else:
                # -------------------------------------------------------------
                # everything was fine, commit temporary `_df` to `df`:
                df = _df
                del _df
        # =====================================================================
        # first: fill empty values as requested by schema
        # =====================================================================
        _fillnas = {
            k: schema["properties"][k]["items"].get("default")
            for k, v in schema["properties"].items()
        }
        fillnas = {
            k: v for k, v in _fillnas.items() if k in df.columns and v is not None
        }
        if fillnas:
            df = df.fillna(value=fillnas, downcast="infer")
        # =====================================================================
        # convert read units to schema expected units (if required)
        # =====================================================================
        if self._is_units:
            self._target_units = {
                k: schema["properties"][k].get("units", "")
                for k in schema["properties"]
            }
            for col, units in self._target_units.items():
                try:
                    df[col] = df[col].pint.to(units)
                except KeyError:
                    pass
                except AttributeError:
                    breakpoint()
            df = df.pint.dequantify()
            df.columns = [t[0] for t in df.columns.tolist()]  # restrict to level 0

        # =====================================================================
        # second: validate
        # =====================================================================
        validator = jsonschema.Draft7Validator(schema)
        # df -> dict -> json -> dict to convert NaN to None
        document = json.loads(json.dumps(df.to_dict(orient="list"), ignore_nan=True))
        report = defaultdict(list)
        for error in validator.iter_errors(document):
            try:
                col, row, *rows = error.absolute_path
            except ValueError:
                report["general"].append(error.message)
            else:
                report[(col, row)].append(error.message)
                report[(col, row)].extend([e.message for e in error.context])
        report = {**dict(report), **intermediate_report}

        return df, len(report) == 0, report


class ValidatorMixin:
    """mixin class built on top of jsonschema"""

    def validator_mixin_init(self):
        """called by Base class __init__()"""
        self._schemas = {}

    def quantify(self, tabname, restrict_to_units=False):
        df = self._data[tabname].copy()
        schema = self._schemas[tabname]
        if not schema._is_units:
            raise ValueError(f"tab {tabname} is not units-aware'")
        units = schema._target_units
        # add dummy rows
        dummy_row = pd.DataFrame({c: [units.get(c, "")] for c in df.columns})
        df = pd.concat((dummy_row, df))
        if restrict_to_units:
            df = df[[c for c in df.columns if c in units]]
        df.columns = pd.MultiIndex.from_tuples(zip(df.columns, df.iloc[0].fillna("")))
        df = df.iloc[1:]
        df = df.pint.quantify(level=-1)
        return df

    def convert_to(self, tabname, units=None):
        """convert units-aware dataframe to units
        units can be:
        * None: will convert to base units
        * string: eg. 'm^3'
        * a dict mapping columns to units
        """
        df = self.quantify(tabname, restrict_to_units=True)
        if units is None:
            df_c = df.pint.to_base_units()
        else:
            if isinstance(units, str):
                units = {c: units for c in df.columns}
            df_c = pd.DataFrame(
                {col: df[col].pint.to(units) for col, units in units.items()}
            )
        return df_c

    def _set_schema(self, tabname, schema):
        """assign a schema to a tab"""
        tabnames = []
        # ---------------------------------------------------------------------
        # generic tabname regex: collect _data tabnames
        if tabname.startswith("^") and tabname.endswith("$"):
            for data_tabname in self._data.keys():
                if re.match(tabname, data_tabname):
                    tabnames.append(data_tabname)
        # ---------------------------------------------------------------------
        # general case. Only one tabname to fill
        else:
            tabnames = [tabname]
        # ---------------------------------------------------------------------
        # iterate over tabnames (usually only one if no regex-tabname supplied)
        # to instanciate a DataFrameSchematizer and fill with a schema
        for tabname in tabnames:
            self._schemas[tabname] = DataFrameSchematizer()
            self._schemas[tabname].add_columns(schema)

    def read_schema(self, *filepath):
        """ assign a global schema by parsing the given filepath"""
        if len(filepath) > 1:
            return self.read_multiple_yamls_schemas(*filepath)
        else:
            filepath = filepath[0]
        _, ext = os.path.splitext(filepath)
        with open(filepath, "r") as fh:
            schema_specs = fh.read()
        if ext == ".json":
            schemas = json.loads(schema_specs)
        elif ext == ".yaml":
            schemas = load_yaml(schema_specs)
        for tabname, schema in schemas.items():
            self._set_schema(tabname, schema)

    def read_multiple_yamls_schemas(self, *files):
        """
        replace `read_schema` in case shcema is made of several YAML files
        """
        schemas = load_yaml(*files)
        for tabname, schema in schemas.items():
            self._set_schema(tabname, schema)

    def _validate_tab(self, tabname):
        """validate a tab using the provided scheme"""
        if tabname not in self._schemas:
            return None, True, {}
        return self._schemas[tabname].validate_dataframe(self._data[tabname])

    def validate(self):
        """
        iterate through all tabs and validate eachone
        """
        # keep initial data before processing them
        if not hasattr(self, "_raw_data"):
            self._raw_data = {tabname: df.copy() for tabname, df in self._data.items()}
        ret = {}
        for tabname, df in self._data.items():
            df, is_ok, report = self._validate_tab(tabname)
            self._data[tabname] = df  # override with filled (fillna) dataframe
            if not is_ok:
                ret[tabname] = report
        return ret

    def dump_template(self):
        """return list of columns ready to be dumped as XLSX template"""
        dic = {}
        for tabname, schema in self._schemas.items():
            dic[tabname] = pd.DataFrame({k: [] for k in schema.columns_specs.keys()})
        return dic


if __name__ == "__main__":
    import doctest

    doctest.testmod(
        optionflags=doctest.ELLIPSIS
        | doctest.IGNORE_EXCEPTION_DETAIL
        | doctest.NORMALIZE_WHITESPACE
    )
