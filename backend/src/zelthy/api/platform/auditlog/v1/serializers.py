import importlib

from rest_framework import serializers

from zelthy.api.platform.tenancy.v1.serializers import AppUserModelSerializerModel
from zelthy.apps.auditlog.models import LogEntry
from zelthy.core.utils import get_datetime_str_in_tenant_timezone, get_current_request


class AuditLogSerializerModel(serializers.ModelSerializer):
    actor = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()
    action = serializers.SerializerMethodField()
    object = serializers.CharField(source="object_repr")
    object_uuid = serializers.SerializerMethodField()
    object_type = serializers.SerializerMethodField()

    def get_action(self, obj):
        return obj.get_action_display().capitalize()

    def get_timestamp(self, obj):
        return get_datetime_str_in_tenant_timezone(
            obj.timestamp, self.context["tenant"]
        )

    def get_actor(self, obj):
        actor = obj.tenant_actor
        if actor is not None:
            return actor.name
        actor = obj.platform_actor
        if actor is not None:
            return actor.user.username
        return None

    def get_object_uuid(self, obj):
        if obj.object_ref is not None:
            return str(obj.object_ref.object_uuid)

    def get_object_type(self, obj):
        return obj.content_type.model

    class Meta:
        model = LogEntry
        fields = [
            "id",
            "actor",
            "action",
            "object",
            "object_id",
            "object_uuid",
            "object_type",
            "timestamp",
            "changes",
        ]