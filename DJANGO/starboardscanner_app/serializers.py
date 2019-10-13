from django.contrib.auth.models import User, Group
from rest_framework import serializers

from starboardscanner_app.models import Report, Record


class ReportSerializer(serializers.ModelSerializer):
    records = serializers.StringRelatedField(many=True)

    class Meta:
        model = Report
        fields = ['id', 'amount_of_nodes', 'start_ip', 'end_ip', 'start_port', 'end_port', 'scan_type',
                  'scan_order', 'records']

    # def create(self, validated_data):
    #     return Report(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.amount_of_nodes = validated_data.get('amount_of_nodes', instance.amount_of_nodes)
    #     instance.start_ip = validated_data.get('start_ip', instance.start_ip)
    #     instance.end_ip = validated_data.get('end_pi', instance.end_ip)
    #     instance.start_port = validated_data.get('start_port', instance.start_port)
    #     instance.end_port = validated_data.get('end_port', instance.end_port)
    #     instance.scan_type = validated_data.get('scan_type', instance.scan_type)
    #     instance.scan_order = validated_data.get('scan_order', instance.scan_order)
    #     return instance


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['ip_port', 'status', 'created_by', 'report_id']

    # def create(self, validated_data):
    #     return Report(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.ip_port = validated_data.get('email', instance.ip_port)
    #     instance.status = validated_data.get('content', instance.status)
    #     instance.created_by = validated_data.get('created', instance.created_by)
    #     instance.report_id = validated_data.get('report_id', instance.report_id)
    #     return instance
