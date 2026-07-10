"""
千川AI投放工具 - 随心推AI策略引擎
自动监控和优化随心推订单投放
"""
import asyncio
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import logging

from app.services.suixintui_client import sxt_client
from app.models.schemas import AITask, AITaskStatus, AITaskAction

logger = logging.getLogger(__name__)


@dataclass
class SxtOrderPerformance:
    """随心推订单表现数据"""
    order_id: int
    cost: float = 0.0
    show: int = 0
    click: int = 0
    play_count: int = 0
    like_count: int = 0
    pay_order_count: int = 0
    pay_order_amount: float = 0.0
    
    @property
    def roi(self) -> float:
        return self.pay_order_amount / self.cost if self.cost > 0 else 0.0
    
    @property
    def ctr(self) -> float:
        return self.click / self.show if self.show > 0 else 0.0
    
    @property
    def cvr(self) -> float:
        return self.pay_order_count / self.click if self.click > 0 else 0.0


class SxtAIStrategyEngine:
    """随心推AI策略引擎 - 自动优化随心推投放"""
    
    def __init__(self):
        self.tasks: Dict[str, AITask] = {}
        self._running = False
        self._task_loop = None
    
    def create_task(self, strategy_config: Dict, order_ids: Optional[List[int]] = None) -> AITask:
        task_id = str(uuid.uuid4())[:8]
        task = AITask(
            task_id=task_id,
            strategy_config=strategy_config,
            managed_ad_ids=order_ids or [],
            status=AITaskStatus.RUNNING
        )
        self.tasks[task_id] = task
        logger.info(f"创建随心推AI任务: {task_id}")
        return task
    
    def pause_task(self, task_id: str) -> bool:
        if task_id in self.tasks:
            self.tasks[task_id].status = AITaskStatus.PAUSED
            logger.info(f"暂停随心推AI任务: {task_id}")
            return True
        return False
    
    def resume_task(self, task_id: str) -> bool:
        if task_id in self.tasks:
            self.tasks[task_id].status = AITaskStatus.RUNNING
            logger.info(f"恢复随心推AI任务: {task_id}")
            return True
        return False
    
    def stop_task(self, task_id: str) -> bool:
        if task_id in self.tasks:
            self.tasks[task_id].status = AITaskStatus.STOPPED
            logger.info(f"停止随心推AI任务: {task_id}")
            return True
        return False
    
    def get_task(self, task_id: str) -> Optional[AITask]:
        return self.tasks.get(task_id)
    
    def list_tasks(self) -> List[AITask]:
        return list(self.tasks.values())
    
    async def run_task_cycle(self, task_id: str):
        task = self.tasks.get(task_id)
        if not task or task.status != AITaskStatus.RUNNING:
            return
        try:
            config = task.strategy_config
            advertiser_id = config.get("advertiser_id")
            performances = await self._fetch_sxt_performances(advertiser_id, task.managed_ad_ids)
            actions = await self._execute_sxt_rules(task, performances)
            for action in actions:
                await self._apply_sxt_action(advertiser_id, action)
                task.total_actions += 1
            task.last_run_time = datetime.now()
            logger.info(f"随心推任务 {task_id} 执行完成, 操作: {len(actions)}")
        except Exception as e:
            logger.error(f"随心推任务 {task_id} 执行失败: {str(e)}")
            task.status = AITaskStatus.ERROR
    
    async def _fetch_sxt_performances(self, advertiser_id: int, order_ids: List[int]) -> List[SxtOrderPerformance]:
        performances = []
        if not order_ids:
            return performances
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            report_data = await sxt_client.get_suixintui_order_data(
                advertiser_id=advertiser_id,
                order_ids=order_ids,
                start_date=today,
                end_date=today
            )
            for item in report_data.get("list", []):
                perf = SxtOrderPerformance(
                    order_id=item.get("order_id", 0),
                    cost=float(item.get("cost", 0)),
                    show=int(item.get("show", 0)),
                    click=int(item.get("click", 0)),
                    play_count=int(item.get("play_count", 0)),
                    like_count=int(item.get("like_count", 0)),
                    pay_order_count=int(item.get("pay_order_count", 0)),
                    pay_order_amount=float(item.get("pay_order_amount", 0))
                )
                performances.append(perf)
        except Exception as e:
            logger.error(f"获取随心推报表数据失败: {str(e)}")
        return performances
    
    async def _execute_sxt_rules(self, task: AITask, performances: List[SxtOrderPerformance]) -> List[AITaskAction]:
        actions = []
        config = task.strategy_config
        for perf in performances:
            # 规则1: ROI过低自动终止
            if config.get("auto_terminate_enabled", True) and perf.cost >= config.get("auto_terminate_cost_threshold", 50):
                if perf.roi < config.get("auto_terminate_roi_threshold", 1.0) and perf.roi > 0:
                    actions.append(AITaskAction(
                        task_id=task.task_id,
                        action_type="TERMINATE_SXT_ORDER",
                        ad_id=perf.order_id,
                        old_value="DELIVERY_OK",
                        new_value="OVER",
                        reason=f"ROI过低: {perf.roi:.2f}, 消耗: {perf.cost:.2f}"
                    ))
            # 规则2: ROI达标自动追加预算
            if config.get("auto_append_budget_enabled", False):
                if perf.roi >= config.get("auto_append_budget_roi_threshold", 3.0) and perf.cost > 0:
                    actions.append(AITaskAction(
                        task_id=task.task_id,
                        action_type="APPEND_SXT_BUDGET",
                        ad_id=perf.order_id,
                        new_value=config.get("auto_append_budget_amount", 200),
                        reason=f"ROI达标: {perf.roi:.2f}"
                    ))
            # 规则3: 高播放低转化预警
            if perf.play_count > 1000 and perf.pay_order_count == 0 and perf.cost > 100:
                logger.warning(f"随心推订单 {perf.order_id} 高播放低转化")
            # 规则4: 无消耗检测
            if perf.cost == 0 and perf.show > 0:
                logger.info(f"随心推订单 {perf.order_id} 有展示无消耗")
        return actions
    
    async def _apply_sxt_action(self, advertiser_id: int, action: AITaskAction):
        try:
            if action.action_type == "TERMINATE_SXT_ORDER":
                await sxt_client.terminate_suixintui_order(advertiser_id=advertiser_id, order_id=action.ad_id)
                logger.info(f"已终止随心推订单 {action.ad_id}: {action.reason}")
            elif action.action_type == "APPEND_SXT_BUDGET":
                await sxt_client.append_suixintui_budget(advertiser_id=advertiser_id, order_id=action.ad_id, budget=action.new_value)
                logger.info(f"已为随心推订单 {action.ad_id} 追加预算 {action.new_value}")
        except Exception as e:
            logger.error(f"应用随心推操作失败 {action.action_type}: {str(e)}")
    
    async def auto_batch_create_sxt(self, advertiser_id: int, video_ids: List[str], base_config: Dict) -> List[Dict]:
        results = []
        for video_id in video_ids:
            try:
                order_data = {
                    "video_id": video_id,
                    "budget": base_config.get("budget", 300),
                    "optimize_goal": base_config.get("optimize_goal", "PRODUCT_BUY"),
                    "bid_type": base_config.get("bid_type", "AUTO"),
                    "duration": base_config.get("duration", 24),
                    "heating_type": base_config.get("heating_type", "DIRECT")
                }
                if base_config.get("bid"):
                    order_data["bid"] = base_config.get("bid")
                if base_config.get("roi_goal"):
                    order_data["roi_goal"] = base_config.get("roi_goal")
                if base_config.get("product_id"):
                    order_data["product_id"] = base_config.get("product_id")
                result = await sxt_client.create_suixintui_order(advertiser_id, order_data)
                results.append({"video_id": video_id, "order_id": result.get("order_id"), "status": "success"})
                logger.info(f"批量创建成功: video={video_id}, order={result.get('order_id')}")
                await asyncio.sleep(1)
            except Exception as e:
                results.append({"video_id": video_id, "status": "failed", "error": str(e)})
                logger.error(f"批量创建失败: video={video_id}, error={str(e)}")
        return results


# 全局随心推AI引擎实例
sxt_ai_engine = SxtAIStrategyEngine()
