from rest_framework import serializers
from filer.models import Image, File, Folder

class FilerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = (
            'id', 
            'folder_id',
            'file',
            'name'
        )
        depth = 1


class FilerFolderSerializer(serializers.ModelSerializer):
    all_files = FilerSerializer(many=True)
    class Meta:
        model = Folder
        fields = (
            'id', 
            'name',
            'all_files',
        )
        depth = 0