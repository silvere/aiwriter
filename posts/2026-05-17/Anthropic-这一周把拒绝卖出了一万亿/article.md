# Anthropic 这一周把"拒绝"卖出了一万亿

> **发布日期**：2026-05-17 | **分类**：AI 商业拆解

## 核心观点

- Anthropic 的加冕日不是 5 月 12 日 Bloomberg 爆估值的那天，是 5 月 14 日——一天之内官宣 Gates 基金会、PwC、和给老用户加价的邮件
- Ramp 34.4% 不是"AI 市场份额"，是"愿意刷企业卡试 AI 的中型公司里 Anthropic 占了多少"——OpenAI 最大的几张合同根本不走信用卡
- "安全"在 Anthropic 这里不是合规成本，是定价锚——这套定价锚必须靠"拒绝"来兑现：拒绝 EU、拒绝把 Mythos 公开、把老用户的 Agent 调用从订阅里剥离

---

## 一、加冕日不是 5 月 12 日，是 5 月 14 日

5 月 12 日 Bloomberg 放出一条独家：Anthropic 在洽谈一轮 300 亿到 500 亿美金的新融资，投前估值挂在 9000 亿到 9500 亿美金之间——这个数字超过 OpenAI 上一轮 8520 亿美金的估值。

中文媒体当天全部跟进，标题都差不多："Anthropic 反超 OpenAI"、"奥特曼急了"、"一万亿"。

这是错的加冕日。

加冕日是 5 月 14 日。

5 月 14 日早上，Anthropic 官网发了第一条公告：和盖茨基金会签 2 亿美金、4 年期合作，钱用于全球健康、生命科学、教育、经济流动——首批病种是脊髓灰质炎、HPV、子痫前期，覆盖 4.6 亿"得不到基本医疗服务的人"。

同一天上午，Anthropic 官网发了第二条公告：和 PwC 把现有联盟扩展。3 万名 PwC 专业人员要拿到 Claude 认证，Claude Code 和 Cowork 从全美推到全球，其中一个客户案例说"保险核保从 10 周降到 10 天"。

同一天晚上 8 点 10 分太平洋时间，Anthropic 给所有 Claude Max 20x 订阅用户发了一封邮件：从 6 月 15 日起，第三方 Agent 调用——Agent SDK、`claude -p` 命令、GitHub Actions、OpenClaw——全部从你的订阅额度里剥离出去，按 API 标价独立计费。Pro 用户每月送 20 美金的 Agent 信用额度，Max 5x 送 100，Max 20x 送 200。不滚存。

兄弟们，加冕的不是估值，是这三件事可以同一天发生。

早上 9 点给道德背书。早上 10 点给机构信用。晚上 8 点 10 分对最忠实的开发者用户加价。一家公司能在 12 小时之内做这三个完全相反的动作——同时还能让所有这三个动作的当事人都觉得"我赚了"——这才是加冕。

Bloomberg 那条估值是结果。5 月 14 日那一天才是因。

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>A single calendar page showing "May 14" with three different envelopes stacked on it, each envelope marked with a different time stamp 9AM 10AM and 8PM, flat design, minimalist illustration, tech style, blue and white color palette with subtle gold accent, no text, no labels, clean white background</pre></details>
</div>

---

## 二、Ramp 那张 34.4% vs 32.3% 的图，刷的是企业卡，不是市场

回到 5 月 12 日，那天真正动了估值的不是 Bloomberg，是 Ramp。Ramp 是一家美国企业卡 + 报销 + 票据 SaaS，5 月 12 日他们发了五月份的 AI Index：Anthropic 在采用率上从 4 月的 30.6% 涨到 34.4%，OpenAI 从 35.2% 跌到 32.3%。

中文媒体的标题翻译成一句话就是——Anthropic 反超 OpenAI，王朝交替了。

但 Ramp 自家在解释这套指数怎么做的页面上，是这么写的：

> "We analyze line-item data from the corporate cards and Bill Pay invoices of more than 50,000 Ramp customers."

翻成中文：我们扫描 5 万多家 Ramp 客户的企业卡刷卡和 Bill Pay 票据，做发票 line-item 级别的 OCR。

