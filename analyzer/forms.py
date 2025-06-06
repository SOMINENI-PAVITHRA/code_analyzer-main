from django import forms


class CodeSubmissionForm(forms.Form):
    code = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "w-full h-64 p-4 border rounded-lg font-mono",
                "placeholder": "Paste your code here...",
            }
        )
    )
