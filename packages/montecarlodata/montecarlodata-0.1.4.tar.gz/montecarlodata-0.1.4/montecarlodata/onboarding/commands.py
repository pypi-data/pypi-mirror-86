import click
import click_config_file

import montecarlodata.settings as settings
from montecarlodata.errors import complain_and_abort
from montecarlodata.onboarding.data_lake.presto import PrestoOnBoardService


@click.group(help='On-board Monte Carlo warehouse or data-lake.')
def onboarding():
    """
    Group for any onboard sub-commands
    """
    pass


@onboarding.command(help='Setup a Presto SQl Connection. For health queries like metrics and distribution.')
@click.pass_obj
@click.option('--host', help='Hostname.', required=True)
@click.option('--port', help='HTTP port (default=8889).', default=8889, type=click.INT)
@click.option('--user', help='Username with access to catalog/schema.', required=False)
@click.password_option('--password', help='User\'s password.', prompt='Password for user (enter to skip)',
                       default='', required=False)
@click.option('--catalog', help='Mount point to access data source.', required=False)
@click.option('--schema', help='Schema to access.', required=False)
@click.option('--http-scheme', help='Scheme for authentication.',
              type=click.Choice(['http', 'https'], case_sensitive=True), required=True)
@click.option('--cert-file', help='Local SSL certificate file to upload to collector.', required=False,
              type=click.Path(dir_okay=False, exists=True))
@click.option('--cert-s3', help='Object path (key) to a certificate already uploaded to the collector.',
              required=False)
@click_config_file.configuration_option(settings.OPTION_FILE_FLAG)
def presto_sql(ctx, host, port, user, password, catalog, schema, http_scheme, cert_file, cert_s3):
    """
    Onboard a presto sql connection
    """
    if not password:
        password = None  # make explicitly null if not set. Prompts can't be None
    if cert_file is not None and cert_s3 is not None:
        complain_and_abort('Can have a cert-file or cert-s3-path, but not both')
    PrestoOnBoardService(config=ctx['config']).onboard_presto_sql(host=host, port=port, user=user, password=password,
                                                                  catalog=catalog, schema=schema,
                                                                  http_scheme=http_scheme, cert_file=cert_file,
                                                                  cert_s3=cert_s3)


@onboarding.command(help='Setup a Presto S3 Connection. For query logs.')
@click.pass_obj
@click.option('--bucket', help='S3 Bucket where query logs are contained.', required=True)
@click.option('--prefix', help='Path to query logs.', required=True)
@click.option('--role', help='Assumable role to use for accessing S3.', required=False)
@click.option('--external-id', help='An external id, per assumable role conditions.', required=False)
@click_config_file.configuration_option(settings.OPTION_FILE_FLAG)
def presto_s3(ctx, bucket, prefix, role, external_id):
    """
    Onboard a presto s3 connection
    """
    PrestoOnBoardService(config=ctx['config']).onboard_presto_s3(bucket=bucket, prefix=prefix,
                                                                 assumable_role=role, external_id=external_id)