这一段话有三层意思。第一层：样本只来自 Ramp 的客户。Ramp 主打中小企业财务管理，不是面向《财富》500 强大企业的 ERP。5 万家"用 Ramp"的公司，跟"用 Anthropic 或 OpenAI"的全美企业池子不是一回事。

第二层：只看通过企业卡和 Bill Pay 处理的支出。OpenAI 自己在 2025 年下半年的多份公开材料里说过，他们最大的几张企业合同——和摩根大通、和德勤、和美国国务院——走的不是企业卡，是合同账单和年度采购协议。Anthropic 同样有类似的大合同，但 Anthropic 的 SMB 端订阅、个人开发者的信用卡支付、Pro/Max 月费——全部都进 Ramp 的可见域。

第三层：line-item OCR。这套抓取是按笔抓的，每多一笔订阅、每多一个开发者刷卡试用一周，都会被算进采用率，不管那笔订阅一个月之后是不是续费。

所以 Ramp 34.4% 真正的口径是：在愿意通过企业卡试 AI 的中型公司里，Anthropic 占了 34.4%。

这个数字是真的，趋势是真的，反超也是真的。但它说的不是"AI 市场份额"，它说的是"中腰部企业的渗透率"。

OpenAI 真正没说出口的反驳应该是：我们最贵的客户从来不刷卡。

但 OpenAI 不会说，因为说了等于承认自己的真实订阅基数被中腰部稀释了。Anthropic 也不会说，因为不说，34.4% 这个数字就可以被一切媒体翻译成"市场份额"。

两边都不说话，市场就默认它是市场份额。Bloomberg 当天放估值，逻辑通了。

这件事的本质是：**Anthropic 是从中腰部攻顶的，OpenAI 是被顶部和底部两头夹的。**

顶部 Pentagon 上周把 Anthropic 拉黑了，OpenAI 拿走 2 亿美金合同。底部消费者 ChatGPT 还在烧补贴。中间一层——那些 50 到 500 人、用 Ramp 卡刷 Claude Code 月费的公司——是 Anthropic 一年时间里安静拿下的盘子。

Ramp 那张图本质上是一张中腰部企业的体检报告。Anthropic 这一年悄悄把这张体检报告给做透了。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：双柱对比 + 注释
【副标题】：Ramp AI Index 五月数据：刷的是企业卡，不是市场份额
【单位】：百分比（Ramp 客户中使用某 AI 的比例）
【核心判断】：34.4% 不是 AI 市场份额，是中腰部企业渗透率
【核心内容】：
  - Anthropic 4月 30.6% → 5月 34.4%（+3.8pp）
  - OpenAI 4月 35.2% → 5月 32.3%（-2.9pp）
  - 总 AI 采用率 50.6%
  - 样本：5万+ Ramp 客户，主要为中小企业
  - 仅统计企业卡 + Bill Pay 票据交易
  - 不包含：年度采购合同、政府采购、大企业 ERP 走账
【配色】：Anthropic 用暖橙色（#D97757），OpenAI 用深蓝色（#10A37F 反色），背景白
【备注】：在图下方加一行小字 "Source: ramp.com/leading-indicators/ai-index-may-2026"</pre></details>
</div>

---

## 三、万亿估值的算盘：$44B 年化收入，inference 毛利 70%+

把估值这条线拆开看。Bloomberg 那条独家说，新一轮融资规模 300 亿到 500 亿美金，投前估值 9000 亿到 9500 亿。这是匿名信源的口风，Bloomberg 自己写明"尚未签署 term sheet"。

但估值不是凭空报的，它必须挂在一个收入数字上。

5 月初 Anthropic 自家的开发者大会上，Dario Amodei 公开说过两个数字：年化收入"超过 440 亿美金"，inference 毛利从过去的 38% 升到了"70% 以上"。

把这两个数字塞进估值模型：

- 9500 亿 / 440 亿 ≈ 21.6 倍年化收入
- 估值假设三年达到稳态、稳态自由现金流率取 25%（70%+ 毛利下不算激进），意味着投资人认 Anthropic 三年后每年烧得起 110 亿美金做研发还能不亏

OpenAI 上一轮 8520 亿美金估值挂的是大约 250 亿年化收入——倍数差不多 34 倍。

