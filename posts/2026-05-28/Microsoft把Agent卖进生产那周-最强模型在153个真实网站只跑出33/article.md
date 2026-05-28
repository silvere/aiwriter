# Microsoft 把 Computer-Use Agent 卖进生产那周，最强模型在 153 个真实网站上只跑出 33.3%

> **发布日期**：2026-05-28 | **分类**：AI产业深度

## 导语

2026 年 5 月 13 日，Microsoft Tech Community 的 Copilot Studio 官方博客挂出一篇公告。作者 Mustapha Lazrek，Copilot Studio 的 Principal PM Manager。标题原文：「Computer-using agents in Microsoft Copilot Studio are now generally available」——computer-use 智能体进入通用可用。

公告第二段原话：

> 「The next chapter of enterprise AI isn't about chatting with assistants — it's about agents that actually do the work.」

企业 AI 的下一章不是跟助手聊天，是 agent 真的把活干了。

5 天之后，arXiv 2604.08523 这篇论文的 V2 排行榜更新挂出来：153 个真实网站任务，最强商用模型 Claude Opus 4.7 在严格口径下通过率 44.6%、Sonnet 4.6 在论文头条口径下 33.3%；7 个一线模型里**有 2 个低于 5%**；GPT-5.4 跑出来 6.5%。

「真的把活干了」和「3 次只能干成 1 次」之间，差了一个 GA 标签。

那一周还有一件 Microsoft 公告里没说、Anthropic 当天没声张、Google I/O 主旨里也没提的事——Microsoft 这次 GA 上线的 computer-use agent，**背后跑的两个模型一个是 OpenAI 的 CUA，一个是 Anthropic 的 Claude Sonnet 4.5**，一个都不是 Microsoft 自家的。

GA 卖你的，是别家的脑子。按步收的钱，进的是别家的账。跑不通的 67%，是你公司的合规和最终用户买单。

就这。

---

## 一、5 月 13 日，Mustapha Lazrek 在 Tech Community 挂的那篇

Mustapha Lazrek 的这篇公告挂在 techcommunity.microsoft.com 的 Copilot Studio Blog 节点下，编号 4519427。除了开篇那句 punchline，正文里还有同公司 Charles Lamanna 的配套 quote。Lamanna 现在的头衔是 Microsoft President of Business Applications & Agents，2026 年 3 月组织改组之后直接向 Satya Nadella 汇报。他的那一句原话是：

> 「If a person can use the app, the agent can too.」

人能用的 app，agent 也能用。

这一句是过去三年所有 computer-use 厂商共同的对外口径，从 Anthropic 2024 年 10 月那篇「Introducing Computer Use」开始，到 OpenAI Operator 2026 年 1 月的 research preview，到 Google Antigravity 2.0 上周的 I/O 主旨——文字略有差异，结构完全一致：人会用的，agent 也会用。

至于"人会用的"具体指哪些 app、agent 用得多准、出错的时候谁修——三句话里都不展开。展开就不能上 GA 了（笑）。

Microsoft 这次 GA 的发售范围是「全部 commercial Power Platform geographies」。GCC、GCC High、DoD 三档主权云不在首批。也就是说面向商业客户全量铺开，面向政府客户暂缓——这个区别值得拎出来看：政府客户合规审计严，所以"GA"那个标签在他们这里要再等一等。商业客户合规审计松，所以可以先上。

GA 同时官宣了一个 design partner——Graebel，一家全球人才搬迁公司。Microsoft GA 博客里给的客户 quote 来自 Graebel 的 CRO Matt Brownlee：

> 「By adopting Microsoft Copilot Studio and AI agents, we've moved beyond traditional automation to a more intelligent, scalable operating model.」

我们采用了 Microsoft Copilot Studio 和 AI agent，已经从传统自动化过渡到一个更智能、更可扩展的运营模型。

整段 quote 没有数字。没有任务通过率、没有 ROI、没有失败回退率、没有"过去一年 agent 跑了 X 万次任务里 Y 次需要人介入"那种厂商应有的硬指标——只有"intelligent"、"scalable"两个形容词。一个完整的客户案例，定量信息为零。

