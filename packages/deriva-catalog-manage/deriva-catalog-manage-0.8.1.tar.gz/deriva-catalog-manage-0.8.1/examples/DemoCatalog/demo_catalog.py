import logging
import os
import os.path

from deriva.core import get_credential, init_logging, DerivaServer
from deriva.utils.catalog.components.deriva_model import DerivaColumn, DerivaModel
from deriva.utils.catalog.components.configure_catalog import DerivaCatalogConfigure
from deriva.utils.catalog.manage.deriva_csv import DerivaCSV

# These need to be changed depending on the host and groups available.
host = 'demo.derivacloud.org'
catalog_id = 1

init_logging()
logger = logging.getLogger(__name__)


# Create a new catalog instance
def create_catalog(server='demo.derivacloud.org', catalog_name='test'):
    global catalog_id

    credentials = get_credential(server)
    catalog = DerivaServer('https', server, credentials=credentials).create_ermrest_catalog()
    catalog_id = catalog.catalog_id
    logger.info('Catalog_id is {}'.format(catalog_id))

    logger.info('Configuring catalog....')
    catalog = DerivaCatalogConfigure(host, catalog_id=catalog_id)
    catalog.configure_baseline_catalog(catalog_name=catalog_name,
                                       admin='DERIVA Demo Admin',
                                       curator='DERIVA Demo Curator',
                                       writer='DERIVA Demo Writer', reader='*')
    return catalog


def create_navbar(catalog, schema_name):
    def menu_url(schema_name, table_name):
        return {
            'name': table_name,
            'url': "/chaise/recordset/#{{{$catalog.id}}}/" + "{}:{}".format(schema_name, table_name)
        }

    dir = os.path.dirname(os.path.abspath(__file__))
    with open(dir + '/about.md') as f:
        about_content = f.read()

    with open(dir + '/help.md') as f:
        help_content = f.read()

    r = list(
        catalog['WWW']['Page'].datapath().insert(
            [
                {
                    'Title': 'About the Catalog',
                    'Content': about_content
                },
                {
                    'Title': 'Help',
                    'Content': help_content
                },
            ]
        )
    )

    about_rid = r[0]['RID']
    help_rid = r[1]['RID']

    # Set up the navigation bar.
    catalog.navbar_menu = {
        'newTab': False,
        'children': [
            {'name': "Browse",
             'children': [
                 menu_url(schema_name, 'Collection'),
                 menu_url(schema_name, 'Study'),
                 menu_url(schema_name, "Experiment"),
                 menu_url(schema_name, 'Replicate'),
                 menu_url(schema_name, 'Specimen'),
                 menu_url(schema_name, "File"),
                 menu_url(schema_name, "Imaging"),
                 menu_url(schema_name, "Anatomy"),
                 menu_url("WWW", "Page")
             ]
             },
            {'name': "About", 'url': '/chaise/record/#{{{$catalog.id}}}/WWW:Page/RID=' + about_rid},
            {'name': "Help", 'url': '/chaise/record/#{{{$catalog.id}}}/WWW:Page/RID=' + help_rid}
        ]
    }


def create_demo_model(catalog, schema_name='Demo'):
    logger.info('Creating schema')
    schema = catalog.create_schema(schema_name, comment='Schema for demonstation catalog')

    # Create Basic Tables.
    with DerivaModel(catalog):
        logger.info('Creating tables....')
        study = schema.create_table('Study',
                                    [DerivaColumn.define('Title', 'text'),
                                     DerivaColumn.define('Description', 'text')])
        study.configure_table_defaults()

        experiment = schema.create_table('Experiment', [
            DerivaColumn.define('Description', 'markdown'),
            DerivaColumn.define('Experiment_Type', 'text')
        ])
        experiment.configure_table_defaults()

        replicate = schema.create_table('Replicate', [DerivaColumn.define('Replicate_Number', 'int4')])
        replicate.configure_table_defaults()

        specimen = schema.create_table('Specimen', [DerivaColumn.define('Specimen_Type', 'text')])
        specimen.configure_table_defaults()

        # Asset tables
        logger.info('Creating asset tables....')
        file = schema.create_asset('File',
                                   column_defs=[
                                       DerivaColumn.define('File_Type', 'text'),
                                       DerivaColumn.define('Description', 'text')
                                   ])
        file.configure_table_defaults()

        imaging = schema.create_asset('Imaging')
        imaging.configure_table_defaults()

        # Create collections.
        collection = schema.create_table('Collection', [DerivaColumn.define('Description', 'text'),
                                                        DerivaColumn.define('Name', 'text')
                                                        ])
        # Create links between tables.
        logger.info('Linking tables....')
        experiment.link_tables(study)
        replicate.link_tables(file)

        collection.associate_tables(specimen)
        collection.associate_tables(study)

        specimen.associate_tables(imaging)
        experiment.associate_tables(imaging)

        anatomy = schema.create_vocabulary('Anatomy', 'DEMO:{RID}')
        specimen.associate_vocabulary(anatomy)

        # Now create the navbar...
        create_navbar(catalog, schema_name)


def add_demo_content(catalog, schema_name='Demo'):
    dir = os.path.dirname(os.path.abspath(__file__))

    # Now add some content.....
    experiment_csv = DerivaCSV(dir + '/Experiment.csv', schema_name)
    experiment_csv.upload_to_deriva(catalog)

    # Load files into hatrac.


def create_demo_catalog():
    catalog = create_catalog()
    create_demo_model(catalog)
    add_demo_content(catalog)
    return catalog


def delete_demo_catalog(catalog):
    logger.info("Deleting catalog ID: %s" % catalog.ermrest_catalog.catalog_id)
    catalog.ermrest_catalog.delete_ermrest_catalog(really=True)
