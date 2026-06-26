# 【Quant101】手把手教你搭建本地因子库 ①经验分享

- **链接**: [Commented] 【Quant101】手把手教你搭建本地因子库 ①经验分享.md
- **作者**: ZH87224
- **发布时间/热度**: 3个月前, 得票: 23

## 帖子正文

新的一期 IQC 已经开跑，又会有一批新顾问进场。平台功能多、接口和字段杂，如果完全wqb、machine_lib或一些零散脚本，因子一多就很难检索、去重和做版本管理。

此外，对于顾问来说，有几个都会遇到的痛点：

- 平台使用美东时间，并且有夏令时切换，但我们都在CN，每次检索&设置还得考虑时区问题
- 现在回测很宝贵，每天就5000次，如何在回测时跳过已经回测过的表达式？
- 如果快速计算Self-Corr，并且区分PPA和RA？
- 如何快速知道哪些因子可以Check？
- ….

本地因子库就是来解决这一问题的，老顾问大多早就有了自己的一套流程和工具，我准备写一系列文章，面向刚入门、还没搭过完整系统的的新手，把本地因子库的搭建思路分享给大家，如果有帮到大家，欢迎点赞评论。

## 环境与工具

- **运行时依赖** ： `tortoise-orm>=1.1.6`
- **Notebook / 交互开发** ：建议安装  `ipykernel` ，在 VSCode 里使用 Jupyter Notebook 进行开发。
- **数据库浏览** ：SQLite 文件用 DataGrip 或 VS Code 的 SQLite 插件都能直接看表结构和数据。

## 为什么用 ORM 做本地因子库

写 SQL 太繁琐了，而且容易出错，ORM框架可以将数据库对象转换为Python对象，像代码一样操作数据库。

至于为什么选择 tortoise-orm，是因为本人有尝鲜情节，再加上 sqlalchemy 实在太笨重了。

## 废话不多说，直接上代码