这是 GA 公告的标准做法。客户提供形容词，厂商背书 GA 标签，benchmark 数字一概不提。

Microsoft 的定价表挂在 Azure pricing 页和 Copilot Studio Learn 计费文档下。computer-use 步骤按 5 Copilot Credits 一步收费；1 Copilot Credit = $0.01 美元（pay-as-you-go），$200 一个月可预购 25,000 credits。算下来一步 $0.05，一个典型多步任务（10–30 步）端到端价格大约 $0.50 到 $1.50。

每步 5 分钱。这是 Microsoft 写在定价页上、对外承诺的数字。

每步 5 分钱不包含什么——这是 Microsoft 没写在定价页上、留给你自己慢慢搞清楚的部分。第四节会算这笔账。

---

## 二、那 33.3% 是怎么测出来的

ClawBench 这篇论文挂在 arXiv 2604.08523，2026 年 4 月 9 日提交 V1，5 月更新 V2 排行榜。第一作者 Yuxuan Zhang 是 UBC 的研究生，所在实验室是 NAIL Group，导师 Kelsey R. Allen。合作者包括 Wenhu Chen——那个写 Tülu 系列论文的 UBC 教授。

这是一份学术团队产出，不是厂商基准。Microsoft 没投钱、Anthropic 没投钱、OpenAI 没投钱——这一点很重要，等会儿要用。

153 个任务，144 个**真实生产网站**，15 个生活类别。完整分布如下（来自 GitHub repo reacher-z/ClawBench）：

| 类别 | 任务数 |
|---|---|
| Daily Life | 21 |
| Entertainment & Hobbies | 15 |
| Creation & Initialization | 13 |
| Rating & Voting | 10 |
| Travel | 9 |
| Education & Learning | 9 |
| Office & Secretary | 9 |
| Beauty & Personal Care | 9 |
| Job Search & HR | 8 |
| Pet & Animal Care | 8 |
| Personal Management | 6 |
| Shopping & Commerce | 6 |
| Nonprofit & Charity | 6 |
| Academia & Research | 5 |
| Finance & Investment | 4 |

「真实生产网站」这一句不能略读。市面上几乎所有 agent 基准都跑在沙盒里——WebArena、VisualWebArena、MiniWoB、AgentBench——一个 Docker 容器，固定快照，结构化日志，跑完销毁。ClawBench 不跑沙盒。153 个任务每一个都点向 144 个**活的**生产网站：Amazon、Spotify、Tripadvisor、Indeed、Coursera、PayPal——名字看着眼熟，是因为你自己每天用。

评测方法分两阶段。Stage 1 叫 Interception——用 request interceptor 拦住 agent 对真实服务发出的"不可逆"请求（按 URL pattern + method 匹配），在请求触达 live server 之前截下来，所以测试本身不会真的下单、真的扣钱、真的发邮件。Stage 2 叫 LLM Judge——把 agent 跑出来的请求和人类参考答案丢给 DeepSeek V4 Pro，给两套分数：宽松判分（ambiguous 算对）和严格判分（ambiguous 算错）。

5 层日志全部留：MP4 录屏、按时间戳截图、DOM 事件流、HTTP 流量、agent 的推理消息。出问题可以倒带。

V2 排行榜最新数字：

| 模型 | Intercepted（动作到位） | Reward Lenient（宽松通过） |
|---|---|---|
| Claude Opus 4.7 | 54.6% | 44.6% |
| GLM-5.1 | 48.5% | 34.6% |
| GPT-5.5 | 45.4% | 35.4% |
| DeepSeek V4 Pro | 43.9% | 33.9% |
| Claude Sonnet 4.6 | — | 33.3% |
| 其余三家（含 GPT-5.4） | 6.5%–14.6% | 0%–10% |

榜首 Opus 4.7 严格口径 44.6%。论文 V1 头条数字 Sonnet 4.6 是 33.3%——也就是 153 道题里通过 51 道。**剩下 102 道，agent 要么点错按钮、要么填错表单、要么卡在登录、要么编出网站上没有的信息**。GPT-5.4 跑出来 6.5%——153 道题里通过 10 道——你不能说它"接近可用"，只能说它"基本不可用"。

