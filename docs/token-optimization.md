# AIWriter Token 优化指南

> 给 scheduled task 跑 /aiwriter 的场景。手工调用不受影响（手工调用时 PUA / 改进提示可能有价值）。

## 2026-07：定时任务卡确认 + 第二轮 token 优化

### 为什么定时跑会卡在"确认权限"

三个独立原因，全部已处理：

1. **Workflow 使用警告弹窗**（"Dynamic workflows run many subagents in parallel…"）。
   查证官方文档（code.claude.com/docs/en/workflows.md、settings.md）：`skipWorkflowUsageWarning` **不是文档化的设置键**，不能指望它生效。官方机制有两个：
   - 弹窗里选 **"Yes, and don't ask again for `<workflow 名>` in `<项目>`"** —— 按项目、按工作流记住，三个 aiwriter 工作流各点一次即可（跟账号走，fresh session 也认）。
   - 用 **Routine（Claude Code on the web 的定时任务）** 跑：官方文档明确 "Routines run autonomously as full Claude Code cloud sessions: there is no permission-mode picker and no approval prompts during a run"。**如果每次都被弹窗问，说明任务不是以 Routine 方式跑的**（比如手动开 web session），改成 Routine 是根治办法。
2. **权限 allow 清单有缺口**（已修 `.claude/settings.json`）：
   - 补了 `Write` / `Edit`（配图代理写 HTML、主控逐节追加 article.md 都要用）；
   - 补了 `WebFetch(domain:*)`（WebFetch 的规则语法是域名限定型）；
   - 补了 `Bash(cat *)` / `Bash(cp *)`；
   - 加了 `permissions.defaultMode: "acceptEdits"`（本地 CLI 跑时降低编辑确认；web 会话以 UI 下拉框为准）。
3. **技能本身的三个"等用户批准"节点**（Step 0 / 2.5 / 3）在无人值守 session 里会永远等不到回复。
   已在 aiwriter.md 加"autonomous mode 全局规则"：定时任务触发时三个节点自动推进，自主决策集中记入交付简报。

### 第二轮 token 优化（已落地到三个 workflow 脚本）

| 改动 | 位置 | 省多少 |
|------|------|--------|
| 审稿校验按批：每 5 条建议 1 个护稿人（原来每条 1 个代理、各自重读全文，≤16 次重读 → ≤4 次） | aiwriter-review.js | 最大项，长文省 ~15-25K/次 |
| 废话刀降级 Sonnet（机械性筛弱段，不需要主控模型） | aiwriter-review.js | 主控模型为 Opus 级时明显 |
| 研究搜索上限按 depth 缩放：快速了解 5/3、标准 8/6、深度 10/8（原来一律 8/6） | aiwriter-research.js | 精炼版文章省 ~10-15K/次 |
| 数字核验降级 Haiku + 上限 WebSearch≤2/WebFetch≤1（原 Sonnet、3/2）；快速了解核验条数 8→6 | aiwriter-research.js | ~5-8K/次 |
| 配图 QA 截图 scale 2→1（视觉输入 token 减半；最终高清渲染仍由 Step 7.4 fill_images.py 负责） | aiwriter-illustrations.js | 每图每轮省约一半图像 token |

预算量级（子代理侧）从「研究 60-100K / 审稿 50-80K」降到「研究 40-80K / 审稿 35-60K」，见 aiwriter.md 编排表。

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