```
from __future__ import annotations

import enum
import hashlib
from datetime import date, datetime
from pathlib import Path
from typing import Any, Self
from zoneinfo import ZoneInfo

from tortoise import Tortoise, fields, signals
from tortoise.models import Model

class AlphaType(enum.StrEnum):
    REGULAR = "REGULAR"
    SUPER = "SUPER"

class Status(enum.StrEnum):
    ACTIVE = "ACTIVE"
    UNSUBMITTED = "UNSUBMITTED"
    DECOMMISSIONED = "DECOMMISSIONED"

class Language(enum.StrEnum):
    FASTEXPR = "FASTEXPR"
    EXPR = "EXPR"
    PYTHON = "PYTHON"

class Instrument(enum.StrEnum):
    CRYPTO = "CRYPTO"
    EQUITY = "EQUITY"

class Region(enum.StrEnum):
    USA = "USA"
    GLB = "GLB"
    EUR = "EUR"
    ASI = "ASI"
    CHN = "CHN"
    IND = "IND"
    HKG = "HKG"

    def universes(self) -> list[Universe]:
        match self:
            case Region.USA:
                return [
                    Universe.TOP3000,
                    Universe.TOP1000,
                    Universe.TOP500,
                    Universe.TOP200,
                    Universe.ILLIQUID_MINVOL1M,
                    Universe.TOPSP500,
                ]
            case Region.GLB:
                return [Universe.TOP3000, Universe.TOPDIV3000, Universe.MINVOL1M]
            case Region.EUR:
                return [
                    Universe.TOP2500,
                    Universe.TOP1200,
                    Universe.ILLIQUID_MINVOL1M,
                    Universe.TOP800,
                    Universe.TOP400,
                    Universe.TOPCS1600,
                ]
            case Region.ASI:
                return [
                    Universe.ILLIQUID_MINVOL1M,
                    Universe.MINVOL1M,
                ]
            case Region.CHN:
                return [Universe.TOP2000U]
            case Region.IND:
                return [Universe.TOP500]
            case Region.HKG:
                return [Universe.TOP800, Universe.TOP500]
            case _:
                raise ValueError(f"Region {self} not supported")

    def neutralizations(self) -> list[Neutralization]:
        basic_neu = [
            Neutralization.NONE,
            Neutralization.MARKET,
            Neutralization.SECTOR,
            Neutralization.INDUSTRY,
            Neutralization.SUBINDUSTRY,
        ]
        stat_neu = [
            Neutralization.REVERSION_AND_MOMENTUM,
            Neutralization.CROWDING,
            Neutralization.FAST,
            Neutralization.SLOW,
            Neutralization.SLOW_AND_FAST,
        ]
        match self:
            case Region.USA:
                return [*basic_neu, *stat_neu, Neutralization.STATISTICAL]
            case Region.GLB | Region.EUR | Region.ASI:
                return [*basic_neu, *stat_neu, Neutralization.STATISTICAL, Neutralization.COUNTRY]
            case Region.CHN | Region.IND:
                return [*basic_neu, *stat_neu]
            case _:
                raise ValueError(f"Region {self} not supported")

class Universe(enum.StrEnum):
    TOP3000 = "TOP3000"
    TOPDIV3000 = "TOPDIV3000"
    TOP2500 = "TOP2500"
    TOP2000U = "TOP2000U"
    TOP1200 = "TOP1200"
    TOP1000 = "TOP1000"
    TOP800 = "TOP800"
    TOP500 = "TOP500"
    TOPSP500 = "TOPSP500"
    TOP400 = "TOP400"
    TOP200 = "TOP200"
    ILLIQUID_MINVOL1M = "ILLIQUID_MINVOL1M"
    MINVOL1M = "MINVOL1M"
    TOPCS1600 = "TOPCS1600"

class Category(enum.StrEnum):
    PRICE_REVERSION = "PRICE_REVERSION"
    PRICE_MOMENTUM = "PRICE_MOMENTUM"
    VOLUME = "VOLUME"
    FUNDAMENTAL = "FUNDAMENTAL"
    ANALYST = "ANALYST"
    PRICE_VOLUME = "PRICE_VOLUME"
    RELATION = "RELATION"
    SENTIMENT = "SENTIMENT"

class Neutralization(enum.StrEnum):
    NONE = "NONE"
    REVERSION_AND_MOMENTUM = "REVERSION_AND_MOMENTUM"
    STATISTICAL = "STATISTICAL"
    CROWDING = "CROWDING"
    FAST = "FAST"
    SLOW = "SLOW"
    MARKET = "MARKET"
    SECTOR = "SECTOR"
    INDUSTRY = "INDUSTRY"
    SUBINDUSTRY = "SUBINDUSTRY"
    SLOW_AND_FAST = "SLOW_AND_FAST"
    COUNTRY = "COUNTRY"

class Switch(enum.StrEnum):
    ON = "ON"
    OFF = "OFF"

class ComponentActivation(enum.StrEnum):
    IS = "IS"
    OS = "OS"

class UnitHandling(enum.StrEnum):
    VERIFY = "VERIFY"

class Color(enum.StrEnum):
    RED = "RED"
    YELLOW = "YELLOW"
    BLUE = "BLUE"
    GREEN = "GREEN"
    PURPLE = "PURPLE"

class Grade(enum.StrEnum):
    AVERAGE = "AVERAGE"
    GOOD = "GOOD"
    EXCELLENT = "EXCELLENT"
    SPECTACULAR = "SPECTACULAR"
    NEEDIMPROVMENT = "NEEDIMPROVMENT"

class Stage(enum.StrEnum):
    IS = "IS"
    OS = "OS"

class SelectionHandling(enum.StrEnum):
    POSITIVE = "POSITIVE"
    NON_ZERO = "NON_ZERO"
    NON_NAN = "NON_NAN"

class ResponseStatus(enum.StrEnum):
    SUCCESS = "SUCCESS"
    LOGIN_FAILED = "LOGIN_FAILED"
    TRY_LATER = "TRY_LATER"
    BAD_REQUEST = "BAD_REQUEST"

class HTTPMethod(enum.StrEnum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    GET_LATER = "GET_LATER"

class FieldType(enum.StrEnum):
    GROUP = "GROUP"
    VECTOR = "VECTOR"
    MATRIX = "MATRIX"
    OTHER = "OTHER"

class OpScope(enum.StrEnum):
    REGULAR = "REGULAR"
    SELECTION = "SELECTION"
    COMBO = "COMBO"

class OpType(enum.StrEnum):
    ARITHMETIC = "ARITHMETIC"
    LOGICAL = "LOGICAL"
    TIMESERIES = "TIMESERIES"
    CROSS_SECTIONAL = "CROSS_SECTIONAL"
    VECTOR = "VECTOR"
    TRANSFORM = "TRANSFORM"
    GROUP = "GROUP"
    SELECTION = "SELECTION"
    COMBO = "COMBO"

class SimulationType(enum.StrEnum):
    REGULAR = "REGULAR"
    SUPER = "SUPER"

class TimeStampMixin:
    """本地时间戳 Mixin"""

    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

class ExternalIDMixin:
    """外部主键 Mixin"""

    id = fields.CharField(max_length=16, primary_key=True)

class AlphaStatusMixin:
    """因子状态 Mixin"""

    status = fields.CharEnumField(Status, description="因子状态")
    stage = fields.CharEnumField(Stage, description="因子阶段")
    date_created = fields.DatetimeField(description="创建日期")
    date_modified = fields.DatetimeField(description="修改日期")
    date_submitted = fields.DatetimeField(description="提交日期", null=True)
    deprecated = fields.BooleanField(description="是否弃用", default=False)

    classifications = fields.JSONField(description="分类", default=list)
    competitions = fields.JSONField(description="比赛", null=True)
    themes = fields.JSONField(description="主题", null=True)
    pyramids = fields.JSONField(description="金字塔", null=True)
    pyramid_themes = fields.JSONField(description="金字塔主题", null=True)
    team = fields.JSONField(description="团队", null=True)

    start_date = fields.DateField(description="开始日期")
    end_date = fields.DateField(description="结束日期")

class AlphaSettingsMixin:
    """回测设置 Mixin"""

    instrument = fields.CharEnumField(Instrument, description="投资工具", default=Instrument.EQUITY)
    language = fields.CharEnumField(Language, description="因子语言", default=Language.FASTEXPR)
    region = fields.CharEnumField(Region, description="投资区域")
    universe = fields.CharEnumField(Universe, description="投资范围")
    delay = fields.IntField(description="Delay", ge=0, le=1)
    decay = fields.IntField(description="Decay", ge=0)
    neutralization = fields.CharEnumField(Neutralization, description="中性化策略")
    truncation = fields.FloatField(description="权重截断", gt=0, le=1)
    pasteurization = fields.CharEnumField(Switch, description="池化", default=Switch.ON)
    unit_handling = fields.CharEnumField(UnitHandling, description="单位验证", default=UnitHandling.VERIFY)
    max_trade = fields.CharEnumField(Switch, description="流动性控制", default=Switch.OFF)
    max_position = fields.CharEnumField(
        Switch, description="最大仓位控制", default=Switch.OFF, db_default=Switch.OFF
    )
    nan_handling = fields.CharEnumField(Switch, description="空值处理", default=Switch.ON)
    visualization = fields.BooleanField(description="高级可视化", default=False)
    test_period = fields.CharField(description="测试期结构", max_length=64, default="P2Y6M", null=True)

class AlphaMarkingMixin:
    """因子标记 Mixin"""

    name = fields.CharField(description="名称", max_length=255, null=True, default=None)
    favorite = fields.BooleanField(description="标星", default=False)
    hidden = fields.BooleanField(description="隐藏", default=False)
    color = fields.CharEnumField(Color, description="颜色", null=True)
    category = fields.CharEnumField(Category, description="类别", null=True)
    tags = fields.JSONField(description="标签", default=list)
    osmosis_points = fields.IntField(description="因子点数", default=None, null=True)

class AlphaPerformanceMixin:
    """因子表现 Mixin"""

    is_pnl = fields.IntField(description="盈亏曲线")
    is_booksize = fields.IntField(description="交易规模")
    is_longcnt = fields.IntField(description="多头数量")
    is_shortcnt = fields.IntField(description="空头数量")
    is_turnover = fields.FloatField(description="成交额")
    is_returns = fields.FloatField(description="收益")
    is_drawdown = fields.FloatField(description="回撤")
    is_margin = fields.FloatField(description="利润")
    is_sharpe = fields.FloatField(description="夏普率")
    is_fitness = fields.FloatField(description="因子评分")
    is_startdate = fields.DateField(description="开始日期")
    is_others = fields.JSONField(description="中性化表现", default=list)
    is_checks = fields.JSONField(description="提交检查器", default=list)

class AlphaRawMixin:
    """因子原始内容 Mixin"""

    record_raw = fields.JSONField(description="因子明细原始数据", null=False, default=None)
    pnl_raw = fields.JSONField(description="盈亏明细", null=True, default=None)
    self_corr_raw = fields.JSONField(description="自相关", null=True, default=None)
    prod_corr_raw = fields.JSONField(description="生产相关性", null=True, default=None)
    combine_perf_raw = fields.JSONField(description="提交前后表现", null=True, default=None)
    yearly_stats_raw = fields.JSONField(description="年度统计", null=True, default=None)

class AlphaComputedMixin:
    """因子计算属性"""

    self_corr = fields.FloatField(description="本地自相关性", null=True, default=None)
    prod_corr = fields.FloatField(description="生产相关性", null=True, default=None)

class HashcodeMixin:
    """自动哈希 Mixin"""

    __hashkey__: list[str] = []
    hashcode = fields.CharField(max_length=512, db_index=True)

    def hashing(self) -> str:
        keys = getattr(self.__class__, "__hashkey__", [])
        parts = [
            str(getattr(self, k, "|")).lower()
            if isinstance(getattr(self, k, "|"), bool)
            else str(getattr(self, k, "|"))
            for k in keys
        ]
        encode = "".join(parts)
        return hashlib.md5(encode.encode("utf-8")).hexdigest()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        async def _pre_save(
            sender: type[Model],
            instance: Model,
            using_db: Any,
            update_fields: list[str],
        ) -> None:
            if not isinstance(instance, cls):
                return
            instance.hashcode = instance.hashing()

        signals.pre_save(cls)(_pre_save)

class ExternalModel(Model, TimeStampMixin, ExternalIDMixin):
    class Meta:
        abstract = True

class LocalModel(Model, TimeStampMixin, HashcodeMixin):
    class Meta:
        abstract = True

    def __str__(self) -> str:
        hashcode = self.hashing()
        return f"{self.__class__.__name__}({getattr(self, 'hashcode') or hashcode})"

class AlphaCore(
    ExternalModel,
    AlphaRawMixin,
    AlphaSettingsMixin,
    AlphaPerformanceMixin,
    AlphaStatusMixin,
    AlphaMarkingMixin,
    AlphaComputedMixin,
):
    class Meta:
        abstract = True

    @classmethod
    def get_kv_from_record(cls, record: dict) -> dict:
        return {
            "id": record["id"],
            "status": Status(record["status"]),
            "stage": Stage(record["stage"]),
            "date_created": datetime.fromisoformat(record["dateCreated"]),
            "date_modified": datetime.fromisoformat(record["dateModified"]),
            "date_submitted": datetime.fromisoformat(record["dateSubmitted"])
            if record["dateSubmitted"]
            else None,
            "instrument": Instrument(record["settings"]["instrumentType"]),
            "language": Language(record["settings"]["language"]),
            "region": Region(record["settings"]["region"]),
            "universe": Universe(record["settings"]["universe"]),
            "delay": record["settings"]["delay"],
            "decay": record["settings"]["decay"],
            "neutralization": Neutralization(record["settings"]["neutralization"]),
            "truncation": record["settings"]["truncation"],
            "pasteurization": Switch(record["settings"]["pasteurization"]),
            "unit_handling": UnitHandling(record["settings"]["unitHandling"]),
            "nan_handling": Switch(record["settings"]["nanHandling"]),
            "max_trade": Switch(record["settings"]["maxTrade"]),
            "visualization": record["settings"]["visualization"],
            "start_date": date.fromisoformat(record["settings"]["startDate"]),
            "end_date": date.fromisoformat(record["settings"]["endDate"]),
            "test_period": record["settings"].get("testPeriod"),
            "name": record["name"],
            "favorite": record["favorite"],
            "hidden": record["hidden"],
            "color": Color(record["color"]) if record["color"] else None,
            "category": Category(record["category"]) if record["category"] else None,
            "tags": record["tags"],
            "classifications": record["classifications"],
            "competitions": record["competitions"],
            "themes": record["themes"],
            "pyramids": record["pyramids"],
            "pyramid_themes": record["pyramidThemes"],
            "team": record["team"],
            "osmosis_points": record["osmosisPoints"],
            "is_pnl": record["is"]["pnl"],
            "is_booksize": record["is"]["bookSize"],
            "is_longcnt": record["is"]["longCount"],
            "is_shortcnt": record["is"]["shortCount"],
            "is_turnover": record["is"]["turnover"],
            "is_returns": record["is"]["returns"],
            "is_drawdown": record["is"]["drawdown"],
            "is_margin": record["is"]["margin"],
            "is_sharpe": record["is"]["sharpe"],
            "is_fitness": record["is"]["fitness"] or 0,
            "is_startdate": date.fromisoformat(record["is"]["startDate"]),
            "is_others": {},
            "is_checks": {
                check_["name"]: {k: v for k, v in check_.items() if k != "name"}
                for check_ in record["is"]["checks"]
            },
            "record_raw": record,
        }

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({getattr(self, 'id')}|{self.is_sharpe})"

    @property
    def checkable(self) -> bool:
        return not bool(list(filter(lambda x: x["result"] == "FAIL", self.is_checks.values())))

class User(ExternalModel):
    username = fields.CharField(max_length=32, description="用户名")
    password = fields.CharField(max_length=32, description="密码")
    permissions = fields.JSONField(default=list, description="帐户权限")
    cookie = fields.CharField(max_length=320, null=True, description="登陆令牌")
    expiry = fields.FloatField(description="令牌时效")

class RegularAlpha(AlphaCore):
    user = fields.ForeignKeyField("niffler.User", related_name="regular_alphas")
    expr = fields.TextField(description="因子表达式")
    description = fields.TextField(description="因子描述", null=True)
    operator_count = fields.IntField(description="操作符数", null=True)

    @classmethod
    def from_record(cls, record: dict) -> Self:
        assert record["type"] == "REGULAR", "因子类型错误"
        kv = cls.get_kv_from_record(record)
        kv = {
            **kv,
            **{
                "user_id": record["author"],
                "expr": record["regular"]["code"],
                "description": record["regular"]["description"],
                "operator_count": record["regular"]["operatorCount"],
            },
        }
        return cls(**kv)

    @classmethod
    def get_keys_from_record(cls, record: dict) -> list[str]:
        return list(cls.get_kv_from_record(record).keys()) + [
            "expr",
            "description",
            "user_id",
            "operator_count",
        ]

    def to_description(self) -> dict:
        return {
            "category": self.category.value if self.category is not None else None,
            "regular": {"description": self.description},
            "color": self.color.value if self.color is not None else None,
            "name": self.name,
            "tags": self.tags,
            "hidden": self.hidden,
            "favorite": self.favorite,
            "osmosisPoints": self.osmosis_points,
        }

    def to_simulation(self) -> dict:
        return {
            "simulation_type": SimulationType.REGULAR,
            "region": self.region,
            "universe": self.universe,
            "delay": self.delay,
            "decay": self.decay,
            "truncation": self.truncation,
            "pasteurization": self.pasteurization,
            "max_trade": self.max_trade,
            "nan_handling": self.nan_handling,
            "visualization": self.visualization,
            "test_period": self.test_period,
            "neutralization": self.neutralization,
            "name": self.name,
            "tags": self.tags,
            "expr": self.expr,
            "description": self.description,
        }

    @property
    def checkable_ra(self) -> bool:
        return not bool(list(filter(lambda x: x["result"] == "FAIL", self.is_checks.values())))

class SuperAlpha(AlphaCore):
    user = fields.ForeignKeyField("niffler.User", related_name="super_alphas")
    combo = fields.TextField(description="因子表达式-组合")
    selection = fields.TextField(description="因子表达式-选择")

    selection_limit = fields.IntField(description="选择限制", ge=10)
    selection_handling = fields.CharEnumField(SelectionHandling, description="选择处理")
    component_activation = fields.CharEnumField(
        ComponentActivation, description="组件激活", default=ComponentActivation.IS
    )

    description_combo = fields.TextField(description="描述-组合", null=True)
    description_selection = fields.TextField(description="描述-选择", null=True)
    operator_count_combo = fields.IntField(description="操作符数-组合", null=True)
    operator_count_selection = fields.IntField(description="操作符数-选择", null=True)

    @classmethod
    def from_record(cls, record: dict) -> Self:
        assert record["type"] == "SUPER", "因子类型错误"
        kv = cls.get_kv_from_record(record)
        kv = {
            **kv,
            **{
                "user_id": record["author"],
                "combo": record["combo"]["code"],
                "selection": record["selection"]["code"],
                "selection_handling": SelectionHandling(record["settings"]["selectionHandling"]),
                "selection_limit": record["settings"]["selectionLimit"],
                "component_activation": ComponentActivation(record["settings"]["componentActivation"]),
                "description_combo": record["combo"]["description"],
                "description_selection": record["selection"]["description"],
                "operator_count_combo": record["combo"]["operatorCount"],
                "operator_count_selection": record["selection"]["operatorCount"],
            },
        }
        return cls(**kv)

    @classmethod
    def get_keys_from_record(cls, record: dict) -> list[str]:
        return list(cls.get_kv_from_record(record).keys()) + [
            "combo",
            "selection",
            "user_id",
            "selection_handling",
            "selection_limit",
            "component_activation",
            "description_combo",
            "description_selection",
            "operator_count_combo",
            "operator_count_selection",
        ]

    def to_description(self) -> dict:
        payload = {
            "name": self.name,
            "color": self.color.value if self.color is not None else None,
            "tags": self.tags,
            "category": self.category.value if self.category is not None else None,
            "regular": {"description": None},
            "favorite": self.favorite,
            "osmosisPoints": self.osmosis_points,
        }
        if self.description_combo is not None:
            payload["combo"] = {"description": self.description_combo}
        if self.description_selection is not None:
            payload["selection"] = {"description": self.description_selection}
        return payload

    def to_simulation(self) -> dict:
        return {
            "simulation_type": SimulationType.SUPER,
            "region": self.region,
            "universe": self.universe,
            "delay": self.delay,
            "decay": self.decay,
            "truncation": self.truncation,
            "pasteurization": self.pasteurization,
            "max_trade": self.max_trade,
            "nan_handling": self.nan_handling,
            "visualization": self.visualization,
            "test_period": self.test_period,
            "neutralization": self.neutralization,
            "name": self.name,
            "tags": self.tags,
            "combo": self.combo,
            "selection": self.selection,
            "description": self.description,
            "selection_limit": self.selection_limit,
            "selection_handling": self.selection_handling,
            "component_activation": self.component_activation,
            "description_combo": self.description_combo,
            "description_selection": self.description_selection,
        }

class AlphaSet(LocalModel):
    __hashkey__ = [
        "user_id",
        "alpha_type",
        "region",
        "universe",
        "delay",
        "date_from",
        "date_to",
        "sharpe_from",
        "sharpe_to",
        "fitness_from",
        "fitness_to",
        "status",
        "tag",
        "name",
        "category",
        "color",
        "hidden",
    ]

    user = fields.ForeignKeyField("niffler.User", related_name="alphasets")
    alpha_ids = fields.JSONField(description="因子集", default=list)
    n_regular = fields.IntField(description="因子集大小(Regular)", default=0)
    n_super = fields.IntField(description="因子集大小(Super)", default=0)

    alpha_type = fields.CharEnumField(AlphaType, description="因子类型", null=True, default=None)
    region = fields.CharEnumField(Region, description="地区", null=True, default=None)
    universe = fields.CharEnumField(Universe, description=" Universe", null=True, default=None)
    delay = fields.IntField(description="延迟", null=True, default=None, ge=0, le=1)
    date_from = fields.DatetimeField(description="开始时间", null=True, default=None)
    date_to = fields.DatetimeField(description="结束时间", null=True, default=None)
    sharpe_from = fields.FloatField(description="最低夏普率", null=True, default=None)
    sharpe_to = fields.FloatField(description="最高夏普率", null=True, default=None)
    fitness_from = fields.FloatField(description="最低稳健性", null=True, default=None)
    fitness_to = fields.FloatField(description="最高稳健性", null=True, default=None)

    status = fields.CharEnumField(Status, description="状态", null=True, default=None)
    tag = fields.CharField(description="检索标签", null=True, default=None, max_length=256)
    name = fields.CharField(description="检索名称", null=True, default=None, max_length=256)
    category = fields.CharEnumField(Category, description="因子类别", null=True, default=None)
    color = fields.CharEnumField(Color, description="因子颜色", null=True, default=None)
    hidden = fields.BooleanField(description="隐藏因子", null=True, default=None)

    def to_params(self) -> dict:
        params: dict[str, Any] = {"order": "-is.fitness"}
        if self.alpha_type is not None:
            params["type"] = self.alpha_type.value
        if self.date_from is not None:
            params["dateCreated>"] = self.date_from.astimezone(ZoneInfo("America/New_York")).isoformat()
        if self.date_to is not None:
            params["dateCreated<"] = self.date_to.astimezone(ZoneInfo("America/New_York")).isoformat()
        if self.status is not None:
            params["status"] = self.status.value
        if self.delay is not None:
            params["delay"] = self.delay

        for setting, setting_s in zip(
            [self.region, self.universe],
            ["region", "universe"],
        ):
            if setting is not None:
                params[f"settings.{setting_s}"] = setting.value

        for is_value, is_value_s in zip(
            [self.sharpe_from, self.sharpe_to, self.fitness_from, self.fitness_to],
            ["sharpe>", "sharpe<", "fitness>", "fitness<"],
        ):
            if is_value is not None:
                params[f"is.{is_value_s}"] = is_value

        for info, info_s in zip([self.tag, self.name], ["tag", "name"]):
            if info is not None:
                params[info_s] = info

        for info, info_s in zip([self.color, self.category], ["color", "category"]):
            if info is not None:
                params[info_s] = info.value

        return params

    @property
    def is_frozen(self) -> bool:
        info = [self.status, self.tag, self.name, self.category, self.color, self.hidden]
        if len([i for i in info if i is not None]) > 0:
            return False
        elif self.date_to is None or self.updated_at is None or self.updated_at < self.date_to:
            return False
        else:
            return True

    def update_from_record(self, record: list) -> Self:
        ra_ids = [rcd["id"] for rcd in record if rcd["type"] == "REGULAR"]
        sa_ids = [rcd["id"] for rcd in record if rcd["type"] == "SUPER"]
        self.alpha_ids = ra_ids + sa_ids
        self.n_regular = len(ra_ids)
        self.n_super = len(sa_ids)
        return self

class Simulation(LocalModel, AlphaSettingsMixin, AlphaMarkingMixin):
    __hashkey__ = [
        "simulation_type",
        "expr",
        "combo",
        "selection",
        "instrument",
        "region",
        "universe",
        "decay",
        "delay",
        "neutralization",
        "truncation",
        "pasteurization",
        "unit_handling",
        "max_trade",
        "max_position",
        "language",
        "nan_handling",
        "visualization",
    ]

    simulation_type = fields.CharEnumField(SimulationType, description="回测类型")
    alpha_id = fields.CharField(default=None, null=True, max_length=64)
    simid = fields.CharField(default=None, null=True, max_length=64)

    expr = fields.TextField(description="因子表达式", null=True, default=None)
    combo = fields.TextField(description="因子表达式-组合", null=True, default=None)
    selection = fields.TextField(description="因子表达式-选择", null=True, default=None)

    selection_limit = fields.IntField(description="选择限制", ge=10, default=10)
    selection_handling = fields.CharEnumField(
        SelectionHandling, description="选择处理", default=SelectionHandling.NON_NAN
    )
    component_activation = fields.CharEnumField(
        ComponentActivation, description="组件激活", default=ComponentActivation.IS
    )

    description = fields.TextField(description="描述", null=True, default=None)
    description_combo = fields.TextField(description="描述-组合", null=True, default=None)
    description_selection = fields.TextField(description="描述-选择", null=True, default=None)

    def to_payload(self) -> dict:
        if self.simulation_type == SimulationType.REGULAR:
            return {
                "type": "REGULAR",
                "settings": {
                    "instrumentType": self.instrument.value,
                    "language": self.language.value,
                    "region": self.region.value,
                    "universe": self.universe.value,
                    "delay": self.delay,
                    "decay": self.decay,
                    "visualization": self.visualization,
                    "neutralization": self.neutralization.value,
                    "truncation": self.truncation,
                    "pasteurization": self.pasteurization.value,
                    "unitHandling": self.unit_handling.value,
                    "nanHandling": self.nan_handling.value,
                    "maxTrade": self.max_trade.value,
                    "maxPosition": self.max_position.value,
                    "testPeriod": self.test_period,
                },
                "regular": self.expr,
            }
        else:
            return {
                "type": "SUPER",
                "settings": {
                    "instrumentType": self.instrument.value,
                    "language": self.language.value,
                    "region": self.region.value,
                    "universe": self.universe.value,
                    "delay": self.delay,
                    "decay": self.decay,
                    "visualization": self.visualization,
                    "neutralization": self.neutralization.value,
                    "truncation": self.truncation,
                    "pasteurization": self.pasteurization.value,
                    "unitHandling": self.unit_handling.value,
                    "nanHandling": self.nan_handling.value,
                    "maxTrade": self.max_trade.value,
                    "maxPosition": self.max_position.value,
                    "selectionLimit": self.selection_limit,
                    "selectionHandling": self.selection_handling.value,
                    "componentActivation": self.component_activation.value,
                    "testPeriod": self.test_period,
                },
                "combo": self.combo,
                "selection": self.selection,
            }

```

