from django import forms

from articles.models import Article


class ArticleCreateNewForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

    def clean(self):
        data = self.cleaned_data
        title = data.get('title')
        qs = Article.objects.filter(title__icontains=title)
        if qs.exists():
            self.add_error('title', f'the same information {title}')
            print(qs)
        return data


class ArticleCreateForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField()

    def clean(self):
        title = self.cleaned_data.get('title')
        if title.lower().strip() == 'worker':
            self.add_error('title', 'title do not be worker')
        content = self.cleaned_data.get('content')
        if content.lower().strip() in 'office' or title.lower() in 'office':
            self.add_error('content', 'content can`t be office')
            raise forms.ValidationError('office is not allowed')
        return self.cleaned_data

    # def clean_title(self):
    #     title = self.cleaned_data.get('title')
    #     if title.lower().strip() == 'worker':
    #         raise forms.ValidationError('title do not be worker')
    #     return title
