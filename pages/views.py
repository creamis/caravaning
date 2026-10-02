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

class CampingView(TemplateView):
    template_name = 'pages/camping.html'


class AlohaCampView(TemplateView):
    template_name = 'pages/alohacamp.html'

    def get_context_data(self, **kwargs):
        from django.conf import settings
        context = super().get_context_data(**kwargs)
        context['alohacamp_affiliate_url'] = settings.ALOHACAMP_AFFILIATE_URL
        return context