接下来是代码解释

## 枚举定义

我们首先定义一组枚举，作用有三点：

1. 平台API交互涉及大量字符串，为了和平台下拉框、API 字符串一一对应，避免魔法字符串散落在业务代码里，我们把这些字符串声明为枚举。
2. `CharEnumField`  直接吃枚举类型，入库仍是字符串，读出来又是枚举，IDE 能补全。
3. 可以给一些枚举绑定方法，例如给 Region 绑定方法，可以获取 Region 对应的所有 Universe 和 Neutralization，写筛选条件时不用翻文档，提交任务时也可以用来校验。

涉及因子与回测的主要枚举包括： `AlphaType` 、 `Status` 、 `Language` 、 `Instrument` 、 `Region` 、 `Universe` 、 `Category` 、 `Neutralization` 、 `Switch` 、 `ComponentActivation` 、 `UnitHandling` 、 `Color` 、 `Grade` 、 `Stage` 、 `SelectionHandling` 、 `SimulationType`  等。

## 模型共享组件

### 时间戳与外部主键

- **`TimeStampMixin`** ： `created_at` （ `auto_now_add` ）、 `updated_at` （ `auto_now` ）自动时间戳
- **`ExternalIDMixin`** ： `id`  为  `CharField(max_length=16, primary_key=True)` ，与平台侧的 alpha id 一致，本地表不再自增整数主键。

