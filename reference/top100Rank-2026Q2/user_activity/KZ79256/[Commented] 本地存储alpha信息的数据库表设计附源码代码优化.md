# 本地存储alpha信息的数据库表设计，附源码代码优化

- **链接**: [Commented] 本地存储alpha信息的数据库表设计附源码代码优化.md
- **作者**: TQ88961
- **发布时间/热度**: 1年前, 得票: 2

## 帖子正文

为提高效率，我们需要将远端alpha信息拉到本地数据库。由于远端alpha信息是嵌套json文件，存放到本地数据库时，需要展开字段。以下是一种设计，采用sqlalchemy来定义。

```
Base = declarative_base()class AlphaFactor(Base):    __tablename__ = 'alpha_factors'      uid = Column(Integer, Sequence('uid_seq'), primary_key=True, autoincrement=True)    id = Column(String, unique=True)    type = Column(String)      author = Column(String)    settings_instrument_type = Column(String)    settings_region = Column(String)    settings_universe = Column(String)    settings_delay = Column(Integer)    settings_decay = Column(Integer)    settings_neutralization = Column(String)    settings_truncation = Column(Float)    settings_pasteurization = Column(String)    settings_unit_handling = Column(String)    settings_nan_handling = Column(String)    settings_max_trade = Column(String)    settings_language = Column(String)    settings_visualization = Column(Boolean)    regular_code = Column(String)    regular_description = Column(String, nullable=True)    regular_operator_count = Column(Integer)    date_created = Column(DateTime)    date_submitted = Column(DateTime, nullable=True)    date_modified = Column(DateTime)    name = Column(String)    favorite = Column(Boolean)    hidden = Column(Boolean)    color = Column(String, nullable=True)    category = Column(String, nullable=True)    tags = Column(String)    classifications = Column(String)    grade = Column(String, nullable=True)    stage = Column(String)    status = Column(String)    is_pnl = Column(Integer)    is_book_size = Column(Integer)    is_long_count = Column(Integer)    is_short_count = Column(Integer)    is_turnover = Column(Float)    is_returns = Column(Float)    is_drawdown = Column(Float)    is_margin = Column(Float)    is_sharpe = Column(Float)    is_fitness = Column(Float)    is_start_date = Column(String)    is_investability_pnl = Column(Integer)    is_investability_book_size = Column(Integer)    is_investability_long_count = Column(Integer)    is_investability_short_count = Column(Integer)    is_investability_turnover = Column(Float)    is_investability_returns = Column(Float)    is_investability_drawdown = Column(Float)    is_investability_margin = Column(Float)    is_investability_fitness = Column(Float)    is_investability_sharpe = Column(Float)    is_risk_neutralized_pnl = Column(Integer)    is_risk_neutralized_book_size = Column(Integer)    is_risk_neutralized_long_count = Column(Integer)    is_risk_neutralized_short_count = Column(Integer)    is_risk_neutralized_turnover = Column(Float)    is_risk_neutralized_returns = Column(Float)    is_risk_neutralized_drawdown = Column(Float)    is_risk_neutralized_margin = Column(Float)    is_risk_neutralized_fitness = Column(Float)    is_risk_neutralized_sharpe = Column(Float)    check_low_sharpe_result = Column(String)    check_low_sharpe_limit = Column(Float)    check_low_sharpe_value = Column(Float)    check_low_fitness_result = Column(String)    check_low_fitness_limit = Column(Float)    check_low_fitness_value = Column(Float)    check_low_turnover_result = Column(String)    check_low_turnover_limit = Column(Float)    check_low_turnover_value = Column(Float)    check_high_turnover_result = Column(String)    check_high_turnover_limit = Column(Float)    check_high_turnover_value = Column(Float)    check_concentrated_weight_result = Column(String)    check_concentrated_weight_date = Column(String)    check_concentrated_weight_limit = Column(Float)    check_concentrated_weight_value = Column(Float)    check_self_correlation_result = Column(String)    check_data_diversity_result = Column(String)    check_prod_correlation_result = Column(String)    check_regular_submission_result = Column(String)    check_matches_competition_result = Column(String)    check_matches_competition_competitions = Column(String)    check_low_2y_sharpe_result = Column(String)    check_low_2y_sharpe_value = Column(Float)    check_low_2y_sharpe_limit = Column(Float)    check_matches_pyramid_result = Column(String)    check_matches_pyramid_multiplier = Column(Float)    check_matches_pyramid_pyramids = Column(String)    check_matches_themes_result = Column(String)    check_matches_themes_themes = Column(String)    check_power_pool_correlation_result = Column(String)    origin = Column(Text)    def __repr__(self):       return f"<AlphaFactor(uid={self.uid}, id='{self.id}', name='{self.name}', stage='{self.stage}')>"def create_db_table(db_path="sqlite:///alpha_factors.db"):    """创建数据库表"""    if not db_path.startswith("sqlite:///"):        db_path = "sqlite:///" + db_path.replace("\\", "/")        # 创建数据库引擎    engine = create_engine(db_path, echo=False)        # 创建表    Base.metadata.create_all(engine)    print(f"数据库表已创建于 {db_path}")
```

---

## 讨论与评论 (2)

### 评论 #1 (作者: KZ79256, 时间: 1年前)

用mongo的话可以直接存json格式的,不需要预先定义表之类的,比较方便把

=============================================================

---

### 评论 #2 (作者: MS51256, 时间: 1年前)

感谢分享，一直想存进数据库中，一直没思路

---

