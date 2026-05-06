# 你用的开源库，正在 Anthropic 的库存里

> **发布日期**：2026-05-06 | **分类**：AI深度

## 核心观点

- Mozilla 上周修了 271 个 Mythos 找到的 Firefox 漏洞，但 Anthropic 自己在官网上写："Over 99% of the vulnerabilities Mythos has found have not yet been patched."——你修的是 1%，没修的 99% 不在公网上，而在一家公司治理结构里
- 这是 AI 行业第一次让 0day 不再是研究员抽屉里的纸条、也不再是黑市挂牌的清单，而是一家上市预备公司资产负债表上能写的"库存"
- 9000 亿美金的 Anthropic 估值，用 SaaS 倍数算到 5000 亿就接近极乐观区间天花板了——剩下那 4000 亿对应的，是这份不在 IPO 招股书风险因素栏里的库存

---

## 导语

Mozilla 上周发了 Firefox 150。Patch notes 里写着 271 个安全修复，全部挂同一个名字——Claude Mythos。

Mozilla 自己写了一篇博客，说"我们看到的每个 bug，理论上都是顶级人类研究员能找到的"，但"没有人类团队能这么快找到 271 个"。这句话被各家媒体当头条转发。

同一周，Anthropic 在它的官方公告页面上写了一行字：**Over 99% of the vulnerabilities Mythos has found have not yet been patched.**

中文翻译：Mythos 找到的漏洞，超过 99% 还没修。

这句话没人转。

整篇文章就讲它。

---

## 一、271 是个尾数

271 这个数字本身已经够吓人。

参考一下规模。Project Zero——Google 顶级 0day 团队，全行业最公开的 vulnerability research 机构——一年公开披露的漏洞大约 100 出头。这是 ~20 个全职顶级研究员一年的总产出。

Mythos 在 Firefox 一次评估里，挖出 271 个。

Mozilla 三个月前用 Claude Opus 4.6 在自家代码库里跑过一轮，结果是 22 个 confirmed bugs，patch 进了 Firefox 148。从 22 到 271，Mozilla 用的不是更多人，是更新的模型。中间唯一变量是 Anthropic 给了它一份 Mythos Preview。

但这是水面上的部分。

Anthropic 自己的描述是这样的：thousands of high-severity vulnerabilities, including some in **every major operating system and every major web browser**——上千个高危漏洞，在每个主流操作系统、每个主流浏览器里都有。

他们没说"几千"是 2 千、5 千还是 1 万。他们说的是一个范围词。

但他们说了 271 是"过去几周内 Mozilla 这一份 collaboration 的产出"。

然后他们又说，已经披露并修补的占比，"Over 99% have not yet been patched"——意思是已修补的不到 1%。

如果 271 就是那个 1%，那剩下的 99% 对应大约 26800 个。

如果 271 只是 Firefox 这一家的份额，剩下的 99% 还要乘上"every major OS and browser"——Chrome、Safari、Edge、Windows、macOS、Linux 内核、Android、iOS——的所有码量。

具体数字 Anthropic 自己也算不清。但他们清楚一件事：他们手上的库存比已经公开的多两个数量级。

271 不是顶，是尾数。

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>An iceberg seen from a side view, only a tiny tip visible above the waterline labeled with binary code, a massive deep underwater portion glowing with thousands of small code fragments, flat design, minimalist illustration, tech style, blue and white color palette, no text, no labels, clean white background</pre></details>
</div>

---

## 二、那 99% 在哪里

99% 是个挺神秘的数字。

它不在公开的漏洞数据库里——CVE 没收，NVD 没收，Bugzilla 没贴。

它不在维护者的桌上——大多数 OSS 项目今天都没收到 Anthropic 的私人邮件说"嘿你们这有个洞"。

它不在攻方手上——按 Anthropic 自己的口径，Mythos Preview 不对外发售，没有人能调它的 API 拿这份能力。

那它在哪。

它在 Anthropic 公司治理结构里。一种叫"已经发现但未披露的漏洞"的资产，按"coordinated vulnerability disclosure"的行业流程合法存在。CVD 这个流程是 1990 年代为人类研究员设计的——一个研究员发现一个漏洞，给厂商 90 天补丁窗口，到点公开。这套流程的设计假设是：漏洞是稀缺的，研究员是分散的，每一个漏洞值得单独处理。

Mythos 把这三条假设全部踩掉了。漏洞不再稀缺，发现源不再分散，单独处理也跟不上速度。所以 CVD 在 Mythos 这里变成了一个新东西——一份可以无限期延长的"未披露状态"。

