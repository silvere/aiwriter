# AIWriter Token 优化指南

> 给 scheduled task 跑 /aiwriter 的场景。手工调用不受影响（手工调用时 PUA / 改进提示可能有价值）。

## 一次任务的 token 消耗分布（基线）

| 来源 | 估算 | 性质 |
|------|------|------|
| aiwriter.md skill 加载 | ~9K | 每次固定（重构后） |
| 按需 Read templates | ~10-15K | 按需 |
| 研究阶段（10 次 WebSearch 结果留存） | ~30K | 已可省 |
| 写作/审稿过程 AI 思考输出 | ~15-20K | 必要 |
| 全文审稿（5000 字文章 × 4 刀回看） | ~15K | 长文已可省 |
| **每 prompt 注入 hooks（self-improvement + PUA）** | ~850 × N | 本文聚焦 |

## 已落地的优化（在 aiwriter.md 里）

1. **Step 2 走 aiwriter-research subagent**（省 25K/次）
2. **aiwriter.md 主文件压缩 + 拆 templates**（按需 Read）
3. **Step 6 长文分节读 + 读者刀走子代理**（深度版省 10-15K）

## 待决策：禁用 hook 注入（改造 4，需要你拍板）

每个 user prompt 都被注入约 850 tokens 的 reminder，一次完整任务约 10-15 prompts = **8-13K tokens 浪费**。

来源：

- **self-improvement-reminder**（~250 tokens/次）
  - 脚本：`~/.claude/scripts/self-improvement-activator.sh`
  - 触发：`~/.claude/settings.json` 的 UserPromptSubmit hook
  - 价值：手工 session 有用（提醒沉淀经验），scheduled task 无用（没人看）

- **PUA reminder**（~600 tokens/次）
  - 脚本：`~/.claude/plugins/cache/pua-skills/pua/3.1.0/hooks/frustration-trigger.sh`
  - 触发：pua-skills plugin 的 frustration detection hook
  - 价值：手工 session 可能有用（高压催促），scheduled task 完全无用（没有"用户挫败"信号）

### 三种禁用方案（按风险从低到高）

**方案 A：永久禁用 PUA frustration trigger**（推荐如果不用 PUA）

```bash
# 备份后清空 trigger 脚本（保留入口，输出空）
cp ~/.claude/plugins/cache/pua-skills/pua/3.1.0/hooks/frustration-trigger.sh \
   ~/.claude/plugins/cache/pua-skills/pua/3.1.0/hooks/frustration-trigger.sh.bak
echo '#!/bin/bash' > ~/.claude/plugins/cache/pua-skills/pua/3.1.0/hooks/frustration-trigger.sh
chmod +x ~/.claude/plugins/cache/pua-skills/pua/3.1.0/hooks/frustration-trigger.sh
```

trade-off：所有 session 都不会再有 PUA 注入（包括手工 session）。如果你不用 PUA，无副作用。

**方案 B：用 marker file 控制（只在 aiwriter 任务时静音）**

修改两个 hook 脚本，在脚本顶部加：

```bash
# 检测 aiwriter 静音 marker（30 分钟内有效）
MARKER="/tmp/aiwriter_quiet"
if [ -f "$MARKER" ]; then
  AGE=$(( $(date +%s) - $(stat -f %m "$MARKER" 2>/dev/null || stat -c %Y "$MARKER") ))
  [ "$AGE" -lt 1800 ] && exit 0
fi
```

然后在 scheduled task 的 SKILL.md 顶部加：
```
任务开始前先运行：touch /tmp/aiwriter_quiet
```

trade-off：需要改两个全局脚本 + scheduled task 配合 touch marker。aiwriter 任务期间静音，手工 session 不受影响。30 分钟自动失效，避免 marker 残留。

**方案 C：完全禁用 self-improvement activator**（最激进）

在 `~/.claude/settings.json` 把 UserPromptSubmit hook 注释或删除。所有 session 都不会再注入 self-improvement reminder。如果你从不看 `.learnings/`，这是最干净的方案。

---

### 我的建议

- 如果你不主动用 PUA 功能 → 走方案 A（一次性，永久）
- 如果你既用 PUA 又跑 scheduled task → 走方案 B（隔离场景）
- 如果你两个 hook 都不需要 → 方案 A + 方案 C 同时做

需要我帮你执行哪个？我可以做 backup 后改脚本。
