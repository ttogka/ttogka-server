from rest_framework.serializers import ModelSerializer

from rest_framework import serializers

from datas.models import Card, Benefit

class CardBaseModelSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

class CardListModelSerializer(CardBaseModelSerializer):
    class Meta(CardBaseModelSerializer.Meta):
        fields = [
            'id',
            'card',
            'brand',
            'image',
            'view_count',
        ]

class BenefitBaseModelSerializer(ModelSerializer):
    class Meta:
        model = Benefit
        fields = '__all__'

class CardDetailModelSerializer(CardBaseModelSerializer):
    class Meta(CardBaseModelSerializer.Meta):
        fields = [
            'id',
            'card',
            'brand',
            'image',
        ]