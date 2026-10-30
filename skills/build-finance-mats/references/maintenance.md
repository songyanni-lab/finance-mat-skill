# 开发者维护接口

仅在开发者明确要求更新技能时执行。当前任务的临时偏好不自动成为永久规则。

## 修改入口

- references/standard.md：制作要求的唯一正文来源，优先在这里改规则。
- SKILL.md：维护触发条件、两条流程及工具能力降级。
- references/house-style.md：维护机构默认字体、模板、格式。
- references/examples.md：添加经认可的正反例方法。
- 仓库 maintenance/feedback-template.md：收集失败现象及期望行为。
- 仓库 tests/cases.json：维护可重复的任务与验收点。
- 仓库 VERSION 和 CHANGELOG.md：版本与变化记录。技能版本与制作规范版本分开。

## 迭代步骤

1. 收集原任务、输入、输出和具体反馈，将问题区分为事实、解释、图示、版式、工具能力或规则歧义。
2. 用最小规则变更解决可复现问题，保留旧版本；避免因一次失败堆积规则。
3. 运行仓库 `python3 scripts/validate.py` 做结构检查。
4. 使用 tests/cases.json 做实际测试，只把技能、prompt和原始输入给执行 Agent；评审者单独看 acceptance，避免泄漏预期答案。
5. 至少覆盖变化相关案例，并回归新建与优化两条路径。脚本通过不代表内容或视觉通过，逐页验收不可省略。
6. 在 CHANGELOG.md 记录理由、变化、验证范围及未测试平台，更新 VERSION，保存 Git 版本。只有开发者授权才上传或发布到远端。

只有安装后的技能目录而没有仓库维护文件时，形成建议或修改已授权文件，不宣称完成版本发布或全量回归。维护流程由开发者发起，不自带定时任务或自动更新。

版本采用 MAJOR.MINOR.PATCH：措辞和链接修复为 PATCH，兼容增强为 MINOR，破坏既有流程的变化为 MAJOR。保留技能名 build-finance-mats，避免更新后触发入口改变。
