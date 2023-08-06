from django.contrib.auth import get_user_model
from rest_framework import serializers
from taggit_serializer.serializers import (
    TagListSerializerField, TaggitSerializer)
from .models import (
    Node,
    Collection, Media,
    MediaImage, MediaFile,
    NodePermission,
)
from .appconfig import MB_IMAGE_EXTENSIONS

import logging
logger = logging.getLogger(__name__)
USER_MODEL = get_user_model()


class FlatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ('id', 'username', 'first_name', 'last_name')


class FlatNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ('slug', 'name')


class NodePermissionSerializer(serializers.ModelSerializer):
    node_data = serializers.SerializerMethodField()
    user_data = serializers.SerializerMethodField()

    def get_node_data(self, instance):
        return FlatNodeSerializer(instance.node).data

    def get_user_data(self, instance):
        return FlatUserSerializer(instance.user).data

    class Meta:
        model = NodePermission
        fields = "__all__"
        extra_kwargs = {
            'node': {'write_only': True},
            'user': {'write_only': True},
        }


class FlatNodePermissionSerializer(serializers.ModelSerializer):
    node = FlatNodeSerializer(read_only=True)
    user = FlatUserSerializer(read_only=True)

    class Meta:
        model = NodePermission
        fields = ('node', 'user',)


class CollectionSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    shared_with = serializers.SerializerMethodField()

    def get_shared_with(self, model):
        data = NodePermission.objects.filter(node=model)
        return FlatNodePermissionSerializer(data, many=True).data

    class Meta:
        model = Collection
        fields = ('slug', 'owner', 'name', 'shared_with', 'parent')


class FlatCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('slug', 'name')


class SharedCollectionSerializer(serializers.ModelSerializer):
    owner = FlatUserSerializer(read_only=True)

    class Meta:
        model = Collection
        fields = ('slug', 'owner', 'name', )


