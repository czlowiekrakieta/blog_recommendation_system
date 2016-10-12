from django import forms
from .models import Comment, Vote, votes

class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea)


    class Meta:
        model = Comment
        fields = [
            'content'
        ]

    def clean(self, *args, **kwargs):
        content = self.cleaned_data.get("content")
        return super(CommentForm, self).clean(*args, **kwargs)


class VoteForm(forms.ModelForm):
    vote = forms.ChoiceField(choices=votes)

    class Meta:
        model = Vote
        fields = [
            'vote'
        ]

    def clean(self, *args, **kwargs):
        vote = self.cleaned_data.get("vote")
        return super(VoteForm, self).clean(*args, **kwargs)

