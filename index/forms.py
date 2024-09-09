from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import ContactSubmission

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-4'
        self.helper.label_class = 'block text-sm font-medium text-gray-700'
        self.helper.field_class = 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring focus:ring-green-200 focus:ring-opacity-50'
        self.helper.layout = Layout(
            'name',
            'email',
            'subject',
            'message',
            Submit('submit', 'Send Message', css_class='w-full bg-green-700 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-md transition duration-300')
        )