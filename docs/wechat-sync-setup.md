# 微信公众号自动同步 — 配置指南

把 AIWriter 生成的 HTML 自动同步到微信公众号草稿箱。流程：本地或 CI 调用微信 API → 上传图片 → 创建草稿 → 你到后台预览群发。

---

## 整体架构

```
你本地跑 /aiwriter
    ↓ 生成 posts/<日期>/<slug>/article.html
    ↓ Step 7.6 aiwriter wechat-sync（本地立即同步，可选）
    ↓ Step 7.5 git push origin main
    ↓
GitHub Actions：fill-images.yml （GitHub-hosted runner，配图）
    ↓ workflow_run 触发
GitHub Actions：wechat-sync.yml （self-hosted runner，同步）
    ↓
微信公众号草稿箱
    ↓ 你手动预览 → 群发
关注者收到推文
```

防重复：同步成功后写 `posts/<日期>/<slug>/.wechat-sync.json`，CI 看到该文件就跳过。

---

## 一、安全：重置 AppSecret（**先做**）

之前的 AppSecret 已经在对话日志里泄露过，**必须废掉**。

1. 登录 https://mp.weixin.qq.com
2. 设置与开发 → 基本配置
3. AppSecret 旁边点 **重置**
4. 复制新串（只显示一次，立刻保存到密码管理器）

---

## 二、微信公众平台后台配置

在 https://mp.weixin.qq.com → 设置与开发 → 基本配置：

### 2.1 IP 白名单

加入将要调用 API 的机器的出口 IP：

```bash
# 在你的 runner 机器上查 IP
curl ifconfig.me
```

一行一个，最多 50 个。如果本地和 self-hosted runner 是同一台机器，加 1 个就够。

### 2.2 确认账号已认证

draft API 需要已认证账号，你发过几十篇应该没问题。否则会返回 errcode=48001。

---

## 三、GitHub Secrets

浏览器打开 https://github.com/silvere/aiwriter/settings/secrets/actions

点 **New repository secret**，加两条：

| Name | Value |
|---|---|
| `WECHAT_APPID` | `wx2137460f8d941dbf` |
| `WECHAT_APPSECRET` | 第一步重置后的新串 |

---

## 四、本地 .env

`/home/user/aiwriter/.env` 已经创建好了（旧 secret，记得回头改）：

```bash
WECHAT_APPID=wx2137460f8d941dbf
WECHAT_APPSECRET=<重置后的新串>
```

`.env` 已在 `.gitignore`，不会被提交。

---

## 五、装 self-hosted runner

GitHub Actions 默认 runner IP 不固定，没法过微信白名单，所以必须用 self-hosted。

### 5.1 注册 runner

1. 浏览器打开 https://github.com/silvere/aiwriter/settings/actions/runners/new
2. 选你机器的 OS（Linux / macOS / Windows）
3. 把页面给的 6 行命令在机器上跑一遍（大致是 mkdir → 下载 tarball → config.sh --url ... --token ...）

### 5.2 装系统依赖（一次性）

```bash
# macOS
brew install cairo librsvg python@3.11

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y libcairo2-dev libcairo2 librsvg2-bin python3.11 python3.11-venv

# Windows
# pip install cairosvg 就够；librsvg/inkscape 可选
```

> 这些是 SVG → PNG 转换需要的（微信不支持 SVG）。装一个就行，按 cairosvg → rsvg-convert → inkscape 顺序兜底。

### 5.3 注册为系统服务（开机自启）

```bash
# 在 actions-runner 目录里
sudo ./svc.sh install
sudo ./svc.sh start
```

- **Linux**：装为 systemd unit，开机自启
- **macOS**：装为 LaunchDaemon，开机自启
- **Windows**：装为 Windows Service

### 5.4 验证

```bash
# Linux
sudo systemctl status 'actions.runner.*'   # 应看到 active (running)

# macOS
sudo launchctl list | grep actions.runner

# 通用
# 浏览器到 https://github.com/silvere/aiwriter/settings/actions/runners
# 状态应该是绿色 Idle
```

### 5.5 几个会让 runner 失联的坑

| 情况 | 影响 | 处理 |
|---|---|---|
| 网络断了又恢复 | 自动重连 | 不用管 |
| 笔记本合盖 / 睡眠 | 期间无法跑任务 | **不建议用笔记本做 runner** |
| 14 天连续无活动 | GitHub 清掉 | 重新 register |
| service 模式 token | 长期有效 | 不用管 |

### 5.6 维护命令

```bash
cd ~/actions-runner
sudo ./svc.sh status         # 看状态
sudo ./svc.sh stop           # 停
sudo ./svc.sh start          # 起
sudo ./svc.sh uninstall      # 卸服务（程序还在）
./config.sh remove --token <TOKEN>   # 彻底注销 runner
```

---

## 六、安装 AIWriter（含 wechat 可选依赖）

