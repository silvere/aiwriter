# AIWriter

微信公众号 / 小红书爆款文章生成套件，基于 Claude Code Skills 构建。

从研究到配图，全流程一键完成，文章自动保存到 Obsidian vault。

---

## 功能

| Skill | 用途 |
|-------|------|
| `/aiwriter` | 完整写作流程：研究 → 大纲 → 逐节写作 → AI配图 → 7维度审稿 → 保存到Obsidian |
| `/aiwriter-research` | 独立深度研究，输出结构化报告（可保存为 MD） |
| `/aiwriter-review` | 对已有文章做专业审稿，7维度打分 + 具体修改建议 |

### 配图能力

- **概念图**：调用 OpenAI `gpt-image-1` 自动生成，扁平风格
- **信息图**：生成规格卡（布局/配色/Prompt），用 Canva/飞书/即梦手动制作
- **兜底**：OpenAI 不可用时自动切换 Unsplash API
- **软失败**：两者均不可用时输出 Prompt 占位注释，不中断写作流程

---

## 安装

### 1. 配置环境变量

复制 `.env.example`，填入你的 API Keys：

```bash
cp .env.example .env
```

把 Keys 写入 Claude Code 配置（会话自动注入）：

```json
// ~/.claude/settings.json
{
  "env": {
    "OPENAI_API_KEY": "sk-...",
    "UNSPLASH_ACCESS_KEY": "..."
  }
}
```

> Unsplash 免费注册：https://unsplash.com/developers

### 2. 安装 Skills

```bash
# 复制 Skills 到 Claude Code 命令目录
mkdir -p ~/.claude/commands/aiwriter
cp skills/*.md ~/.claude/commands/
cp skills/scripts/*.py ~/.claude/commands/aiwriter/

# 安装 Python 依赖（仅图片生成需要）
pip3 install openai
```

### 3. 启动

在 Claude Code 中输入：

```
/aiwriter
```

---

## 使用示例

```
/aiwriter
> 主题：Agent 的 Harness 架构
> 平台：微信公众号
> 风格：半佛仙人
> Vault 路径：~/Documents/Obsidian/Silvere/05AI/
```

Claude 会依次完成：研究 → 推荐体裁 → 生成5个标题 → 大纲确认 → 逐节写作 → 配图 → 审稿 → 保存 Markdown。

---

## 项目结构

```
.
├── skills/                  # Claude Code Skills
│   ├── aiwriter.md          # 主写作 skill
│   ├── aiwriter-research.md # 研究 skill
│   ├── aiwriter-review.md   # 审稿 skill
│   └── scripts/
│       ├── generate_image.py  # 图片生成（gpt-image-1 + Unsplash）
│       ├── setup_vault.py     # Obsidian vault 目录初始化
│       ├── slugify.py         # 标题 → 文件名 slug
│       └── download_image.py  # 直链图片下载
├── aiwriter/                # Python CLI（开发中）
├── config.toml.example      # 配置示例
├── pyproject.toml
└── .env.example
```

---

## 依赖

- [Claude Code](https://claude.ai/code)（Skills 运行环境）
- Python 3.9+
- `openai` Python 包（`pip3 install openai`）
- OpenAI API Key（图片生成，`gpt-image-1`）
- Unsplash API Key（可选，图片兜底）