### 因子共用字段（Regular / Super 都会用到）

按职责拆成多个 Mixin，全部叠在后面的抽象核心上：

Mixin
职责概要

 `AlphaStatusMixin` 
状态、阶段、各日期、弃用标记、分类/比赛/主题/金字塔等 JSON

 `AlphaSettingsMixin` 
instrument、language、region、universe、delay、decay、neutralization、truncation、pasteurization、unit_handling、max_trade、max_position、nan_handling、visualization、test_period

 `AlphaMarkingMixin` 
name、favorite、hidden、color、category、tags、osmosis_points

 `AlphaPerformanceMixin` 
IS 维度的 pnl、booksize、换手、收益、夏普、fitness、checks 等

 `AlphaRawMixin` 

 `record_raw`  存整包平台 JSON，以及 pnl / 自相关等原始明细 JSON

 `AlphaComputedMixin` 
本地二次计算字段，如  `self_corr` 、 `prod_corr` 

这样 Super 与 Regular 只在自己类里追加差异不分，其余列结构一致，后续修改方便（例如最近新增的 MaxPosition 只需要给 AlphaSettingMixin 新增一个字段，所有的本地因子都自动获得该属性）。

### 基础抽象模型

- **`ExternalModel`** ： `Model`  +  `TimeStampMixin`  +  `ExternalIDMixin` ， `abstract = True` 。所有带平台ID的实体从这里派生，例如  `User` 、RegularAlpha、SuperAlpha。
- **`LocalModel`** ： `Model`  +  `TimeStampMixin`  +  `HashcodeMixin` ， `abstract = True` 。主键不是平台 id、本地保存的对象，例如后面的  `AlphaSet` 、 `Simulation` 。

