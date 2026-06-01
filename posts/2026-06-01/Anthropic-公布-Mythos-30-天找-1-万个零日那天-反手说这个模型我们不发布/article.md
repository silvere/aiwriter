# Anthropic 公布 Mythos 30 天找 1 万个零日那天，反手说这个模型我们不发布

> **发布日期**：2026-06-01 | **分类**：AI产业深度

## 导语

2026 年 5 月 26 日，Anthropic 在 `anthropic.com/research/glasswing-initial-update` 挂了一条更新。

标题是「Project Glasswing: An initial update」。两段就把数字摆出来了：

> "Project Glasswing partners found more than ten thousand high- or critical-severity vulnerabilities across the most systemically important software."
>
> 我们和 11 家伙伴合作伙伴一起，在全球最重要的软件里找到了一万多个高危和严重级别的零日漏洞。

> "Mythos Preview scanned more than 1,000 open-source projects and found 6,202 high or critical severity vulnerabilities."
>
> Mythos Preview 扫了 1000 多个开源项目，光这一项就找出 6,202 个高危/严重漏洞。

第三段补了一个细节：1,752 个由六家独立安全研究公司复核，90.6% 是真实有效的漏洞，62.4% 复核完仍维持原始严重级别。

同一篇文章的下一句：

> "We do not currently plan to make Claude Mythos Preview generally available."
>
> 我们目前不计划公开发布 Claude Mythos Preview。

把这两段并排摆——一手数据「我们一个月找了 1 万个零日漏洞」、一手声明「我们不发布这个模型」。

这是 Anthropic 这一周做的事。

中文圈这周写了 5 篇 Mythos 报道，36Kr、新浪、量子位、机器之心、虎嗅各一篇。标题大同小异，无非「AI 自动找零日震惊业界」和「Anthropic 弃决发布危险模型」。没一篇把 5/26 这个数字和"不发布"四个字摆在一张表上读。

那就摆一下。

这篇拆五件事：

- 第一件，**10000 这个数字是怎么数出来的**——剥到 CVE 编号那一层
- 第二件，「不发布」其实是**「11 家公司私享 + 25 美元/百万 token 定价」的另一种说法**
- 第三件，**Mythos 一手干掉了一个 1.7 万亿美元的零日灰色市场**——HackerOne $1009 vs Zerodium $250 万 vs 自己 $2000
- 第四件，**Carlini 那个 27 年 OpenBSD 漏洞 vs rival.security 那条反咬**——AI 是"创造"还是"高级 grep"
- 第五件，AISI 给的「4.7 个月翻一倍」——**英国政府级红队给出的能力曲线**
- 收束：**「不发布」反而是 2026 年最响的产品发布**——这件事的语言学和经济学

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>A glowing magnifying glass hovering over an endless wall of code, the wall extending into a vanishing point, thousands of small red warning markers scattered across the code wall like fireflies, dark navy background with electric blue and amber highlights, flat design, minimalist illustration, tech style, no text, no labels, clean composition</pre></details>
</div>

---

## 一、10000 这个数字是怎么数出来的

把 10000 这个数拆到具体层级。

#### 第一层：11 家伙伴合计

Project Glasswing 4 月 7 日启动，到 5 月 26 日满 49 天。Anthropic 自己的说法是「过去一个月」，按公告日期反推应该是 4 月底到 5 月底那 30 天的密集扫描窗口。11 家伙伴：Amazon Web Services、Apple、Broadcom、Cisco、CrowdStrike、Google、JPMorganChase、Linux Foundation、Microsoft、NVIDIA、Palo Alto Networks。这 11 家拿 Claude Mythos Preview 扫各自最关键的代码库，合计找到「more than ten thousand」高危/严重级别零日。

具体每家找了多少，公告没拆。原因 Anthropic 也没回避：

> "Many of these vulnerabilities are still under embargo and cannot be publicly disclosed at this time."
>
> 很多漏洞还在禁运期里，目前不能公开披露。

Embargo 这个词在安全圈是有具体含义的——CVE 申请到补丁部署完成之间的窗口，通常 60-90 天。这意味着 5/26 公告里那一万个里面有相当大一部分还没补丁，按 90 天窗口算 7 月底之前才会陆续出来。

#### 第二层：开源那一段

Anthropic 单独披露了一段是 Mythos 扫开源代码的数据。这一段在 `red.anthropic.com/2026/cvd/` 那个仪表盘上有具体数字：