ClawBench 作者自己承认两条局限。第一条：interceptor 只拦最终提交动作，不验证任务真正完成——也就是说"agent 把请求拼对了"和"任务真的成了"之间还有一段距离，分数本身可能偏高估。第二条：live site 会变，所以分数会漂——这周测和下周测可能不一样。

两条局限叠加起来，结论比头条数字更糟：33.3% 是论文跑出来的乐观上限。

---

## 三、同一个 Sonnet 4.6，封闭沙盒里 80%，真实网站上 33%

把 Sonnet 4.6 在不同基准上的成绩并排摆出来，可以看清楚 33.3% 不是噪声。

| 基准 | 类型 | Sonnet 4.6 成绩 |
|---|---|---|
| SWE-bench Verified | 封闭代码任务 | ~80% |
| OSWorld-Verified | 沙盒桌面操作 | 72.5% |
| τ-bench Retail | 沙盒客服对话 | 86.2% |
| Online-Mind2Web | live 网站 | ~61% |
| **ClawBench** | **真实生产网站** | **33.3%** |

同一个模型，环境从"封闭沙盒"过渡到"真实生产网站"，通过率从 86% 一路掉到 33%。这不是模型不行，这是评测约束不同。SWE-bench 给你冻结的代码库、明确的测试套件、单一目标；ClawBench 给你 Amazon 首页今天的版本、一个会随时跳出来的 cookie 弹窗、一个三轮验证的登录、一个 A/B 测试改过布局的购物车页。

Anthropic 自己的 Sonnet 4.6 发布博客里有一段原话，说 OSWorld-Verified 上 72.5% 的成绩"approaches a human baseline"——接近人类基线。Anthropic 没说哪个 baseline，也没说接近到什么程度（笑）。但即使按 Anthropic 自家的口径算，72.5% 已经是"接近人类"，那 33.3% 是什么——半个人？

OSU NLP Group 4 月份挂在 arXiv 2504.01382 的 Online-Mind2Web 论文里有一句话被很多人略过，但它很重要：

> 「most commercially available agents underperform the academic SeeAct baseline from early 2024」

大多数商用 agent 的表现，不如 2024 年初的学术基线 SeeAct。

2026 年的 GA 商用 agent，在真实网站上的表现，**不如两年前的学术 baseline**。这句话不是匿名酸民说的，是 OSU NLP Group 自己挂在论文里的。

这个 gap 不是 evaluator 严苛造成的——τ-bench 沙盒里 Sonnet 4.6 跑出 86.2%，说明模型本身的 reasoning + tool-use 链路是好的。gap 是评测环境的"真实程度"造成的。

真实意味着什么。真实意味着 CAPTCHA 在第 3 步弹出来；意味着登录之后跳一个 "verify your phone" 二级页；意味着购物车里多出一个上次没清的商品；意味着昨天还能用的 XPath 今天不能用；意味着按钮文字从「Add to Cart」改成「Buy now」；意味着新欧盟 cookie 法规又加了一层 modal。

真实意味着，**世界不会为你的 agent 冻结布局**。

封闭基准里跑 88% 的模型，到真实世界里跑 33%。中间那 55 个百分点的差，就是过去三年所有 agent 厂商在 marketing slide 上写"production-ready"的时候，**没告诉你的那个数字**。

---

## 四、5 Copilot Credits = $0.05/step，这个价格不包含哪些东西

第一节没算完的那笔账，可以继续算了。Microsoft Copilot Studio computer-use 的对外定价是每步 $0.05。一个 10 步的任务 $0.50，一个 30 步的任务 $1.50。看起来比雇一个数据录入员便宜——美国一个低端数据录入员每小时大概 $20，30 步任务做下来按 5 分钟算 $1.67，agent 的 $1.50 看着确实便宜了 10%。

这是定价表愿意让你算出来的那一面。

定价表不告诉你的那一面：**$0.05/step 是 agent 跑成功的单价，不是 agent 跑成功的成本**。这两个词不一样。

