from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = 'pages/about.html'

class ContactView(TemplateView):
    template_name = 'pages/contact.html'

class LegalView(TemplateView):
    template_name = 'pages/legal.html'

class PrivacyView(TemplateView):
    template_name = 'pages/privacy.html'

class CookiesView(TemplateView):
    template_name = 'pages/cookies.html'

class AffiliatesView(TemplateView):
    template_name = 'pages/affiliates.html'
