from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from del_corso.config import general_config
from store.models import SeasonCategory


class BannerImage(models.Model):
    image = models.FileField(
        upload_to=general_config.TARGET_IMAGE_DIR,
        verbose_name="Изображение",
        validators=[FileExtensionValidator(allowed_extensions=("png", "jpg"))],
    )
    main = models.BooleanField(default=False, verbose_name="Главная фотография")
    season_category = models.OneToOneField(
        SeasonCategory,
        on_delete=models.CASCADE,
        verbose_name="Фотография сезона",
        null=True,
        blank=True
    )

    def clean(self):
        if self.main and self.season_category:
            raise ValidationError({'main': 'Выберите либо Главную фотографию, либо Фотографию сезона'})

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        storage.delete(path)

        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"
