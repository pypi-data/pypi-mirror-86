import collections
import importlib
import logging
import multiprocessing
import os
import subprocess
import time
import types
import typing

from bert import \
    queues as bert_queues, \
    constants as bert_constants, \
    shortcuts as bert_shortcuts, \
    encoders as bert_encoders, \
    exceptions as bert_exceptions

from bert import naming as bert_naming

ZIP_EXCLUDES: typing.List[str] = [
    '*.exe', '*.DS_Store', '*.Python', '*.git', '.git/*', '*.zip', '*.tar.gz',
    '*.hg', 'pip', 'docutils*', 'setuputils*', '__pycache__/*',
]
COMMON_EXCLUDES: typing.List[str] = ['env', 'lambdas']

logger = logging.getLogger(__name__)

def scan_jobs(module_name: str) -> typing.Dict[str, typing.Any]:
    jobs: typing.Dict[str, typing.Any] = {}
    module = importlib.import_module(f'{module_name}.jobs')
    for member_name in dir(module):
        if member_name.startswith('_'):
            continue

        member = getattr(module, member_name)
        if type(member) != types.FunctionType:
            continue

        if not hasattr(member, 'done_key') or not hasattr(member, 'work_key'):
            continue

        jobs[member_name] = member

    # Order the jobs correctly
    ordered = collections.OrderedDict()
    while len(ordered.keys()) != len(jobs.keys()):
        if len(ordered.keys()) == 0:
            for job_name, job in jobs.items():
                if job.parent_func == 'noop':
                    ordered[job_name] = job
                    break

            else:
                raise NotImplementedError(f'NoopSpace not found')

        else:
            latest: types.FunctionType = [item for item in ordered.values()][-1]
            for job_name, job in jobs.items():
                if job.parent_func == latest:
                    ordered[job_name] = job
                    break
    return ordered

