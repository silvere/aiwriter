---
name: wechat-sync
description: "同步文章到微信公众号草稿箱，并支持一键发布。可查看同步状态、触发 CI 同步指定文章、或发布已同步的草稿。触发词：同步到微信、微信同步、发布到公众号、wechat sync、/wechat-sync。"
argument-hint: "[post路径 | 留空=最新文章] [publish=media_id]"
---

# /wechat-sync — 微信公众号同步 & 发布

## 职责

在 `/Users/jingweisun/Code/AIWriter` 仓库里，管理文章从本地到微信公众号草稿箱的同步，以及草稿的正式发布。

---

## 执行流程

### Step 1：解析参数

| 输入 | 处理 |
|------|------|
| 无参数 | 自动找最近 7 天内未同步的文章 |
| `posts/YYYY-MM-DD/slug` | 同步指定文章 |
| `publish=<media_id>` | 跳过同步，直接发布指定草稿 |

### Step 2：确定目标文章

**无参数时**，在 `posts/` 目录下找最近未同步的文章：

```bash
find /Users/jingweisun/Code/AIWriter/posts -name "article.html" | while read html; do
  dir=$(dirname "$html")
  if [ ! -f "$dir/.wechat-sync.json" ]; then
    echo "$dir"
  fi
done | sort -r | head -5
```

列出候选文章，让用户确认同步哪一篇（或全部）。

**有路径参数时**，直接使用该路径。

### Step 3：检查同步状态

读取 `{post_dir}/.wechat-sync.json`（若存在）：

```bash
cat "{post_dir}/.wechat-sync.json"
```

输出状态摘要：
```
📋 《{title}》同步状态
  ✅ 已同步  /  ⏳ 未同步
  media_id: {media_id}（若已同步）
  同步时间: {synced_at}（若已同步）
```

### Step 4：触发同步（未同步时）

触发 GitHub Actions CI 同步：

```bash
gh workflow run "同步到微信公众号草稿箱" \
  --field "post={post_path}" \
  -R silvere/aiwriter
```

然后等待完成（轮询，最多 3 分钟）：

```bash
# 拿最新一次 wechat-sync run ID
RUN_ID=$(gh run list --workflow="同步到微信公众号草稿箱" \
  --limit 1 --json databaseId --jq '.[0].databaseId' \
  -R silvere/aiwriter)

# 等待完成
gh run watch "$RUN_ID" -R silvere/aiwriter
```

完成后拉取最新代码获取 `.wechat-sync.json`：

```bash
git -C /Users/jingweisun/Code/AIWriter pull origin main --quiet
```

读取结果并输出：
```
✅ 同步完成：《{title}》
   media_id: {media_id}
   封面已上传，图片 {N} 张
   
👀 预览：打开 https://mp.weixin.qq.com → 草稿箱 → 点「预览」发到手机
📤 发布命令：/wechat-sync publish={media_id}
```

### Step 5：发布草稿（`publish=<media_id>` 时）

发布前先二次确认：

```
准备将草稿发布给所有粉丝：
  media_id: {media_id}

⚠️  发布后无法撤回，每天限发 1 次。
确认发布？(y/n)
```

用户确认后触发发布 workflow：

```bash
gh workflow run "发布微信公众号文章" \
  --field "media_id={media_id}" \
  -R silvere/aiwriter

# 等待结果
RUN_ID=$(gh run list --workflow="发布微信公众号文章" \
  --limit 1 --json databaseId --jq '.[0].databaseId' \
  -R silvere/aiwriter)
gh run watch "$RUN_ID" -R silvere/aiwriter
```

成功后输出：
```
🎉 已发布！《{title}》正在推送给所有粉丝。
   发布时间: {时间}
```

---

## 典型用法

```
/wechat-sync                              → 查看最近未同步文章，一键同步
/wechat-sync posts/2026-05-25/some-slug   → 同步指定文章
/wechat-sync publish=-Eu-2F7Muk...        → 发布已同步的草稿
```

---

## 注意事项

- CI 同步在自托管 runner 上运行，需 runner 在线（Mac mini 上的 `actions-runner`）
- runner 离线时用 `launchctl start actions.runner.silvere-aiwriter.jingweideMac-mini` 拉起
- `.wechat-sync.json` 是防重复同步标记，删除后 CI 会重新同步（会创建新草稿）
- 发布每天限 1 次，发出后无法撤回
