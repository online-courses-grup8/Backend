from rest_framework import serializers
from courses.models import Instructor,InstructorSkill


class InstructorSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Instructor
        fields = ['id', 'name', 'photo', 'specialization']

    def get_photo(self, obj):
        if obj.photo:
            return obj.photo.name.split("/")[-1]
        return None

class InstructorDetailSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()  # arka plan görseli

    class Meta:
        model = Instructor
        fields = [
            "id", "name", "photo","thumbnail", "specialization",
            "experience", "position",
            "bio_hardskill", "bio_softskill",
            "facebook", "instagram", "linkedin", "twitter"
        ]

    def get_photo(self, obj):
        if obj.photo:
            return obj.photo.name.split("/")[-1]
        return None

    def get_thumbnail(self, obj):
        # sadece dosya adını döndürür
        if obj.thumbnail:
            return obj.thumbnail.name.split("/")[-1]
        return None

class InstructorListSerializer(serializers.ModelSerializer):
    # teacher listesi sayfası için
    thumbnail = serializers.SerializerMethodField()  # arka plan görseli

    class Meta:
        model = Instructor
        fields = [
            'id', 'name', 'slug', 'thumbnail', 'position',
            'facebook', 'instagram', 'linkedin', 'twitter'
        ]

    def get_thumbnail(self, obj):
        # sadece dosya adını döndürür
        if obj.thumbnail:
            return obj.thumbnail.name.split("/")[-1]
        return None

class InstructorSkillSerializer(serializers.ModelSerializer):
    # skill bar'lar için
    class Meta:
        model = InstructorSkill
        fields = ['skill', 'percentage']


class TeacherDetailSerializer(serializers.ModelSerializer):
    # teacher detay sayfası için, skill bar'lar dahil
    photo = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()  # arka plan görseli
    skills = InstructorSkillSerializer(many=True, read_only=True)

    class Meta:
        model = Instructor
        fields = [
            "id", "name", "slug", "photo", "thumbnail", "specialization",
            "experience", "position", "phone_number",
            "bio_hardskill", "bio_softskill",
            "facebook", "instagram", "linkedin", "twitter",
            "skills"
        ]

    def get_photo(self, obj):
        if obj.photo:
            return obj.photo.name.split("/")[-1]
        return None

    def get_thumbnail(self, obj):
        # sadece dosya adını döndürür
        if obj.thumbnail:
            return obj.thumbnail.name.split("/")[-1]
        return None