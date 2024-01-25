from rest_framework import serializers
from .models import Ksiazka, FormaKsiazki, Gatunek


class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='tytul')
    author = serializers.CharField(source='autor')
    is_online = serializers.SerializerMethodField()
    availability = serializers.BooleanField(source='dostepnosc')
    genre = serializers.CharField(source='gatunek.nazwa')

    class Meta:
        model = Ksiazka
        fields = ['id', 'title', 'author', 'is_online', 'availability', 'genre']

    def get_is_online(self, obj):
        return obj.forma.nazwa == "Online"


class BookUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='tytul')
    author = serializers.CharField(source='autor')
    is_online = serializers.BooleanField(write_only=True)
    genre = serializers.CharField(source='gatunek.nazwa')

    class Meta:
        model = Ksiazka
        fields = ['title', 'author', 'is_online', 'genre']

    def update(self, instance, validated_data):
        instance.tytul = validated_data.get('tytul', instance.tytul)
        instance.autor = validated_data.get('autor', instance.autor)

        if 'is_online' in validated_data:
            is_online = validated_data.get('is_online')
            forma_nazwa = "Online" if is_online else "Papierowa"
            try:
                forma = FormaKsiazki.objects.get(nazwa=forma_nazwa)
                instance.forma = forma
            except FormaKsiazki.DoesNotExist:
                raise serializers.ValidationError({'forma': f'Forma "{forma_nazwa}" nie istnieje.'})

        if 'gatunek' in validated_data:
            gatunek_nazwa = validated_data.get('gatunek')['nazwa']
            try:
                gatunek = Gatunek.objects.get(nazwa=gatunek_nazwa)
                instance.gatunek = gatunek
            except Gatunek.DoesNotExist:
                raise serializers.ValidationError({'gatunek': f'Gatunek "{gatunek_nazwa}" nie istnieje.'})

        instance.save()
        return instance
