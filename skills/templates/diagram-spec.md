# Diagram 规格卡完整说明

> 当 aiwriter.md 主流程在 Step 5 配图阶段需要插入 diagram 类型时 Read 此文件。

## diagram 占位块格式

在该节正文下方插入占位块，**pre 里放完整规格卡**（格式固定，fill_images.py 会解析）。

**默认渲染路径是 HTML/SVG**（矢量、中文永不乱码、零依赖），云端 CI 与本地均稳定。只有当需要 300dpi PNG 发朋友圈/公众号时，才在规格卡里加 `【渲染】：matplotlib`。

```html
<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：条形图 / 对账图 / 流程图 / 饼图（选一）
【副标题】：一句 ≤ 20 字的语境提示（可选）
【单位】：亿美元 / % / 人 / 万次……全部数值共用一个单位（可选）
【核心判断】：图表的一句话 punchline，会渲染成底部 banner（强烈建议）
【核心内容】：
  - 标签1 [流入]：330
  - 标签2 [流出]：1000
  - 标签3 [参照]：300</pre></details>
</div>
```

## 字段说明

| 字段 | 作用 | 不填时 |
|------|------|-------|
| `【图类型】` | 选 `条形图` / `对账图`（成对对比） / `流程图` / `饼图` | 默认条形图 |
| `【副标题】` | 标题栏第二行小字 | 只显示主标题 |
| `【单位】` | 数值后自动补单位 | 不补 |
| `【核心判断】` | 底部深蓝 punchline 条 | 不显示 |
| `【数据行 [分组]】` | 支持 `流入`（蓝）/`流出`（红）/`参照`（灰）/`正`（绿）/`负`（橙） | 默认蓝 |
| `【渲染】` | `html`（默认）或 `matplotlib` | html |

## 图类型选型指南

- **对账图**：两类数据成对对比（流入 vs 流出 / 收入 vs 支出 / 我方 vs 对方）——最适合"揭穿"类文章
- **条形图**：单列排列，多项并列对比（5 家公司营收 / 3 年数据对比）
- **流程图**：步骤演进，节数 ≥ 3
- **饼图**：占比拆解，项 ≤ 6 个

## 对账图示例（Anthropic 循环收入）

```
【图类型】：对账图
【副标题】：Anthropic 的钱，最终流向谁
【单位】：亿美元
【核心判断】：投资进 480 亿，算力出 1300 亿，Anthropic 净付给三大云厂商 820 亿
【核心内容】：
  - AWS 投资 Anthropic [流入]：330
  - Anthropic 承诺 AWS 算力 [流出]：1000
  - Microsoft 投资 Anthropic [流入]：150
  - Anthropic 承诺 Azure 算力 [流出]：300
```

## concept 类（概念/氛围图）

```html
<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>{节内容英文描述}, flat design, minimalist illustration, tech style, blue and white color palette, no text, no labels, clean white background</pre></details>
</div>
```

fill_images.py 会用 Gemini 2.5 Flash Image 自动生成。

## ⚠️ 关键约束（违反则脚本零匹配）

- **`</div>` 不得省略**——fill_images.py 的正则依赖此结构
- **写【核心判断】不要偷懒**——这条就是图表的灵魂。没它，图就是一坨数字；有它，图就是一个论点
- **量级悬殊时**：如果最大值/最小值 > 10x，渲染器会用 sqrt 压缩让小条也可见
