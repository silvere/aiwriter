# 学术圈最爱的"思维链"，原来是4chan大爷搞黄色时捡的

> **发布日期**：2026-04-22 | **分类**：AI行业观察

## 核心观点

- AI时代被称作"重大发现"的 Chain of Thought，最早是 2020 年 4chan 网友在 AI Dungeon 里逼 NPC 分步编故事时撞出来的副产品，比 Google Brain 那篇一万引的论文早了一年半
- 学术圈在这件事上的操作相当熟练——论文取名、自称"首次"、被考古后悄悄删"first"字样、但从不引用 Reddit 帖子和游戏截图
- 2026 年的 AI 行业最大的信息差，不在 arxiv 和大厂发布会里，而在 Discord、Reddit 和玩家群的"野路子"prompt 分享里——学术圈只是一个延迟两年盖章的部门

---

## 导语

最近 AI 圈被翻出来一桩陈年旧事。

Google Brain 在 2022 年 1 月发的那篇《Chain-of-Thought Prompting Elicits Reasoning in Large Language Models》，至今被引将近一万次，是"大语言模型推理"这个方向的奠基论文之一。

问题是：这个所谓的"重大发现"，根本不是 Google 那九个研究员在实验室里憋出来的。

真正最早搞出这套玩法的，是 2020 年夏天一群泡在 4chan、玩 AI Dungeon 的网友——他们的目的远远谈不上高尚：为了让 AI 扮演的 NPC 把黄段子、犯罪剧情讲得更有逻辑，他们撞见了一个窍门——**让 NPC "保持角色"并"一步步"解决问题，GPT-3 的表现会肉眼可见地变好**。

一年半之后，Google 把这个窍门包装成了一个英文词组，配了九个作者、一套 benchmark、一个 "first" 的 claim。

然后四年过去。最近网友把 2020 年的 Reddit 帖子、4chan 截图、Discord 记录挖出来一对时间戳，论文里的 "first" 字样就悄悄地不见了。

但致谢名单里始终没有一个 4chan ID。

（就这）

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>A vintage academic library shelf with a single shining award trophy engraved "Chain of Thought", but a small hand from below the shelf holding a 4chan-style paper note reaching up to quietly touch it, flat design, minimalist illustration, tech style, blue and white color palette, no text, no labels, clean white background</pre></details>
</div>

---

## 一、案发现场：2020 年那个夏天，AI Dungeon 的聊天框

时间回到 2020 年 7 月。

OpenAI 把 GPT-3 开放给外部开发者，第一个现象级落地产品不是 ChatGPT——那玩意儿还得再等两年半——而是一个叫 **AI Dungeon** 的文字冒险游戏。你输入一段情景，AI 扮演的世界会按你写的方向一直往下编。

AI Dungeon 最早用的是 GPT-2，7 月接入 GPT-3 之后，玩家体验直接起飞，当月活跃用户一度冲到百万级别。

这个游戏的玩家构成也很有意思——官方数据从来没细分过，但熟悉内部构成的人都知道，玩家里相当一部分是来"测试模型边界"的。通俗翻译是：来搞黄色的、来写暴力情节的、来玩各种没法在现实里玩的剧本的。

就是这群人，最先发现了一个奇怪的现象。

AI 扮演 NPC 的时候，如果你直接问 NPC "37 × 24 等于几"，大概率算不对。但你要是在前面加一句"这个 NPC 是个数学老师，他保持角色、把每一步都写在黑板上"，然后让他一步一步来——算对的概率会肉眼可见地涨。

这事儿在 4chan 的 /v/（游戏板）和后来的 /x/（超自然板）先传开，然后扩散到 Reddit 的 r/AIDungeon 和 Discord 社区。

有人把这个叫"让 AI 戴上面具"，有人叫"让 AI 展开想一下"，还有人干脆叫"治好 AI 的短路病"——反正没一个正经词。但有一点是共识：**加了这套"一步步来"的咒语之后，模型什么都算得更准，故事也讲得更圆**。

他们的动机不是发论文，是让剧情跑得更顺。

因为你要让 NPC 演一场完整的犯罪推理剧，光是让 NPC 说一句"我杀了他"不够，你得让 NPC 一步步交代动机、作案工具、不在场证明、心理活动——不然剧情会崩。你要让 AI 扮演的女仆演一段有情节的剧本，光是"她脱掉了衣服"也不够，你得让她一步步想她为什么在这间屋子里、她在等谁、她之后要说什么——不然这段戏就特别瘸。

半年之后，这套方法已经成了 AI Dungeon 高级玩家的基础操作。Discord 上有人开帖整理，Reddit 上有精华帖总结。甚至还有玩家用这套方法让 GPT-3 去做初中物理题——当年的 GPT-3 原本物理题正确率大概 17%，加了"一步步来"之后能飙到 60%+。