这份"未披露状态"有读者。

它的读者是 Project Glasswing 的 12 家 launch partners：AWS、Apple、Broadcom、Cisco、CrowdStrike、Google、JPMorgan Chase、Linux Foundation、Microsoft、NVIDIA、Palo Alto Networks，加上 Anthropic 自己。

它还有 40 多个延伸读者——Anthropic 公开说的"organizations that build or maintain critical software infrastructure"，但具体名单不公开。

它还有一个公开但不公告的读者——NSA。Axios 4 月 19 日的报道证实了这一点。

把这些读者放在一起看：12 + 40 + 国安局 + Anthropic 自己——这是一份能看见 99% 的名单。

剩下的人只能看见 1%。

271 是 1% 那一栏的当期产出。

以前的 0day 有两个市场——Project Zero 这种公开市场，Zerodium 和 NSO 这种黑市。两个市场都不大：公开市场流量按年计百级，黑市按公开估算单家年成交也是几十到一百出头。两边的总量还不够 Mythos 一个 Firefox eval。

现在多出第三个。一家上市预备公司的资产负债表。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：饼图
【副标题】：Mythos 找到的漏洞总池子里，谁能看见多少
【单位】：%
【核心判断】：271 是公开披露的 1%，剩下的 99% 在 Glasswing 名单内可见，名单外只能等
【核心内容】：
  - 公开披露（Firefox 150 等）：1
  - Glasswing 内部可见但未公开：99</pre></details>
</div>

---

## 三、库存这个词不是比喻

讨论"漏洞作为资产"这件事的时候，行业里有人会说：研究员个人也持有过 0day 啊，没什么新鲜的。

不对。

研究员个人持有 0day 是一种流动性极差的资产。这个研究员退休、转行、跳槽到防御方、或者哪天意识到这件事不舒服——库存就归零了。这份漏洞跟着这个人一起走、一起退、一起死。它没法记账。

公司持有 0day 是另一种东西。它写在某种数据库里、某种工单系统里、某种漏洞跟踪流水线里。员工 A 离职了员工 B 接着用，董事会换届了流程不变，公司被收购了资产打包过户。公司持有的漏洞可以继承、可以估值、可以在并购时被尽职调查算到对价里。

Anthropic 的法律性质从这件事上变了一次。

它不再只是一家训练大模型卖月费的 SaaS 公司。它是一家持有未公开关键软件漏洞库存的有限责任公司。这两个法律身份在 IPO 招股书里要分开写。

Anthropic 现在的估值数字是 9000 亿美金。年化收入按上个月公告 300 亿。我们做一道行业标准的算术题。

成熟 SaaS 公司估值倍数在 8-12 倍 ARR，对应 2400-3600 亿。AI 类高速增长 SaaS 给到 15-20 倍，对应 4500-6000 亿。即使按 AI 行业可见过的最激进倍数 25 倍算，也就是 7500 亿。

9000 亿减去 7500 亿，剩 1500 亿。这是 SaaS 估值模型解释不了的部分。

如果再考虑 Anthropic 的 ARR 是从 2 月 90 亿涨到 4 月 300 亿——两个月 3.3 倍，这种增速不可能持续 12 个月——那"极激进倍数"本身也站不住。剩下需要解释的口径只会更大。

这部分溢价对应什么？三件事：政府订单（NSA 已确认在用 Mythos）、Glasswing 类别的特许许可、那笔 99% 没修的库存。

前两件好理解，是收入项，能写到 Pricing 那一栏。第三件没法直接定价，因为 Anthropic 自己也没说库存怎么变现——但市场愿意为这种"不知道怎么变现但显然有用"的东西付钱。这种付钱方式有个名字叫期权溢价。

普通 SaaS 公司没有这种期权可以卖。Anthropic 有。

这就是 0day 库存第一次进入估值模型。

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>A bank vault door wide open showing rows of safety deposit boxes, but instead of money or documents, each box contains glowing lines of source code and binary digits, flat design, minimalist illustration, tech style, blue and white color palette, no text, no labels, clean white background</pre></details>
</div>

---

## 四、你装的那个 npm 包，在哪一栏

回到具体一点的视角。

你打开自己电脑上的某个项目，看一眼 package.json，里面 dependencies 列了几十个包。再点开 node_modules，里面是 1500 个间接依赖。这 1500 个里，至少有 100 个是 5 年没更新过的，至少有 30 个是单人维护的，至少有 5 个的 GitHub repo 已经 archived 了。

