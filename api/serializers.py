from rest_framework import serializers
from django.contrib.auth import get_user_model

from posts.models import Post, Comment, Group, Follow


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    following = serializers.SlugRelatedField(queryset=User.objects.all(),
                                             slug_field='username')

    class Meta:
        fields = ('id', 'user', 'following')
        model = Follow

    def validate(self, data):
        following = data['following']
        user = User.objects.get(username=self.context['request'].user)
        follow = Follow.objects.filter(user=user, following=following)
        if follow:
            raise serializers.ValidationError("Вы уже подписаны")
        data['following'] = following
        data['user'] = user
        return data