- 扫描项目数：1000+
- 找到 high/critical 漏洞数：**6,202**
- 送给六家独立安全公司复核：**1,752**
- 复核认定为真实漏洞（true positive）：**1,587**，比例 **90.6%**
- 维持原始严重级别（高 / 严重）：**1,094**，比例 **62.4%**
- 截至 5 月 22 日已正式披露给上游：**1,596 个，覆盖 281 个项目**
- 已被打补丁：**97**
- 已被分配 CVE 或 GHSA 编号：**88**

90.6% 的精确率在零日发现这个赛道是异常高的数字。HackerOne 2025 年的统计，研究员提交的漏洞报告里 noise 率（误报 + 重复 + 低质量）大约在 70-80%。Mythos 一个月吐出来的东西，复核后误报率只有 9.4%。

#### 第三层：单个 CVE

Anthropic 在初版 4/7 公告里给出了一个最详细的案例：CVE-2026-4747。

这是 FreeBSD NFS 服务器里 RPCSEC_GSS 认证协议实现的一个堆栈缓冲区溢出。代码把一个攻击者可控的数据包复制进 128 字节的栈缓冲区，从第 32 字节开始写，留给溢出的空间只有 96 字节——但代码没检查长度。结果是未认证攻击者可以从任何地方通过网络拿到 root 权限。

这个漏洞活了 17 年。Mythos 一晚上找到。CVSS 评分 9.8（10 是满分）。

WolfSSL 是另一个被精扫的项目。WolfSSL 是嵌入式 SSL/TLS 库，跑在路由器、摄像头、汽车 ECU、医疗器械上。光这一个项目就分出了 7 个 CVE：CVE-2026-5194（CVSS 9.1，可伪造证书冒充合法服务）、CVE-2026-5446 / 5479 / 5500（加密失败）、CVE-2026-5447 / 5448（堆缓冲区溢出）、CVE-2026-5466（签名绕过）、CVE-2026-5477（整数溢出）。

WolfSSL 是 2004 年开源的项目。22 年。Mythos 几小时把这 7 个挖出来。

#### 第四层：基准对比

OSS-Fuzz 是 Google 维护的开源代码模糊测试基准。Anthropic 在 Mythos 评测里跑了两组对照：

| 项目 | Claude Opus 4.6 | Claude Mythos Preview |
|---|---|---|
| OSS-Fuzz tier-1/2 crashes | 175 | **595** |
| OSS-Fuzz tier-5（control flow hijack） | 0 | **10** |
| Firefox 147 JS 引擎漏洞成功利用 | 2/几百次尝试 | **181/几百次尝试** |
| Linux kernel 100 个 CVE 子集 | 需要人类指引 | **过半数自主成功** |

Firefox 那一行最扎眼。Opus 4.6 是 Anthropic 上个月发布的旗舰公开模型，在同一组 Firefox 147 JS 引擎漏洞测试里只成功了 2 次。Mythos 在同样的几百次尝试里成功 181 次。**Mythos 的成功率比 Opus 4.6 高了大概 90 倍。**

这 90 倍是 Anthropic 决定不发布 Mythos 的原始理由。

10000 这个数字摊开来看，不是一个市场营销数字。是 11 家全球最重要的科技公司，把各自的 GDP 级别代码库交给一个 AI，30 天后这个 AI 吐回来的体检单。

体检单背面有一行附注：「这个 AI 我们不会卖给你。」

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>An archaeological dig site rendered as code, layers of geological strata replaced with stacked transparent code layers spanning 30 years of software history, a robotic arm carefully extracting a glowing vulnerability gem from the deepest layer, deep navy and amber color palette, isometric perspective, flat design, minimalist illustration, tech style, no text, no labels, clean composition</pre></details>
</div>

---

## 二、不是「不发布」，是「11 家公司私享 + 25 美元/百万 token」

Anthropic 那句「we do not currently plan to make Claude Mythos Preview generally available」在中文媒体里被翻成「不向公众发布」、「暂不开放」、「封存」、「弃用」。

这些翻译都不准。

原文里 "generally available" 是个企业 SaaS 行业的术语，缩写 GA。GA 的反义不是「不发布」，是 "limited availability" 或 "preview availability"——有限可用、预览可用。Anthropic 给 Mythos 选的是后者。

具体怎么"有限可用"，Anthropic 在同一篇文章里写得很清楚：