这是 2026 年绝大部分项目的真实形状。npm 上注册了大约 300 万个 package，PyPI 上 60 万，Maven Central 80 万。这些是软件世界的真正长尾。

Glasswing 名单上没有它们。

名单上有 Linux Foundation——但 LF 是个组织，不是分发渠道。LF 收 Anthropic 给的 100 万 / 400 万捐款（Anthropic 公告里是 $100M usage credits 给 partners + $4M donations 给 OSS security 组织），它能资助一些核心 OSS 项目。Linux 内核能被覆盖到。Curl 这种基础库可能被覆盖到。但你 package.json 里那个 `is-odd@1.0.0` 包，没人覆盖。

那 Mythos 会扫它吗？

会。Mythos 不挑食，扫到哪算哪。

那扫到的漏洞会被披露给那个 npm 包的维护者吗？

按 Anthropic 的口径，会进入 coordinated disclosure 流程。CVD 流程里，第一步是联系 maintainer。但这个 maintainer 可能 2019 年就停止响应邮件了。CVD 流程的下一步是"如果 maintainer 不响应，公开披露"——但这是个 90 天的钟。在那 90 天里，这个漏洞躺在 Anthropic 库存里。

90 天到了之后呢？

如果这个包还有人在用——典型情况是有的，npm 上的休眠包用得是真的多——那么"公开披露"就变成"公开告诉所有攻击者：这个包有这个漏洞，没人会修"。CVD 流程在 maintainer 缺席的时候，结果是把漏洞从 Anthropic 库存搬到 attacker 手上。

这是 CVD 设计的副作用，不是 Mythos 制造的。但 Mythos 把这个副作用从"偶发现象"变成"工业化产出"。

按 Anthropic 自己的说法，受波及的范围是"every major operating system and every major web browser"。再加上无数它没特别提到的中间件、运行时、库。这些里面有名单的会进入 Glasswing 流程被快速 patch，没名单的进入"披露但无人修"的状态。

你用的开源库，要么在前者，要么在后者。

绝大多数在后者。

不是说现在已经发生了大规模的"披露但无人修"事件——Anthropic 还在按部就班地走 CVD 流程，目前看到的是 Mozilla 这种有人有钱有团队的项目接住了 271 个 patch。但 Mozilla 是名单上的浮标。沉在水底的是 GitHub 上几千万个不响应邮件的 repo。

这些 repo 不是 Anthropic 的客户，也不是 Glasswing 的合作伙伴，也不会进入估值模型——但它们承载了今天软件世界一半以上的实际运行代码。它们被扫到一个漏洞之后，能做的事只有一件：等。

等什么？等 90 天的钟走完。然后从 Anthropic 库存的"未披露"变成 GitHub 公开 issue 上的"已披露但无人修"。

这是 Mythos 这套设计在 OSS 长尾上的真实形状。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：对账图
【副标题】：Glasswing 名单内外的软件世界
【单位】：个
【核心判断】：12 + 40 个组织能拿到 Mythos 的"提前披露"待遇，npm/PyPI 长尾上几百万个包不在名单上
【核心内容】：
  - Glasswing launch partners [流入]：12
  - 延伸 critical infra orgs [流入]：40
  - npm 注册 packages [流出]：3000000
  - PyPI 注册 packages [流出]：600000
  - Maven Central [流出]：800000</pre></details>
</div>

---

## 五、招股书里这一行字怎么写

Anthropic 的 IPO 时间窗口 CNBC 的报道里写了一句"as early as October 2026"——10 月，5 个月后。

S-1 招股书是个有意思的文件。它有一节叫 Risk Factors，公司必须在里面列出可能影响经营的风险。这个章节的写法行业里有惯例——把所有可能被 SEC 抓的、可能被原告律师抓的事情都写一遍，写得越保守越好。

Anthropic 的 Risk Factors 这一节会写什么。

肯定会写"AI 模型可能产生偏见或错误内容，可能被恶意使用"——这是 OpenAI、Microsoft、Google 招股书里都有的标准条款。

肯定会写"AI 训练涉及版权争议"——这是 NYT 诉 OpenAI 之后所有 AI 公司都要写的。

肯定会写"Mythos 等高级模型的能力可能被用于网络攻击"——他们已经在 red.anthropic.com 这种半官方页面上写了，IPO 时改写成法律语言。

会写"我们当前持有约数千个未公开披露的高危漏洞，相关披露时间表受 coordinated disclosure 流程约束，期间任何意外泄露可能引发全球关键基础设施的安全事故"吗？

不知道。