听起来 OpenAI 更贵。但 OpenAI 那 250 亿里有大约 60% 来自 ChatGPT 消费者订阅，毛利率公认低（Sam Altman 2024 年那句"我们每个 Pro 用户都在亏钱"的梗到现在还没洗掉）。Anthropic 那 440 亿里面来自 API 调用和企业订阅的比例公认更高，毛利更厚。

这里 21.6 倍和 34 倍的差距，市场给出来的解读不是"Anthropic 更便宜"，是"Anthropic 那 440 亿是真钱，OpenAI 那 250 亿是流量"。

所以 9500 亿估值的真正定价锚不是模型，是每一美金收入背后的毛利结构。

这件事的反常识在哪？行业默认 AI 公司估值靠的是技术领先和用户规模——所谓 talent density 和 daily active users。但 Anthropic 这一轮的估值锚是单位收入的赚钱能力。这是已经成熟的 SaaS 公司的估值逻辑，不是早期赛道公司的逻辑。

换句话说，资本市场已经默认 Anthropic 不是一家"AI 创业公司"，是一家"SaaS 公司"。

万亿估值的另一面是这个：从此 Anthropic 必须按 SaaS 的标准答卷——每一个季度毛利、续费率、净留存——不再有早期赛道的容错空间。

5 月 13 日晚上那封给 Max 20x 用户加价的邮件，本质就是 SaaS 公司在做 ARPU 优化。SaaS 公司要保毛利，不是要保用户体验。

资本市场吃这一套。开发者社区不一定吃。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：估值锚对比表
【副标题】：Anthropic 9500亿 vs OpenAI 8520亿 估值拆解
【单位】：美元 / 倍数 / 百分比
【核心判断】：Anthropic 估值锚是单位收入毛利，OpenAI 估值锚是用户规模
【核心内容】：
  | 指标 | Anthropic | OpenAI |
  | 估值 | $950B | $852B |
  | 年化收入 | $44B | ~$25B |
  | 估值/收入倍数 | 21.6x | 34.1x |
  | 收入构成主体 | API + 企业订阅 | ChatGPT 消费者订阅 |
  | Inference 毛利 | 70%+ | 未公开 |
【配色】：Anthropic 暖橙，OpenAI 深绿
【备注】：底部加 "Source: Amodei 公开发言 + Bloomberg 5/12 报道，未签 term sheet"</pre></details>
</div>

---

## 四、Mythos：Anthropic 给整个网络安全行业出了张反常识定价表

5 月 11 日 CNBC 那篇报道里有一句话被中文媒体完全跳过了：欧盟委员会发言人公开说，Anthropic 在 Mythos 的访问问题上"还没到 OpenAI 那个阶段——OpenAI 已经把 GPT-5.5-Cyber 给 EU 的网络安全团队做了限定预览"。

Anthropic 自己的红队博客上 Mythos 的描述是这样的：

> "capable of identifying and then exploiting zero-day vulnerabilities in every major operating system and every major web browser"

翻成中文：能在每一个主流操作系统和每一个主流浏览器里识别并利用零日漏洞。

红队博客同时给出了三个具体的数字：

- 在 Firefox 中发现了"近 300 个"零日漏洞
- 在 OpenBSD 中找到一个存在了 27 年的 bug
- 单次模型运行成本"低于 50 美金"，单次发现项目成本"大约 20,000 美金"

这三个数字单独看是 Anthropic 自夸。合在一起看是一张定价表。

行业惯例：一个有商业价值的 0day 在地下市场报价 5 万到 50 万美金不等，重点取决于操作系统和触发条件。一个 bug bounty 项目里挖一个 0day 的悬赏均价在 5,000 到 50,000 美金之间，重大漏洞悬赏可以到 100 万。

Mythos 把这个数字直接打到 20,000 美金，而且这是模型自己挖的，不是雇人挖的。

把这个数字往 Project Glasswing 的预算里塞：1 亿美金的使用额度，按 20,000 美金一个 0day 算，是 5,000 个可发现漏洞。

5,000 个 0day 是什么概念？

美国 NIST 国家漏洞数据库 2025 全年收录的所有"严重等级 (Critical)"漏洞总数大约是 4,500 个。也就是说，Anthropic 给 Project Glasswing 的预算，理论上能用机器复刻整个 NIST 一年的"严重漏洞"目录。

