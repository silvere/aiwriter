# 理解图（understanding）配图规范

> aiwriter Step 5 配图阶段，**微信公众号文章默认走这套**。
> 核心来自 illustrate 配图框架：配图不是装饰，是**替读者做理解工作**。
> concept（AI 氛围图）/ diagram（数据规格卡）仍可用，但公众号优先产出「理解图」。

---

## 0. 一句话

通读全文 → 找到读者会卡壳的地方 → 只在「补充理解」处配图。每张图都能通过**删图测试**：
删了它，读者理解会变差吗？不会 → 是装饰，删掉。解释型配图用 **HTML→PNG**
（中文/数字精确、风格统一），只有「抽象概念→艺术类比」「想象一下」才用 AI 生图。

## 1. 五条必守（否则退化成装饰图）

1. **先读懂，再配图**：没建立文章理解模型就配图，出来的一定是装饰。
2. **配图优先级 = 理解难度(1-5) × 内容重要性(1-5)**：难度 ≤2 或重要性 ≤2 的不配。
3. **删图测试**：删掉它读者理解会变差吗？不会就删。
4. **一张图只解一个卡点**：别把一整段塞进一张图。
5. **克制**：精炼版 2-3 张、标准版 3-4 张、深度版 4-5 张「做功的图」，远胜十张「好看的图」。

## 2. 工作流（5 步）

```
通读全文 → 定位难点 → 配图设计（过删图测试）→ 生成占位 → 配图地图
```

- **通读**：抽出主旨 / 论证链 / 关键资产（概念·机制·数据·流程·对比·时间线）+ 读者画像（决定"什么算难"）。
- **定位难点**：按 §3 表扫描，按 `难度×重要性` 打分排序，取 Top N。
- **配图设计**：每张图回答配图三问——读者卡在哪 / 这张图做什么理解工作 / 图注怎么把图钉回正文；过删图测试。
- **生成占位**：解释型 → understanding（HTML→PNG，见 §4）；抽象类比/想象一下 → concept（AI 生图）；纯数据 → diagram（规格卡，见 diagram-spec.md）。
- **配图地图**：完成后在汇报里列出每张图（位置/难点类型/理解工作/图注）+ 说明「哪些地方没配图、为什么」。

## 3. 难点分类 → 配图工作 → 材料

| 难点类型 | 检测信号 | 配图要做的理解工作 | 用哪类占位 |
|---|---|---|---|
| 多步机制/原理 | 因果链 ≥3 环、"背后的逻辑" | 拆成有序因果流（步骤+箭头） | **understanding** |
| 多要素结构关系 | "由 A/B/C 组成"、"X 与 Y 的关系" | 显式画谁连谁/谁含谁 | **understanding** |
| 数据堆叠/对比 | 一段 ≥3 个数字、"是…的 N 倍" | 把数字变成可比的长短/面积 | understanding 或 diagram |
| 反直觉结论 | "出乎意料"、"恰恰相反"、"误区" | 并置「以为 vs 其实」两列对照 | **understanding** |
| 时间线/演变 | 年份、"三个阶段"、迭代 | 沿轴铺开演变，标拐点 | **understanding** |
| 多方对比/权衡 | "A vs B"、"各有利弊"、取舍 | 同维度对照矩阵 | **understanding** |
| 抽象概念无锚点 | 新术语、"所谓 X"、纯定义 | 给一个具象类比/视觉锚 | concept（AI 生图） |
| **想象一下 ★硬触发** | **"想象一下""设想""试想""假如你""脑补"** | 把那个画面画出来 | concept（AI 生图）。要标注精确信息时配一张 understanding 叠在旁边 |

> ★ "想象一下" 几乎必配：作者亲口承认纯文字撑不起画面、主动让位给视觉。

## 4. understanding 占位块格式（HTML→PNG）

在该节正文下方插入占位块。**`<pre>` 里放 HTML 转义后的 `.illustration` 片段**，
fill_images.py 会 unescape → 用 render_illustration（Playwright/Chromium）截图成 `images/illus_NN.png`。

```html
<div class="img-placeholder understanding" data-caption="一句图注，把图钉回正文，别写'如图所示'">
  <div class="img-placeholder-icon">🧩</div>
  <div class="img-placeholder-label">理解图占位</div>
  <details><summary>理解图 HTML</summary><pre>
&lt;div class="illustration"&gt;
  &lt;h2&gt;主标题：一句话点出这张图解决什么卡点&lt;/h2&gt;
  &lt;div class="sub"&gt;副标题：补充语境&lt;/div&gt;
  &lt;div class="row"&gt;
    &lt;div class="step"&gt;&lt;div class="n"&gt;1&lt;/div&gt;&lt;div class="label"&gt;步骤名&lt;/div&gt;&lt;div class="desc"&gt;一句解释&lt;/div&gt;&lt;/div&gt;
    &lt;div class="arrow"&gt;→&lt;/div&gt;
    &lt;div class="step"&gt;&lt;div class="n"&gt;2&lt;/div&gt;&lt;div class="label"&gt;步骤名&lt;/div&gt;&lt;div class="desc"&gt;一句解释&lt;/div&gt;&lt;/div&gt;
  &lt;/div&gt;
&lt;/div&gt;
</pre></details>
</div>
```

### 关键约束（违反则脚本零匹配 / 图丑）

- **`<pre>` 里的 `<` `>` `&` 必须转义成 `&lt;` `&gt;` `&amp;`**——否则中间 HTML 会破坏文章结构。
- **`</details>` 与最外层 `</div>` 不得省略**——fill_images 正则依赖它们。
- **`data-caption` 是图注**——务必写，且别写"如图所示"，要把图的结论钉回正文。
- **`<pre>` 内不要出现 `</details>` 或 `</pre>` 字样**。

### 统一 CSS 约定（一篇文章所有图共用 → 成套感）

不用写 `<style>`，render_illustration 会自动注入下面这套变量与基础类。直接用这些 class 即可：

- 变量：`--primary`(#3B5BDB 主蓝) `--accent`(#E8590C 强调橙) `--good`(#2B8A3E 绿) `--ink`(墨) `--sub`(灰) `--line`(描边) `--bg-soft`(浅底)
- 容器：`.illustration`（外层卡片，**必须有，截图选择器靠它**） `.illustration h2` / `.sub`
- 流程：`.row` 横排，`.step`（含 `.n` 序号圆点 / `.label` / `.desc`），`.arrow` 箭头
- 对照：`.vs` 两列，`.vs .think`（"以为"浅橙）/ `.vs .fact`（"其实"浅绿），配 `.tag.think` / `.tag.fact` 标签
- 对比条：`.bar-row`（含 `.name` / `.bar`（设 `style="width:..."`）/ `.val`）
- 底部：`.note` 收口小字（很适合放删图测试结论或一句 punchline）

需要更复杂的样式，可在片段里自带 `<style>`（会覆盖默认），或内联 `style=""`。

## 5. 接入与降级

- 公众号文章默认产出 understanding；纯抽象概念/"想象一下"用 concept；纯数据可用 diagram。
- fill_images.py 自动渲染，落地 `images/illus_NN.png`（PNG，微信草稿同步直接上传，无需转换）。
- 渲染层不可用（无 Node/Playwright/Chromium）时 → 该占位**跳过保留**，不中断流程，后续步骤照常。
