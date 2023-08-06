table_file_template = """
import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

{groups}

table_name = '{table_name}'

schema_name = '{schema_name}'

{column_annotations}

{column_defs}

{table_annotations}

{key_defs}

{fkey_defs}

{table_def}


def main(catalog, mode, replace=False, really=False):
    updater = CatalogUpdater(catalog)
    table_def['column_annotations'] = column_annotations
    table_def['column_comment'] = column_comment
    updater.update_table(mode, schema_name, table_def,replace=replace, really=really)


if __name__ == "__main__":
    host = {host!r}
    catalog_id = {catalog_id}
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
"""


schema_file_template = """
import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

{groups}

schema_name = '{schema_name}'

{table_names}

{annotations}

{acls}

{comments}

schema_def = em.Schema.define(
        '{schema_name}',
        comment=comment,
        acls=acls,
        annotations=annotations,
    )

def main(catalog, mode, replace=False):
    updater = CatalogUpdater(catalog)
    updater.update_schema(mode, schema_def, replace=replace)


if __name__ == "__main__":
    host = {host!r}
    catalog_id = {catalog_id}
    mode, replace, host, catalog_id = parse_args(host, catalog_id)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
"""

catalog_file_template = """
import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args
from deriva.core import tag as chaise_tags
import deriva.core.ermrest_model as em

{groups}

{tag_variables}


{annotations}


{acls}

def main(catalog, mode, replace=False):
    updater = CatalogUpdater(catalog)
    updater.update_catalog(mode, annotations, acls, replace=replace)


if __name__ == "__main__":
    host = {host!r}
    catalog_id = {catalog_id}
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_catalog=True)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
"""
