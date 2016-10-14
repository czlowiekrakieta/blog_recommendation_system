from .models import Blog, UserFollowings, Rating, languages, fields
from django import forms
rates = [x for x in enumerate(['not at all', 'a bit', 'evenly with other topics', 'dominates others',
                               'speaks only about it'])]


class SearchForm(forms.Form):
    search = forms.CharField()

    class Meta:
        fields = [
            'search'
        ]

class AdvSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AdvSearchForm, self).__init__(*args, **kwargs)
        self.initial['and_or'] = 1
        for f in fields:
            self.initial[f + "lesser"] = 4
            self.fields[f + "lesser"].label = str(f.replace("_", " ") + " lesser than")
            self.fields[f + "greater"].label = str(f.replace("_", " ") + " greater than")

    and_or = forms.ChoiceField(choices=[(0, "AND"), (1, "OR")], required=False)
    search = forms.CharField(required=False)
    politicsgreater = forms.ChoiceField(choices=rates)
    politicslesser = forms.ChoiceField(choices=rates[::-1])
    sportsgreater = forms.ChoiceField(choices=rates)
    sportslesser = forms.ChoiceField(choices=rates[::-1])
    travelgreater = forms.ChoiceField(choices=rates)
    travellesser = forms.ChoiceField(choices=rates[::-1])
    fashiongreater = forms.ChoiceField(choices=rates)
    fashionlesser = forms.ChoiceField(choices=rates[::-1])
    soft_sciencegreater = forms.ChoiceField(choices=rates)
    soft_sciencelesser = forms.ChoiceField(choices=rates[::-1])
    hard_sciencegreater = forms.ChoiceField(choices=rates)
    hard_sciencelesser = forms.ChoiceField(choices=rates[::-1])
    techgreater = forms.ChoiceField(choices=rates)
    techlesser = forms.ChoiceField(choices=rates[::-1])
    culturegreater = forms.ChoiceField(choices=rates)
    culturelesser = forms.ChoiceField(choices=rates[::-1])
    general_ratingsgreater = forms.ChoiceField(choices=rates)
    general_ratingslesser = forms.ChoiceField(choices=rates[::-1])

    class Meta:
        fields = [
            'search',
            'and_or',
            'politicsgreater',
            'politicslesser',
            'sportsgreater',
            'sportslesser',
            'fashionlesser',
            'fashiongreater',
            'travelgreater',
            'travellesser',
            'culturegreater',
            'culturelesser',
            'techgreater',
            'techlesser',
            'soft_sciencegreater',
            'soft_sciencelesser',
            'hard_sciencegreater',
            'hard_sciencelesser',
            'general_ratingsgreater',
            'general_ratingslesser',
        ]

class NewBlogForm(forms.ModelForm):
    name = forms.CharField()
    author = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    language = forms.ChoiceField(choices=languages)
    politics = forms.ChoiceField(choices=rates)
    sports = forms.ChoiceField(choices=rates)
    travel = forms.ChoiceField(choices=rates)
    fashion = forms.ChoiceField(choices=rates)
    soft_science = forms.ChoiceField(choices=rates)
    hard_science = forms.ChoiceField(choices=rates)
    tech = forms.ChoiceField(choices=rates)
    culture = forms.ChoiceField(choices=rates)

    class Meta:
        model = Blog
        fields = [
            'name',
            'author',
            'description',
            'language',
            'politics',
            'sports',
            'fashion',
            'travel',
            'culture',
            'tech',
            'soft_science',
            'hard_science',
        ]

    def clean(self, *args, **kwargs):
        name = self.cleaned_data.get('name')
        author = self.cleaned_data.get('author')
        description = self.cleaned_data.get('description')
        language = self.cleaned_data.get('language')
        politics = self.cleaned_data.get("politics")
        travel = self.cleaned_data.get("travel")
        sports = self.cleaned_data.get("sports")
        culture = self.cleaned_data.get("culture")
        tech = self.cleaned_data.get("tech")
        soft_science = self.cleaned_data.get("soft_science")
        hard_science = self.cleaned_data.get("hard_science")
        fashion = self.cleaned_data.get("fashion")
        #general_ratings = self.cleaned_data.get("rating")

        return super(NewBlogForm, self).clean(*args, **kwargs)

class RatingForm(forms.ModelForm):
    politics = forms.ChoiceField(choices=rates)
    sports = forms.ChoiceField(choices=rates)
    travel = forms.ChoiceField(choices=rates)
    fashion = forms.ChoiceField(choices=rates)
    soft_science = forms.ChoiceField(choices=rates)
    hard_science = forms.ChoiceField(choices=rates)
    tech = forms.ChoiceField(choices=rates)
    culture = forms.ChoiceField(choices=rates)
    general_ratings = forms.ChoiceField(choices=[x for x in enumerate(["bad", "meh", "good"])])

    class Meta:
        model = Rating
        fields = [
            'politics',
            'sports',
            'fashion',
            'travel',
            'culture',
            'tech',
            'soft_science',
            'hard_science',
            'general_ratings'
        ]

    def clean(self, *args, **kwargs):
        politics = self.cleaned_data.get("politics")
        travel = self.cleaned_data.get("travel")
        sports = self.cleaned_data.get("sports")
        culture = self.cleaned_data.get("culture")
        tech = self.cleaned_data.get("tech")
        soft_science = self.cleaned_data.get("soft_science")
        hard_science = self.cleaned_data.get("hard_science")
        fashion = self.cleaned_data.get("fashion")
        general_ratings = self.cleaned_data.get("rating")

        return super(RatingForm, self).clean(*args, **kwargs)


