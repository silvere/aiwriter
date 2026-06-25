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

## 4.5 高大上铁律：把想法画出来，不要给文字加底色

这一节是配图从「一般」到「高大上」的分水岭，**每张图都必须过**。

**一句话**：图是把观点*视觉化*（一个形状 / 一段空间关系 / 一个隐喻），不是把文字放进圆角盒子里。

### 视觉形态词表（难点类型 → 用什么形态画，别再默认堆步骤卡）

| 难点 | 视觉形态 | 主要手段 |
|------|----------|---------|
| 一个关键比例/占比/规模 | **一个大数字** `bignum` + 一句话；必要时配**一根** `proportion` 比例条 | 大数 + 直接标注 |
| 构成/拆分（≤4 项） | **一根** `proportion` 分段条 + 图例直接标注 | 禁止画多根柱 |
| 多步机制/因果 | 带**连接线/箭头**的流程；能用隐喻就用隐喻（墙、闸门、回路） | 内联 SVG + `.step` |
| 包含/层级关系 | **嵌套**（同心圆、套盒）——让"谁在谁里面"一眼可见 | 内联 SVG 圆/矩形 |
| 反直觉对照 | 并置两侧（`.vs`），或用**大小/位置**编码强弱 | `.vs` 或 SVG |
| 时间线/演变 | 一条主轴 + 拐点标注 | 内联 SVG 轴线 |
| 真·多序列数据 | 才用图表（ECharts）；**3 根以内的柱子一律改成大数字/比例条** | 见 §6 |

### 反模式（出现任何一条＝重做）

1. **纯文字罗列**：整张图删掉边框后就是几行字 → 不合格，必须有一个删不掉的视觉形状。
2. **裸条形图**：三五根没有设计的柱子 → 改成「大数字 + 一根比例条」或直接标注。
3. **emoji 当图标**：🧩🎨📊 只能出现在占位块图标处，**绝不进 `.illustration` 画面**；要图标用内联 SVG 线性图标。
4. **一张图塞多个想法**：一图只解一个卡点；元素（卡片/条目）总数 ≤ 6。
5. **花哨配色**：≥2 个强调色 = 廉价。全图只用 **1 个**强调色（`--accent`），其余灰阶。

### 验收闸（accept 前自问，任一"否"就重做）

- 把图里所有文字遮住，还剩一个**能看懂大意的形状**吗？
- 有没有**一个**明确的视觉焦点（最大的那个元素）？
- 是否只用了 1 个强调色 + 大留白？
- 这张图是**画出了**观点，还是只是把那段话*排版*了一遍？

## 4.6 统一设计系统（自动注入，直接用 class，别自带 `<style>`）

render_illustration 自动注入下面这套**编辑级**变量与组件，保证整篇成套：

