# 金融垫板制作与优化 Skill

按《垫板制作规范 V2 修订版》制作金融客户沟通页面：结论清晰、证据支持、呈现简洁、必要图表辅助理解。

支持两种任务：给定主题和使用场景新建垫板；读取已有 PPT/PDF/图片优化指定页面。覆盖市场趋势、基础知识与产品机制、工具比较、政策规则四类。运行规则不绑定某一模型、API或PPT库；实际文件生成与视觉检查取决于宿主能力。

## 目录与使用

可安装单元是 `skills/build-finance-mats/`，其余文件用于开发和发布。完整复制技能目录，不要只复制 SKILL.md。

- Claude Code：放到项目 `.claude/skills/build-finance-mats/` 或个人 `~/.claude/skills/build-finance-mats/`。
- CodeBuddy：放到项目 `.codebuddy/skills/build-finance-mats/`，按当前客户端设置启用。
- WorkBuddy：提供专用导出器，添加开放平台所需展示元数据；用平台的导入/发布入口加载，不将开放平台发布与本地安装混为一谈。
- 其他支持 Agent Skills 的宿主：将完整技能目录放入其支持的技能目录。不同产品的安装路径、触发方式和工具权限可能不同。
- 不支持技能目录的 Agent：显式提供 SKILL.md 及其引用的 references 文件，并要求按内容执行。这是手动上下文使用，不保证自动触发。

`agents/openai.yaml` 仅是 OpenAI 展示元数据，不是运行依赖，其他宿主可忽略。未捆绑任何付费 API、字体或机构 PPT 模板。

## 调用示例

新建：

> 使用 build-finance-mats。主题是复利与翻倍时间，给第一次接触理财的客户讲解，制作一页可编辑 PPT。使用我提供的品牌模板；用标明假设的数字算例帮助理解。

存量优化：

> 使用 build-finance-mats，优化附件资配理念的实际第3页。保留有效走势图及模板配色，补足结论和图中依据，正文基于已有材料，事实错误核查后修正。

维护：

> 根据 maintenance/feedback-template.md 中的反馈更新技能。说明改动理由，运行结构检查及受影响案例，记录新版本；暂不发布。

## 检查与导出

维护脚本仅依赖 Python 3.9+ 标准库；制作垫板本身不要求运行这些脚本。

```bash
python3 scripts/validate.py
python3 scripts/export_skill.py --target standard --output dist/standard
python3 scripts/export_skill.py --target workbuddy --author "你的发布者名称" --output dist/workbuddy
```

输出是完整的 `build-finance-mats` 文件夹。已有目标目录会拒绝覆盖，避免丢失修改。按目标平台导入要求处理该目录；脚本不自动上传或发布。WorkBuddy 导出会从同一核心正文生成额外元数据，不手工维护第二套规则。

将本仓库的内容上传到你选择的 GitHub 仓库即可；不包含客户文件、机构品牌资源、原始PPT或历史产物。尚未选择开源许可证，上传到公开仓库前由开发者决定授权方式。此项目不自动创建公开仓库。

## 开发者维护

1. 修改制作要求：`skills/build-finance-mats/references/standard.md`。
2. 调整机构默认项：`references/house-style.md`。
3. 调整执行流程：`SKILL.md`；补充有效方法：`references/examples.md`。
4. 记录反馈：`maintenance/feedback-template.md`；新增回归任务：`tests/cases.json`。
5. 按 `maintenance/release-checklist.md` 检查，更新 `VERSION` 和 `CHANGELOG.md`，通过 Git 记录变更。

GitHub Actions 只做结构检查，不调用模型、读取金融资料或自动发布。规则、模型和工具升级后均可用固定案例复测；“接口”是明确的文件入口与检查流程，不是自动自我修改的服务。

## 兼容性与验证边界

按开放 Agent Skills 的最小 frontmatter 编写，并核对 Claude Code、CodeBuddy 与 WorkBuddy 的官方说明。格式适配不代表已在各平台端到端运行；具体生成质量受模型、工具和模板影响。参考 `maintenance/validation-report.md` 查看本版实际验证范围。

官方依据（核对日期：2026-10-30）：

- https://agentskills.io/specification
- https://code.claude.com/docs/en/skills
- https://www.codebuddy.ai/docs/ide/Features/Skills
- https://open.workbuddy.cn/docs/skill