### HashcodeMixin：本地去重与索引🌟

这个组件帮助大家解决一个核心痛点：回测时如何跳过已经回测过的因子？

这个组件里定义了类属性  `__hashkey__` ：这里面的键会作为模型的唯一参数来计算模型哈希值，而在我们的因子库里，哈希值可以设置成唯一的。

（但我实际上没有设计成唯一的，而是在使用的时候检查哈希值是否存在的方式手动控制重复性）

## 抽象核心：AlphaCore

**`AlphaCore`**  继承  `ExternalModel` ，并混入上述所有 Alpha 相关 Mixin， `Meta.abstract = True` 。它是 Regular / Super 的公共父类，本身不对应单独一张业务表。

值得单独说的几个点：

1. **`get_kv_from_record(record: dict)`**
   类方法，把平台返回的一条 alpha 记录（字典）转换成 Tortoise 构造函数可用的扁平  `kwargs` ：这里你可以直接把平台API接口返回的JSON对象胃进来，通过时间戳自动转换，帮助我们解决了国际时区的痛点
2. **`checkable`  属性**
   扫  `is_checks`  里是否出现  `result == "FAIL"` ，用于快速判断是否满足提交前检查，当is_checks 是 True 时，平台上的 Check 是绿的，帮助我们解决又一个痛点