到这一步，"Mythos 是什么"才说得清楚——Mythos 不是 AI 安全研究产品，是一个可被估值的国家战略物资。

Project Glasswing 的 12 个创始成员名单是这样的：AWS、Apple、Broadcom、Cisco、CrowdStrike、Google、JPMorganChase、Linux Foundation、Microsoft、NVIDIA、Palo Alto Networks。这里面 6 家是美国前 10 大企业，3 家是美国国家网络安全防御体系的基础设施，1 家（Apache Software Foundation 拿了 150 万美金捐赠）是全球开源代码的最关键节点之一。

整个名单一个欧洲公司都没有。

不是巧合。Anthropic 一边给 Glasswing 联盟的成员开放 Mythos Preview，一边给欧盟监管者关门。这两件事是同一件事的两面。

"安全" 这个词在 Anthropic 这里，意思是"我替美国管，不替欧盟管"。

欧盟想要的是"独立第三方监管者的访问权"。Anthropic 给出的回答是"在 CAISI（美国 AI 安全机构）的监管下我们可以做"，但 CAISI 不是中立的第三方，是美国商务部下属机构。

这件事用 Anthropic 内部自己的话翻译过来是这样的：**我们不是不接受监管，我们只接受美国的监管。**

Mythos $20,000 的单位成本是个铺垫。真正的产品是"对谁开放、对谁关门"这套权限分级。

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>A circular door or vault entrance with twelve key-shaped logos arranged around it in a ring representing access tokens, while one outline of Europe shape is on the outside looking in through a separate small porthole, flat design, minimalist illustration, tech style, blue and white color palette with subtle red accent on the porthole, no text, no labels, clean white background</pre></details>
</div>

---

## 五、SMB 与 Max 加价：同一套定价心理学的两面

回到 5 月 13 日。那天 Anthropic 同时做了两件事，方向看起来完全相反。

第一件事：Claude for Small Business 发布。QuickBooks、PayPal、HubSpot、Canva、DocuSign、Google Workspace、Microsoft 365 七个连接器，15 个预制工作流，15 个 Skills。Anthropic 自己出 10 城路演——芝加哥、底特律、亚特兰大、达拉斯、丹佛等等——每站给 100 名 SMB 主免费培训。

Anthropic 公告里有一段话原文是这样的：

> "Small and medium-sized businesses contribute approximately 44% of U.S. GDP and employ nearly half of the private workforce."

翻成中文：中小企业贡献了美国 44% 的 GDP，雇佣了近一半的私营部门员工。这一段是用来支撑 SMB 套件的市场体量。

第二件事：当晚 8 点 10 分太平洋时间那封邮件。前面提过——Pro / Max 5x / Max 20x 用户从 6 月 15 日起，所有第三方 Agent 调用从订阅额度里剥离。Pro 用户每月送 20 美金独立 Agent 信用额度，Max 5x 送 100，Max 20x 送 200。

InfoWorld 当天有跟进，提到一批做 Coding Agent 的小公司（OpenClaw、Continue 等）当晚客户支持渠道直接被开发者打爆——很多人订阅 Max 20x 月费 200 美金的核心理由就是无限制跑 Coding Agent。

这两件事放在一起，方向完全相反：一头是把门栏拉低让 SMB 进来，一头是把已经进门的开发者重新分箱收费。

但仔细看，这两件事其实是同一回事。

Anthropic 在做用户分级。

层级从上到下大概是这样：
1. 美国大企业 + 政府 + 国家级网络安全联盟（Project Glasswing 成员）——拿 Mythos Preview，定价不公开
2. 华尔街金融机构（5 月 5 日的 Wall Street 发布会上展示的那批 Agent 模板）——拿 Claude Opus 4.7 + 金融 Agent
3. 大型咨询机构（PwC 那 3 万人）——拿 Claude Code + Cowork 认证
4. 中型企业（Ramp 数据池里的那 5 万家）——刷企业卡用月费版
5. 小型企业（5 月 13 日的 Claude for SMB）——七大连接器 + Skills 模板
6. 个人开发者（5 月 13 日邮件加价的那批人）——订阅额度 + 单独购买 Agent 信用
7. 欧盟监管者（5 月 11 日 CNBC 那段）——闭门

