import jdatetime
from rest_framework import serializers

from .models import Artist, GenreMovie, GenreMusic, Image, Movie, Music, Serial, Staff, Comment


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ["id", "first_name", "last_name", "nick_name", "birth_date", "birth_date_persian"]

    birth_date_persian = serializers.SerializerMethodField()

    def get_birth_date_persian(self, obj):
        if obj.birth_date:
            return jdatetime.date.fromgregorian(date=obj.birth_date).strftime("%Y/%m/%d")
        return None


class GenreMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreMovie
        fields = ["id", "title"]


class GenreMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreMusic
        fields = ["id", "title"]


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["user", "username", "email", "full_name", "phone_number"]
        read_only_fields = ["user"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["user", "text", "is_active", "movie", "serial", "music"]

    user = StaffSerializer()


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            "image"
        ]

    image = serializers.StringRelatedField()

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "year",
            "runtime",
            "runtime_minutes",
            "status",
            "director",
            "country",
            "plot",
            "poster",
            "rating",
            "release_date",
            "genre",
            "cast",
            "comments",
            "images"
        ]

    runtime_minutes = serializers.SerializerMethodField()
    director = ArtistSerializer(read_only=True)
    genre = GenreMovieSerializer(many=True, read_only=True)
    cast = ArtistSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    def get_runtime_minutes(self, movie):
        return f"{movie.runtime} minutes"

    def validate(self, data):
        ALAKI_YEAR = 1945
        if data["year"] == ALAKI_YEAR:
            raise serializers.ValidationError(
                f"The year {ALAKI_YEAR} was after WW2 and no movies released in {ALAKI_YEAR}!"
            )
        return data

    # اگر تابع update رو بنویسیم، مطابق چیزی که ما نوشتیم عمل میکنه. اگه ننویسیم از دیفالت خودش استفاده میکنه.
    # def update(self, instance: Movie, validated_data):
    #     instance.plot = validated_data.get('plot', "اگه پلات ارسال نشده بود این رو بنویس :دی هر چیز دیگه ای رو هم میشه تغییر داد. نمونه نوشتم که داشته باشیم.")
    #     instance.save()
    #     return instance


class SerialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serial
        fields = [
            "id",
            "title",
            "number_of_seasons",
            "number_of_episodes",
            "average_runtime",
            "average_runtime_minutes",
            "begin_year",
            "end_year",
            "country",
            "plot",
            "poster",
            "rating",
            "start_release_date",
            "end_release_date",
            "director",
            "genre",
            "cast",
        ]

    average_runtime_minutes = serializers.SerializerMethodField()
    director = ArtistSerializer(read_only=True)
    genre = GenreMovieSerializer(many=True, read_only=True)
    cast = ArtistSerializer(many=True, read_only=True)

    def get_average_runtime_minutes(self, serial):
        return f"{serial.average_runtime} minutes"


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        exclude = ["datetime_created", "datetime_modified"]

    duration_seconds = serializers.SerializerMethodField()
    duration_minutes = serializers.SerializerMethodField()
    main_singer = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())
    main_singer_info = ArtistSerializer(source="main_singer", read_only=True)
    genre = GenreMovieSerializer(many=True, read_only=True)
    other_singers = ArtistSerializer(many=True, read_only=True)

    def get_duration_seconds(self, music):
        return f"{music.duration} seconds"

    def get_duration_minutes(self, music):
        t = music.duration
        m = t // 60
        s = t % 60
        return f"{m:02}:{s:02}"