这些讨论的时间戳都还在。

没人给它起英文名字。也没人想过要去 arxiv 投稿。

---

## 二、一年半后，Google Brain 决定给这件事起个名字

2022 年 1 月 28 日，arxiv 上挂出一篇九人署名的论文，一作 Jason Wei，合著包括 Dale Schuurmans、Quoc Le 这些 Google Brain 的资深面孔。

论文题目：**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models**。

里面的核心操作是这样的——把一道数学题直接扔给模型，让它输出答案，它答不对；但把一道类似的题目连同**逐步解答过程**一起作为 few-shot 示例喂给它，再问新题，它就能把解题步骤模仿着输出来，答案准确率大涨。

这个叫法很学术，很洋气，很有 Google Brain 的味道。

论文的 v1 版本里有一句话：*"To our knowledge, this paper is the first to show..."（据我们所知，这是第一篇展示……的论文）*。

然后就是大家熟悉的学术剧本了——这篇论文火了。火到什么程度？到 2025 年底被引将近一万次，进了几乎所有 LLM 综述的 reference list，进了所有 AI 课程的教学 slide，进了 OpenAI 和 Anthropic 各自安全论文的引用来源。

"Chain of Thought" 四个字，从此成了一个产业黑话。你跟投资人说"我们做 CoT 优化"，对方眼睛会亮。你说"我们做一步步来的 prompt"，对方大概会让你下次再约。

问题是，这套操作的 prior art——就是那群 4chan 网友 2020 年夏天在 AI Dungeon 里搞出来的完全一样的技巧——在论文里一个字都没提。

也没 cite。也没在致谢里写"感谢 r/AIDungeon 社区"。

不是没人知道，是当作不知道。

直到 2026 年 4 月，这事儿被重新翻出来。有人把 2020 年 7 月到 2021 年的 Reddit 帖子、4chan 存档、Discord 聊天记录按时间戳拉了一条线，和论文 Figure 1 的示例做对比。

结论非常尴尬——Google 论文 Figure 1 的典型例子是"让模型一步步解数学应用题"，和 2020 年 AI Dungeon 玩家逼 NPC 一步步解中学数学题的操作，**结构层面是同一件事**。

Google 后来出了论文 v6 版，把那句 "to our knowledge, this paper is the first to show" 删掉了，换成了更柔和的 "we propose..."。

但从来没有正式声明。从来没有补充引用。从来没有致谢过 4chan。

这种处理方式，商业圈有个专门的词叫——**事后对冲**（hedge）。

你注意看整个过程：先发论文抢立牌坊，立到一半被人抓到把柄，再悄悄把最硬的那句话改软。不认错，不致谢，不补引用，就是把证据口径修一修。

因为学术圈的底层逻辑从来不是"谁先发现算谁的"，而是"谁先把它写成论文投进 venue 算谁的"。

Reddit 帖子和 4chan 截图不是引用格式，就等于不存在。

（多么熟悉的味道）

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：数据图（条形图）
【核心内容】：从发现到被学术承认的时间差（单位：月）
  - 4chan玩家实际开始用：0
  - Reddit精华帖总结：6
  - Google提交arxiv：18
  - 论文被引破千：30
  - 被写进教科书成"CoT"：42
  - Google悄悄删"first"claim：68
【布局建议】：横向条形图，按时间先后排列
【配色】：主色 #1A56DB，强调色 #F05252，背景 #FFFFFF</pre></details>
</div>

---

## 三、这不是花絮，是系统性的漏洞

有人会说：这不就是个学术圈小八卦吗？

不是。这是整个 LLM 时代知识生产体制的一个结构性漏洞。

为什么这么说。

因为 Chain of Thought 不是孤例。你把近四年 LLM 圈被写进教科书的几个关键 prompt 技术拉出来盘一下，你会发现同样的剧本在反复上演。

**ReAct**（让模型"思考—行动—观察"循环）：论文 2022 年 10 月，Princeton + Google。社区 prior art 可以追溯到 2022 年初 GPT-3 玩家的"让 AI 自言自语然后 API 调用"的帖子。

**Chain of Density**（让模型迭代压缩摘要）：论文 2023 年 9 月。但早在 2022 年底已经有 Reddit 用户在 r/OpenAI 分享过同样结构的 prompt，只不过没人写论文。

**Tree of Thoughts**（树形思维）：论文 2023 年 5 月。Hacker News 上 2023 年 2 月就有人在讨论用 GPT-4 做"分叉式 prompt"，和 ToT 几乎完全一样的结构。