每一层都有自己的定价和访问权限。这是一套完整的分级产品矩阵。

行业一直觉得 AI 公司只能两条路：要么做 to C 走平台规模（OpenAI 路线），要么做 to B 走单一企业大单（Cohere 路线）。Anthropic 这一周用产品组合证明了第三条路：做"美国为中心、按地缘政治分级"的全产品堆栈。

这套堆栈的核心定价机制不是"功能差异"，是"访问权限差异"。

最顶上那一层之所以最贵，不是因为 Mythos 比 Claude Opus 4.7 强多少，是因为 Mythos 拒绝了 EU 监管者、拒绝了所有非 Glasswing 成员。"被拒绝"这件事本身在定价。

最下面那一层（个人开发者）之所以可以加价，不是因为 Agent SDK 多了什么新功能，是因为 Anthropic 已经验证了开发者社区会咽下这口气——你已经把 Claude Code 集成进你日常工作流了，每月 200 美金的迁移成本远高于 Anthropic 加价的边际幅度。

这是典型的"先免费后加价"的 SaaS 套路，但 Anthropic 的版本是"先深度集成后加价"。深度集成是免费的，但只是一次性免费。

5 月 13 日同一天的两个动作，对外的话术不一样（SMB 那边是"赋能中小企业的繁荣"，Max 那边是"让定价更公平"），但底层动作是同一个：**用户分级、按分级定价、按分级管访问。**

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：金字塔分层图
【副标题】：Anthropic 的七层产品矩阵：从 Mythos 到欧盟
【单位】：用户层级
【核心判断】：定价不是按功能，是按"被允许访问"的程度
【核心内容】：
  顶层 → 底层（每层标注典型客户 + 访问权限）：
  1. Mythos / Glasswing（AWS/Apple/Google/Microsoft/JPMorgan 等 12 家）
  2. Wall Street Tier（Moody's/JPMorgan + 金融 Agent 模板）
  3. PwC Tier（3 万认证专业人员）
  4. 中型企业（Ramp 池子里 5 万家）
  5. Claude for SMB（10 城路演 SMB 主）
  6. 个人开发者（Pro/Max，6/15 起 Agent 单独计费）
  ——— 围墙 ———
  7. 欧盟监管者：拒绝访问
【配色】：从深橙到浅橙渐变，最底层（欧盟）用灰色，与上方分割
【备注】：底部加一行 "每一层的访问权限本身就是产品的一部分"</pre></details>
</div>

---

## 六、"拒绝"是 Anthropic 唯一不可复制的产品

回到那个最大的问题：为什么是 Anthropic？

不是模型。Claude Opus 4.7 在公开 benchmark 上没有压倒性优势，GPT-5.5 在多个评测里仍然领先。

不是安全研究能力。OpenAI 也有 Cyber 模型，Google 也有 DeepMind 的安全团队，Microsoft Security Copilot 上线两年了。

不是企业销售能力。OpenAI 的企业销售团队规模更大，渠道覆盖更广。

是 Anthropic 这一周表演了一种别人复制不了的姿态——它可以同一天给最受尊敬的慈善基金会签支票、给最大的咨询公司发认证、给最忠诚的开发者用户加价，而不被骂。

OpenAI 试一次同样的组合动作，市场和媒体会问"你赚钱赚得这么急吗"。
Google 试一次，反垄断诉讼当天会多出三条新指控。
Microsoft 试一次，Windows 用户社区一周就能让股价跌 5%。

Anthropic 试了，没事。

为什么？因为 Anthropic 这五年时间里把"我们更在乎安全"的人设打得太透。透到这家公司的每一个商业动作，都会被默认是"在为更深远的安全目标做权衡"。

拒绝 Pentagon 是为安全。
拒绝 EU 是为安全。
给 SMB 开门是为"让更多人用上安全的 AI"。
给老用户加价是为"让基础设施的可持续性匹配安全研究的投入"。

每一句话都说得通。每一句话都站得住脚。每一句话都让对手攻不进来。

这就是"安全"作为品牌的最大商业价值——它是一个永远可以挡刀的话术。