- **配色**：`--accent`(#E0792B 暖橙，唯一强调色) `--accent-deep` `--accent-soft` ｜ `--ink`(近黑) `--sub`(灰) `--hair`(发丝线) ｜ `--neutral`/`--neutral-soft`(冷灰) ｜ `--good`/`--bad`
- **文头**：`.kicker`（小字间距大写眉标，放栏目/主体名）→ `h2`（38px 大标题）→ `.sub`（副标题）
- **大数字**：`.bignum`（150px 焦点数字，内可放 `<small>%</small>`）——少量数据首选
- **比例条**：`.proportion`（容器）内放若干 `.seg`（`style="width:..%;background:.."`）+ `.scale`（左右刻度）——替代多根柱
- **图例/直接标注**：`.legend` 容器 + `.lg`（含 `.dot` / `.n` 大数 / `.t` 小注）
- **流程**：`.row` 横排 + `.step`（`.n` 序号 / `.label` / `.desc`）+ `.arrow`
- **对照**：`.vs` 两列（`.think` 暖 / `.fact` 绿）+ `.tag.think` / `.tag.fact`
- **收口**：`.punch`（底部主张条，`<b>` 走强调色）/ `.note`（小字补充）
- **容器**：`.illustration`（**必须有**，截图选择器靠它；已含纸底+留白+阴影）

**内联 SVG 是高大上的关键**：嵌套圆、连接线箭头、墙/闸门/回路等隐喻，都用内联 `<svg>` 画（文字用 `<text>` 但只放短标签）。SVG 配色复用上面的 hex。需要覆盖默认时可内联 `style=""`。

### 一个「好图」示例（大数字 + 比例条，替代裸柱）

```html
&lt;div class="illustration"&gt;
  &lt;div class="kicker"&gt;META · 2026 年这次重组&lt;/div&gt;
  &lt;h2&gt;一次动了全球 1/5 的人&lt;/h2&gt;
  &lt;div class="row" style="align-items:center;gap:48px;margin-top:28px"&gt;
    &lt;div class="bignum"&gt;20&lt;small&gt;%&lt;/small&gt;&lt;/div&gt;
    &lt;div style="flex:1"&gt;
      &lt;div class="proportion"&gt;
        &lt;div class="seg" style="width:57%;background:var(--accent-deep)"&gt;裁&lt;/div&gt;
        &lt;div class="seg" style="width:43%;background:var(--accent)"&gt;转&lt;/div&gt;
      &lt;/div&gt;
      &lt;div class="legend" style="margin-top:22px"&gt;
        &lt;div class="lg"&gt;&lt;div class="dot" style="background:var(--accent-deep)"&gt;&lt;/div&gt;&lt;div&gt;&lt;div class="n"&gt;~8000&lt;/div&gt;&lt;div class="t"&gt;裁员&lt;/div&gt;&lt;/div&gt;&lt;/div&gt;
        &lt;div class="lg"&gt;&lt;div class="dot" style="background:var(--accent)"&gt;&lt;/div&gt;&lt;div&gt;&lt;div class="n"&gt;~7000&lt;/div&gt;&lt;div class="t"&gt;强制转岗做 AI&lt;/div&gt;&lt;/div&gt;&lt;/div&gt;
      &lt;/div&gt;
    &lt;/div&gt;
  &lt;/div&gt;
  &lt;div class="punch"&gt;同一周，扎克伯格认错：&lt;b&gt;我们犯了错误，几乎肯定会再犯更多&lt;/b&gt;&lt;/div&gt;
&lt;/div&gt;
```

## 6. 真·多序列数据图（ECharts，已接入）

**先判断要不要图表**：≤4 个数据点、单序列 → 一律走「大数字 + 比例条」（§4.6），**不要画图表**。只有「多序列 × 多类目」（趋势线、分组对比、占比拆解）裸条表达不了时，才用 ECharts。

render_illustration 检测到片段里有 `echarts` 就**自动内联** vendored 库（离线，不依赖 CDN）。直接在 `.illustration` 里放一个图表容器 + init 脚本即可。**必须**：用 `renderer:'svg'`（矢量清晰、CJK 文字可靠）、`document.fonts.ready.then(...)` 里再 `setOption`（否则中文画成方块）、`animation:false`。

极简主题约定（套用，保证高大上 + 成套）：单强调色 `#E0792B` + 灰 `#9AA4B2`；去掉重网格线（`splitLine` 用 `#F0ECE4`）；坐标轴线 `#D7DCE3`、不要刻度；图例右上、`roundRect` 图标。

```html
&lt;div class="illustration"&gt;
  &lt;div class="kicker"&gt;眉标&lt;/div&gt;
  &lt;h2&gt;一句话点出图表的主张&lt;/h2&gt;
  &lt;div id="c" style="width:980px;height:400px;margin-top:6px"&gt;&lt;/div&gt;
  &lt;script&gt;
  document.fonts.ready.then(function(){
    var ch = echarts.init(document.getElementById('c'), null, {renderer:'svg'});
    ch.setOption({
      animation:false,
      textStyle:{fontFamily:'PingFang SC,Noto Sans CJK SC,WenQuanYi Zen Hei,sans-serif'},
      color:['#E0792B','#9AA4B2'],
      legend:{top:2,right:4,icon:'roundRect',itemWidth:14,textStyle:{color:'#717584'}},
      grid:{left:6,right:20,top:54,bottom:6,containLabel:true},
      xAxis:{type:'category',data:['2023','2024','2025','2026'],
        axisLine:{lineStyle:{color:'#D7DCE3'}},axisTick:{show:false},axisLabel:{color:'#717584',fontSize:15}},
      yAxis:{type:'value',splitLine:{lineStyle:{color:'#F0ECE4'}},axisLabel:{color:'#9AA4B2'}},
      series:[
        {name:'序列A',type:'line',smooth:true,data:[100,90,60,20],lineStyle:{width:3.5},symbolSize:9,areaStyle:{color:'rgba(224,121,43,.10)'}},
        {name:'序列B',type:'line',smooth:true,data:[20,45,90,170],lineStyle:{width:3.5},symbolSize:9}
      ]
    });
  });
  &lt;/script&gt;
&lt;/div&gt;
```

> 图表也要过 §4.5 验收闸：一图一主张、单强调色、有焦点。能用一条趋势线讲清的，别堆五组柱子。

## 7. 接入与降级

- 公众号文章默认产出 understanding（按 §4.5 铁律设计）；纯抽象概念/"想象一下"用 concept；多序列数据见 §6。
- fill_images.py 自动渲染，落地 `images/illus_NN.png`（PNG，微信草稿同步直接上传，无需转换）。
- 渲染层不可用（无 Node/Playwright/Chromium）时 → 该占位**跳过保留**，不中断流程，后续步骤照常。