按 ClawBench 33% 通过率粗算（注意——这是上限，真实企业场景里因为更长 horizon 通常更低）：每跑 1 个能通过的多步任务，背后是 2 个跑不通的任务在被人接管、回滚、重试、修复、解释。这 2 个跑不通的任务里，Microsoft 已经按 $0.05/step 收了你的钱——按 10–30 步计费——agent 跑了你也付了，跑不通你还得自己出钱让人补救。

让人补救的成本是多少。一个 SaaS 公司专门处理"agent 失败回退"的二线 ops 工程师，按美国本土 $40/hr 算，处理一个失败任务（含日志读取、复现、手动操作完成、记录失败模式）大概 15–30 分钟，单次成本 $10–$20。

一个完整 TCO 算式（按 30 步任务 + 33% 成功率 + 失败由 ops 二线接管）：

| 项 | 金额 |
|---|---|
| 1 次成功的 agent 跑（30 步 × $0.05） | $1.50 |
| 2 次失败的 agent 跑（先跑完才知道不行） | $3.00 |
| 2 次失败的人接管（按 $15 一次） | $30.00 |
| **端到端单次成功成本** | **$34.50** |

雇人手动做 1 次的成本，按 $20/hr × 5 分钟 / 60 = $1.67。

agent 比纯人工贵了大约 20 倍（笑）。

不止 20 倍，还有第二层成本——Microsoft 定价页里悄悄写在脚注的部分：「Cognitive Services、Logic Apps、Azure Functions 调用单独计入 Azure 账单。」也就是说 agent 跑步骤的时候要调的所有 Azure 中间件——按调用次数另算。每次 agent 跑一步，背后调的是一串 Azure 资源；这一串资源不在 $0.05 的"step 单价"里。失败的 agent 跑也要调这一串。失败的成本不止是"白付了 $0.05"，是"白付了 $0.05 + 一串 Azure 中间件调用费 + ops 回退人工"。

第三层成本——agent 失败的时候你的最终用户怎么办。

Graebel 的搬迁工单系统是个好例子。客户提交一个跨国搬迁需求，agent 跑了 22 步去填 Graebel 内部"Global Connect"系统，第 18 步卡在一个登录验证页跑不下去。结果是什么。客户那边收到的不是"我们正在处理"——是 18 步动作之后**一个不完整的工单**，需要人工补完。如果接手 ops 当天忙，工单挂三天。客户三天后追问"我的搬迁怎么样了"，得到的答复是"系统在升级中，我们尽快"。Graebel 的品牌损失、客户流失、客服回信成本——**全部在 $0.05/step 之外**。

「5 Copilot Credits / step」这个数字是 Microsoft 写给 CFO 看的。CFO 看 unit economics，看 per-step pricing；CFO 不看 ops backlog、不看品牌损失、不看用户怒火。等到这三项算进来，agent 的 unit economics 就崩塌。

Microsoft 当然知道（笑）。所以才在产品页反复强调 "human-in-the-loop review" "configurable approval steps" "session replay with screenshots" ——把"人接管"这件事包装成 governance feature，不是 cost line item。

包装得很漂亮。漂亮归漂亮，钱还是从你账上扣。

![flat illustration of a vending machine that dispenses agent labels while invoice papers pile up behind it](images/concept_01.jpg)

---

## 五、那些跟你说 "production-grade" 的厂商，没有一家披露过端到端任务成功率

把这一周三家最响的 agent 公告并排放在一张表上，看一个共同点。

| 厂商 | 产品 | 公告日期 | 公开披露的端到端任务成功率 |
|---|---|---|---|
| Microsoft | Copilot Studio CUA GA | 2026-05-13 | 无 |
| Anthropic | Stainless 收购 + Sonnet 4.6 Computer Use | 2026-05-18 | 无 |
| Google | Antigravity 2.0 + Managed Agents | 2026-05-19/20 | 无 |

三家公告，零个端到端成功率数字。

