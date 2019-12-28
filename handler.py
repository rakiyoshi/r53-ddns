import boto3
import json
import os
from datetime import date, datetime


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ('Type %s not serializable' % type(obj))


def _get_hosted_zone_id(client, hostname):
    hosted_zones = client.list_hosted_zones_by_name(DNSName=hostname)['HostedZones']
    hosted_zones = hosted_zones
    if len(hosted_zones) != 1:
        return None
    hosted_zone_id = hosted_zones[0]['Id']
    return hosted_zone_id


def _get_record_sets(client, hosted_zone_id):
    record_sets = client.list_resource_record_sets(HostedZoneId=hosted_zone_id)['ResourceRecordSets']
    return record_sets


def _get_home_record_set(record_sets, hostname):
     target = [item for item in record_sets if item['Name'] == hostname and item['Type'] == 'A'][0]
     return target


def _update_recordset(client, target_resource_record_set, hosted_zone_id):
    response = client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Comment': 'r53-ddns',
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': target_resource_record_set
                }
            ]
        }
    )
    return response['ChangeInfo']


def hello(event, context):
    ip_addr = event['body'].get('ip')
    # Check whether ip field exist
    if not ip_addr:
        response = {
            'statusCode': 400,
            'body': '\'ip\' must be specified'
        }
    else:
        hostname = os.environ.get('HOSTNAME')
        recordset_name = os.environ.get('RECORDSET_NAME')

        client = boto3.client('route53')
        hosted_zone_id = _get_hosted_zone_id(client, hostname)
        print('HostedZoneId: {}'.format(hosted_zone_id))
        record_sets = _get_record_sets(client, hosted_zone_id)
        target = _get_home_record_set(record_sets, recordset_name)
        if ip_addr != target['ResourceRecords'][0]['Value']:
            print('Update')
            target['ResourceRecords'][0]['Value'] = ip_addr
            print(target)
            result = _update_recordset(client, target, hosted_zone_id)
            print(result)
            response = {
                'statusCode': 200,
                'result': json.loads(json.dumps(result, default=json_serial))
            }
        else:
            response = {
                'statusCode': 200,
                'result': 'IP address was not changed.'
            }

    print(response)
    return response
