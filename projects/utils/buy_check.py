from django.conf import settings
from ..models.model_project_buy import ModelProjectBuy


def buy_check(request, project):
    if request.user.is_authenticated:

        return ModelProjectBuy.objects.filter(
            project=project, user=request.user
        ).exists()
    else:
        return False