但这件事是真实存在的。Anthropic 自己的官网上写了"Over 99% of the vulnerabilities Mythos has found have not yet been patched"。这一行字在 IPO 之前是 marketing copy，在 IPO 之后会被 SEC 审计师抓出来要求重新表述。重新表述的版本可能会出现在 Risk Factors 里，也可能被律师团队压成更柔软的措辞。但不管怎么写，那笔库存的存在不会消失。

进了 S&P 500 之后还有别的东西要发生。

被动指数基金会被动持有 Anthropic 股票。Vanguard、BlackRock、State Street 三家加起来管 20 多万亿美金资产，规则要求它们按指数权重买入所有成分股。一旦 Anthropic 入选，每一只追踪 S&P 500 的 ETF 都要被动持有它。

这意味着每一只美国 401k 退休计划的默认配置里，都会按比例持有"那家持有未披露 0day 库存的 AI 公司"。

你的退休金会变成这家公司的股东。你不需要同意，你的雇主选了 default fund 就够了。

回头看 Mythos Preview 4 月 7 日那次发布。当时的口径是"我们暂不开放给公众使用"。这听起来像是负责任的姿态——能力太强先压一压。但今天看，它不是压一压，是把使用权切给了一份名单内的客户、把发现物入库给了一家公司。

公众这个角色，从"客户"被请出去之后，没有进任何角色。

不是观众，因为公开披露的内容是 1%。

不是受益人，因为修复路径要走 CVD，长尾 OSS 接不住。

不是股东，因为还没 IPO；IPO 之后是被动持有，不是主动持有。

不是知情者，因为 99% 的库存按定义是 undisclosed。

这个角色的名字叫**库存的标的**。

你的浏览器、你的操作系统、你的 npm 包、你的银行 app、你的医院信息系统——它们里面如果有 Mythos 找到的漏洞，你不知道这个漏洞存在，你不知道它什么时候被修，你不知道在它被修之前谁能看到它。

你只知道一件事：它有个价格。这个价格被打包进了 Anthropic 9000 亿美金估值里。

至于这个价格折现回来对应到你头上是多少风险——招股书会用律师的语言告诉你，写在 Risk Factors 第十几条上。

但 271 这个数字，已经把那一行字预演了一遍。

就这。

## 数据来源

- [Claude Mythos Preview — red.anthropic.com (2026-04-07)](https://red.anthropic.com/2026/mythos-preview/)
- [Project Glasswing — Anthropic (2026-04-07)](https://www.anthropic.com/glasswing)
- [The zero-days are numbered — Mozilla Blog (2026-04)](https://blog.mozilla.org/en/privacy-security/ai-security-zero-day-vulnerabilities/)
- [Anthropic in talks to raise funds at $900 billion valuation, higher than OpenAI — CNBC (2026-04-29)](https://www.cnbc.com/2026/04/29/anthropic-weighs-raising-funds-at-900b-valuation-topping-openai.html)
- [Sources: Anthropic potential $900B+ valuation round could happen within 2 weeks — TechCrunch (2026-04-30)](https://techcrunch.com/2026/04/30/anthropic-potential-900b-valuation-round-could-happen-within-two-weeks/)
- [NSA using Anthropic's Mythos despite Defense Department blacklist — Axios (2026-04-19)](https://www.axios.com/2026/04/19/nsa-anthropic-mythos-pentagon)
- [Mythos autonomously exploited vulnerabilities that survived 27 years of human review — VentureBeat (2026-04)](https://venturebeat.com/security/mythos-detection-ceiling-security-teams-new-playbook)
- [Anthropic's latest AI model identifies thousands of zero-day vulnerabilities — Tom's Hardware (2026-04)](https://www.tomshardware.com/tech-industry/artificial-intelligence/anthropics-latest-ai-model-identifies-thousands-of-zero-day-vulnerabilities-in-every-major-operating-system-and-every-major-web-browser-claude-mythos-preview-sparks-race-to-fix-critical-bugs-some-unpatched-for-decades)
- [What Anthropic's Mythos Means for the Future of Cybersecurity — Schneier on Security (2026-04)](https://www.schneier.com/blog/archives/2026/04/what-anthropics-mythos-means-for-the-future-of-cybersecurity.html)
- [Pentagon tech chief says Anthropic is still blacklisted, but Mythos is a separate issue — CNBC (2026-05-01)](https://www.cnbc.com/2026/05/01/pentagon-anthropic-blacklist-mythos-michael.html)
- [New frontier of AI forces Trump's heavy hand — Axios (2026-05-05)](https://www.axios.com/2026/05/05/trump-anthropic-ai-regulation-mythos-cyber)