def map_jobs(jobs: typing.Dict[str, typing.Any], module_name: str) -> None:
    confs: typing.Dict[str, typing.Dict[str, typing.Any]] = {}
    bert_configuration = bert_shortcuts.load_configuration() or {}
    deployment_config = bert_shortcuts.obtain_deployment_config(bert_configuration)

    # Validate we have access to objects in AWS
    bert_shortcuts.head_bucket_for_existance(deployment_config.s3_bucket)

    for job_name, job in jobs.items():
        identity_encoders: typing.List[str] = bert_shortcuts.merge_lists(
            bert_configuration.get('every_lambda', {'identity_encoders': []}).get('identity_encoders', []),
            bert_configuration.get(job_name, {'identity_encoders': []}).get('identity_encoders', []),
            ['bert.encoders.base.IdentityEncoder'])

        queue_encoders: typing.List[str] = bert_shortcuts.merge_lists(
            bert_configuration.get('every_lambda', {'queue_encoders': []}).get('queue_encoders', []),
            bert_configuration.get(job_name,        {'queue_encoders': []}).get('queue_encoders', []),
            ['bert.encoders.base.encode_aws_object'])

        queue_decoders: typing.List[str] = bert_shortcuts.merge_lists(
            bert_configuration.get('every_lambda', {'queue_decoders': []}).get('queue_decoders', []),
            bert_configuration.get(job_name,        {'queue_decoders': []}).get('queue_decoders', []),
            ['bert.encoders.base.decode_aws_object'])

        invoke_args: typing.List[str] = bert_shortcuts.merge_lists(
            bert_configuration.get('every_lambda', {'invoke_args': []}).get('invoke_args', []),
            bert_configuration.get(job_name,        {'invoke_args': []}).get('invoke_args', []),
            [])
        invoke_args: typing.List[typing.Dict[str, typing.Any]] = bert_shortcuts.load_invoke_args(invoke_args)

        binary_paths: typing.List[str] = bert_shortcuts.merge_lists(
            bert_configuration.get('every_lambda', {'binary_paths': []}).get('binary_paths', []),
            bert_configuration.get(job_name, {'binary_paths': []}).get('binary_paths', []),
            [])

        layers: typing.List[str] = bert_shortcuts.merge_lists(
            bert_configuration.get('every_lambda', {'layers': []}).get('layers', []),
            bert_configuration.get(job_name, {'layers': []}).get('layers', []),
            [])

        # This ENVVar will exist when the bert-etl-monitor function is deployed to AWS Lambda. bert-etl-monitor is a 
        #  utility function and doesn't require any additional packages, encoders or decoders.
        if not os.environ.get('BERT_MODULE_NAME', None) is None:
            identity_encoders = []
            queue_encoders = []
            queue_decoders = []

        # Make sure the encoders exist
        bert_encoders.load_encoders_or_decoders(identity_encoders)
        bert_encoders.load_encoders_or_decoders(queue_encoders)
        bert_encoders.load_encoders_or_decoders(queue_decoders)

        ignore_items: typing.List[str] = bert_shortcuts.merge_lists(
            bert_configuration.get('every_lambda', {'ignore': []}).get('ignore', []),
            bert_configuration.get(job_name, {'ignore': []}).get('ignore', []),
            [])

        # concurrency_limit is checked against AWS account execution limit in bert.deploy.utils
        concurrency_limit: int = bert_shortcuts.get_if_exists('concurrency_limit', '0', int, bert_configuration.get('every_lambda', {}), bert_configuration.get(job_name, {}))
        runtime: int = bert_shortcuts.get_if_exists('runtime', 'python3.6', str, bert_configuration.get('every_lambda', {}), bert_configuration.get(job_name, {}))
        memory_size: int = bert_shortcuts.get_if_exists('memory_size', '128', int, bert_configuration.get('every_lambda', {}), bert_configuration.get(job_name, {}))
        if int(memory_size / 64) != memory_size / 64:
            raise bert_exceptions.BertConfigError(f'MemorySize[{memory_size}] must be a multiple of 64')
        min_proced_items: int = bert_shortcuts.get_if_exists('min_proced_items', '25', int, bert_configuration.get('every_lambda', {}), bert_configuration.get(job_name, {}))

        # iam
        iam_execution_role_arn: str = bert_shortcuts.get_if_exists(
            'iam.execution_role_arn', None, str,
            bert_configuration.get('every_lambda', {'iam':{}}),
            bert_configuration.get(job_name, {'iam': {}}))

        # kms
        kms_alias: str = bert_shortcuts.get_if_exists(
            'kms.alias', None, str,
            bert_configuration.get('every_lambda', {'kms': {}}),
            bert_configuration.get(job_name, {'kms': {}}))

        kms_usernames: typing.List[str] = bert_shortcuts.get_and_merge_if_exists(
            'kms.usernames', None, list,
            bert_configuration.get('every_lambda', {'kms': {}}),
            bert_configuration.get(job_name, {'kms': {}}))

        invoke_args: typing.List[typing.Dict[str, typing.Any]] = bert_shortcuts.load_invoke_args(invoke_args)
        # events
        # sns topic to proc lambda
        sns_topic_arn: str = bert_shortcuts.get_if_exists(
            'events.sns_topic_arn', None, str,
            bert_configuration.get('every_lambda', {'events':{}}),
            bert_configuration.get(job_name, {'events': {}}))

        # schedule_expression will be validated before executing the deploy script
        schedule_expression: str = bert_shortcuts.get_if_exists(
            'events.schedule_expression', None, str,
            bert_configuration.get('every_lambda', {'events':{}}),
            bert_configuration.get(job_name, {'events': {}}))
        bottle_schedule_expression: str = bert_shortcuts.get_if_exists(
            'events.bottle_schedule_expression', 'rate(5 minutes)', str,
            bert_configuration.get('every_lambda', {'events':{}}),
            bert_configuration.get(job_name, {'events': {}}))

        cognito = bert_shortcuts.get_if_exists(
            'cognito', {}, dict,
            bert_configuration.get('every_lambda', {'triggers': []}),
            bert_configuration.get(job_name, {'triggers': []}))

        dynamodb_tables = bert_shortcuts.get_if_exists(
            'dynamodb.tables', [], list,
            bert_configuration.get('every_lambda', {'dynamodb': {}}),
            bert_configuration.get(job_name, {'dynamodb': {}}))

        api_stage: str = bert_shortcuts.get_if_exists(
            'api.stage', None, str,
            bert_configuration.get('every_lambda', {'api': {}}),
            bert_configuration.get(job_name, {'api': {}}))
        api_path: str = None
        api_method: str = None

        api = getattr(job, '_api', None)
        if not api is None:
            if api_stage is None:
                raise bert_exceptions.BertConfigError(f'Stage not found in bert-etl file for job[{job_name}]')

            api_path: str = api.route.route.strip('/')
            api_method: str = api.method.value

        batch_size: int = bert_shortcuts.get_if_exists('batch_size', '100', int,
            bert_configuration.get('every_lambda', {}),
            bert_configuration.get(job_name, {}))
        batch_size_delay: int = bert_shortcuts.get_if_exists('batch_size_delay', '0', int,
            bert_configuration.get('every_lambda', {}),
            bert_configuration.get(job_name, {}))

        timeout: int = bert_shortcuts.get_if_exists('timeout', '900', int, bert_configuration.get('every_lambda', {}), bert_configuration.get(job_name, {}))
        env_vars: typing.Dict[str, str] = bert_shortcuts.merge_env_vars(
            bert_configuration.get('every_lambda', {'environment': {}}).get('environment', {}),
            bert_configuration.get(job_name, {'environment': {}}).get('environment', {}))

        # Set QueueType to dynamodb unless they've specifically requested a BERT_QUEUE_TYPE
        env_vars['BERT_QUEUE_TYPE'] = env_vars.get('BERT_QUEUE_TYPE', 'dynamodb')
        env_vars['BERT_MODULE_NAME'] = module_name
        if not cognito.get('triggers', None) is None:
            env_vars['COGNITO_CLIENT_ID'] = cognito['client_id']
            env_vars['COGNITO_USER_POOL_ID'] = cognito['user_pool_id']

        requirements: typing.Dict[str, str] = bert_shortcuts.merge_requirements(
            bert_configuration.get('every_lambda', {'requirements': {}}).get('requirements', {}),
            bert_configuration.get(job_name, {'requirements': {}}).get('requirements', {}))

        if not api_stage is None:
            job_handler = f'{job.func_space}.{job_name}_api_handler'

        elif job.pipeline_type is bert_constants.PipelineType.BOTTLE and job.parent_noop_space == False:
            job_handler = f'{job.func_space}.{job_name}_manager'

        else:
            job_handler = f'{job.func_space}.{job_name}_handler'

        confs[job_name] = {
                'job': job,
                'deployment': {key: value for key, value in deployment_config._asdict().items()},
                'aws-deployed': {
                    'events': {},
                    'bottle': {},
                    'iam': {},
                    'kms': {},
                    'cognito': {},
                    'dynamodb': {},
                },
                'aws-deploy': {
                    'timeout': timeout,
                    'runtime': runtime,
                    'memory-size': memory_size, # must be a multiple of 64, increasing memory size also increases cpu allocation
                    'requirements': requirements,
                    'handler': job_handler,
                    'lambda-name': job_name,
                    'work-table-name': job.work_key,
                    'done-table-name': job.done_key,
                    'environment': env_vars,
                    'cognito': cognito,
                    'batch-size': batch_size,
                    'batch-size-delay': batch_size_delay,
                    'concurrency-limit': concurrency_limit,
                    'invoke-args': invoke_args,
                    'layers': layers,
                    'dynamodb': {
                        'tables': dynamodb_tables,
                    },
                },
                'aws-build': {
                    'lambdas-path': os.path.join(os.getcwd(), 'lambdas'),
                    'excludes': ZIP_EXCLUDES + COMMON_EXCLUDES + ignore_items,
                    'path': os.path.join(os.getcwd(), 'lambdas', job_name),
                    'archive-path': os.path.join(os.getcwd(), 'lambdas', f'{job_name}.zip')
                },
                'runner': {
                    'environment': env_vars,
                    'max-retries': 10,
                },
                'iam': {
                    'execution-role-arn': iam_execution_role_arn,
                },
                'kms': {
                    'alias': kms_alias,
                    'usernames': kms_usernames,
                },
                'events': {
                    'schedule-expression': schedule_expression,
                    'sns-topic-arn': sns_topic_arn,
                    # "cron(0 20 * * ? *)" or "rate(5 minutes)"
                    # 'rate': 'rate(5 minutes)',
                },
                'api': {
                    'stage': api_stage,
                    'name': f'{job_name}-rest-api',
                    'path': api_path,
                    'method': api_method,
                },
                'bottle': {
                    'schedule-expression': bottle_schedule_expression,
                },
                'spaces': {
                    'func_space': job.func_space,
                    'work-key': job.work_key,
                    'done-key': job.done_key,
                    'pipeline-type': job.pipeline_type,
                    'workers': job.workers,
                    'scheme': job.schema,
                    'parent': {
                        'noop-space': job.parent_noop_space,
                        'space': job.parent_space,
                        'work-key': job.parent_func_work_key,
                        'done-key': job.parent_func_done_key,
                    },
                    'min_proced_items': min_proced_items,
                },
                'encoding': {
                    'identity_encoders': identity_encoders,
                    'queue_encoders': queue_encoders,
                    'queue_decoders': queue_decoders,
                }
            }
        pass

    return confs

