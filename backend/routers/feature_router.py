from fastapi import APIRouter

from backend.models.request_models import FeatureRequest
from backend.services.feature_planner import plan_feature


router = APIRouter()


@router.post("/plan")
def create_feature_plan(req: FeatureRequest) -> dict:
    return plan_feature(req.request)