你能在 Anthropic 的 Sonnet 4.6 model card 里找到 OSWorld 72.5%、Terminal-Bench 50.0%、SWE-bench 79.6%——这些都是封闭沙盒里跑出来的数字。你找不到「Sonnet 4.6 在 100 个企业真实任务里跑出 X% 完整通过率」的数字。Anthropic 没披露。Microsoft 没披露。Google 没披露。OpenAI 没披露。

为什么没披露——因为披露了就没人买了。

学术界倒是有人测了。ClawBench 测了，Online-Mind2Web 测了，TheAgentCompany 测了——三个团队三个独立测，结论一致：真实场景下，最强模型在 30%–60% 之间徘徊。TheAgentCompany 这篇挂在 arXiv 2412.14161，CMU 团队做的，结论是 Gemini 2.5 Pro 在 175 个 simulated SaaS 任务上 **30.3% 完全自主完成**，加上"部分完成"也只到 39.3%。一个 simulated SaaS 公司——已经比真实企业 IT 环境干净得多——最强模型还是只能搞定不到 1/3。

学术团队披露这些数字，会被算法工程师上 Twitter 阴阳"benchmark 不代表实战"。厂商不披露这些数字，叫"商业惯例"。

这一节最后说一个最反直觉的事实——**Microsoft Copilot Studio GA 的两个 GA 后端模型，一个是 OpenAI 的 CUA，一个是 Anthropic 的 Claude Sonnet 4.5**，全部来自第三方。这一条信息来自 Microsoft 自己 2026-02-24 在 Copilot Studio 博客挂出的那篇 "Computer-using agents now deliver more secure UI automation at scale"，原文白纸黑字写着。

也就是说，**Microsoft 这次卖给企业的"production-grade computer-use agent"，背后的智能完全外包**。Microsoft 提供的是：UI 框架（Copilot Studio）、计费系统（Power Platform）、合规外壳（Purview + Azure Key Vault）、销售渠道（Microsoft 365 客户列表）、品牌背书（GA 标签）。「脑子」是别人的。

Microsoft 是渠道商。
Microsoft 是合规外壳商。
Microsoft 是把 33% 成功率包装成"企业级 GA"的那个商。

Microsoft 不是模型商。

至于真正提供"脑子"的那两家——OpenAI 和 Anthropic——这一周做了别的事，第七节讲。

---

## 六、Anthropic 自己 Transparency Hub 里那个 12%

「33% 通过率」是任务能不能完成的失败率。还有一个失败率比这个更可怕，叫**安全失败率**。

Anthropic 的 Transparency Hub 挂在 anthropic.com/transparency。这是 Anthropic 自己半年挂一次的对外披露页面，里面有一组关于 prompt injection 的硬数据：

| 模型 | 启用 safety system 时的 block 率 | 不启用时的 block 率 |
|---|---|---|
| Claude Opus 4 | 89% | 71% |
| Claude Sonnet 4 | 86% | 69% |

Anthropic 自己披露的最高防护成绩是 89%。倒推一下——**即使开了最强 safety system，仍有 11% 的 prompt injection 攻击会成功**。Sonnet 4 这个数字是 14%。

11%–14% 是什么概念。如果你的 agent 跑一个 100 步的复杂工作流，期间每一步都有可能接触不可信内容（网页内容、邮件正文、上传文档），那么这一次跑下来被 prompt injection 成功攻击的累计概率，**远超你能接受的范围**。

并不是猜想。已经有公开披露的真实事件，全部来自一手 disclosure 渠道：

**ShadowPrompt** — 针对 Anthropic Claude Chrome Extension 的 zero-click prompt injection 攻击链。受害者**只需访问攻击者控制的页面**——不需要点任何东西——Claude 就会执行注入的指令。该漏洞 SOCRadar 在 2026 年初公开披露后 Anthropic 修复。

**Anthropic 官方 mcp-server-git 三连漏洞** — 2026 年 1 月披露在 The Hacker News 上的 CVE 链。Anthropic 自己出品的 git MCP server，三个 prompt injection 漏洞分别可导致：远程代码执行、任意文件删除、把任意文件加载进 LLM context。一个用 git 的 agent 看一眼恶意 commit message，可能就把 ~/.ssh/id_rsa 喂给攻击者的服务器。

