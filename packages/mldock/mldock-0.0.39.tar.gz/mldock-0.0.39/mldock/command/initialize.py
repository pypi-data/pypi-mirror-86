import os
import sys
import json
import logging
import click
from pathlib import Path
from future.moves import subprocess

from mldock.config.config_manager import \
    ResourceConfigManager, SagifyConfigManager, PackageConfigManager, \
        HyperparameterConfigManager, InputDataConfigManager
from mldock.api.local import \
    _copy_boilerplate_to_dst, _rename_file

click.disable_unicode_literals_warning = True
logger=logging.getLogger('mlmldockdoc')

@click.command()
@click.option('--dir', help='Set the working directory for your sagify container.', required=True)
@click.option('--new', is_flag=True)
@click.option('--testing_framework', default=None, help='(Optional) Pytest framework. This creates a few health-check tests')
@click.pass_obj
def init(obj, dir, new, testing_framework):
    """
    Command to initialize container configs required by sagemaker-training.
    """
    helper_library_path=obj['helper_library_path']
    try:
        logger.info("Getting Sagify config")
        sagify_manager = SagifyConfigManager(
            filepath=os.path.join(dir, ".sagify.json")
        )
        if new:
            sagify_manager.setup_config()
            # write .sagify file
            logger.info("\n\nWriting a new .sagify file")
            sagify_manager.write_file()

        sagify_manager.pretty_print()

        logger.info("Getting Requirements")
        package_manager = PackageConfigManager(
            filepath=os.path.join(dir, "requirements.txt")
        )
        package_manager.pretty_print()
        # write to package manager
        package_manager.write_file()


        path_to_payload = Path(os.path.join(dir, "payload.json"))
        if not path_to_payload.exists():
            path_to_payload.write_text(json.dumps({"feature1": 10, "feature2":"groupA"}))

        # get sagify_module_path name
        sagify_config = sagify_manager.get_config()
        src_directory = os.path.join(
            dir,
            sagify_config.get("sagify_module_dir", "src")
        )

        template_dir = os.path.join(
            helper_library_path,
            'templates',
            sagify_config['platform']
        )

        sagify_module_path = os.path.join(
            src_directory,
            'sagify_base'
        )

        

        test_path = os.path.join(sagify_module_path, 'local_test', 'test_dir')
        config_path = os.path.join(test_path, 'input/config')

        if new:
            logger.info("Creating new workspace")
            _copy_boilerplate_to_dst(os.path.join(template_dir,'src/'), src_directory)
        if testing_framework == 'pytest':
            logger.info("Adding pytest container tests")
            _copy_boilerplate_to_dst(os.path.join(template_dir,'tests/'), 'tests/')
            logger.info("renaming test file")

            _rename_file(
                base_path='tests/container_health',
                current_filename='_template_test_container.py',
                new_filename='test_{ASSET_DIR}.py'.format(ASSET_DIR=dir)
            ) 

        # set resource config
        logger.info("\n\nGetting Container Resource config")
        resource_config = ResourceConfigManager(
            filepath=os.path.join(config_path, "resourceconfig.json")
        )
        resource_config.ask_for_resourceconfig()
        resource_config.write_file()
        # set input data channels
        logger.info("\n\nGetting Input Data config")
        input_data_channels = InputDataConfigManager(
            filepath=os.path.join(config_path, "inputdataconfig.json")
        )
        input_data_channels.ask_for_input_data_channels()
        input_data_channels.write_file()

        # set hyperparameters
        logger.info("\n\nGetting Hyperparameters config")
        hyperparameters = HyperparameterConfigManager(
            filepath=os.path.join(config_path, "hyperparameters.json")
        )
        hyperparameters.pretty_print()
        hyperparameters.ask_for_hyperparameters()
        hyperparameters.write_file()

        logger.info("\nlocal container volume is ready! ヽ(´▽`)/")
    except subprocess.CalledProcessError as e:
        logger.debug(e.output)
        raise
    except Exception as e:
        logger.info("{}".format(e))
        sys.exit(-1)
