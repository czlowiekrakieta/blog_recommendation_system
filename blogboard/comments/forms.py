from django import forms
from .models import Comment, Vote, votes

class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea)
    path = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Comment
        fields = [
            'content',
            'path'
        ]

    def clean(self, *args, **kwargs):
        content = self.cleaned_data.get("content")
        path = self.cleaned_data.get('path')
        return super(CommentForm, self).clean(*args, **kwargs)

    def set_path(self, path):
        self.initial = {"path": path}


class VoteForm(forms.ModelForm):
    vote = forms.ChoiceField(choices=votes)
    path = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Vote
        fields = [
            'vote',
            'path'
        ]

    def clean(self, *args, **kwargs):
        vote = self.cleaned_data.get("vote")
        path = self.cleaned_data.get("path")
        return super(VoteForm, self).clean(*args, **kwargs)

    def set_path(self, path):
        self.initial = {"path": path}