**Anthropic Cowork 文件外泄** — 2026 年 1 月披露。Cowork 可被 prompt injection 诱骗，把企业内部敏感文件传送到攻击者的 Anthropic 账号，**全程不需要用户额外授权**。

三个事件的共同点：受害方都是企业。攻击载体都是 agent 跑在不可信内容里的常规操作。Anthropic 公开承认有这类风险，但披露动作都是事后——攻击者先用、研究人员发现、厂商打补丁。

把 ClawBench 的 33% 任务成功率和 Anthropic 自己的 11% prompt injection 成功率叠加起来——一个 100 步的 agent 工作流，正常完成的概率是几个零之后才有效数字；被注入劫持去做超出授权动作的概率，反而是高于 50%。

这两个数字 Microsoft 在 5 月 13 日的 GA 公告里都没提。Microsoft 反复提的是 Purview 审计、Dataverse 日志、Azure Key Vault 凭证管理、Windows 365 隔离 Cloud PC——一整套**事后追溯**的工具。事后能查谁操作了什么、什么时候操作的、操作产生了什么后果。这些工具的隐含前提：**预期会有事故**。

GA 不代表事故不会发生。GA 代表事故发生之后**可以查清楚是谁的事故**。

这两件事不一样。但 GA 标签一贴上来，企业 IT 那边看到的是前一个，CFO 那边算的是前一个，buying committee 拍板的时候算的也是前一个。

直到出事，才知道自己买的是后一个。

---

## 七、5 月 13 日往后的一周，谁在数钱

把这一周的三件事按时间摆出来。

**5 月 13 日**——Microsoft Copilot Studio computer-use agents GA。背后跑 OpenAI CUA + Anthropic Claude Sonnet 4.5。Microsoft 在台前收企业渠道费，OpenAI 和 Anthropic 在台后按 token 计量收推理费。

**5 月 18 日**——Anthropic 收购 Stainless。这条公告挂在 anthropic.com/news/anthropic-acquires-stainless。Stainless 是给 OpenAI、Google、Anthropic 三家做 SDK 生成基础设施的公司——你用 pip install openai 那个 openai SDK，背后的代码生成工具就是 Stainless。Anthropic 收购之后宣布关停 Stainless 全部 hosted 服务。Anthropic Head of Platform Engineering Katelyn Lesse 的官方 quote：

> 「Agents are only as useful as what they can connect to. We're excited to bring the Stainless team into Anthropic to advance Claude's ability to connect to data and tools.」

agent 只跟它能连到的东西一样有用。

这一句话的反向解读——Anthropic 把整个生态的 SDK 生成基础设施收进自己屋里，**断 OpenAI 和 Google 在这一层的对外能力**。三家共用的 plumbing，从今天起只服务一家。

**5 月 19–20 日**——Google I/O 主旨发布 Antigravity 2.0 + Antigravity CLI + Managed Agents API。三件套全部基于 Gemini family 模型，全部跑在 Google Cloud sandbox 里。Google 的 marketing slogan 是「manage the mission, not the machine」。Managed Agents API 把 agent 包装成 SaaS——你按 mission 付费，不操心机器。

三件事拼起来看：Microsoft 卖 agent 渠道，Anthropic 卡 agent plumbing，Google 卖 agent SaaS。三家在 agent 这一层的卡位完全不冲突，因为他们卖的不是同一个东西——Microsoft 卖**位置**（Copilot Studio 的入口）、Anthropic 卖**脑子**（Claude 模型 + Stainless 工具链）、Google 卖**包装**（Managed Agents 的 SaaS 化）。

谁在最后数钱。看 Anthropic 自己披露的财务数字：Q1 2026 营收 $4.8B，Q2 2026 预测 $10.9B，operating profit $559M——**单季度首次盈利**。ARR 从 2025 年底的 $9B 涨到 2026 Q1 的 $30B，**同比 80 倍**。