但话术挡刀只是表层。深层是这套话术构成了一个不可复制的护城河。任何 AI 公司想做"安全 AI"作为差异化，会立刻被市场问："那你和 Anthropic 比有什么不一样？"——而 Anthropic 用了五年时间、上百篇可解释性论文、Constitutional AI 这套对外披露的训练框架，给"我们更在乎安全"这件事砌了一道无法被一夜超越的墙。

这道墙的存在本身，就是一个产品。

OpenAI 这一周也在做安全 AI（GPT-5.5-Cyber 给 EU），但媒体在写它的时候只会用"OpenAI 也跟进了"。Google 这一周也在发布安全工具，但行业读出来的是"防御性动作"。Anthropic 做的是同一件事，行业读出来的是"原教旨主义"。

原教旨主义是可以收溢价的。原教旨主义可以拒绝。原教旨主义可以加价。原教旨主义可以同一天做三件方向相反的事而不被质疑动机。

5 月 14 日那一天，Anthropic 真正加冕的，不是它的估值，是它的话语权。它已经成了 AI 行业唯一一家可以用"我们出于安全考虑"作为任何商业决策的最终解释的公司。

这种权利按市场口径定价，确实值 9500 亿美金。

加冕完了之后，Anthropic 的下一道关，是怎么把"我们更在乎安全"这件事用得既不让市场厌倦也不让自己破功。

Pentagon 上周已经试过怎么破这个功了——Hegseth 在国防部那场新闻发布会上当着记者面骂 Amodei 是"骗子，有上帝情结"。骂得很难听，但市场没接，企业客户没流失。

为什么？因为骂 Anthropic 这件事在叙事上太对称——你越骂它"原教旨"，它的"原教旨"溢价反而越高。

但下一次可能就没那么容易了。EU 那边正在酝酿真正的反制——5 月初已经有传言说 EU 在考虑把 Anthropic 的 Mythos 拒绝写入 AI Act 第二轮修订作为执法案例。如果 EU 真的把 Anthropic 列入"高风险供应商"清单，市场对"原教旨溢价"的反应可能就要变了。

万亿估值到那时候，挡的是另一种刀。

但这是另一篇文章的事了。

这一篇要说的是，这一周已经发生的事——Anthropic 教所有 AI 公司怎么靠"拒绝"挣钱，怎么把"安全"两个字做成一道无法被复制的护城河，怎么在加冕日那天同时完成道德、机构、定价权三件套。

教学完毕。

学不学得会，要看下一家公司有没有 Anthropic 这五年时间和这套话语耐心。

短期内，看不到。

就这？就这。

---

## 数据来源

- [Anthropic Newsroom](https://www.anthropic.com/news)
- [Anthropic - Claude for Small Business](https://www.anthropic.com/news/claude-for-small-business)
- [Anthropic - Gates Foundation Partnership](https://www.anthropic.com/news/gates-foundation-partnership)
- [Anthropic - PwC Expanded Partnership](https://www.anthropic.com/news/pwc-expanded-partnership)
- [Anthropic - Project Glasswing](https://www.anthropic.com/project/glasswing)
- [Anthropic Red Team - Mythos Preview](https://red.anthropic.com/2026/mythos-preview/)
- [Ramp AI Index - May 2026](https://ramp.com/leading-indicators/ai-index-may-2026)
- [Ramp - How We Built the AI Index](https://ramp.com/velocity/how-we-built-the-ramp-ai-index)
- [CNBC - OpenAI to give EU access to new cyber model but Anthropic still holding out on Mythos (2026-05-11)](https://www.cnbc.com/2026/05/11/openai-eu-cyber-model-anthropic-mythos-gpt.html)
- [Fortune - Behold the Googlebook (2026-05-13)](https://fortune.com/2026/05/13/behold-the-googlebook/)
- [Fortune - Google catches hackers cybersecurity warning (2026-05-11)](https://fortune.com/2026/05/11/google-catches-hackers-cybersecurity-warning-ai-anthropic-mythos/)
- [PwC PRNewswire - PwC and Anthropic Expand Partnership](https://www.prnewswire.com/news-releases/pwc-and-anthropic-expand-alliance.html)
- [Gates Foundation Press Release - Anthropic Partnership](https://www.gatesfoundation.org/ideas/media-center/press-releases/2026/05/anthropic-partnership)