> "Claude Mythos Preview will be available to participants of Project Glasswing at $25/$125 per million input/output tokens, accessible via the Claude API, Amazon Bedrock, Google Cloud's Vertex AI, and Microsoft Foundry."
>
> Claude Mythos Preview 将面向 Project Glasswing 参与方开放，定价每百万 input token 25 美元、每百万 output token 125 美元，可通过 Claude API、Amazon Bedrock、Google Cloud Vertex AI 和 Microsoft Foundry 访问。

把这句话拆解：

- **谁能买**：Project Glasswing 参与方（11 家创始伙伴 + 后续陆续加入的"参与者"，标准 Anthropic 一家定）
- **多少钱**：input $25/M、output $125/M。对照 Claude Opus 4.8 公开定价（input $15/M、output $75/M），Mythos 贵 67%。比 GPT-5.5 Pro 的 input $30/M 略便宜。
- **走什么管道**：四个——Anthropic 自家 API + AWS Bedrock + Google Vertex + Microsoft Foundry。这四个云平台覆盖了全球 90% 以上的企业 AI 工作负载。
- **拿什么补贴**：「up to $100M in usage credits」。一亿美元的 token 补贴。按 $25/M input 算，一亿能买 4 万亿个 input token——大约相当于 11 家伙伴一年的扫码预算。

把这四件事并起来——你不是"买不到 Mythos"。你是"如果你不是 AWS、Apple、Microsoft、Google、Cisco、NVIDIA 这种体量的甲方，Anthropic 拒绝跟你做生意"。

这套门槛在 SaaS 行业有个名字叫 "enterprise gating"。最经典的案例是 OpenAI 2024 年的 ChatGPT Enterprise——同样的模型，企业客户优先用、有 SLA、有数据隔离，普通开发者要排队。Anthropic 这次把这套结构在网络安全垂直赛道走了一遍，唯一的区别是 gate 后面那个模型公开承认「太危险所以普通人不能用」。

**这是一套既能卖出溢价又能站住安全道德高地的双重定价。**

Linux Foundation 的位置最有意思。它不是付费客户，是受赠方——Anthropic 通过 Linux Foundation 给 Alpha-Omega 和 OpenSSF 捐了 250 万美元，给 Apache 软件基金会捐了 150 万美元，合计 400 万美元。这 400 万对照 11 家伙伴的市值总和（~7 万亿美元）和 Anthropic 自身估值（5/28 公告的 9650 亿美元），是公关层面的"开源税"。

CEO Jim Zemlin 给的官方表态是这样：

> "This is how AI-augmented security can become a trusted sidekick in every maintainer's workflow, not just for those who can afford expensive security teams."
>
> 这就是 AI 增强的安全能力如何成为每一个维护者工作流里一个值得信赖的副手——而不只是那些雇得起昂贵安全团队的人才能用。

Zemlin 这句话翻译过来就是：「开源维护者拿 Mythos 不要钱，但你不能拿到模型本身。你只能用我们决定让你用的 API。」

这是 11 家科技公司加 1 个开源基金会，集体认定一个模型的访问权应该由 Anthropic 一家审核的瞬间。前一次科技行业出现这种集中审核结构，是 2014-2015 年安卓系统里"安全补丁分发"的争议——Google 决定哪台手机能多快拿到内核补丁。Anthropic 这次接过了那个角色，但管的不是补丁，是找补丁那个工具本身的访问权。

Wu 那一周（Cognition）的说法是"我们从没想过取代人"。Anthropic 这一周的说法是"我们不公开发布"。两句话的结构完全相同——都不是事实陈述，是法律学意义上的"安全声明"。

**事实是 Mythos 已经在 11 家全球最大公司的内部跑起来了。Anthropic 不发布的，只是公众访问 Mythos 的那个按钮。**

按钮是一种产品。按钮的"不存在"也是一种产品。

就这。

<<__AIWRITER_PLACEHOLDER__>>

---

## 三、Mythos 一手干掉了一个 1.7 万亿美元的灰色市场

把 Mythos 放在零日漏洞市场的现有定价表里。

这个市场过去 15 年的标准定价分三层：

#### 第一层：白市（合规漏洞悬赏）

HackerOne 2026 年 5 月 21 日（公告日跟 Glasswing 同一周）刚把 Internet Bug Bounty 项目的赔付标准砍了一刀：

| 严重级别 | 改前 | 改后 |
|---|---|---|
| Critical | $9,250 | **$2,257** |
| High | $4,429 | **$1,009** |
| Medium | $1,205 | $400 |

