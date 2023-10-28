from django import forms


class RejectAndApprovalNotificationForm(forms.Form):
    id = forms.IntegerField(label="id", widget=forms.HiddenInput)
    media_id = forms.IntegerField(widget=forms.HiddenInput)
