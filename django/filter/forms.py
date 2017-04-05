# -*- encoding: utf-8
from django import forms
class FilterForm(forms.Form):
    age = (
        (None,'----'),
        (0, '13-17'),
        (1, '18-24'),
        (2, '25-34'),
        (3, '34-44'),
        (4, '45-54'),
        (5, '55-64'),
        (6, '65+'),
    )

    gen = (
        (None, '----'),
        (0,'male'),
        (1,'female'),
    )
    dev = (
        (None, '----'),
        (0,'desktop'),
        (1,'mobile'),
    )
    ch_os = (
        (None, '----'),
        (0,'Android'),
        (1,'Windows'),
        (2,'Linux'),
        (3,'Mac'),
        (4,'iOs'),
    )

    region = forms.CharField(max_length=5, required=False, label=u'Регион')
    age_group = forms.ChoiceField(choices=age, required=False, label=u'Возр группы', )
    gender = forms.ChoiceField(choices=gen, required=False, label=u'Пол')
    device = forms.ChoiceField(choices=dev, required=False, label=u'Устройства')
    os = forms.ChoiceField(choices=ch_os, required=False, label=u'ОС')