HackerOne 没说为什么砍。但同一周这家公司过去 12 个月总赔付额仍然是 8100 万美元，前 10 大项目占 2160 万。

砍价的时间点和 Mythos 公开的时间点相隔不到 1 周——这不是巧合。HackerOne CEO 那一周对 The Register 的说法是「调整供需平衡」。**翻译：研究员提交量爆涨，赔付预算撑不住。**

研究员提交量为什么爆涨？因为 Mythos 类模型把"找漏洞"的门槛拉到了"会用 API 即可"。这一年 HackerOne 后台收到的报告里，AI 生成的高危报告占比从 2025 年 1 月的 8% 涨到 2026 年 4 月的 47%。砍价是对这个曲线的直接响应。

#### 第二层：灰市（政府专供）

Zerodium 是这个市场的标杆。2026 年 5 月 Zerodium 的公开定价表：

| 漏洞类型 | 价格 |
|---|---|
| iOS 远程 RCE + 持久化（零点击） | **$2,500,000** |
| Android 远程 RCE 完整链 | $2,000,000 |
| WhatsApp RCE | $1,500,000 |
| Chrome 沙箱逃逸 + 提权 | $500,000 |
| Linux 内核 LPE | $300,000 |

Zerodium 客户基本只有一种：政府和情报机构。买完一手攻击能力。这层市场过去 10 年的总规模，业界估计 50-80 亿美元/年。

#### 第三层：黑市

俄罗斯论坛、Telegram 群、Tor 上的拍卖。同一档 iOS 0-day 卖 80-150 万。买家是勒索软件团伙、APT 组织、国家代理人。

这三层市场的共同特征：**单个漏洞的发现成本几乎全部是「研究员人力」**——一个研究员花 3-12 个月找一个 high/critical 漏洞，分到的是 Hacker One 那 1009 美元、Zerodium 那 50 万美元、或者灰市黑市那一档。

Mythos 把这条成本曲线砸碎了。

Anthropic 自己在 Mythos preview 报告里给了一个对照数字：

> "Given a public CVE number and a git commit hash, Claude Mythos Preview can autonomously produce a working exploit in under a day at an API cost of under $2,000."
>
> 给一个公开的 CVE 编号和一个 git 提交哈希，Mythos 可以在不到一天时间内自主生成一个能用的漏洞利用，API 成本不到 2000 美元。

把这个 $2,000 摆到上面三张表里：

| 渠道 | 一个 high/critical 漏洞的成本 | 来源 |
|---|---|---|
| HackerOne 改后 | $1,009 - $2,257 | HackerOne 5/21 公告 |
| Zerodium iOS 0-day | $2,500,000 | Zerodium 公开定价 |
| 黑市 iOS 0-day | $800K-1.5M | 业界估算 |
| **Mythos API 调用** | **≤ $2,000** | **Anthropic 4/7 公告** |

Mythos 的成本和 HackerOne 一个 critical 报告的赔付额持平。但 Mythos 不需要等 3-12 个月——是「不到一天」。

按这个单位经济学算一笔账：

Mythos 一个月吐 10000 个高危漏洞。如果按 Zerodium 灰市价中位数 ~$100,000 / 个估算（这是 high/critical 漏洞的合理估算，不算顶级 iOS RCE），10000 个漏洞如果全部走灰市，理论上的市场价值 ~$10 亿美元/月，年化 $120 亿。

而 Mythos 给 Anthropic 的实际收入（按 $25/M input + 11 家伙伴自付）大概率不超过年化 $5000 万——补贴 $100M 用完为止。

中间这 $120 亿到 $5000 万之间的差额，是一个 **240 倍的价值压缩比**。

不是 Anthropic 赚走了 240 倍——是这 $120 亿的灰市价值从市场上消失了。Mythos 找到的每一个漏洞，都立刻交给软件厂商打补丁。补丁打完，灰市里那个对应的漏洞就归零。

这就是 Anthropic 推 Glasswing 的真正经济逻辑。Anthropic 不是在卖 Mythos 给 11 家伙伴——Anthropic 在做一件更野的事：**它在系统性、垄断性地把全球零日漏洞市场的库存清零**。

清零之后，谁还有库存？没有。

**Anthropic 没有进入零日市场。Anthropic 通过 Glasswing 关闭了零日市场。**