3. **`__str__`**
   打印类名、平台  `id`  和  `is_sharpe` ，日志里好辨认。

## 具体模型（每张表一类）

### User

继承  `ExternalModel` 。存用户名、密码、权限列表、登录 cookie 与过期时间等账号维度的字段。

### RegularAlpha 与 SuperAlpha

二者都继承  `AlphaCore` ，区别在平台类型与代码字段

### AlphaSet

继承  `LocalModel` ，带完整的  `__hashkey__` （用户、因子类型、地区、universe、delay、时间范围、夏普与 fitness 区间、状态、标签、名称、类别、颜色、是否隐藏等）。

- `alpha_ids` 、 `n_regular` 、 `n_super`  保存结果集统计；
- `to_params()`  把条件转成平台列表接口的 query 参数（含美东时区下的  `dateCreated`  边界）；
- `is_frozen`  判断该快照是否还可视为已冻结；
- `update_from_record`  从原始 record 列表拆出 Regular / Super 的 id。

为什么要设计这么个对象？当我们从平台检索大量因子时（例如我要看近一年所有美区的已模拟因子）非常耗时，但对于某些检索条件，其结果是已冻结的（就是不会改变，例如我要看 3月20～3月21日的Sharpe>1.5的USA因子，由于今天已经过了 3月21，且因子的Sharpe是固定的，所以这个检索条件的结果永远都是固定的，就是已冻结）我们就可以通过本地缓存快速获取，节省大量时间（尤其是每天要挑选交什么因子的时候。

