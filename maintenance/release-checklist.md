# 发布检查

1. 明确本次变化来自哪条反馈，是否应推广为通用规则。
2. standard.md 保持唯一规范正文；其他文件不得复制出相互矛盾的规则。
3. 运行 `python3 scripts/validate.py`，并试导出通用版和 WorkBuddy 版。
4. 使用 tests/cases.json 的相关任务实际运行技能。执行 Agent 只看 prompt 和原始输入，评审者看 acceptance；检查新建及优化两条路径。
5. PPT 任务必须实际打开渲染图验收；仅返回内容方案的测试不得记为 PPT 端到端通过。
6. 在 validation-report.md 记录平台、模型、日期、任务、结果和未覆盖范围，不能把未测试写成通过。
7. 更新 VERSION 和 CHANGELOG.md，保存提交。由开发者决定 GitHub 发布范围与许可；不自动上传客户或品牌素材。
8. 安装端更新完整技能目录，保留机构本地配置；不要只换 SKILL.md 导致引用版本不一致。需要回退时从已验证版本重新导出。