def run_command(cmd: str, allow_error: typing.List[int] = [0]) -> str:
    ologger = logging.getLogger('.'.join([__name__, multiprocessing.current_process().name]))
    cmd: typing.List[str] = cmd.split(' ')
    proc = subprocess.Popen(' '.join(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    while proc.poll() is None:
        time.sleep(.1)

    if proc.poll() > 0:
        if not proc.poll() in allow_error:
            raise NotImplementedError(f'{proc.poll()}, {proc.stderr.read()}')

        return proc.stderr.read().decode(bert_constants.ENCODING)

    return proc.stdout.read().decode(bert_constants.ENCODING)


def comm_binders(func: types.FunctionType) -> typing.Tuple['QueueType', 'QueueType', 'ologger']:
    ologger = logging.getLogger('.'.join([func.__name__, multiprocessing.current_process().name]))
    ologger.debug(f'Bert Queue Type[{bert_constants.QueueType}]')
    if bert_constants.QueueType is bert_constants.QueueTypes.Dynamodb:
        return bert_queues.DynamodbQueue(func.work_key), bert_queues.DynamodbQueue(func.done_key), ologger

    elif bert_constants.QueueType is bert_constants.QueueTypes.StreamingQueue:
        return bert_queues.StreamingQueue(func.work_key), bert_queues.StreamingQueue(func.done_key), ologger

    elif bert_constants.QueueType is bert_constants.QueueTypes.LocalQueue:
        return bert_queues.LocalQueue(func.work_key), bert_queues.LocalQueue(func.done_key), ologger

    elif bert_constants.QueueType is bert_constants.QueueTypes.Redis:
        return bert_queues.RedisQueue(func.work_key), bert_queues.RedisQueue(func.done_key), ologger

    else:
        raise NotImplementedError(f'Unsupported QueueType[{bert_constants.QueueType}]')


def flush_db():
    if bert_constants.QueueType in [
        bert_constants.QueueType.Dynamodb,
        bert_constants.QueueType.StreamingQueue]:
        raise NotImplementedError(f'Flush Dynamodb Tables')

    elif bert_constants.QueueType is bert_constants.QueueType.Redis:
        import redis
        from bert import constants, datasource
        redis_connection: datasource.RedisConnection = datasource.RedisConnection.ParseURL(constants.REDIS_URL)
        logger.info(f'Flushing Redis DB[{redis_connection.db}]')
        redis_connection.client.flushdb()

    else:
        raise NotImplementedError(constants.QueueType)


