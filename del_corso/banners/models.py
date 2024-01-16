from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from del_corso.config import general_config


class BannerImage(models.Model):
    image = models.FileField(
        upload_to=general_config.TARGET_IMAGE_DIR,
        verbose_name="Изображение",
        validators=[FileExtensionValidator(allowed_extensions=("png", "jpg"))],
    )
    main = models.BooleanField(default=False, verbose_name="Главная фотография")
    popular_categories = models.BooleanField(default=False, verbose_name="Фотография популярных категорий")

    def clean(self):
        if self.main and self.popular_categories:
            raise ValidationError({'main': 'Выберите либо Главную фотографию, либо Фотографию популярных категорий'})

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        storage.delete(path)

        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"