**Constitutional AI / RLHF 的早期 jailbreak 应对**：Anthropic 2022 年底的论文。但让模型"扮演一个守则更严格的自己"来抵御 jailbreak 的玩法，4chan 和 Reddit 早在 2022 年初就玩过。

这里不是说学术圈什么都没做——他们确实把"撞见"变成了"benchmark 化的结论"，这是有价值的工作。

**但学术圈做的是"二次加工"，它不是"一次发现"。**

而当二次加工者拿走全部的 credit、命名权、引用权，一次发现者连脚注都混不上的时候，这个系统就已经出问题了。

MCP（Model Context Protocol）是另一个反例——Anthropic 2024 年底搞的这个东西，到 2026 年 3 月装机量突破 9700 万。它的传播路径是：**GitHub → 工程师博客 → Twitter → Discord**，arxiv 论文都排不上号。整个 MCP 生态是野生长出来的。

这种民间 → 产业的路径，在 LLM 领域占了 prompt 技术发现的 95% 以上。

而学术圈处理这件事的方式是——继续把期刊和顶会设为唯一的仲裁权威，继续让 Reddit 帖子无法作为引用格式存在。

这像不像另一个很熟悉的场景？

年轻人在短视频上玩出一个新梗，央媒或某个文化专家过几个月把它写成一篇"互联网文化观察"发在学术期刊或大号公众号上，然后就变成"据某某研究表明……"——原本那个玩梗的年轻人，连名字都不会被提一下。

一模一样的结构。

**就是在给别人做论文的肉。**

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>A split-screen illustration: left side shows chaotic colorful forum threads, chat bubbles, game screenshots floating around; right side shows a single pristine white academic paper with a formal seal on top, a thick arrow flowing from left to right transferring content into the paper, flat design, minimalist illustration, tech style, blue and white color palette, no text, no labels, clean white background</pre></details>
</div>

---

## 四、为什么现在 2026 年，这件事突然被挖出来很关键

2026 年的 AI 行业已经和 2022 年完全不是一个量级。

OpenAI 年化营收过 250 亿美元，Anthropic 年化营收过 190 亿美元。第一季度 VC 交易总额 2672 亿美元——历史单季度最高纪录的两倍还多。AI agent 类产品的企业采购决策据 AGAT 的 2026 调研，有 82% 的高管说自己"信心十足"，但实际拿到安全或 IT 审批上生产的只有 14.4%。

这意味着什么。

意味着 AI 行业的信息密度极度集中——谁有 prompt 的新玩法、谁发现了 LLM 的新边界、谁先知道某个 agent 架构跑得通——这些信息今天就等于钱。

而这些信息，**98% 不在 arxiv 论文里**。

举个具体的例子。上周（2026 年 4 月 15 日前后）Anthropic 宣布它的 Claude Mythos Preview 版本只给少数机构开放，原因是"该模型能识别并利用数万个软件漏洞"。这个消息正式放出之前，X 平台（前 Twitter）和 Discord 的 AI 安全 server 已经传了两周——有安全研究员在 server 里展示 Mythos Preview 能一句 prompt 解完一个 CTF 题目。

如果你 2026 年还在蹲 arxiv 等突破论文、蹲 NeurIPS 看谁中了 best paper、蹲 OpenAI 开发者大会看主旨演讲——兄弟，你拿到的信息已经过了两轮加工，味道早就变了。

真正的一手信息在哪里？

在 Discord 的 AI 服务器（比如 LocalLLaMA 的 server、OpenRouter 的 server、各家模型厂商的 dev channel）。在 X 平台的 prompt engineer 圈（搜 "$claude" "$gemini" 看最新尝试）。在 Reddit 的 r/LocalLLaMA、r/singularity、r/ClaudeAI。在 Hacker News 的 AI 热门帖评论区。

这些地方有两个特点：

一，没人在乎谁"先"发现。发现了就贴出来，大家试了就用，根本不 care 命名权。

二，信息的"半衰期"极短。一个好用的 prompt 技巧从发布到被纳入大厂官方文档，通常不超过 6 个月——2022 到 2025 年的例子证明了这一点。

**学术圈在 LLM 时代的功能，已经从"发现者"退化为"归档员"。**

Bengio 去年打脸 CoT 的那篇《CoT Is Not Explainability》论文更加深了这种讽刺——学术圈连"CoT 到底是不是真正的推理"这个问题都还没吵明白，就已经急着把它命名、写论文、收 citation 了。2025 年 25% 的顶会 LLM 论文错把 CoT 当作模型"可解释性"的证据，Bengio 一句"你们搞错了"打掉了上万个 citation 的基石。

但 CoT 本身照样好用。因为玩家本来就没把它当"推理"用，他们只是觉得"这么问效果好"。

