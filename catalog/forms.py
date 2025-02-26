from django import forms
from django.core.exceptions import ValidationError

from .models import Category, Product

FORBIDDEN_WORDS = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]
        exclude = ("owner", "views_counter")

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label="Выберите категорию", required=False
    )

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        # Добавление классов CSS к полям формы
        self.fields["name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите название продукта"})
        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите описание продукта", "rows": 3}
        )
        self.fields["image"].widget.attrs.update({"class": "form-control"})
        self.fields["category"].widget.attrs.update({"class": "form-select"})
        self.fields["price"].widget.attrs.update({"class": "form-control", "placeholder": "Введите цену продукта"})

    def clean_name(self):
        name = self.cleaned_data["name"]
        self.validate_forbidden_words(name)
        return name

    def clean_description(self):
        description = self.cleaned_data["description"]
        self.validate_forbidden_words(description)
        return description

    def validate_forbidden_words(self, text):
        text_lower = text.lower()
        for word in FORBIDDEN_WORDS:
            if word in text_lower:
                raise forms.ValidationError(f'Слово "{word}" недопустимо в данном поле.')

    def clean_price(self):
        price = self.cleaned_data.get("price")

        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")

        return price

    def clean_image(self):
        image = self.cleaned_data.get("image")

        # Проверка формата файла
        if image:
            # Получаем расширение файла
            ext = image.name.split(".")[-1].lower()
            valid_extensions = ["jpeg", "jpg", "png"]

            if ext not in valid_extensions:
                raise ValidationError("Файл должен быть в формате JPEG или PNG.")

            # Проверка размера файла (максимум 5 МБ)
            if image.size > 5 * 1024 * 1024:  # 5 MB in bytes
                raise ValidationError("Размер файла не должен превышать 5 МБ.")

        return image

class ProductModeratorForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["description", "category", "is_published"]
