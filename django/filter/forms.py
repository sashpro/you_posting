# -*- encoding: utf-8
from django import forms
class FilterForm(forms.Form):
    age = (
        (None,'----'),
        ('13-17', '13-17'),
        ('18-24', '18-24'),
        ('25-34', '25-34'),
        ('34-44', '34-44'),
        ('45-54', '45-54'),
        ('55-64', '55-64'),
        ('65+', '65+'),
    )

    gen = (
        (None, '----'),
        ('male','male'),
        ('female','female'),
    )
    dev = (
        (None, '----'),
        ("desktop","DESKTOP"),
        ("mobile","MOBILE"),
        ("tablet","TABLET"),
    )
    ch_os = (
        (None, '----'),
        ('android','Android'),
        ('windows','Windows'),
        ('linux','Linux'),
        ('mac','Mac'),
        ('ios','iOs'),
    )


    region = forms.CharField(max_length=5, required=False, label=u'Регион')
    age_group = forms.ChoiceField(choices=age, required=False, label=u'Возр группы', )
    gender = forms.ChoiceField(choices=gen, required=False, label=u'Пол')
    device = forms.ChoiceField(choices=dev, required=False, label=u'Устройства')
    os = forms.ChoiceField(choices=ch_os, required=False, label=u'ОС')
    view_rate_min = forms.IntegerField(required=False)
    view_rate_max = forms.IntegerField(required=False)