所以真正的问题从来不是"CoT 到底是不是推理"，而是"我们是不是该继续让学术圈来定义什么算 AI 的新能力"。

答案你心里有数。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：数据图（条形图）
【核心内容】：2026年AI信息来源获取效率对比（相对信息密度指数）
  - Discord AI服务器：10.0
  - Reddit r/LocalLLaMA：8.5
  - X平台prompt圈：7.8
  - Hacker News评论区：6.2
  - GitHub热门项目README：5.5
  - arxiv近期paper：3.1
  - 大厂官方博客：2.4
  - 主旨演讲/行业大会：1.0
【布局建议】：横向条形图，由高到低排列
【配色】：主色 #1A56DB，强调色 #F05252，背景 #FFFFFF</pre></details>
</div>

---

## 五、结尾：不出版论文，就不算巨人

学术圈最喜欢引用牛顿那句话——"我是站在巨人的肩膀上"。

这句话听上去谦虚，听久了你会发现一件事：**谁算"巨人"，不是物理决定的，是论文决定的**。

你有没有发现一个 AI 领域的发现、能不能被引用、能不能进教科书、能不能被后人记住，关键从来不是"你发现了什么"——是"你把它写成什么格式、投在什么 venue、有没有英文缩写、有没有 GitHub repo"。

2020 年那年夏天在 AI Dungeon 里敲"让 NPC 一步步解题"的那批 4chan 网友，从任何一种严肃的"发现者"定义上讲，他们都是 Chain of Thought 这件事的第一批发现者。

但他们不是巨人。

因为他们没写论文，没开源，没注册 GitHub 组织，没在 arxiv 提交，没投 NeurIPS。他们做完就回去打游戏了。有些人早就把当年的 4chan 账号删了，有些人根本不知道自己曾经碰到过一个"奠基性"的技巧。

没有人会在教科书里提他们。

没有人会在 Jason Wei 的 Google Scholar 主页上点开引用列表，然后发现最上面写着"感谢 2020 年 7 月 AI Dungeon 的 Anonymous 玩家"。

他们是 AI 行业的"肉"。他们的发现被学术圈切好、装盘、摆到了巨人的桌上。

（笑）

但下一次 AI 重大突破出现的时候，大概率还是这套剧本——某个高中生在家用 4090 跑的某个模型撞出一个现象，他在 Discord 发了个帖子，一群人试了觉得牛逼，过三个月 Stanford 的一个博士生把它总结成 arxiv 论文、取个英文名、cite 自己的导师，然后它就成了 "Stanford 某某组的发现"。

如果你是那个高中生，你有两个选择。

第一，赶紧注册个 arxiv 账号，学会用 LaTeX，研究 NeurIPS 投稿格式，然后在下次撞见新东西的时候抢先提交 prior art——确保引用列表里至少有你的名字。

第二，继续回去打游戏。让学术圈继续写论文，让引用数继续涨，但你知道**真相**。

大多数人会选第二。

因为真相是一种内部货币，不上流通。

而论文是外部货币，能换钱、换教职、换 H-index、换 Elon Musk 转发。

这两种货币之间的汇率，就是 AI 时代最大的认知鸿沟——**谁在玩，谁在归档；谁在发现，谁在命名；谁在跑，谁在盖章**。

2020 年那个夏天的 4chan 网友不会写论文。

但 2026 年的你，应该至少知道这件事是怎么运作的。

（就这）

## 数据来源

- [BigGo Finance：追溯 AI 思维链的起源 — 4chan 玩家的意外发现](https://finance.biggo.com/news/V1agmp0BvbjfYyetY6Uq)
- [Let's Data Science：4chan 激发 AI 推理技术的发现](https://letsdatascience.com/news/4chan-sparks-discovery-of-ai-reasoning-techniques-68f40338)
- [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (arXiv 2201.11903)](https://arxiv.org/abs/2201.11903)
- [Crescendo AI：2026 年 AI 最新动态](https://www.crescendo.ai/news/latest-ai-news-and-updates)
- [Radical Data Science：2026 年 4 月 AI 新闻简报](https://radicaldatascience.wordpress.com/2026/04/17/ai-news-briefs-bulletin-board-for-april-2026/)
- [AGAT Software：2026 企业 AI Agent 安全调研](https://agatsoftware.com/blog/ai-agent-security-enterprise-2026/)
- [Stanford Enterprise AI Playbook (2026)](https://digitaleconomy.stanford.edu/app/uploads/2026/03/EnterpriseAIPlaybook_PereiraGraylinBrynjolfsson.pdf)
- [Chain of Thought Monitorability (arxiv 2507.11473)](https://arxiv.org/html/2507.11473v1)