```bash
cd /home/user/aiwriter
pip install -e '.[wechat]'

# 验证
aiwriter check
# 应该看到「微信公众号  已配置」
```

---

## 七、跑通三步验证

按 A → B → C 顺序来，每步过了再做下一步。

### A. CLI 单测：同步一篇旧文章

```bash
cd /home/user/aiwriter
aiwriter wechat-sync posts/2026-05-15/DeepSeek-收钱了-本子是国家递的
```

**预期输出**：

```
→ 同步到微信草稿箱: DeepSeek 收钱了：本子是国家递的
Step 1/3: 上传正文图片
  ✓ concept_01.svg → https://mmbiz.qpic.cn/...
  ✓ concept_02.svg → https://mmbiz.qpic.cn/...
Step 2/3: 上传封面
  ✓ 封面: concept_01.png (media_id=xxx)
Step 3/3: 创建草稿
  ✓ 草稿已创建: media_id=xxx

✓ 同步完成: DeepSeek 收钱了：本子是国家递的
```

**验证**：到 mp.weixin.qq.com 后台 → 草稿箱，应该能看到。检查样式损失是否在可接受范围（`<style>` 块被剥离是正常的）。

> 提示：这一步会在 post 目录写 `.wechat-sync.json`，重跑会被跳过。需要重发就删掉该文件。

### B. 全流程：`/aiwriter` 写一篇小文章

在 Claude Code 里：

```
/aiwriter
> 主题：（随便选一个最近的小话题）
```

走完到 Step 7.6 时应看到 `aiwriter wechat-sync` 自动执行。
**验证**：草稿箱出现新文章。

### C. CI 链路：push 触发自动同步

最稳的方式：等下一篇真文章 push 到 main，观察两个 workflow 是否依序触发：

1. https://github.com/silvere/aiwriter/actions/workflows/fill-images.yml — 配图
2. https://github.com/silvere/aiwriter/actions/workflows/wechat-sync.yml — 同步

第二个跑完后草稿箱应该出现新文章（且 marker 文件应该被 bot commit 回主分支）。

如果想在测试分支上验：临时把 `fill-images.yml` 的 `branches: [main]` 改成 `[main, test/**]`，测完改回去。

---

## 八、跑通后告诉我

A/B/C 都过了之后，告诉我"全过了"，我帮你开 PR 把 `claude/wechat-auto-sync-4Xlbj` 合到 main。

---

## 常见错误

| errcode | 含义 | 解决 |
|---|---|---|
| 40164 | IP 不在白名单 | 第二步加 IP |
| 40001 | AppSecret 错 | 重新复制粘贴，注意末尾空格 |
| 48001 | 接口未授权 | 账号未认证或权限缺失 |
| 53503 | 草稿涉嫌违规 | 标题/正文触发审核，去后台看具体提示 |
| 45009 | 接口调用频次超限 | draft/add 每天 100 次，正文图 100 次 |
| 40007 | media_id 不合法 | 封面图上传失败（检查格式、尺寸） |

## 已知限制（不是 bug）

1. **`<style>` 块会被微信剥离** —— article.html 里的 CSS 变量、`linear-gradient`、`@media` 进了草稿全失效，只有 `<p>`/`<h2>`/`<blockquote>`/`<img>` 这些结构 + inline style 留得下来。想要排版一致需要 CSS 内联（后续可加 premailer）。
2. **SVG 必须转 PNG** —— 微信不支持 SVG。代码按 cairosvg → rsvg-convert → inkscape 顺序兜底。三个都没装会跳过该图并告警。
3. **封面必须有** —— 优先 `posts/<日期>/<slug>/cover.{png,jpg,jpeg,gif}`，没有就用正文第一张光栅图。建议每篇放一张 900×500 cover.jpg。
4. **每天 100 次** —— draft/add 和正文图上传都是 100/天，日更够用。
5. **草稿不自动发布** —— 按你的选择，跑完不推送给关注者，需要你手动到后台群发。

---

## 文件清单（这次修改了什么）

| 文件 | 说明 |
|---|---|
| `aiwriter/wechat.py` | 微信 API 客户端（token / 图片上传 / 草稿创建） |
| `aiwriter/cli.py` | 新增 `aiwriter wechat-sync` 命令 |
| `aiwriter/config.py` | 增加 `[wechat]` 配置块和环境变量读取 |
| `config.toml.example` | 增加 `[wechat]` 示例 |
| `pyproject.toml` | 增加 `wechat` extra（cairosvg） |
| `.github/workflows/wechat-sync.yml` | CI 工作流，串在 fill-images 之后 |
| `skills/aiwriter.md` | `/aiwriter` 流程末尾增加 Step 7.6 |
| `.gitignore` | 忽略 `.stub-vault/` 和根目录 `config.toml` |
| `.env`（本地） | 已写入旧 secret，待你重置后更新 |
