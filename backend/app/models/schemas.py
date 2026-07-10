"""
千川AI投放工具 - 数据模型定义
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime
from enum import Enum


class ResponseCode(int, Enum):
    """响应码"""
    SUCCESS = 0
    PARAM_ERROR = 40001
    AUTH_ERROR = 40002
    API_ERROR = 40003
    SYSTEM_ERROR = 50001


class BaseResponse(BaseModel):
    """基础响应"""
    code: int = Field(default=0, description="业务状态码")
    message: str = Field(default="success", description="状态描述")
    data: Optional[Any] = Field(default=None, description="响应数据")


class AuthCallback(BaseModel):
    """授权回调参数"""
    auth_code: str = Field(..., description="授权码")
    state: Optional[str] = Field(default=None, description="自定义状态")


class TokenInfo(BaseModel):
    """Token信息"""
    access_token: str = Field(..., description="访问令牌")
    refresh_token: str = Field(..., description="刷新令牌")
    expires_in: int = Field(..., description="过期时间(秒)")
    refresh_expires_in: int = Field(..., description="刷新令牌过期时间(秒)")
    advertiser_ids: List[int] = Field(default=[], description="广告主ID列表")
    token_type: str = Field(default="Bearer", description="令牌类型")


class TokenRefreshRequest(BaseModel):
    """Token刷新请求"""
    refresh_token: str = Field(..., description="刷新令牌")


class Advertiser(BaseModel):
    """广告主信息"""
    advertiser_id: int = Field(..., description="广告主ID")
    advertiser_name: str = Field(..., description="广告主名称")
    advertiser_role: Optional[str] = Field(default=None, description="角色")
    is_valid: bool = Field(default=True, description="是否有效")


class AccountBalance(BaseModel):
    """账户余额"""
    advertiser_id: int = Field(..., description="广告主ID")
    balance: float = Field(..., description="账户余额")
    valid_grant_balance: float = Field(default=0.0, description="赠款余额")
    valid_cash_balance: float = Field(default=0.0, description="现金余额")


class CampaignStatus(str, Enum):
    """计划组状态"""
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"
    DELETE = "DELETE"


class CampaignType(str, Enum):
    """计划组类型"""
    DAILY_BUDGET = "DAILY_BUDGET"
    TOTAL_BUDGET = "TOTAL_BUDGET"


class CampaignCreateRequest(BaseModel):
    """创建计划组请求"""
    advertiser_id: int = Field(..., description="广告主ID")
    campaign_name: str = Field(..., min_length=1, max_length=100, description="计划组名称")
    budget_mode: str = Field(default="BUDGET_MODE_DAY", description="预算模式")
    budget: float = Field(default=500.0, ge=300, description="预算金额")
    landing_type: str = Field(default="SHOP", description="推广目的")
    marketing_goal: str = Field(default="VIDEO_AND_IMAGE", description="营销目标")
    marketing_scene: str = Field(default="FEED", description="营销场景")


class CampaignInfo(BaseModel):
    """计划组信息"""
    campaign_id: int = Field(..., description="计划组ID")
    advertiser_id: int = Field(..., description="广告主ID")
    campaign_name: str = Field(..., description="计划组名称")
    budget_mode: str = Field(..., description="预算模式")
    budget: float = Field(..., description="预算")
    status: str = Field(..., description="状态")
    landing_type: str = Field(..., description="推广目的")
    marketing_goal: str = Field(..., description="营销目标")
    create_time: Optional[str] = Field(default=None, description="创建时间")


class CampaignListRequest(BaseModel):
    """计划组列表查询请求"""
    advertiser_id: int = Field(..., description="广告主ID")
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=10, ge=1, le=100, description="每页数量")
    status: Optional[str] = Field(default=None, description="状态筛选")


class AdStatus(str, Enum):
    """广告计划状态"""
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"
    DELETE = "DELETE"
    AUDIT = "AUDIT"
    REJECT = "REJECT"


class OptimizationGoal(str, Enum):
    """优化目标"""
    CLICK = "CLICK"
    CONVERT = "CONVERT"
    PAY_ROI = "PAY_ROI"
    PRODUCT_BUY = "PRODUCT_BUY"
    LIVE_PAY_ROI = "LIVE_PAY_ROI"


class AdCreateRequest(BaseModel):
    """创建广告计划请求"""
    advertiser_id: int = Field(..., description="广告主ID")
    campaign_id: int = Field(..., description="计划组ID")
    ad_name: str = Field(..., min_length=1, max_length=100, description="计划名称")
    delivery_mode: str = Field(default="MANUAL", description="投放模式")
    pricing_type: str = Field(default="PRICING_OCPM", description="计费类型")
    bid: Optional[float] = Field(default=None, description="出价")
    budget: float = Field(default=500.0, ge=300, description="计划预算")
    budget_mode: str = Field(default="BUDGET_MODE_DAY", description="预算模式")
    optimization_goal: str = Field(default="PAY_ROI", description="优化目标")
    deep_external_action: Optional[str] = Field(default=None, description="深度转化目标")
    deep_bid_type: Optional[str] = Field(default=None, description="深度出价方式")
    roi_goal: Optional[float] = Field(default=None, description="ROI目标")
    audience: Optional[Dict[str, Any]] = Field(default=None, description="定向包设置")
    creative_material_mode: str = Field(default="CUSTOM", description="创意生成方式")
    aweme_id: Optional[str] = Field(default=None, description="抖音号ID")
    product_id: Optional[int] = Field(default=None, description="商品ID")
    external_url: Optional[str] = Field(default=None, description="落地页链接")


class AdInfo(BaseModel):
    """广告计划信息"""
    ad_id: int = Field(..., description="计划ID")
    advertiser_id: int = Field(..., description="广告主ID")
    campaign_id: int = Field(..., description="计划组ID")
    ad_name: str = Field(..., description="计划名称")
    status: str = Field(..., description="状态")
    delivery_mode: str = Field(..., description="投放模式")
    pricing_type: str = Field(..., description="计费类型")
    bid: Optional[float] = Field(default=None, description="出价")
    budget: float = Field(..., description="预算")
    optimization_goal: str = Field(..., description="优化目标")
    roi_goal: Optional[float] = Field(default=None, description="ROI目标")
    create_time: Optional[str] = Field(default=None, description="创建时间")
    modify_time: Optional[str] = Field(default=None, description="修改时间")
    delivery_stat: Optional[str] = Field(default=None, description="投放状态")


class AdListRequest(BaseModel):
    """广告计划列表查询"""
    advertiser_id: int = Field(..., description="广告主ID")
    campaign_ids: Optional[List[int]] = Field(default=None, description="计划组ID列表")
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=10, ge=1, le=100, description="每页数量")
    status: Optional[str] = Field(default=None, description="状态筛选")


class AdStatusUpdateRequest(BaseModel):
    """更新广告计划状态"""
    advertiser_id: int = Field(..., description="广告主ID")
    ad_ids: List[int] = Field(..., min_length=1, max_length=10, description="计划ID列表")
    opt_status: str = Field(..., description="操作: ENABLE-启用, DISABLE-暂停, DELETE-删除")


class AdBudgetUpdateRequest(BaseModel):
    """更新广告计划预算"""
    advertiser_id: int = Field(..., description="广告主ID")
    ad_ids: List[int] = Field(..., min_length=1, max_length=10, description="计划ID列表")
    budget: float = Field(..., ge=300, description="新预算")


class AdBidUpdateRequest(BaseModel):
    """更新广告计划出价"""
    advertiser_id: int = Field(..., description="广告主ID")
    ad_ids: List[int] = Field(..., min_length=1, max_length=10, description="计划ID列表")
    bid: float = Field(..., ge=0.1, description="新出价")


class CreativeInfo(BaseModel):
    """创意信息"""
    creative_id: int = Field(..., description="创意ID")
    ad_id: int = Field(..., description="计划ID")
    creative_name: str = Field(..., description="创意名称")
    status: str = Field(..., description="状态")
    video_id: Optional[str] = Field(default=None, description="视频ID")
    image_ids: Optional[List[str]] = Field(default=None, description="图片ID列表")
    title: Optional[str] = Field(default=None, description="标题")


class ReportRequest(BaseModel):
    """报表查询请求"""
    advertiser_id: int = Field(..., description="广告主ID")
    start_date: str = Field(..., description="开始日期 YYYY-MM-DD")
    end_date: str = Field(..., description="结束日期 YYYY-MM-DD")
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=10, ge=1, le=1000, description="每页数量")
    group_by: Optional[List[str]] = Field(default=None, description="分组维度")
    filtering: Optional[Dict[str, Any]] = Field(default=None, description="筛选条件")


class AdReportData(BaseModel):
    """广告计划报表数据"""
    ad_id: Optional[int] = Field(default=None, description="计划ID")
    ad_name: Optional[str] = Field(default=None, description="计划名称")
    campaign_id: Optional[int] = Field(default=None, description="计划组ID")
    campaign_name: Optional[str] = Field(default=None, description="计划组名称")
    stat_datetime: Optional[str] = Field(default=None, description="统计时间")
    show: int = Field(default=0, description="展示数")
    click: int = Field(default=0, description="点击数")
    ctr: float = Field(default=0.0, description="点击率")
    cost: float = Field(default=0.0, description="消耗")
    convert: int = Field(default=0, description="转化数")
    conversion_rate: float = Field(default=0.0, description="转化率")
    convert_cost: float = Field(default=0.0, description="转化成本")
    pay_order_count: int = Field(default=0, description="成交订单数")
    pay_order_amount: float = Field(default=0.0, description="成交金额")
    pay_roi: float = Field(default=0.0, description="支付ROI")
    live_watch_cnt: int = Field(default=0, description="直播间观看数")
    live_pay_order_count: int = Field(default=0, description="直播间成交订单数")


class AIStrategyConfig(BaseModel):
    """AI策略配置"""
    strategy_name: str = Field(..., description="策略名称")
    advertiser_id: int = Field(..., description="广告主ID")
    daily_budget: float = Field(default=500.0, ge=300, description="日预算")
    max_budget_per_ad: float = Field(default=1000.0, ge=300, description="单计划最大预算")
    bid_strategy: str = Field(default="ROI", description="出价策略: ROI/COST")
    target_roi: float = Field(default=2.0, ge=0.5, le=10.0, description="目标ROI")
    max_bid: float = Field(default=50.0, description="最高出价")
    min_bid: float = Field(default=5.0, description="最低出价")
    delivery_schedule: Optional[Dict[str, Any]] = Field(default=None, description="投放时段设置")
    optimization_goal: str = Field(default="PAY_ROI", description="优化目标")
    auto_pause_enabled: bool = Field(default=True, description="是否启用自动暂停")
    auto_pause_roi_threshold: float = Field(default=1.0, description="自动暂停ROI阈值")
    auto_pause_cost_threshold: float = Field(default=100.0, description="自动暂停消耗阈值")
    auto_increase_budget_enabled: bool = Field(default=False, description="是否启用自动加预算")
    auto_increase_budget_roi_threshold: float = Field(default=3.0, description="自动加预算ROI阈值")
    auto_increase_budget_amount: float = Field(default=200.0, description="自动加预算金额")


class AITaskStatus(str, Enum):
    """AI任务状态"""
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"
    ERROR = "ERROR"


class AITask(BaseModel):
    """AI投放任务"""
    task_id: str = Field(..., description="任务ID")
    strategy_config: Dict[str, Any] = Field(..., description="策略配置")
    status: AITaskStatus = Field(default=AITaskStatus.RUNNING, description="任务状态")
    managed_ad_ids: List[int] = Field(default=[], description="管理的计划ID列表")
    create_time: datetime = Field(default_factory=datetime.now, description="创建时间")
    last_run_time: Optional[datetime] = Field(default=None, description="最后执行时间")
    total_actions: int = Field(default=0, description="总操作次数")


class AITaskCreateRequest(BaseModel):
    """创建AI任务请求"""
    strategy_config: AIStrategyConfig = Field(..., description="策略配置")
    ad_ids: Optional[List[int]] = Field(default=None, description="指定管理的计划ID列表")


class AITaskAction(BaseModel):
    """AI任务执行记录"""
    task_id: str = Field(..., description="任务ID")
    action_type: str = Field(..., description="操作类型")
    ad_id: int = Field(..., description="计划ID")
    old_value: Optional[Any] = Field(default=None, description="旧值")
    new_value: Optional[Any] = Field(default=None, description="新值")
    reason: str = Field(..., description="操作原因")
    timestamp: datetime = Field(default_factory=datetime.now, description="操作时间")


class UniPromotionType(str, Enum):
    """全域推广类型"""
    PRODUCT = "PRODUCT"
    LIVE = "LIVE"
    AWEME_PRODUCT = "AWEME_PRODUCT"
    AWEME_LIVE = "AWEME_LIVE"


class UniPromotionAdCreateRequest(BaseModel):
    """创建全域推广计划请求"""
    advertiser_id: int = Field(..., description="广告主ID")
    ad_name: str = Field(..., min_length=1, max_length=100, description="计划名称")
    aweme_id: str = Field(..., description="抖音号ID")
    marketing_goal: str = Field(default="VIDEO_AND_IMAGE", description="营销目标")
    marketing_scene: str = Field(default="FEED", description="营销场景")
    budget: float = Field(default=500.0, ge=300, description="计划预算")
    budget_mode: str = Field(default="BUDGET_MODE_DAY", description="预算模式")
    product_ids: Optional[List[int]] = Field(default=None, description="商品ID列表")
    video_materials: Optional[List[Dict[str, Any]]] = Field(default=None, description="视频素材列表")
    block_materials: Optional[List[str]] = Field(default=None, description="排除素材ID列表")
    roi_goal: Optional[float] = Field(default=None, description="ROI目标")
    schedule_time: Optional[str] = Field(default=None, description="投放时段")
    audience: Optional[Dict[str, Any]] = Field(default=None, description="定向设置")
    creative_material_mode: str = Field(default="CUSTOM", description="创意生成方式")
    external_url: Optional[str] = Field(default=None, description="落地页链接")
    room_id: Optional[str] = Field(default=None, description="直播间ID")
    live_schedule_type: Optional[str] = Field(default=None, description="直播投放时间类型")


class UniPromotionAdUpdateRequest(BaseModel):
    """编辑全域推广计划请求"""
    advertiser_id: int = Field(..., description="广告主ID")
    ad_id: int = Field(..., description="计划ID")
    ad_name: Optional[str] = Field(default=None, description="计划名称")
    budget: Optional[float] = Field(default=None, description="预算")
    product_ids: Optional[List[int]] = Field(default=None, description="商品ID列表")
    video_materials: Optional[List[Dict[str, Any]]] = Field(default=None, description="视频素材列表")
    block_materials: Optional[List[str]] = Field(default=None, description="排除素材ID列表")
    roi_goal: Optional[float] = Field(default=None, description="ROI目标")
    schedule_time: Optional[str] = Field(default=None, description="投放时段")
    audience: Optional[Dict[str, Any]] = Field(default=None, description="定向设置")


class UniPromotionAdStatusUpdateRequest(BaseModel):
    """更新全域计划状态"""
    advertiser_id: int = Field(..., description="广告主ID")
    ad_ids: List[int] = Field(..., min_length=1, max_length=10, description="计划ID列表")
    opt_status: str = Field(..., description="操作: ENABLE-启用, DISABLE-暂停, DELETE-删除")


class UniPromotionAdBudgetUpdateRequest(BaseModel):
    """更新全域计划预算"""
    advertiser_id: int = Field(..., description="广告主ID")
    ad_ids: List[int] = Field(..., min_length=1, max_length=10, description="计划ID列表")
    budget: float = Field(..., ge=300, description="新预算")


class UniPromotionAdNameUpdateRequest(BaseModel):
    """更新全域计划名称"""
    advertiser_id: int = Field(..., description="广告主ID")
    ad_id: int = Field(..., description="计划ID")
    name: str = Field(..., min_length=1, max_length=100, description="新名称")


class UniPromotionMaterialAddRequest(BaseModel):
    """添加全域计划素材"""
    advertiser_id: int = Field(..., description="广告主ID")
    ad_id: int = Field(..., description="计划ID")
    materials: List[Dict[str, Any]] = Field(..., description="素材列表")


class UniPromotionMaterialDeleteRequest(BaseModel):
    """删除全域计划素材"""
    advertiser_id: int = Field(..., description="广告主ID")
    ad_id: int = Field(..., description="计划ID")
    material_ids: List[int] = Field(..., description="素材ID列表")


class UniPromotionProductDeleteRequest(BaseModel):
    """删除全域计划商品"""
    advertiser_id: int = Field(..., description="广告主ID")
    ad_id: int = Field(..., description="计划ID")
    product_ids: List[int] = Field(..., min_length=1, max_length=10, description="商品ID列表")


class ControlTaskCreateRequest(BaseModel):
    """创建调控任务"""
    advertiser_id: int = Field(..., description="广告主ID")
    ad_id: int = Field(..., description="计划ID")
    task_name: str = Field(..., description="任务名称")
    control_type: str = Field(..., description="调控类型")
    control_value: float = Field(..., description="调控值")
    start_time: Optional[str] = Field(default=None, description="开始时间")
    end_time: Optional[str] = Field(default=None, description="结束时间")


class ControlTaskStatusUpdateRequest(BaseModel):
    """更新调控任务状态"""
    advertiser_id: int = Field(..., description="广告主ID")
    task_ids: List[int] = Field(..., min_length=1, max_length=10, description="任务ID列表")
    status: str = Field(..., description="新状态")


class UniPromotionReportRequest(BaseModel):
    """全域推广报表请求"""
    advertiser_id: int = Field(..., description="广告主ID")
    start_date: str = Field(..., description="开始日期 YYYY-MM-DD")
    end_date: str = Field(..., description="结束日期 YYYY-MM-DD")
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=10, ge=1, le=1000, description="每页数量")
    group_by: Optional[List[str]] = Field(default=None, description="分组维度")


class UniPromotionAdInfo(BaseModel):
    """全域推广计划信息"""
    ad_id: int = Field(..., description="计划ID")
    advertiser_id: int = Field(..., description="广告主ID")
    ad_name: str = Field(..., description="计划名称")
    status: str = Field(..., description="状态")
    marketing_goal: str = Field(..., description="营销目标")
    marketing_scene: str = Field(..., description="营销场景")
    budget: float = Field(..., description="预算")
    budget_mode: str = Field(..., description="预算模式")
    aweme_id: Optional[str] = Field(default=None, description="抖音号ID")
    roi_goal: Optional[float] = Field(default=None, description="ROI目标")
    product_count: Optional[int] = Field(default=None, description="商品数量")
    material_count: Optional[int] = Field(default=None, description="素材数量")
    create_time: Optional[str] = Field(default=None, description="创建时间")
    modify_time: Optional[str] = Field(default=None, description="修改时间")


class UniPromotionProductInfo(BaseModel):
    """全域推广商品信息"""
    product_id: int = Field(..., description="商品ID")
    product_name: Optional[str] = Field(default=None, description="商品名称")
    product_img: Optional[str] = Field(default=None, description="商品图片")
    price: Optional[float] = Field(default=None, description="商品价格")
    status: Optional[str] = Field(default=None, description="状态")


class UniPromotionMaterialInfo(BaseModel):
    """全域推广素材信息"""
    material_id: int = Field(..., description="素材ID")
    video_id: Optional[str] = Field(default=None, description="视频ID")
    video_url: Optional[str] = Field(default=None, description="视频URL")
    title: Optional[str] = Field(default=None, description="标题")
    status: Optional[str] = Field(default=None, description="状态")
    audit_status: Optional[str] = Field(default=None, description="审核状态")


class UniPromotionAwemeInfo(BaseModel):
    """全域推广抖音号信息"""
    aweme_id: str = Field(..., description="抖音号ID")
    aweme_name: Optional[str] = Field(default=None, description="抖音号名称")
    avatar: Optional[str] = Field(default=None, description="头像")
    follower_count: Optional[int] = Field(default=None, description="粉丝数")
    is_authorized: bool = Field(default=True, description="是否已授权")


class UniPromotionStrategyConfig(BaseModel):
    """全域推广AI策略配置"""
    strategy_name: str = Field(..., description="策略名称")
    advertiser_id: int = Field(..., description="广告主ID")
    promotion_type: str = Field(default="PRODUCT", description="推广类型")
    daily_budget: float = Field(default=1000.0, ge=300, description="日预算")
    max_budget_per_ad: float = Field(default=5000.0, ge=300, description="单计划最大预算")
    target_roi: float = Field(default=2.0, ge=0.5, le=10.0, description="目标ROI")
    auto_product_select: bool = Field(default=False, description="是否自动选择商品")
    product_count: int = Field(default=5, ge=1, le=50, description="自动选择商品数量")
    auto_material_manage: bool = Field(default=True, description="是否自动管理素材")
    max_materials_per_ad: int = Field(default=10, ge=1, le=30, description="单计划最大素材数")
    auto_schedule: bool = Field(default=False, description="是否自动优化投放时段")
    auto_pause_enabled: bool = Field(default=True, description="是否启用自动暂停")
    auto_pause_roi_threshold: float = Field(default=1.0, description="自动暂停ROI阈值")
    auto_pause_cost_threshold: float = Field(default=500.0, description="自动暂停消耗阈值")
    auto_increase_budget_enabled: bool = Field(default=True, description="是否启用自动加预算")
    auto_increase_budget_roi_threshold: float = Field(default=2.5, description="自动加预算ROI阈值")
    auto_increase_budget_amount: float = Field(default=500.0, description="自动加预算金额")
    auto_exclude_material: bool = Field(default=True, description="是否自动排除低效素材")
    material_ctr_threshold: float = Field(default=0.01, description="素材CTR阈值")
    material_cost_threshold: float = Field(default=200.0, description="素材检测消耗阈值")


class SuixintuiOrderStatus(str, Enum):
    """随心推订单状态"""
    AUDIT = "AUDIT"
    BOOK = "BOOK"
    DELIVERY_OK = "DELIVERY_OK"
    FINISHED = "FINISHED"
    FAILED = "FAILED"
    FROZEN = "FROZEN"
    OFFLINE_AUDIT = "OFFLINE_AUDIT"
    OVER = "OVER"
    TIMEOUT = "TIMEOUT"
    UNPAID = "UNPAID"
    UNPAIDCANCEL = "UNPAIDCANCEL"


class SuixintuiOrderCreateRequest(BaseModel):
    """创建随心推订单请求"""
    advertiser_id: int = Field(..., description="广告主ID")
    video_id: str = Field(..., description="视频ID")
    budget: float = Field(..., ge=100, description="预算金额")
    optimize_goal: str = Field(default="PRODUCT_BUY", description="优化目标")
    bid_type: str = Field(default="AUTO", description="出价方式: AUTO-自动, MANUAL-手动")
    bid: Optional[float] = Field(default=None, description="手动出价金额")
    roi_goal: Optional[float] = Field(default=None, description="ROI目标")
    audience: Optional[Dict[str, Any]] = Field(default=None, description="定向设置")
    product_id: Optional[int] = Field(default=None, description="商品ID")
    duration: int = Field(default=24, ge=2, le=48, description="投放时长(小时)")
    heating_type: str = Field(default="DIRECT", description="加热类型: DIRECT-直接加热, INDIRECT-间接加热")


class SuixintuiOrderTerminateRequest(BaseModel):
    """终止随心推订单请求"""
    advertiser_id: int = Field(..., description="广告主ID")
    order_id: int = Field(..., description="订单ID")


class SuixintuiOrderAppendBudgetRequest(BaseModel):
    """追加随心推订单预算请求"""
    advertiser_id: int = Field(..., description="广告主ID")
    order_id: int = Field(..., description="订单ID")
    budget: float = Field(..., ge=100, description="追加预算金额")


class SuixintuiOrderDataRequest(BaseModel):
    """获取随心推订单数据请求"""
    advertiser_id: int = Field(..., description="广告主ID")
    order_ids: List[int] = Field(..., description="订单ID列表")
    start_date: str = Field(..., description="开始日期 YYYY-MM-DD")
    end_date: str = Field(..., description="结束日期 YYYY-MM-DD")


class SuixintuiOrderInfo(BaseModel):
    """随心推订单信息"""
    order_id: int = Field(..., description="订单ID")
    advertiser_id: int = Field(..., description="广告主ID")
    video_id: Optional[str] = Field(default=None, description="视频ID")
    status: str = Field(..., description="订单状态")
    budget: float = Field(..., description="预算")
    cost: float = Field(default=0.0, description="已消耗")
    optimize_goal: str = Field(..., description="优化目标")
    bid_type: str = Field(..., description="出价方式")
    bid: Optional[float] = Field(default=None, description="出价")
    roi_goal: Optional[float] = Field(default=None, description="ROI目标")
    duration: int = Field(default=24, description="投放时长")
    start_time: Optional[str] = Field(default=None, description="开始时间")
    end_time: Optional[str] = Field(default=None, description="结束时间")
    create_time: Optional[str] = Field(default=None, description="创建时间")


class SuixintuiOrderData(BaseModel):
    """随心推订单报表数据"""
    order_id: Optional[int] = Field(default=None, description="订单ID")
    stat_datetime: Optional[str] = Field(default=None, description="统计时间")
    show: int = Field(default=0, description="展示数")
    click: int = Field(default=0, description="点击数")
    ctr: float = Field(default=0.0, description="点击率")
    cost: float = Field(default=0.0, description="消耗")
    convert: int = Field(default=0, description="转化数")
    conversion_rate: float = Field(default=0.0, description="转化率")
    convert_cost: float = Field(default=0.0, description="转化成本")
    pay_order_count: int = Field(default=0, description="成交订单数")
    pay_order_amount: float = Field(default=0.0, description="成交金额")
    pay_roi: float = Field(default=0.0, description="支付ROI")
    play_count: int = Field(default=0, description="播放量")
    like_count: int = Field(default=0, description="点赞数")
    comment_count: int = Field(default=0, description="评论数")
    share_count: int = Field(default=0, description="分享数")
    follow_count: int = Field(default=0, description="新增粉丝数")
    fans_count: int = Field(default=0, description="粉丝数")
    home_visited_count: int = Field(default=0, description="主页访问量")
    shopping_cart_click_count: int = Field(default=0, description="购物车点击数")
    product_click_count: int = Field(default=0, description="商品点击数")


class SuixintuiSuggestBidRequest(BaseModel):
    """获取随心推建议出价请求"""
    advertiser_id: int = Field(..., description="广告主ID")
    video_id: str = Field(..., description="视频ID")


class SuixintuiPredictRequest(BaseModel):
    """获取随心推效果预估请求"""
    advertiser_id: int = Field(..., description="广告主ID")
    video_id: str = Field(..., description="视频ID")
    budget: float = Field(..., description="预算")
    optimize_goal: str = Field(default="PRODUCT_BUY", description="优化目标")


class SuixintuiUniAccountDataRequest(BaseModel):
    """获取随心推全域账户数据请求"""
    advertiser_id: int = Field(..., description="广告主ID")
    start_date: str = Field(..., description="开始日期 YYYY-MM-DD")
    end_date: str = Field(..., description="结束日期 YYYY-MM-DD")


class SuixintuiUniOrderDataRequest(BaseModel):
    """获取随心推全域订单数据请求"""
    advertiser_id: int = Field(..., description="广告主ID")
    order_ids: List[int] = Field(..., description="订单ID列表")
    start_date: str = Field(..., description="开始日期 YYYY-MM-DD")
    end_date: str = Field(..., description="结束日期 YYYY-MM-DD")


class SuixintuiUniOrderCreateRequest(BaseModel):
    """创建随心推全域订单请求"""
    advertiser_id: int = Field(..., description="广告主ID")
    video_id: str = Field(..., description="视频ID")
    budget: float = Field(..., ge=100, description="预算金额")
    optimize_goal: str = Field(default="PRODUCT_BUY", description="优化目标")
    duration: int = Field(default=24, ge=2, le=48, description="投放时长(小时)")
    product_id: Optional[int] = Field(default=None, description="商品ID")


class SxtAIConfig(BaseModel):
    """随心推AI策略配置"""
    strategy_name: str = Field(default="随心推自动策略", description="策略名称")
    advertiser_id: int = Field(..., description="广告主ID")
    auto_terminate_enabled: bool = Field(default=True, description="是否启用自动终止")
    auto_terminate_roi_threshold: float = Field(default=1.0, description="ROI低于此值自动终止")
    auto_terminate_cost_threshold: float = Field(default=50.0, description="消耗达到此值才触发终止")
    auto_append_budget_enabled: bool = Field(default=False, description="是否启用自动追加预算")
    auto_append_budget_roi_threshold: float = Field(default=3.0, description="ROI高于此值追加预算")
    auto_append_budget_amount: float = Field(default=200.0, description="追加预算金额")


class SxtAITaskCreateRequest(BaseModel):
    """创建随心推AI任务请求"""
    strategy_config: SxtAIConfig = Field(..., description="策略配置")
    order_ids: Optional[List[int]] = Field(default=None, description="管理的订单ID列表")


class SxtBatchCreateRequest(BaseModel):
    """批量创建随心推订单请求"""
    advertiser_id: int = Field(..., description="广告主ID")
    video_ids: List[str] = Field(..., description="视频ID列表")
    budget: float = Field(default=300.0, ge=100, description="单个订单预算")
    optimize_goal: str = Field(default="PRODUCT_BUY", description="优化目标")
    bid_type: str = Field(default="AUTO", description="出价方式")
    bid: Optional[float] = Field(default=None, description="手动出价金额")
    roi_goal: Optional[float] = Field(default=None, description="ROI目标")
    duration: int = Field(default=24, ge=2, le=48, description="投放时长(小时)")
    heating_type: str = Field(default="DIRECT", description="加热类型")
    product_id: Optional[int] = Field(default=None, description="商品ID")
