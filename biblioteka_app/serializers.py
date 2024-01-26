from rest_framework import serializers
from .models import Ksiazka, FormaKsiazki, Gatunek


class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='tytul')
    author = serializers.CharField(source='autor')
    is_online = serializers.BooleanField(source='czy_online')
    availability = serializers.BooleanField(source='dostepnosc')
    genre = serializers.CharField(source='gatunek.nazwa')

    class Meta:
        model = Ksiazka
        fields = ['id', 'title', 'author', 'is_online', 'availability', 'genre']


class BookUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='tytul')
    author = serializers.CharField(source='autor')
    is_online = serializers.BooleanField(source='czy_online')
    genre = serializers.CharField(source='gatunek.nazwa')

    class Meta:
        model = Ksiazka
        fields = ['title', 'author', 'is_online', 'genre']

    def update(self, instance, validated_data):
        instance.tytul = validated_data.get('tytul', instance.tytul)
        instance.autor = validated_data.get('autor', instance.autor)
        instance.czy_online = validated_data.get('czy_online', instance.czy_online)
        if 'gatunek' in validated_data:
            gatunek_nazwa = validated_data.get('gatunek')['nazwa']
            try:
                gatunek = Gatunek.objects.get(nazwa=gatunek_nazwa)
                instance.gatunek = gatunek
            except Gatunek.DoesNotExist:
                raise serializers.ValidationError({'genre': f'Genre "{gatunek_nazwa}" does not exist.'})

        instance.save()
        return instance