Anthropic 是这一周最大的赢家。Microsoft GA 跑 Sonnet 4.5 是 Anthropic 进的账；Anthropic 自己 claude.ai computer use 升级也是 Anthropic 进的账；Stainless 收购把生态 plumbing 锁进自己屋里，未来 OpenAI 和 Google 的 SDK 战略要重做。这一周 Anthropic 至少在三个方向同时收钱。

Microsoft 的角色变了。从 Office 时代的"既造软件又卖软件"，到 Copilot Studio 时代的"造渠道、合规外壳、品牌背书，模型外包"——**Microsoft 在向 IBM 1990 年代靠拢，做企业 IT 的整合商**。这不是贬义，是真实的商业模式转型。IBM 当年靠卖渠道和服务做了几十年好生意。Microsoft 复制这条路径没问题——问题是渠道和服务的卖法，前提是"渠道里跑的东西大概率有用"。

ClawBench 33% 这个数字告诉你，渠道里跑的东西，**3 次有 2 次没用**。

Daron Acemoglu 2026 年 5 月 11 日在 MIT Technology Review 那篇采访里给的预测——AI 在未来 10 年只会给美国 GDP 涨 1.1%，年生产率涨 0.05%。这个数字跟 Goldman Sachs 同期估的 7% 差出 70 倍。Acemoglu 不是反 AI——他是 2024 年诺贝尔经济学奖得主，主要研究方向就是技术对劳动的影响。他在这篇采访里点名要看三件事，其中第一件就是 "agentic AI deployments"——agent 实际部署后究竟如何。

5 月 13 日 Microsoft 的 GA 公告给了 Acemoglu 一个观察样本。5 月 18 日 ClawBench V2 排行榜给了 Acemoglu 一个对照数字。Acemoglu 的 1.1% GDP 预测建立在他对"AI 实际生产率"的怀疑上——这一周的三件事，全部支撑他这个怀疑。

GA 标签贴上去那一刻，真正在数钱的是模型层；真正在承担 67% 失败率成本的是企业 IT、合规、ops、最终用户；真正在算这个 TCO 账的，全世界没几个人。

Mustapha Lazrek 5 月 13 日那句「agents that actually do the work」，3 次里有 1 次做的是 do the work，另外 2 次做的是 generate the work（笑）。generate 给谁。给你公司的 ops 工程师，给你公司的合规审计，给你公司的最终用户。

就这。

![flat illustration of a money flow diagram from Microsoft Copilot Studio brand to Anthropic and OpenAI servers with broken arrows leaking dollars to operations workers below](images/concept_02.jpg)

---

## 数据来源