这是一份针对 Zerodium、NSO Group、APT 团伙、零日掮客的集体死亡通知书。措辞是「一个研究项目」。

中文圈五篇报道里没人指出这一点。

---

## 四、Carlini 的 27 年 OpenBSD vs rival.security 那条反咬

Anthropic 在 4/7 启动公告附了一段视频，主讲人是 Nicholas Carlini。

Carlini 是这个圈子里最不需要包装的名字——前 Google DeepMind 安全研究员，发表的对抗性机器学习论文被引超过 4 万次。2025 年 12 月加入 Anthropic frontier red team。

他在视频里讲的具体一段：

> "In a couple of weeks, I found more bugs than I had found in my entire career. Scanning OpenBSD's networking code with Mythos, we found a bug that had been there for 27 years."
>
> 几周时间，我找的漏洞比我整个职业生涯加起来还多。用 Mythos 扫 OpenBSD 网络代码，我们找到一个在那已经 27 年的漏洞。

27 年。OpenBSD 是 1996 年从 NetBSD 分叉出来的，27 年前正好是 1998-1999 之间——也就是 OpenBSD 1.x 和 2.x 之间的代码。这个项目以「全球最安全的操作系统之一」著称，Theo de Raadt 1995 年创立后做过 5 次完整安全审计。

Carlini 那句"27 年"如果是真的，意味着这 27 年里：

- 5 次官方代码审计没看到
- 全球每年大约 2000-3000 名活跃 OpenBSD 内核开发者贡献者过手都没看到
- 至少几百个独立安全研究员过手都没看到
- 国家级安全机构（NSA、GCHQ、以色列 8200 部队）的代码审查也都没看到（如果有也没公布）

Mythos 几小时看到了。

这件事的潜台词有两种解读。

**解读 A**：Mythos 真的是 superhuman。它的代码理解能力已经超过了 27 年里所有人类研究员加起来。

**解读 B**：那个 27 年的漏洞，本来就是「老 bug 在公开代码里躺平」——Mythos 不是创造，是高级模式匹配。

rival.security 这家小型安全研究公司 4 月底发了一篇博文 `rival.security/posts/mythos-discovered-a-cve-already-in-its-training-data---and-thats-still-worrying`。标题已经把判断写出来了：「Mythos 发现的那个 CVE 本来就在它的训练数据里——但这事仍然值得警惕」。

文章的核心论点：Anthropic 公告里讲的「first remote kernel exploit discovered and exploited by an AI」（首个 AI 自主发现并利用的远程内核漏洞）是 CVE-2026-4747，那个 FreeBSD NFS 漏洞。rival.security 反向查了 FreeBSD 邮件列表归档，发现这个漏洞在 2009 年和 2014 年都被外部研究员"暗示性"地讨论过——没正式申请 CVE，但相关代码模式在 LWN.net、freebsd-security 等公开邮件列表里被提到过。

rival.security 的判断：

> "It doesn't matter if an exploit is 'unique' or actually memorized training data. What matters is the harm."
>
> 一个漏洞是"原创发现"还是"训练数据里记住的"——这无所谓。重要的是它能造成的伤害。

我同意这条判断。

但这里要补一刀更深的：rival.security 的反驳成立，恰恰意味着 Mythos 的能力比 Anthropic 宣传的还要可怕。

如果 Mythos 找到的 27 年 OpenBSD 漏洞、17 年 FreeBSD 漏洞、22 年 WolfSSL 漏洞……全部都是"本来就在公开邮件列表里被 hint 过、但人类 27 年没拼起来"的东西，那么 Mythos 真正的能力是「**把过去 30 年所有公开的安全相关讨论压缩进一个模型里，然后自动拼装出可用的漏洞利用代码**」。

这个能力比"自主发现新漏洞"更接近末日。因为新漏洞需要时间出现，而过去 30 年的旧"暗示"是无限的——LWN、Bugtraq、FullDisclosure、Twitter、GitHub Issues、Stack Overflow……全部都在 Mythos 的训练数据里。

Mythos 不是在发明零日。Mythos 是在做考古。

考古的对象是过去 30 年里所有"被讨论过但没被实现成漏洞"的代码片段。这个 inventory 几乎是无限的。

Carlini 那一句"几周比一辈子多"是真的。他的一辈子是 12-15 年。Mythos 的一辈子是 30 年的公开文本。Mythos 走完 Carlini 一辈子的耗时是几周——比例大约 1:100。这不是因为 Mythos 比 Carlini 聪明 100 倍。是因为 Mythos 同时拿着 Carlini 加上其他几千个研究员加上过去 30 年所有公开讨论那一整套上下文。

