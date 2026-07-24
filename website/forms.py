from django import forms
from .models import CareerOpening, Inquiry, JobApplication


class InquiryForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput, label="Leave empty")

    class Meta:
        model = Inquiry
        fields = ("name", "email", "company", "phone", "service", "budget", "message")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Work email", "autocomplete": "email"}),
            "company": forms.TextInput(attrs={"placeholder": "Company / brand", "autocomplete": "organization"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone number", "autocomplete": "tel", "inputmode": "tel"}),
            "service": forms.Select(choices=[
                ("", "Select a service"),
                ("Website development", "Website development"),
                ("Digital marketing", "Digital marketing"),
                ("SEO & content", "SEO & content"),
                ("Social media", "Social media management"),
                ("App development", "App development"),
                ("ERP / CRM", "ERP / CRM & business software"),
                ("Something else", "Something else"),
            ]),
            "budget": forms.Select(choices=[
                ("", "Select your budget"),
                ("INR 0-25K", "INR 0 - 25,000"),
                ("INR 25K-50K", "INR 25,000 - 50,000"),
                ("INR 50K-1L", "INR 50,000 - 1 lakh"),
                ("INR 1L-2.5L", "INR 1 lakh - 2.5 lakh"),
                ("INR 2.5L-5L", "INR 2.5 lakh - 5 lakh"),
                ("INR 5L+", "INR 5 lakh+"),
                ("Discuss", "Not sure - let us discuss"),
            ]),
            "message": forms.Textarea(attrs={"placeholder": "Briefly describe your goals, requirements and preferred timeline", "rows": 5}),
        }

    def clean_website(self):
        value = self.cleaned_data.get("website", "")
        if value:
            raise forms.ValidationError("Unable to submit this request.")
        return value
class JobApplicationForm(forms.ModelForm):
    consent = forms.BooleanField(required=True, label="I agree that The Webfix may use these details to review my application.")

    class Meta:
        model = JobApplication
        fields = ("opening", "name", "email", "phone", "current_location", "experience", "portfolio_url", "linkedin_url", "cover_note", "resume")
        widgets = {
            "opening": forms.Select(),
            "name": forms.TextInput(attrs={"placeholder": "Full name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email address", "autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone number", "autocomplete": "tel", "inputmode": "tel"}),
            "current_location": forms.TextInput(attrs={"placeholder": "City, State"}),
            "experience": forms.TextInput(attrs={"placeholder": "Example: 3 years"}),
            "portfolio_url": forms.URLInput(attrs={"placeholder": "Portfolio or GitHub URL"}),
            "linkedin_url": forms.URLInput(attrs={"placeholder": "LinkedIn profile URL"}),
            "cover_note": forms.Textarea(attrs={"placeholder": "Tell us about relevant work, your role in it, and why this opportunity interests you.", "rows": 6}),
            "resume": forms.ClearableFileInput(attrs={"accept": ".pdf,.doc,.docx"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["opening"].queryset = CareerOpening.objects.filter(is_active=True)
        self.fields["opening"].empty_label = "Select an open role"

    def clean_resume(self):
        resume = self.cleaned_data.get("resume")
        if not resume:
            return resume
        extension = resume.name.rsplit(".", 1)[-1].lower() if "." in resume.name else ""
        if extension not in {"pdf", "doc", "docx"}:
            raise forms.ValidationError("Upload a PDF, DOC or DOCX resume.")
        if resume.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Resume size must be 5 MB or less.")
        return resume