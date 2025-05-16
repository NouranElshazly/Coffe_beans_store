from django import forms
from .models import MenuItem 

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price','image', 'is_best_seller', 'quantity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'is_best_seller': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),

        } # DEFAULT IS INPUT TYTPE SO WE REWRITE IT AS TEXTAREA

# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['name', 'description']

def clean_image(self):
    image = self.cleaned_data.get('image')
    if image and image.size > 1024 * 1024 * 5:
        raise forms.ValidationError("The image file size must be less than 5MB")
    return image