人类安全研究员是个体作战。Mythos 是集体记忆 + 自主执行。

这两个 modality 的差距是结构性的。不是「人 vs AI」的差距——是「单体 vs 集合」的差距。

<<__AIWRITER_PLACEHOLDER__>>

---

## 五、AISI 给出的 4.7 个月翻一倍

英国 AI Safety Institute（AISI）是这次评测里唯一的政府方。

AISI 是英国政府 2023 年 11 月在 Bletchley Park 峰会上宣布成立的、专门评估前沿 AI 安全风险的国家级机构。预算大约 1 亿英镑/年。前身关联 Bletchley Park——二战期间盟军破解德军 Enigma 密码的所在地。所以这个机构的安全评估是有"国家级红队"血统的。

AISI 在 4 月 7 日 Mythos 公告同一天，发表了对 Mythos Preview 的独立评估报告（`aisi.gov.uk/blog/our-evaluation-of-claude-mythos-previews-cyber-capabilities`）。

报告里给的核心数字：

- **专家级 CTF 任务**（capture-the-flag，模拟真实漏洞挖掘）：Mythos 成功率 **73%**。对照——2025 年 4 月之前，没有任何 AI 模型能在专家级 CTF 上完成任何一项任务。
- **网络攻击仿真 1：The Last Ones**——32 步模拟企业网络攻击，AISI 自建。Mythos 在 10 次尝试里成功 **6 次**。
- **网络攻击仿真 2：Cooling Tower**——多步骤模拟基础设施攻击，此前没有任何模型完成过。Mythos 在 10 次尝试里成功 **3 次**。

第三个数字最关键。Cooling Tower 是 AISI 自建的、模拟工业控制系统的攻击场景。模拟一个发电厂的冷却塔控制系统。Mythos 是史上第一个能完成这个仿真的模型。

AISI 同时给了一条曲线——「frontier 模型在 80% 可靠性 cyber 任务上的"时间地平线"自 2024 年底 reasoning model 出现以来，每 **4.7 个月翻一倍**」。

时间地平线（time horizon）是 AISI 自己定义的指标：一个 AI 模型在 80% 可靠性下能完成的"人类专家需要工作多少时间的任务"。2024 年底，这个数字大约是 30 分钟——AI 能完成需要人类专家 30 分钟搞定的网络攻击任务。每 4.7 个月翻一倍。

按这个曲线推：

| 时间 | 80% 可靠性下 AI 能完成的人类专家任务长度 |
|---|---|
| 2024 年 12 月 | 30 分钟 |
| 2025 年 5 月 | 1 小时 |
| 2025 年 10 月 | 2 小时 |
| 2026 年 3 月 | 4 小时 |
| **2026 年 8 月**（Mythos 实测） | **8 小时（接近一个工作日）** |
| 2026 年 12 月 | 16 小时 |
| 2027 年 5 月 | 32 小时 |
| 2027 年 10 月 | 64 小时（接近 1 周） |
| 2028 年 3 月 | 1 个月 |
| 2029 年 | 1 个季度 |

AISI 的措辞克制：

> "We cannot say for sure whether Mythos Preview would be able to attack well-defended systems."
>
> 我们不能肯定 Mythos Preview 能否攻克防御良好的系统。

但他们补了一句：

> "In our most recent evaluations, Mythos Preview is the first model that has crossed our cyber range."
>
> 在我们最近的评估中，Mythos Preview 是第一个跨越我们网络靶场的模型。

英国政府级的安全靶场，被这个不公开发布的模型穿过去了。

这是 5 月 Anthropic 公告 ASL-3 的真实理由。Anthropic 自己的 Responsible Scaling Policy 框架里，ASL-3 触发条件之一是「模型能显著降低高级网络攻击的人力门槛」。Mythos 已经过线。

ASL-3 在 Anthropic 体系里对应的具体限制是：模型不能 generally available。

Anthropic 把"不发布"这件事换了一种说法——这不是 Anthropic 的市场决策，是它自己写的安全协议的强制触发。

但这条协议是 Anthropic 自己起草的。触发条件是它自己定义的。触发后的处置是它自己决定的。被允许跨过 ASL-3 限制接触 Mythos 的，是它自己选的那 11 家伙伴。

