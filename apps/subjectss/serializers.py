from rest_framework.serializers import ModelSerializer

from subjectss.models import GeneralSubject


class GeneralSubjectBaseSerializer(ModelSerializer):
    class Meta:
        model: GeneralSubject = GeneralSubject
        fields: str | tuple[str] = "__all__"
