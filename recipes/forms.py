from django import forms

from recipes.models import Recipe, RecipeIngredient


class RecipeForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    name = forms.CharField(help_text='This is your help <a href="/contact/">Contact use</a>')
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    directions = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Recipe
        fields = ['name', 'description', 'directions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs.update({'class': 'form-control'})
        # self.fields['name'].label = ''
        for field in self.fields:
            add_data = {
                'class': 'form-control',
                'placeholder': f'Recipe {field}',
                'hx-post': '.',
                'hx-trigger': 'keyup change delay:100ms',
                'hx-target': '#recipe-container',
                'hx-swap': "outerHTML"
            }
            self.fields[field].widget.attrs.update(**add_data)


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['name', 'quantity', 'unit']