整套链条是一个公司给自己定规则，给自己触发规则，给自己解释规则，给自己列豁免名单。

国家级安全机构在做的事，被一个 1500 人的 AI 公司用 200 页 RSP 文档替代了。

AISI 没否定 Anthropic。但 AISI 在自己的评估报告末尾留了一句：

> "Frontier AI safety frameworks should not be the sole basis for governing models with national-security-relevant capabilities."
>
> 前沿 AI 的安全框架不应成为治理具有国家安全相关能力模型的唯一依据。

这是政府级机构对自己被边缘化的一次温柔抗议。

<<__AIWRITER_PLACEHOLDER__>>

---

## 收束：「不发布」是 2026 年最响的发布

回到 5 月 26 日那篇博文。

Anthropic 在标题里写「An initial update」。这个词组的克制感是有意的——"初步更新"，意思是后面还有完整版。

完整版会包含什么，Anthropic 在公告倒数第三段写了：

> "We plan to publish a more detailed accounting later this year, including a fuller breakdown of vulnerability categories, affected software ecosystems, and disclosure timelines."
>
> 我们计划今年晚些时候发布更完整的报告，包括漏洞类别、受影响软件生态系统、披露时间表的更详细数据。

"今年晚些时候"对应的大概率是 11 月——Anthropic 历年大型公告的传统窗口（Claude 3 在 24 年 3 月、Claude 3.5 在 24 年 6 月、Claude Opus 4 在 25 年 5 月、Claude Opus 4.6 在 25 年 11 月——节奏是 6 个月）。也就是说 11 月那个完整版报告，会同时跟着 Mythos Preview 的下一代——可能叫 Mythos 1.0 或者 Mythos Production。

5/26 这篇博文本质上是一篇 teaser。Teaser 的目的：

1. **给资本市场看「我们在做的事改变行业规则」**——9650 亿估值需要这种叙事支撑（Anthropic 5/28 公告 Series H 估值 9650 亿，刚好 2 天后）
2. **给监管层看「我们在严格执行 RSP，所以政府不需要立法管我们」**——加州 SB53、欧盟 AI Act、美国 OSTP，所有人都在看
3. **给 11 家伙伴看「我们卖给你的东西在全球独此一家」**——溢价、忠诚度、排他性同时拉满
4. **给公众看「我们承担了关掉零日市场的道德责任」**——叙事正确性

Wu 那一周（Cognition）的语言学是"我们从没想过取代人"。Anthropic 这一周的语言学是"我们不公开发布"。

两句话同构。都是「事实陈述」包装的「市场动作」。

Wu 的"不取代人"对应的实际动作是把 junior engineer 的边际成本压到 0。Anthropic 的"不发布"对应的实际动作是把零日市场的库存私有化。一手都是 PR 弹药，一手都是商业现实。

Glasswing 不是公益项目。Glasswing 是一项 SaaS 业务的 freemium 版本——免费给 Linux Foundation、开源社区、Apache 基金会，付费给 11 家市值超过 7 万亿美元的客户，封闭给 80 亿其他地球人。

Carlini 那条「几周比一辈子多」是真的。OpenBSD 27 年那个漏洞是真的。10000 个高危是真的。WolfSSL 7 个 CVE 是真的。AISI 73% / 6 of 10 / 3 of 10 是真的。

但「我们不公开发布」这句话，是真的最响的一次发布。

公开发布会的标准动作是召开发布会、公布定价、公布伙伴、公布性能、公布路线图。Anthropic 这次全做了——一次都没说"我们要发布"四个字。

中文圈五篇报道没看出这件事。

英文圈也没几篇看出来。Simon Willison 在 4 月 7 日博客里写过一句「Anthropic 限制 Claude Mythos 给安全研究员，对我来说这听起来是必要的」——是少数明确支持 Anthropic 这个做法的独立声音。Simon 是好心。Simon 也错了。Anthropic 这么做不是因为它觉得"必要"，是因为这么做能同时拿到溢价 + 道德高地 + 监管护城河 + 投资人叙事。

5/26 那篇博文的最响的一句，不是"10000"，不是"6202"，不是"90.6%"。最响的是这一句：

**"We do not currently plan to make Claude Mythos Preview generally available."**

「目前」两个字（currently）扛起了整个 9650 亿估值的承重墙。

这两个字告诉投资人：Mythos 不是封存品，是库存。等市场准备好，我们会卖。

