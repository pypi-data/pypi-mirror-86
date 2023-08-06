# localambda
A simple way to test lambdas locally

# Installation
```bash
pip install localambda
```

# Who is localambda for??
Do you ever find yourself saying any of the following:

- I cannot easily test changes to this lambda because someone else has deployed it to dev
- Every change to this repo takes forever to build and deploy
- I really like using cleverly-designed in-house CLI tools

If so, then localambda is for you!

# What does localambda do?

1. It can run one or more Lambdas locally and routet traffic between the local Lambdas
2. It can build a sinlge Lambda at a time without having to build the entire repo

# Usage

### Prerequisites
You will need redis running on your local machine, to easily run an instance of redis bind a docker container to your localhost port
```bash
docker run --name lola-redis -d -p 6379:6379 redis
```

Or run Redis with [brew](#https://gist.github.com/tomysmile/1b8a321e7c58499ef9f9441b2faa0aa8).

### Setup your localambda configs
```bash
lola --setup
```

This will create your `lola` home directory, the default location is your user home (`~`). You will need to place a file named `lola.yaml` in this directory. The contens of this file should look like this:

```yaml
repo_home: "/path/to/your/repo_home"

stacks:
  - LambdaResource1:
      location: repo-dir-name
      stack_name: name-of-stack-when-deployed
      resources:
        - CftResourceName1           # CFT Resource Name
        - CftResourceName2
  - LambdaResource2:
      location: repo-dir-name2
      stack_name: name-of-stack-when-deployed2
      resources:
        - CftResourceName1k           # CFT Resource Name
```
A fully completed version (on a mac) would look like this:

The fields are:

* **repo_home**: The base directory for all of your git repos, assuming you place them all in the same directory. If provided, local lambda looks for each of the resources defined below in this directory by concatenating this field and the **location** of each stack resource together.
* **stacks**: Each stack that you are currently deploying should be listed here, if you are no longer developing on one of these stacks or you do not want it to be served locally it should probably be removed or commented out from this list
* * **Logical name**: These fields are only used for outputting logging messages so that you know what stack created which log message. The examples provided are `LambdaResource1` and `LambdaResource2`.
* * **location**: The location of the directory that contains the stack. LocaLambda will attempt to concatenate this with the **repo_name** above, if that directory does not exist it will treat this as an absolute or relative path to attempt to find the contents.
* * **stack_name**: The name of the stack that you would use when using `sam deploy ...`. LocaLambda currently expects a very specific naming convention where all lambdas are deployed with the function naming convention: `{stack_name}-{LambdaResourceName}-{env}`. By providing the stack name in this field it allows the matching logic for the man in the middle to find the correct event.
* * **resources**: These are the resource names for the lambdas in the `template.yaml` file. LocaLambda also currently requires that `LambdaResourceName` for the function name (mentioned above) and the AWS resource name be the same. Again, this is to allow the man in the middle to match the correct flows.


### Build & Serve
LocaLambda has two primary functions when it comes to testing lambdas locally:

* **Building**: this step builds the lambdas that are specified in your lola file, adding all of the requirements and creating the local docker container that can be invoked. LocaLambda ONLY builds the services defined in your lola.yaml file so you don't need to build an entire repo to test.

* **Serving**: localambda will serve your code locally and it will automatically route traffic that is heading to AWS to your local lambda for each of the resources defined in your lola.yaml file. You don't even have to change your code!


### Running lambdas locally
By now you should have installed localambda, set up your `lola.yaml`, added a handful of services and now your're ready to test. What **exactly** is localambda doing for you?

The build process is two steps:
- Localambda creates configurations that will be used to send traffic to AWS and to the local HTTPS proxy server. The first step it takes is to read in the `lola.yaml` file and to read each of the `template.yaml` files in each of the repos and to extract the lambda function names and expected URLs for each. It then serializes that information and makes it available in Redis for the man in the middle.
- The configurations are also used to create local builds (this is the exact same thing as when you run `sam build --use-container`) with the exception that localambda is excluding all resources that you do not define. This allows you to test as few as one lambda at a time if you'd like.

In the server step:
- Localambda creates an HTTPs proxy server, your machine then automatically routes all HTTPs activity through that server.
- Once the server is up, the man in the middle script is launched. This runs outside of localambda and it processes each HTTPs event your machine receives. The man in the middle is launched to only include traffic to the **aws domain** right now.
- For each of the stacks in the `lola.yaml` file, the associated resources are launched locally. Once completed, you can invoke them on your machine.


![localambda](images/lola.gif)

### Verify boto3 client
One very important aspect to running localambda is that the boto3 client must **not** verify SSL certificates. Since traffic is being routed through a local HTTPS proxy the request looses the ability to validate that the certificate is correct. In order to get around this we simply need to make sure that all lambdas which are being invoked locally are called from a client that is not verifying the SSL cert. You can turn on SSL validation like this:

```python 
import boto3

l = boto3.client('lambda', verify=False)
```

Lambda clients that calls another local lambda need to have SSL verification turned off since your local machine will not have the certs to verify the aws domain. Since you may be testing more than one lambda locally you will need to pass in a flag during the build stage in order to build a local lambda that will not verify the SSL certificates. The suggested approach is to add a parameter `Verify_SSL` with the default set to `true` in your CFT. Localambda will automatically inject `Verify_SSL`=`false` when deploying locally:

1) Add a parameter Ssl_Verify in the parameters section to the CFT:
```yaml 
Parameters:
  Verify_SSL:
    Description: Whether or not to verify SSL certificates for AWS clients
    Default: true
    Type: String
    AllowedValues: [true, false]
```
2) Pass in this environment variable to all lambdas:
```yaml 
...
Environment:
  Variables:
    ...
    VERIFY_SSL: !Ref Verify_SSL
    ...
```

3) Read this value into the lambda client
```python
import os 
import boto3
VERIFY_SSL = True if os.environ.get('VERIFY_SSL', 'true').lower().startswith('t') else False

lambda_client = boto3.client('lambda', verify=VERIFY_SSL)
```

### Boto3 client for Ubuntu. 

Ubuntu requires explicit proxy definition. Make sure that the port defined matches the port of your local HTTPS proxy.


```python
import boto3 
from botocore.config import Config 

lambda_client = boto3.client('lambda', verify=SSL_VERIFY, config=Config(proxies={'https': 'localhost:8766'}))
``` 


# Examples

In the examples folder you will find:
 
- A fully deployable pair of Lambdas, to deploy these Lambdas navigate to `examples/deployable_lambda` and run `sh deploy.sh`, make sure to update:
- - The deployment bucket: `DEPLOY_BUCKET='your-deployment-bucket'` in the `deploy.sh` script
- - The Role ARN to give to the Lambdas in the parameters section of the `template.yaml`
- A sample script that will invoke the Lambdas above, once deployed `examples/invoke_local.py`
- A sample config file, `examples/sample_config.yaml` that can be used to recreate your own `lola.yaml` file

# TODO / Areas of improvement
- Allow custom matching logic
- handle layers better - local layers, imported layers
- ssh tunnels for lambdas that need to access databases in private networks
- Handle different structures for templates in a repo (multi template, sub directory template, etc.)
