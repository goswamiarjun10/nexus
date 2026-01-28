from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'tags', 'published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input block w-full bg-gray-100 rounded-xl border border-gray-300 focus:border-indigo-500 focus:bg-white px-4 py-3 text-lg',
                'placeholder': 'Title',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-input block w-full min-h-[150px] bg-gray-100 rounded-xl border border-gray-300 focus:border-indigo-500 focus:bg-white px-4 py-3 text-lg',
                'placeholder': 'Content',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-3 file:px-5 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 cursor-pointer',
            }),
            'category': forms.Select(attrs={
                'class': 'form-input block w-full bg-gray-100 rounded-xl border border-gray-300 focus:border-indigo-500 focus:bg-white px-4 py-3 text-lg',
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-input block w-full bg-gray-100 rounded-xl border border-gray-300 focus:border-indigo-500 focus:bg-white px-4 py-3 text-lg',
            }),
            'published': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded',
            }),
        }