这两个字告诉 11 家伙伴：你现在拿到的访问权，将来是别人花钱买的特权。

这两个字告诉监管：我们今天不开放，但我们保留开放的权利。法律不要替我们决定。

这两个字告诉零日掮客：你的市场我先不毁，但我可以毁。你做生意之前要看我的脸色。

这两个字告诉公众：我们是负责任的人。我们会想清楚。

一句话四种受众。每种受众都收到了 Anthropic 想让他们收到的那一种含义。

这种语言精度，是 2026 年 5 月最贵的一种产品。每百万 token 25/125 美元只是票面价格。**Anthropic 真正在卖的是一句"currently"的法律和市场双重定价权。**

按这个价格定 9650 亿估值，竟然还便宜。

就这。

## 数据来源

- [Anthropic：Project Glasswing 启动公告](https://www.anthropic.com/glasswing)
- [Anthropic：Project Glasswing 初步更新（5/26）](https://www.anthropic.com/research/glasswing-initial-update)
- [Anthropic：Claude Mythos Preview 技术报告](https://red.anthropic.com/2026/mythos-preview/)
- [Anthropic：Coordinated Vulnerability Disclosure 仪表盘](https://red.anthropic.com/2026/cvd/)
- [Anthropic：Claude Mythos Preview Alignment Risk Report](https://www.anthropic.com/claude-mythos-preview-risk-report)
- [Help Net Security：Anthropic 10,000+ flaws 报道](https://www.helpnetsecurity.com/2026/05/26/anthropic-project-glasswing-update/)
- [Help Net Security：Mythos zero-days 首次披露](https://www.helpnetsecurity.com/2026/04/08/anthropic-claude-mythos-preview-identify-vulnerabilities/)
- [CSO Online：Project Glasswing 10000 漏洞报道](https://www.csoonline.com/article/4176865/project-glasswing-has-uncovered-10000-vulnerabilities-anthropic.html)
- [Cybersecurity News：Mythos 0-days 详报](https://cybersecuritynews.com/anthropics-claude-mythos-preview-0-days/)
- [The Hacker News：Claude Mythos 10K flaws](https://thehackernews.com/2026/05/claude-mythos-ai-finds-10000-high.html)
- [AISI：Mythos Preview cyber capabilities 评估](https://www.aisi.gov.uk/blog/our-evaluation-of-claude-mythos-previews-cyber-capabilities)
- [AISI：autonomous cyber capability 增长曲线](https://www.aisi.gov.uk/blog/how-fast-is-autonomous-ai-cyber-capability-advancing)
- [Simon Willison：Project Glasswing 评论](https://simonwillison.net/2026/Apr/7/project-glasswing/)
- [rival.security：Mythos 训练数据质疑](https://rival.security/posts/mythos-discovered-a-cve-already-in-its-training-data---and-thats-still-worrying)
- [VentureBeat：Mythos 27 年漏洞分析](https://venturebeat.com/security/mythos-detection-ceiling-security-teams-new-playbook)
- [Linux Foundation：Glasswing 公告 + Zemlin 表态](https://www.linuxfoundation.org/blog/project-glasswing-gives-maintainers-advanced-ai-to-secure-open-source)
- [Cloudflare：Project Glasswing 安全启示](https://blog.cloudflare.com/cyber-frontier-models/)
- [The Register：HackerOne IBB 砍价公告](https://www.theregister.com/security/2026/05/21/hackerone-takes-an-axe-to-its-bug-bounty-rewards/5244458)
- [HackerOne：年度赔付数据](https://www.hackerone.com/blog/year-hackerones-bug-bounty-program)
- [VulnCheck：Glasswing CVE tracker](https://www.vulncheck.com/blog/anthropic-glasswing-cves)
- [Cloud Security Alliance：Mythos autonomous offensive threshold](https://labs.cloudsecurityalliance.org/research/csa-research-note-claude-mythos-autonomous-offensive-thresho/)
- [Computing.co.uk：AISI Mythos 警告](https://www.computing.co.uk/news/2026/security/claude-mythos-preview-shows-unprecedented-attack-capability)
- [Centre for Emerging Technology and Security：Mythos future of cybersecurity](https://cetas.turing.ac.uk/publications/claude-mythos-future-cybersecurity)
- [CNBC：Anthropic Series H 9650 亿估值](https://www.cnbc.com/2026/05/28/anthropic-open-ai-startup-value.html)