class SharedMediaFileSerializer(TaggitSerializer, serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    tags = TagListSerializerField()

    def get_file_url(self, model):
        if not model.file:
            return ''
        return model.get_file_url()

    class Meta:
        model = MediaFile
        fields = ('slug', 'file_url', 'tags', )


class SharedMediaImageSerializer(
        TaggitSerializer, serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    tags = TagListSerializerField()

    def get_image_url(self, model):
        if not model.image:
            return ''
        return model.get_image_url()

    class Meta:
        model = MediaImage
        fields = ('image_url', 'alt_text', 'height', 'width', 'tags',)


SHARED_MEDIA_SERIALIZERS = {
    "mediaimage": SharedMediaImageSerializer,
    "mediafile": SharedMediaFileSerializer
}


class SharedMediaSerializer(TaggitSerializer, serializers.ModelSerializer):
    owner = FlatUserSerializer(read_only=True)
    tags = TagListSerializerField()
    media = serializers.SerializerMethodField()
    permission = serializers.SerializerMethodField()

    def get_media(self, model):
        media_type = model.media_type
        if media_type:
            data = SHARED_MEDIA_SERIALIZERS[media_type](
                model.media_data, context=self.context).data
            data["type"] = media_type
            return data
        return None

    def get_permission(self, model):
        try:
            return NodePermission.objects.get(
                user=self.context['request'].user, node=model).permission
        except Exception:
            return ''

    class Meta:
        model = Media
        fields = (
            'slug',
            'name',
            'owner',
            'parent',
            'published',
            'tags',
            'permission',
            'media',
        )
        extra_kwargs = {
            'name': {'read_only': True}
        }


class SharedWithSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=USER_MODEL.objects.all())
    permission = serializers.ChoiceField(
        choices=(("e", "Edit"), ("v", "View")), write_only=True)


class MediaImageSerializer(TaggitSerializer, serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    parent = FlatCollectionSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    image = serializers.ImageField(write_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(
        write_only=True, source='parent', required=False,
        queryset=Collection.objects.all())
    tags = TagListSerializerField(required=False, write_only=True)

    thumbnail = serializers.SerializerMethodField()
    published_path = serializers.ReadOnlyField()

    def get_thumbnail(self, model):
        if not model.thumbnail:
            return ''
        return model.get_thumbnail_url()

    def get_image_url(self, model):
        if not model.image:
            return ''
        return model.get_image_url()

    def validate(self, data):
        vdata = super().validate(data)
        parent_data = vdata.get('parent', None)
        if parent_data:
            if parent_data.owner == vdata['owner'] or \
                    NodePermission.objects.filter(
                        user=vdata['owner'], parent=parent_data,
                        permission='e').exists():
                return vdata
            else:
                raise serializers.ValidationError(
                    'Not enough permission for adding to this parent')
        else:
            return vdata

    class Meta:
        model = MediaImage
        fields = (
            'owner',
            'parent',
            'parent_id',
            'image_url',
            'image',
            'alt_text',
            'thumbnail',
            'height',
            'width',
            # 'shared_with',
            'published',
            'published_path',
            'tags',
            'name',
        )
        extra_kwargs = {
            "name": {"required": False},
            # "shared_with": {"write_only": True},
        }


class MediaFileSerializer(TaggitSerializer, serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    parent = FlatCollectionSerializer(read_only=True)
    file_url = serializers.SerializerMethodField()
    file = serializers.FileField(write_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(
        write_only=True, source='parent', required=False,
        queryset=Collection.objects.all())

    tags = TagListSerializerField(required=False, write_only=True)
    published_path = serializers.ReadOnlyField()

    def get_file_url(self, model):
        if not model.file:
            return ''
        return model.get_file_url()

    def validate(self, data):
        vdata = super().validate(data)
        parent_data = vdata.get('parent', None)
        if parent_data:
            if parent_data.owner == vdata['owner'] or \
                    NodePermission.objects.filter(
                        user=vdata['owner'], parent=parent_data,
                        permission='e').exists():
                return vdata
            else:
                raise serializers.ValidationError(
                    'Not enough permission for adding to this parent')
        else:
            return vdata

    class Meta:
        model = MediaFile
        fields = (
            'owner',
            'parent',
            'parent_id',
            # 'shared_with',
            'file_url',
            'file',
            'published',
            'published_path',
            'tags',
            'name',
        )
        extra_kwargs = {
            "name": {"required": False},
            "published": {"write_only": True},
            # "shared_with": {"write_only": True},

        }


MEDIA_SERIALIZERS = {
    "mediaimage": MediaImageSerializer,
    "mediafile": MediaFileSerializer
}
MEDIA_FIELD = (("mediaimage", "image"), ("mediafile", "file"))


class MediaSerializer(TaggitSerializer, serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = TagListSerializerField(required=False)
    media_file = serializers.FileField(write_only=True)
    media_object = serializers.DictField(write_only=True, required=False)
    media = serializers.SerializerMethodField()
    shared_user = serializers.SerializerMethodField()

    def get_media(self, model):
        media_type = model.media_type
        if media_type:
            data = MEDIA_SERIALIZERS[media_type](
                model.media_data, context=self.context).data
            data["type"] = media_type
            return data
        return None

    def get_shared_user(self, instance):
        data = instance.shared_with.all()
        return FlatUserSerializer(data, many=True).data

    class Meta:
        model = Media
        fields = (
            'slug',
            'name',
            'owner',
            'parent',
            'tags',
            'published',
            'media_file',
            'media_object',
            'media',
            'shared_user',
        )
        extra_kwargs = {
            "name": {"required": False},
            "parent": {"write_only": True},
        }

    def media_field_name(self, file):
        extension = str(file).split(".")[-1].lower()
        if extension in MB_IMAGE_EXTENSIONS:
            return MEDIA_FIELD[0]
        else:
            return MEDIA_FIELD[1]

    def update(self, instance, validated_data):
        # extract all data
        validated_data.update(validated_data.get("media_object", {}))

        parent = validated_data.get("parent")
        if(parent):
            validated_data["parent_id"] = parent.id

        media_file = validated_data.pop("media_file")
        media_type, field_name = self.media_field_name(media_file)
        validated_data[field_name] = media_file

        serailizer = MEDIA_SERIALIZERS[media_type]
        sobj = serailizer(
            instance.media_data, data=validated_data, context=self.context)
        validity = sobj.is_valid()
        logger.critical(f"{validity}---{sobj.errors}")
        m = sobj.save()
        return Media.objects.get(id=m.id)

    def create(self, validated_data):
        # extract all different  data
        validated_data.update(validated_data.get("media_object", {}))

        # add parent if necessary
        parent = validated_data.get("parent")
        if(parent):
            validated_data["parent_id"] = parent.id

        # Get proper field and file
        media_file = validated_data.pop("media_file")
        media_type, field_name = self.media_field_name(media_file)
        validated_data[field_name] = media_file

        # Serialize and save data
        serailizer = MEDIA_SERIALIZERS[media_type]
        sobj = serailizer(data=validated_data, context=self.context)
        validity = sobj.is_valid()
        logger.critical(f"{validity}---{sobj.errors}")
        m = sobj.save()

        return Media.objects.get(id=m.id)
