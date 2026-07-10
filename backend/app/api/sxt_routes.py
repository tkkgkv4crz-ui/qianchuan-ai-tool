"""
千川AI投放工具 - 随心推API路由
小店随心推 + 随心推全域 完整接口
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging

from app.models.schemas import (
    BaseResponse,
    SuixintuiOrderCreateRequest,
    SuixintuiOrderTerminateRequest,
    SuixintuiOrderAppendBudgetRequest,
    SuixintuiOrderDataRequest,
    SuixintuiSuggestBidRequest,
    SuixintuiPredictRequest,
    SuixintuiUniAccountDataRequest,
    SuixintuiUniOrderDataRequest,
    SuixintuiUniOrderCreateRequest,
    SxtAITaskCreateRequest,
    SxtBatchCreateRequest
)
from app.services.suixintui_client import sxt_client
from app.services.sxt_ai_strategy import sxt_ai_engine

logger = logging.getLogger(__name__)

sxt_router = APIRouter(prefix="/suixintui", tags=["随心推"])


# ==================== 随心推订单管理 ====================

@sxt_router.get("/order/list", response_model=BaseResponse)
async def get_suixintui_order_list(
    advertiser_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None
):
    """获取随心推订单列表"""
    try:
        result = await sxt_client.get_suixintui_order_list(
            advertiser_id=advertiser_id,
            page=page,
            page_size=page_size,
            status=status,
            start_time=start_time,
            end_time=end_time
        )
        return BaseResponse(data=result)
    except Exception as e:
        logger.error(f"获取随心推订单列表失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.get("/order/{order_id}", response_model=BaseResponse)
async def get_suixintui_order_detail(advertiser_id: int, order_id: int):
    """获取随心推订单详情"""
    try:
        result = await sxt_client.get_suixintui_order_detail(advertiser_id, order_id)
        return BaseResponse(data=result)
    except Exception as e:
        logger.error(f"获取随心推订单详情失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.post("/order/create", response_model=BaseResponse)
async def create_suixintui_order(request: SuixintuiOrderCreateRequest):
    """创建随心推订单"""
    try:
        order_data = {
            "video_id": request.video_id,
            "budget": request.budget,
            "optimize_goal": request.optimize_goal,
            "bid_type": request.bid_type,
            "duration": request.duration,
            "heating_type": request.heating_type
        }
        if request.bid:
            order_data["bid"] = request.bid
        if request.roi_goal:
            order_data["roi_goal"] = request.roi_goal
        if request.audience:
            order_data["audience"] = request.audience
        if request.product_id:
            order_data["product_id"] = request.product_id
        
        result = await sxt_client.create_suixintui_order(request.advertiser_id, order_data)
        return BaseResponse(data=result)
    except Exception as e:
        logger.error(f"创建随心推订单失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.post("/order/terminate", response_model=BaseResponse)
async def terminate_suixintui_order(request: SuixintuiOrderTerminateRequest):
    """终止随心推订单"""
    try:
        result = await sxt_client.terminate_suixintui_order(
            advertiser_id=request.advertiser_id,
            order_id=request.order_id
        )
        return BaseResponse(data=result)
    except Exception as e:
        logger.error(f"终止随心推订单失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.post("/order/budget/append", response_model=BaseResponse)
async def append_suixintui_budget(request: SuixintuiOrderAppendBudgetRequest):
    """追加随心推订单预算"""
    try:
        result = await sxt_client.append_suixintui_budget(
            advertiser_id=request.advertiser_id,
            order_id=request.order_id,
            budget=request.budget
        )
        return BaseResponse(data=result)
    except Exception as e:
        logger.error(f"追加随心推预算失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# ==================== 随心推报表 ====================

@sxt_router.post("/order/data", response_model=BaseResponse)
async def get_suixintui_order_data(request: SuixintuiOrderDataRequest):
    """获取随心推订单数据（报表）"""
    try:
        result = await sxt_client.get_suixintui_order_data(
            advertiser_id=request.advertiser_id,
            order_ids=request.order_ids,
            start_date=request.start_date,
            end_date=request.end_date
        )
        return BaseResponse(data=result)
    except Exception as e:
        logger.error(f"获取随心推订单数据失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# ==================== 随心推工具接口 ====================

@sxt_router.get("/suggest/bid", response_model=BaseResponse)
async def get_suixintui_suggest_bid(advertiser_id: int, video_id: str):
    """获取随心推短视频建议出价"""
    try:
        result = await sxt_client.get_suixintui_suggest_bid(advertiser_id, video_id)
        return BaseResponse(data=result)
    except Exception as e:
        logger.error(f"获取建议出价失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.get("/suggest/roi", response_model=BaseResponse)
async def get_suixintui_suggest_roi(advertiser_id: int, video_id: str):
    """获取随心推ROI建议出价"""
    try:
        result = await sxt_client.get_suixintui_suggest_roi(advertiser_id, video_id)
        return BaseResponse(data=result)
    except Exception as e:
        logger.error(f"获取ROI建议失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.get("/predict", response_model=BaseResponse)
async def get_suixintui_predict(
    advertiser_id: int,
    video_id: str,
    budget: float,
    optimize_goal: str = "PRODUCT_BUY"
):
    """获取随心推投放效果预估"""
    try:
        result = await sxt_client.get_suixintui_predict(
            advertiser_id=advertiser_id,
            video_id=video_id,
            budget=budget,
            optimize_goal=optimize_goal
        )
        return BaseResponse(data=result)
    except Exception as e:
        logger.error(f"获取效果预估失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.get("/video/available", response_model=BaseResponse)
async def get_suixintui_available_video(
    advertiser_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """获取随心推可投视频列表"""
    try:
        result = await sxt_client.get_suixintui_available_video(
            advertiser_id=advertiser_id,
            page=page,
            page_size=page_size
        )
        return BaseResponse(data=result)
    except Exception as e:
        logger.error(f"获取可投视频失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.get("/interest/tags", response_model=BaseResponse)
async def get_suixintui_interest_tags(advertiser_id: int):
    """获取随心推兴趣标签"""
    try:
        result = await sxt_client.get_suixintui_interest_tags(advertiser_id)
        return BaseResponse(data=result)
    except Exception as e:
        logger.error(f"获取兴趣标签失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.get("/quota", response_model=BaseResponse)
async def get_suixintui_quota(advertiser_id: int):
    """查询随心推使用中订单配额信息"""
    try:
        result = await sxt_client.get_suixintui_quota(advertiser_id)
        return BaseResponse(data=result)
    except Exception as e:
        logger.error(f"获取配额信息失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# ==================== 随心推全域 ====================

@sxt_router.post("/uni/account/data", response_model=BaseResponse)
async def get_suixintui_uni_account_data(request: SuixintuiUniAccountDataRequest):
    """获取随心推全域账户数据"""
    try:
        result = await sxt_client.get_suixintui_uni_account_data(
            advertiser_id=request.advertiser_id,
            start_date=request.start_date,
            end_date=request.end_date
        )
        return BaseResponse(data=result)
    except Exception as e:
        logger.error(f"获取随心推全域账户数据失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.post("/uni/order/data", response_model=BaseResponse)
async def get_suixintui_uni_order_data(request: SuixintuiUniOrderDataRequest):
    """获取随心推全域订单数据"""
    try:
        result = await sxt_client.get_suixintui_uni_order_data(
            advertiser_id=request.advertiser_id,
            order_ids=request.order_ids,
            start_date=request.start_date,
            end_date=request.end_date
        )
        return BaseResponse(data=result)
    except Exception as e:
        logger.error(f"获取随心推全域订单数据失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.get("/uni/order/list", response_model=BaseResponse)
async def get_suixintui_uni_order_list(
    advertiser_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """获取随心推全域订单列表"""
    try:
        result = await sxt_client.get_suixintui_uni_order_list(
            advertiser_id=advertiser_id,
            page=page,
            page_size=page_size
        )
        return BaseResponse(data=result)
    except Exception as e:
        logger.error(f"获取随心推全域订单列表失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.post("/uni/order/create", response_model=BaseResponse)
async def create_suixintui_uni_order(request: SuixintuiUniOrderCreateRequest):
    """创建随心推全域订单"""
    try:
        order_data = {
            "video_id": request.video_id,
            "budget": request.budget,
            "optimize_goal": request.optimize_goal,
            "duration": request.duration
        }
        if request.product_id:
            order_data["product_id"] = request.product_id
        
        result = await sxt_client.create_suixintui_uni_order(request.advertiser_id, order_data)
        return BaseResponse(data=result)
    except Exception as e:
        logger.error(f"创建随心推全域订单失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.post("/uni/order/budget/append", response_model=BaseResponse)
async def append_suixintui_uni_budget(
    advertiser_id: int,
    order_id: int,
    budget: float
):
    """追加随心推全域订单预算"""
    try:
        result = await sxt_client.append_suixintui_uni_budget(
            advertiser_id=advertiser_id,
            order_id=order_id,
            budget=budget
        )
        return BaseResponse(data=result)
    except Exception as e:
        logger.error(f"追加随心推全域预算失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.get("/uni/suggest", response_model=BaseResponse)
async def get_suixintui_uni_suggest(
    advertiser_id: int,
    video_id: str,
    budget: float
):
    """获取随心推全域投放建议"""
    try:
        result = await sxt_client.get_suixintui_uni_suggest(
            advertiser_id=advertiser_id,
            video_id=video_id,
            budget=budget
        )
        return BaseResponse(data=result)
    except Exception as e:
        logger.error(f"获取随心推全域投放建议失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.get("/uni/predict", response_model=BaseResponse)
async def get_suixintui_uni_predict(
    advertiser_id: int,
    video_id: str,
    budget: float
):
    """获取随心推全域投放效果预估"""
    try:
        result = await sxt_client.get_suixintui_uni_predict(
            advertiser_id=advertiser_id,
            video_id=video_id,
            budget=budget
        )
        return BaseResponse(data=result)
    except Exception as e:
        logger.error(f"获取随心推全域效果预估失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.get("/uni/suggest/roi", response_model=BaseResponse)
async def get_suixintui_uni_suggest_roi(
    advertiser_id: int,
    video_id: str,
    budget: float
):
    """获取随心推全域手动出价计划建议ROI"""
    try:
        result = await sxt_client.get_suixintui_uni_suggest_roi(
            advertiser_id=advertiser_id,
            video_id=video_id,
            budget=budget
        )
        return BaseResponse(data=result)
    except Exception as e:
        logger.error(f"获取随心推全域建议ROI失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# ==================== 随心推AI策略路由 ====================

@sxt_router.post("/ai/tasks", response_model=BaseResponse)
async def create_sxt_ai_task(request: SxtAITaskCreateRequest):
    """创建随心推AI策略任务"""
    try:
        config = request.strategy_config.dict()
        task = sxt_ai_engine.create_task(
            strategy_config=config,
            order_ids=request.order_ids
        )
        return BaseResponse(data={
            "task_id": task.task_id,
            "status": task.status.value,
            "strategy_name": config.get("strategy_name", "默认策略"),
            "order_count": len(request.order_ids or [])
        })
    except Exception as e:
        logger.error(f"创建随心推AI任务失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.get("/ai/tasks", response_model=BaseResponse)
async def list_sxt_ai_tasks():
    """获取随心推AI任务列表"""
    try:
        tasks = sxt_ai_engine.list_tasks()
        return BaseResponse(data={
            "tasks": [
                {
                    "task_id": t.task_id,
                    "status": t.status.value,
                    "strategy_name": t.strategy_config.get("strategy_name", "默认策略"),
                    "managed_count": len(t.managed_ad_ids),
                    "total_actions": t.total_actions,
                    "create_time": t.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "last_run_time": t.last_run_time.strftime("%Y-%m-%d %H:%M:%S") if t.last_run_time else None
                }
                for t in tasks
            ]
        })
    except Exception as e:
        logger.error(f"获取随心推AI任务列表失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.get("/ai/tasks/{task_id}", response_model=BaseResponse)
async def get_sxt_ai_task(task_id: str):
    """获取随心推AI任务详情"""
    try:
        task = sxt_ai_engine.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="任务不存在")
        return BaseResponse(data={
            "task_id": task.task_id,
            "status": task.status.value,
            "strategy_config": task.strategy_config,
            "managed_ad_ids": task.managed_ad_ids,
            "total_actions": task.total_actions,
            "create_time": task.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "last_run_time": task.last_run_time.strftime("%Y-%m-%d %H:%M:%S") if task.last_run_time else None
        })
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取随心推AI任务详情失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.post("/ai/tasks/{task_id}/pause", response_model=BaseResponse)
async def pause_sxt_ai_task(task_id: str):
    """暂停随心推AI任务"""
    try:
        result = sxt_ai_engine.pause_task(task_id)
        if not result:
            raise HTTPException(status_code=404, detail="任务不存在")
        return BaseResponse(message="任务已暂停", data={"task_id": task_id, "status": "PAUSED"})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"暂停随心推AI任务失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.post("/ai/tasks/{task_id}/resume", response_model=BaseResponse)
async def resume_sxt_ai_task(task_id: str):
    """恢复随心推AI任务"""
    try:
        result = sxt_ai_engine.resume_task(task_id)
        if not result:
            raise HTTPException(status_code=404, detail="任务不存在")
        return BaseResponse(message="任务已恢复", data={"task_id": task_id, "status": "RUNNING"})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"恢复随心推AI任务失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.post("/ai/tasks/{task_id}/stop", response_model=BaseResponse)
async def stop_sxt_ai_task(task_id: str):
    """停止随心推AI任务"""
    try:
        result = sxt_ai_engine.stop_task(task_id)
        if not result:
            raise HTTPException(status_code=404, detail="任务不存在")
        return BaseResponse(message="任务已停止", data={"task_id": task_id, "status": "STOPPED"})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"停止随心推AI任务失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.post("/ai/tasks/{task_id}/run", response_model=BaseResponse)
async def run_sxt_ai_task(task_id: str):
    """手动执行一次随心推AI任务"""
    try:
        task = sxt_ai_engine.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="任务不存在")
        await sxt_ai_engine.run_task_cycle(task_id)
        return BaseResponse(message="任务执行完成", data={"task_id": task_id, "total_actions": task.total_actions})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"手动执行随心推AI任务失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@sxt_router.post("/ai/batch-create", response_model=BaseResponse)
async def batch_create_sxt_orders(request: SxtBatchCreateRequest):
    """批量创建随心推订单"""
    try:
        base_config = {
            "budget": request.budget,
            "optimize_goal": request.optimize_goal,
            "bid_type": request.bid_type,
            "bid": request.bid,
            "roi_goal": request.roi_goal,
            "duration": request.duration,
            "heating_type": request.heating_type,
            "product_id": request.product_id
        }
        results = await sxt_ai_engine.auto_batch_create_sxt(
            advertiser_id=request.advertiser_id,
            video_ids=request.video_ids,
            base_config=base_config
        )
        success_count = sum(1 for r in results if r.get("status") == "success")
        failed_count = len(results) - success_count
        return BaseResponse(
            message=f"批量创建完成: 成功 {success_count}, 失败 {failed_count}",
            data={"results": results, "success_count": success_count, "failed_count": failed_count}
        )
    except Exception as e:
        logger.error(f"批量创建随心推订单失败: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
