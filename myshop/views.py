from django.views.generic import TemplateView
from django.contrib.auth.models import User


class PortfolioView(TemplateView):
    template_name = "index.html"

class DashboardView(TemplateView):
    template_name = "dashboard.html"
class MyDashView(TemplateView):
    template_name = "mydash.html"