### Simulation

继承  `LocalModel` ，并混入  `AlphaSettingsMixin`  与  `AlphaMarkingMixin。`

该对象增加了 `to_payload()`  ，可以直接输出回测用的 JSON Payload。

## 使用案例

将上面的代码放到  [`brain.py`](http://brain.py)  文件内，然后另开一个 Jupyter：

```
import brain

from tortoise import Tortoise

ctx = await Tortoise.init(
    config={
        "connections": {"default": "sqlite://./db.sqlite"},
        "apps": {
            "niffler": {
                "models": ["brain"],
                "default_connection": "default",
            }
        },
        "use_tz": True,
        "timezone": "Asia/Shanghai",
    },
    _enable_global_fallback=True,
)

_ = await Tortoise.generate_schemas(safe=True)

```

只需要执行以上代码，你就可以生成一个基于 SQLite 的本地因子库。

看到这里你可能会有疑问，现在我有了本地因子库了，如何使用呢？（创建因子、获取因子）接下来你需要

1. 可以去研究一下 Tortoise 语法，学习一下如何操作Models，然后再结合进自己的工作流中
2. 将 Tortoise 语法包装成高级接口

我正在马不停蹄的撰写下一篇文章：BuildYourOwnClient，手把手教大家包装一个高级 Client，这里可以给点预告：

```
class MyClient:
    # ...    

    # 获取 Alpha
    # 如果 Alpha 在本地因子库，则直接拉取，如果Alpha不在，则尝试获取远程
    async def get_alpha(self, alpha_id: str, force: bool = False) -> RegularAlpha | SuperAlpha:
        if not force:
            ra = await RegularAlpha.get_or_none(id=alpha_id)
            sa = await SuperAlpha.get_or_none(id=alpha_id)
            if ra is not None:
                # self._logger.debug(f"读取本地 RA: {ra}")
                return ra
            if sa is not None:
                # self._logger.debug(f"读取本地 SA: {sa}")
                return sa
        rcd = await self.get(url=self._config.platform.alpha_info.format(alpha_id=alpha_id))
        assert isinstance(rcd, dict), "获取因子失败"
        if rcd["type"] == "SUPER":
            alpha = SuperAlpha.from_record(rcd)
            keys = SuperAlpha.get_keys_from_record(rcd)
            alpha_batch = await self.batch_update_or_create(
                [alpha], SuperAlpha, [k for k in keys if k not in ["id"]]
            )
        elif rcd["type"] == "REGULAR":
            alpha = RegularAlpha.from_record(rcd)
            keys = RegularAlpha.get_keys_from_record(rcd)
            alpha_batch = await self.batch_update_or_create(
                [alpha], RegularAlpha, [k for k in keys if k not in ["id"]]
            )
        else:
            raise ValueError(f"alpha type {rcd['type']} not supported")
        alpha_get = alpha_batch[0]
        self._logger.debug(f"在线加载因子: {alpha_get}")
        return alpha_get

```

求赞求赞

---

## 讨论与评论 (10)

### 评论 #1 (作者: YD77867, 时间: 3个月前)

学习学习

---

### 评论 #2 (作者: CZ39633, 时间: 3个月前)

这篇内容对我这个不知道怎么分析和从总体来看alpha的表来说太实用了，大佬是在补“基础设施”这一课。很多人只盯着因子本身，却忽略了数据管理与流程工程，结果一旦数量上来就陷入混乱。其中大佬把时区处理、回测去重、Self-Corr 计算、Check 状态筛选这些真实痛点逐条拆开，再用本地因子库做系统性解决，思路非常专业。

---

### 评论 #3 (作者: SL99784, 时间: 3个月前)

谢谢大佬！期待下一篇！催更啦！

---

### 评论 #4 (作者: YW86963, 时间: 3个月前)

期待大佬的继续更新

－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－

**********************************diversity * quality * stable ************************************

－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－

---

### 评论 #5 (作者: MZ45384, 时间: 3个月前)

大佬的代码能力太强了！！！我当初入坑的时候哪有这条件，我现在用的mongoDB储存alpha信息和pnl，远没有大佬的代码系统这么全面，也没用表达式去重。所以学习了，恭喜大佬。

======================================================================================
知难上，戒骄狂，常自省，穷途明。“寻找可以重复数千次的东西。”——吉姆·西蒙斯（量化投资之王、文艺复兴科技创始人）
# Alpha∞ Engine Status: ONLINE [♦♦♦♦♦♦♦♦♦♦] 100%
# sys.setrecursionlimit(α∞) 
# PnL = ∑(Robustness * Creativity)
#无限探索、鲁棒性优先，创新性增值 
#Where there is a will, there is a way. 路漫漫其修远兮，吾将上下而求索。
======================================================================================

---

### 评论 #6 (作者: LG87838, 时间: 3个月前)

数据库一直是我的弱项，论坛里很多大佬，包括几位老师也多次建议大家围绕数据库建立自己的工作流，还在探索中。感谢分享。

--------------------------------------------------------------------------------------------------------------

慢慢来，相信时间的力量。

--------------------------------------------------------------------------------------------------------------

---

### 评论 #7 (作者: ZZ81910, 时间: 3个月前)

====================================================================================

谢谢大佬分享

================================踏破千重荆棘路，扶摇万里大鹏心==========================

---

### 评论 #8 (作者: YQ51506, 时间: 3个月前)

====================================================================================感谢佬的分享，我是直接基于pg写的因子库，相比于wq的存储多了几个字段，方便我统计计算一些数据，佬的代码也可以直接 复制给ai嵌入的我都系统中，希望佬早日GM
=====================================输入理解输出=====================================

---

### 评论 #9 (作者: WQ37772, 时间: 2个月前)

厉害啊,我还在用tinydb,学习到了,感谢大佬的分享.

--------------------------------------------------------------------------------------------------------------

祝大佬vf永1

--------------------------------------------------------------------------------------------------------------

---

### 评论 #10 (作者: LW67640, 时间: 2个月前)

已经让ai学习了这篇帖子，完成了代码的修改。

感谢分享，数据库是提高产出alpha效率的有效途径，各位新人早点用起来，用熟练，避免像我这样人工低效的耗费时间。

============================================================

长风破浪会有时，直挂云帆济沧海。

============================================================

---