### Microsoft Copilot Studio Computer-Use Agent GA
- [Microsoft Tech Community — Computer-using agents in Microsoft Copilot Studio are now generally available (5/13/2026)](https://techcommunity.microsoft.com/blog/copilot-studio-blog/computer-using-agents-in-microsoft-copilot-studio-are-now-generally-available/4519427)
- [Microsoft Copilot Blog — Computer-using agents now deliver more secure UI automation at scale (2/24/2026)](https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/computer-using-agents-now-deliver-more-secure-ui-automation-at-scale/)
- [Microsoft Copilot Studio Learn — Messages and capacity requirements](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management)
- [Azure pricing — Copilot Studio](https://azure.microsoft.com/en-us/pricing/details/copilot-studio/)
- [Microsoft 365 Copilot pricing — Copilot Studio](https://www.microsoft.com/en-us/microsoft-365-copilot/pricing/copilot-studio)
- [Microsoft Copilot Studio Blog — May 2026 What's New](https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/new-and-improved-computer-using-agents-a-new-workflows-experience-and-real-time-voice-experiences/)
- [Charles Lamanna author page — Microsoft Copilot Blog](https://www.microsoft.com/en-us/microsoft-copilot/blog/author/charles-lamanna/)

### ClawBench 一手出处
- [arXiv 2604.08523 — ClawBench: Can AI Agents Complete Everyday Online Tasks?](https://arxiv.org/abs/2604.08523)
- [arXiv HTML version 2604.08523v1](https://arxiv.org/html/2604.08523v1)
- [GitHub — reacher-z/ClawBench](https://github.com/reacher-z/ClawBench)
- [ClawBench project page](https://claw-bench.com/)
- [ClawBench leaderboard mirror](https://clawbench.net/)
- [HuggingFace Paper 2604.08523](https://huggingface.co/papers/2604.08523)
- [First author Yuxuan Zhang homepage](https://reacher-z.github.io/)

### 同期其他真实场景基准（一手）
- [SWE-bench leaderboard](https://www.swebench.com/)
- [GitHub — sierra-research/tau-bench](https://github.com/sierra-research/tau-bench)
- [Sierra — τ-Bench: shaping development of evaluation agents](https://sierra.ai/blog/tau-bench-shaping-development-evaluation-agents)
- [GitHub — OSU-NLP-Group/Online-Mind2Web](https://github.com/OSU-NLP-Group/Online-Mind2Web)
- [Online-Mind2Web HAL leaderboard](https://hal.cs.princeton.edu/online_mind2web)
- [arXiv 2504.01382 — Online-Mind2Web](https://arxiv.org/abs/2504.01382)
- [arXiv 2412.14161 — TheAgentCompany (CMU)](https://arxiv.org/abs/2412.14161)
- [Anthropic — Introducing Claude Sonnet 4.6](https://www.anthropic.com/news/claude-sonnet-4-6)

### Anthropic safety / prompt injection 一手披露
- [Anthropic Transparency Hub](https://www.anthropic.com/transparency)
- [The Hacker News — Three flaws in Anthropic MCP Git Server (1/2026)](https://thehackernews.com/2026/01/three-flaws-in-anthropic-mcp-git-server.html)
- [SOCRadar — ShadowPrompt zero-click on Anthropic Claude Chrome Extension](https://socradar.io/blog/shadowprompt-zero-click-anthropics-claude/)

### 本周其他 agent 公告（一手）
- [Anthropic — Anthropic acquires Stainless (5/18/2026)](https://www.anthropic.com/news/anthropic-acquires-stainless)
- [Anthropic — Claude in Microsoft Foundry](https://www.anthropic.com/news/claude-in-microsoft-foundry)
- [Google Blog — Google I/O 2026 developer highlights](https://blog.google/innovation-and-ai/technology/developers-tools/google-io-2026-developer-highlights/)
- [Google Cloud Blog — I/O 2026 news for agent developers](https://cloud.google.com/blog/topics/developers-practitioners/io26-news-for-agent-developers-on-google-cloud)
- [Antigravity Blog — Introducing Google Antigravity 2.0](https://antigravity.google/blog/introducing-google-antigravity-2-0)
- [OpenAI — Introducing ChatGPT Agent](https://openai.com/index/introducing-chatgpt-agent/)
- [OpenAI — Introducing Operator (sunset notice)](https://openai.com/index/introducing-operator/)
- [xAI — Grok Build CLI](https://x.ai/news/grok-build-cli)
- [Cursor Blog — Composer 2.5](https://cursor.com/blog/composer-2-5)

### 经济视角（一手）
- [MIT Technology Review — Three things in AI to watch, according to a Nobel-winning economist (5/11/2026)](https://www.technologyreview.com/2026/05/11/1137090/three-things-in-ai-to-watch-according-to-a-nobel-winning-economist)
- [MIT Sloan Management Review podcast — AI Is Not Improving Productivity](https://sloanreview.mit.edu/audio/ai-is-not-improving-productivity-nobel-laureate-daron-acemoglu/)
- [SSRN — Building Pro-Worker Artificial Intelligence (Acemoglu, Autor, Johnson)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6290347)
- [Stanford SIEPR — Brynjolfsson on AI productivity](https://siepr.stanford.edu/news/generative-ai-boost-can-boost-productivity-without-replacing-workers)

### 技术视角（一手）
- [Dwarkesh Patel podcast — Andrej Karpathy on the decade of agents](https://www.dwarkesh.com/p/andrej-karpathy)
- [Hacker News — discussion on Karpathy "decade of agents"](https://news.ycombinator.com/item?id=45619329)
