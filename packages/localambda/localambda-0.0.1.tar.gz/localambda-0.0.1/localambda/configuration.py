from os import makedirs, path

from cfn_tools import load_yaml, dump_yaml
import shutil
import yaml

from . import localogger

logger = localogger.LocaLogger(group_name='LocaLambda Configs', group_id=0)


class NoLocaLambdaResourceFileFound(Exception):
    """Exception raised for when no lola resource file exists. Generally means that
    `lola --seup` has not been run.
    """

    def __init__(self, message="No localambda resource file found, did you run 'lola --setup'?"):
        self.message = message
        super().__init__(self.message)


class NoLocaLambdaFileFound(Exception):
    """Exception raised for when no lola file exists for the configurations to be
    deployed or built.
    """

    def __init__(self, message="No localambda config file found to deploy resources"):
        self.message = message
        super().__init__(self.message)


class ConfigManager(object):

    # These are the only resource types that will be kept in the 
    # template.yaml when deployed locally
    BASE_SLIM_REQUIRES_BUILD_RESOURCES = [
        'AWS::Serverless::Function'
    ]

    DEFAULT_LOLA_RC_FILE = '.lolarc'
    DEFAULT_LOLA_SERVE_FILE = 'lola.yaml'

    def __init__(self, lola_file: str = None):
        self.resource_file = path.join(path.expanduser("~"), self.DEFAULT_LOLA_RC_FILE)
        if not path.exists(self.resource_file):
            raise NoLocaLambdaResourceFileFound()

        self.lola_confs = None
        self.lola_file = None
        self.lola_home = None
        self._lola_file_yaml = None
        self.load_default_confs()
        self.set_user_configs_from_rc_configs(lola_file)
        self.validate_lola_file()

    def load_default_confs(self) -> None:
        self.lola_confs = self.load_yaml_configs(self.resource_file)

    def build_final_lola_file(self):
        """For each of the items in the lola file, the following logic is applied:

            - stacks:
                - Adds a template key for the name of the template if it does not exist
                - Creates fully-qualified file locations for the template
        """
        if 'repo_home' in self.lola_file_yaml and 'stacks' in self.lola_file_yaml:
            repo_base = self.lola_file_yaml['repo_home']
            deploy_region = self.lola_file_yaml.get('region', 'us-east-1')
            for stack_item in self.lola_file_yaml['stacks']:
                stack_name = list(stack_item.keys())[0]
                

                if not stack_item[stack_name].get('template'):
                    stack_item[stack_name]['template'] = 'template.yaml'

                if (not stack_item[stack_name].get('location', '').startswith(path.sep)
                    and not path.isdir(stack_item[stack_name].get('location'))):
                    stack_item[stack_name]['location'] = path.join(repo_base, stack_item[stack_name]['location'])

                self.build_slim_deploy(stack_item, region=deploy_region)

    def is_buildable_resource(self, resource_key: str, resources) -> bool:
        """Checks to see if a given resource requires a build by AWS sam
        """
        return resources[resource_key]['Type'] in self.BASE_SLIM_REQUIRES_BUILD_RESOURCES

    def build_slim_deploy(self, stack_item, region):
        """Builds a slim deployment, essentially only the resources required to 
        execute lambdas locally.

        :param stack_item:
        :return: None
        """
        logical_name = list(stack_item.keys())[0]
        stack_details = stack_item[logical_name]

        lambda_region = stack_item.get('region') or region
        stack_details['region'] = lambda_region

        # Capture the logical resource name, also referred to as "to" in the lola.yaml
        keep_resources = [k for k in stack_details['resources']]

        cft = load_yaml(open(path.join(stack_details['location'], stack_details['template'])).read())

        resources = cft['Resources']
        remove_resources = []  # Items to remove fromm the CFT
        proxy_routes = []      # Items to route to the proxy
        for resource in resources:
            if self.is_buildable_resource(resource, resources) and resource not in keep_resources:
                remove_resources.append(resource)
            else:
                # If this is a resource we are keeping, capturing the proxy routing information
                if resource in keep_resources:
                    resources[resource]['Properties']['CodeUri'] = path.join(
                        stack_details['location'], resources[resource]['Properties']['CodeUri']
                    )
                    fn_name_key = list(resources[resource]['Properties']['FunctionName'].keys())[0]
                    fn_name_stripped = (
                        resources[resource]['Properties']['FunctionName'][fn_name_key]
                        .replace('${AWS::StackName}-', '')
                        .replace('${EnvStageName}', '')  
                    )
                    proxy_routes.append({'from': fn_name_stripped, 'to': resource})

                # Create a fully qualified path for layer code
                elif resources[resource]['Type'] == 'AWS::Serverless::LayerVersion':
                    resources[resource]['Properties']['ContentUri'] = path.join(
                        stack_details['location'], resources[resource]['Properties']['ContentUri']
                    )

        for remove_r in remove_resources:
            cft['Resources'].pop(remove_r)

        # Create the name of the temp file to save this config for the Butler deployment
        tmp_dir = path.join(self.lola_home, 'temp_deploy')

        build_dir = path.join(tmp_dir, stack_details['stack_name'], 'build')
        serve_dir = path.join(tmp_dir, stack_details['stack_name'], 'serve')
        temp_build_template_file = path.join(build_dir, 'template.yaml')
        temp_serve_template_file = path.join(serve_dir, 'template.yaml')

        # Forcibly remove all build resources
        if path.exists(build_dir):
            shutil.rmtree(build_dir)

        # Set the proxy routes item for the stack item, this is used by the proxy server to route events
        stack_details['proxy_routes'] = proxy_routes
        stack_details['build_dir'] = build_dir
        stack_details['serve_dir'] = serve_dir
        stack_details['build_template'] = temp_build_template_file
        stack_details['serve_template'] = temp_serve_template_file

        # Update the location of the deployment file
        cft['Resources'] = resources
        dumped_yaml = dump_yaml(cft)
        if not path.exists(path.dirname(temp_build_template_file)):
            makedirs(path.dirname(temp_build_template_file))

        with open(temp_build_template_file, 'w') as out_file:
            out_file.write(dumped_yaml)
            out_file.flush()

    @property
    def lola_file_yaml(self) -> dict:
        """Loads a lola yaml file on demand"""
        if self._lola_file_yaml is None:
            self._lola_file_yaml = self.load_yaml_configs(self.lola_file)
            self.build_final_lola_file()
        return self._lola_file_yaml

    def set_user_configs_from_rc_configs(self, provided_lola_file) -> None:
        """Sets user configurations for the lola process from their .lolarc file if
        the lola file was not already passed in

        :param provided_lola_file: The location for a lola configuration file provided
                                   by the client.
        """
        if isinstance(self.lola_confs, dict):
            self.lola_home = self.lola_confs['lola_home']
            _lola_file = self.lola_confs.get('lola_file')
            if _lola_file:
                self.lola_file = _lola_file

        if provided_lola_file:
            self.lola_file = provided_lola_file

    def validate_lola_file(self) -> None:
        """Validates that a lola file exists"""
        # TODO: validate the content of the file
        if not path.exists(self.lola_file):
            raise NoLocaLambdaFileFound()

    @staticmethod
    def load_yaml_configs(f: str) -> dict:
        """
        Load yaml configurations for endpoints that enable specific endpoints to be routed
        to AWS or to localhost

        :param f: A string representing the absolute location of a file
        :return: A dict created from a YAML file
        """
        if path.exists(f):
            with open(f) as file:
                return yaml.load(file, Loader=yaml.FullLoader)
        else:
            logger.log_warning_msg(
                "No .lolarc file has been setup yet!! Run 'lola setup' to be guided through the setup"
            )

    @staticmethod   
    def write_yaml_configs(f: str, d: dict) -> None:
        """Writes YAML configs to a given location

        :param f: A string representing the absolute location of a file to save
        :param d: A dictionary of values to write
        :return: None
        """
        with open(f, 'w') as file:
            yaml.dump(d, file)

