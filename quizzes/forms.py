from django import forms

class QuizSettingsForm(forms.Form):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    QUESTION_CHOICES = [
        (5, '5'),
        (10, '10'),
        (15, '15'),
    ]

    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        widget=forms.RadioSelect
    )

    question_count = forms.ChoiceField(
        choices=QUESTION_CHOICES
    )

    timer_enabled = forms.BooleanField(
        required=False,
        label="Enable Timer"
    )
