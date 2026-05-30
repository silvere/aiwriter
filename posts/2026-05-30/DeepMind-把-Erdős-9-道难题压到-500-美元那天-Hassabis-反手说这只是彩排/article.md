# DeepMind 把 Erdős 9 道难题压到 500 美元那天，Hassabis 反手说这只是彩排

> **发布日期**：2026-05-30 | **分类**：AI产业深度

## 导语

2026 年 5 月 21 日，arXiv 上挂了一篇预印本，编号 2605.22763v1，标题《Advancing Mathematics Research with AI-Driven Formal Proof Search》。第一作者 George Tsoukalas，过去做过 PutnamBench 的形式化数学评测，现在挂的单位是 Google DeepMind。

论文做了一件事。把 Thomas Bloom 维护在 erdosproblems.com 上的 353 道 Erdős 公开未解难题各刷一遍，破了 9 道。其中 2 道是 1970 年由 Paul Erdős 和 András Sárközy 一起提出来挂了 56 年的——包括 Erdős #12(i)。附带战利品 44 条 OEIS 整数序列猜想，顺手清掉。

每道破题的推理成本，论文原文：

> 「inference costs ranged from roughly \$100 to \$500 per problem — less than a graduate student's weekly stipend.」
>
> 每道题 100 到 500 美元——比一个博士生一周的津贴还便宜。

5 天后，5 月 26 日，Demis Hassabis 接受 Axios 首席科技记者 Ina Fried 的专访。专访里关键两句：

> 「You can imagine the agentic era in this next year is a little bit like a practice run.」
>
> agent 时代这一年，就当一次彩排。

> 「This is partly why I use some of the terms I used, yeah, which were a little bit provocative.」
>
> 我用这些词，是有点挑衅的意思。

Hassabis 把 AGI 时间表，从原来「2024 - 2030 区间」挪到「2029 是真实可能」，加了一句 plus or minus a year。挪了大约 3 年。

同一周里 DeepMind 干了两件事。

第一件——把数学难题的破解单价拉到 500 美元一道。这是头版新闻，全球转发。

第二件——让 CEO 亲自出来，把 AGI 这条线往后挪 3 年，并把这次破解 9 道难题定性为「彩排」。这个动作没几个人写。

两件事都是好新闻。两件事一起干，就值得多想一层。

破 9 道难题这事，会上头条。挂 344 道没破的题，没人写。「这不是 AGI」这句话，被当成谦虚转发了。

这篇拆三件事：
- 第一件，**9 道破了** 和 **344 道没破** 哪个是真信号
- 第二件，「**这不是 AGI**」为什么必须由 CEO 本人在这一周说
- 第三件，这次真正的赢家是谁。提示一下，不是 Gemini 3.1 Pro，也不是 Hassabis。

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>A scattered pile of vintage handwritten mathematics manuscripts being converted into small printed receipts, half-revealed pages showing equations and Erdős-style number theory notation, minimalist flat illustration, muted academic palette of cream, navy, and charcoal, clean white background, no text labels, conceptual illustration style</pre></details>
</div>

---

## 一、9 道破了，344 道没破——2.5% 的命中率才是这次的真信号

把论文里那张表摆出来看。

总样本：**353 道**。来源：Thomas Bloom 维护的 erdosproblems.com——剑桥大学数学家 2022 年起收录、社区认证的 Erdős 一生公开问题清单。每一道都被人类数学界翻过很多遍，仍然未解。

成功破解：**9 道**。命中率 **2.5%**。

被英文报道点名的破解编号有 4 个：**#12(i)**（1970 年由 Erdős 和 Sárközy 提出）、**#125**、**#138**、**#741**。剩下 5 个编号没在新闻里出现——挂在论文附录的表里，源码挂在 GitHub `google-deepmind/alphaproof-nexus-results` 仓库的 `APNOutputs/ErdosProblems/` 子目录。该仓库截稿时 144 个 star，14 个 fork，5 个 commit，一共一个 open issue（笑）。

成本：每道 100 - 500 美元。

这是一组干净数字。但单看「9 道破了」，看不到完整故事。完整故事是——**344 道没破**。

把那 344 道挑出来想 1 分钟。

每道也跑了同等推理预算。按区间中位数 300 美元算：344 × 300 = **10.3 万美元**。加上 9 道成功的最高 4500 美元，总开销大约在 **10 - 11 万美元**区间。

10 万美元买 9 道破解，单价 1.1 万美元一道。论文把分子写成 100 - 500，没写分母。

这个数字怎么参考？

Paul Erdős 本人生前给重要问题开过悬赏。erdosproblems.com 上的奖金表是公开的：

- 1 万美元一档：挂 11 道，破了 1 道
- 5000 美元一档：挂 1 道，没破
- 1000 美元一档：挂 10 道，破了 3 道
- 最早一笔赏金：1974 年付给 Endre Szemerédi，1000 美元

也就是说，Erdős 本人按"问题市场价"对这些题的估值是 1000 - 1 万美元一道。DeepMind 用 10 万美元买 9 道，单价 1.1 万——压在 Erdős 自己定的估价线上沿，没有打骨折，没有翻天覆地的成本革命。

只是有 Lean 验证器在闸门口卡住，让 AI 不能交着「貌似对的论文」蒙混过关。这点后面讲。

「a few hundred dollars」（几百美元）这句话，出现在所有英文媒体头条里。论文里没出现，Hassabis 在 Axios 专访里也没说。这是记者炼出来的词。

论文里最接近的句子是 "less than a graduate student's weekly stipend"——比博士生一周津贴还便宜。

博士生一周津贴是多少？美国 NSF 数学博士后年薪标准约 6 万美元，每周折合 1150。Tier 1 学校博士后能拿到 8 万，每周 1500。

也就是说，每道题成本 ≤ 500 美元，对应**博士后半周的人头费**。

不是星巴克。是博士后半周时间。

而那位博士后这半周破不破得了这道题，不知道。AlphaProof Nexus 这 500 美元打不打得了水漂，也不知道——命中率 2.5%。两边都赌的话，博士后这半周的工资旱涝保收，AI 那 500 美元有 97.5% 的概率沉海。

把 2.5% 翻过来看：**每破 1 道题，要烧 39 道失败的试验**。把 39 道 × 300 美元 ≈ 1.17 万美元的失败成本加回去，单道破解的真实成本回到 **1 - 1.5 万美元**——好巧，正好落在 Erdős 本人 1 万美元那档悬赏线上。

DeepMind 这次最厉害的不是把成本压低，是把它压到了**和 Erdős 自己开的悬赏价一样**。

巧吗？

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：对账图
【副标题】：AlphaProof Nexus 在 353 道 Erdős 难题上的真实账本
【单位】：万美元
【核心判断】：每破 1 道题烧 39 道失败实验，单道真实成本 1.1 万——正好压在 Erdős 本人悬赏线上沿
【核心内容】：
  - 9 道破解直接成本 [流入]：0.45
  - 344 道失败实验成本 [流出]：10.32
  - 每道破解的真实摊销成本 [参照]：1.1
  - Erdős 1 万美元档悬赏线 [参照]：1.0</pre></details>
</div>

---

## 二、"这不是 AGI"——为什么这句话必须由 CEO 本人在这一周说

Hassabis 在 Axios 那场专访里，绕来绕去就在解释一件事：**AlphaProof Nexus 不是 AGI**。

原文怎么说？

> 「[AlphaProof Nexus] is a narrower research workflow advance.」

一个更窄的研究 workflow 进展。一个 narrower workflow。把"破解了挂 56 年的数学难题"翻译成"一个窄的工作流升级"，这个译法的语言学难度，比那 9 道难题还高（笑）。

接着他给 AGI 划线：

> 「[AGI must be] original, creative and have a wide range of skills across a multitude of areas, not just a specific one.」
>
> AGI 必须是原创的、有创意的、跨多个领域的，不只是一个特定领域。

划完线还补一句——同一周他在 Big Technology Podcast 上的版本：**"nowhere near"**——离 AGI 远着呢。

这句话听起来像谦虚。把这周日历上其他几件事翻一翻，谦虚的味道就不太对了。

**5 月 20 日**——AlphaProof Nexus 论文挂 arXiv 前一天——OpenAI 发布 GPT-5.2 Pro 把 1946 年的 Erdős planar-unit-distance 猜想"证伪了"（自然语言证明，没 Lean 验证）。openai.com/index/gpt-5-2-for-science-and-math/ 挂的官方博客。OpenAI 那条新闻挂出来，Hassabis 隔天就得回应。

**5 月 27 日**——美国 NIST CAISI（Trump 政府重组 Biden 时代 AISI 后的新机构）正式公开和 Google DeepMind、Microsoft、xAI 三家签的「预部署评估协议」。NIST 公告原文有一句很扎眼：

> 「developers frequently provide CAISI with models that have reduced or removed safeguards.」
>
> 开发商经常向 CAISI 提交去除了护栏的模型版本。

也就是说，DeepMind 已经把"去护栏版"的 Gemini 系列交给美国政府评估。Anthropic 不在协议里。OpenAI 当天也发了一份《Frontier Governance Framework》——openai.com/index/openai-frontier-governance-framework/——主动对齐加州 SB53 和欧盟 AI Act 的 GPAI Code of Practice。

**5 月 29 日**——加州 SB53「Transparency in Frontier AI Act」生效窗口前夜。

把这条时间线连起来——

5 月 20 日 OpenAI 破 1946 年猜想，5 月 21 日 DeepMind 破 9 道 Erdős，5 月 26 日 Hassabis 说"还不是 AGI"，5 月 27 日三家把无护栏模型交给国安部，5 月 29 日加州监管钟摆要落。

**"这不是 AGI"这句话，是 5 月 26 日上市公司 CEO 必须说出口的合规咒语。**

为什么？因为 AGI 是触发条款。

加州 SB53 对 frontier model 有 critical safety incident 报告义务。EU AI Act 对 systemic risk 的 GPAI 有强制评估义务。OpenAI 章程里有"AGI 出现则董事会有权 pause"条款。Microsoft - OpenAI 商业协议有"达到 AGI 则 Microsoft 算力授权终止"条款。Anthropic 自己 RSP（Responsible Scaling Policy）里把 ASL 等级和 capability 强绑定。

也就是说——**只要 CEO 嘴上承认"这是 AGI 了"，全行业的契约结构会同时翻一遍**。Microsoft 失去 OpenAI 的算力优先权。SB53 立即触发强制审计。Anthropic 触发 ASL-4 - 5 升级。所有融资文件里"在 AGI 出现前"的条款全部失效。

行业的契约语言，吊在"AGI 还没到"这根线上。

Hassabis 这周必须出来，把这根线再吊紧 3 年。「2029，plus or minus a year」——给市场一个能继续融资估值的盼头，又把法律触发推到 3 年后。彩排 practice run 这个词用得有水平：既承认这是 agent 时代了、又否认 agent 等于 AGI。

同一场专访里他还说 Anthropic 那个内部 codename「Mythos」是 「a good warning shot across the bow」（一发好的警告炮）——给政府和企业敲钟用的。

翻译一下——「友商那个东西已经够吓人到该给监管打个招呼的程度，但**我们的 AlphaProof Nexus 不算**，我们还是窄 workflow，监管不用现在动手。」

这是政治声明，不是技术声明。

谁掌握了 AGI 的定义权，谁就掌握了"什么时候触发监管"的开关。

破 9 道 Erdős 难题是结果。CEO 守住"这还不是 AGI"才是产品。

就这。

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>A goal post on a sports field being slowly moved farther away by an invisible hand, with multiple chalk-marked old positions visible on the ground showing previous locations, minimalist flat illustration, muted palette of slate gray, navy blue, and white, conceptual style, no text labels, clean background</pre></details>
</div>

---

## 三、Lean 4.27——这次真正的赢家不是 Gemini

回到论文。

AlphaProof Nexus 的架构在论文 §3 写得清楚。整套系统是一个叫「Ralph loop」的循环：一池子异步 subagent 用 P-UCB 采样从证明库里挑出"父草稿"，每个 subagent 开一个 Gemini 3.1 Pro 对话，做多轮链式推理，用 search-and-replace 工具改证明草稿。每一轮结束，subagent 在 **Lean** 里重新编译该草稿；一个 episode 结束时，**SafeVerify** 模块拿目标定理的规范说明书去验证草稿，并防止 agent 偷偷往证明里塞 axiom 蒙混。

如果草稿里还留着 `sorry`（Lean 里"这步先空着"的占位符），subagent 写一段反思评论、从当前草稿继续下一个 episode。如果 SafeVerify 验不过，整段回滚。

这套架构里，Gemini 3.1 Pro 负责"猜"。Lean 4.27 负责"判"。

Gemini 猜错了无所谓——下一轮再猜。Lean 一旦说"通过"，就是通过——后面没人能翻案。

论文里这套架构的具体特征：

| 角色 | 模型 | 作用 |
|---|---|---|
| 主推理 | Gemini 3.1 Pro | 多轮 CoT 改草稿 |
| 评估 | Gemini 3.0 Flash | 高吞吐 rating |
| 验证 | Lean 4.27 | 编译 + 类型检查 |
| 防作弊 | SafeVerify | 拦截 axiom 注入 |

**SafeVerify 这一关，是这次系统能跑通的真正命门**。

Lean 是一个基于依赖类型论（Calculus of Inductive Constructions 的变体）的证明助手。它的可信内核（trusted kernel）大约几千行代码。任何一个定理，在 Lean 里都会被 elaborate 成一个闭项（closed term）——这个项的**类型**就是命题、**构造**就是证明。kernel 只要做一件事：检查这个项的类型对不对。

通过了，意味着：在 mathlib 的公理体系里，这个证明可以独立由一台普通笔记本上的 lean4lean 再校验器（Mario Carneiro 写的独立实现）重新验证——不需要相信 DeepMind 没作弊，不需要相信 Gemini 没幻觉，不需要相信 OpenAI 那篇博客的英文措辞精确。

Gemini 写完证明，全世界任何一个数学家可以下载这个 .lean 文件，跑一遍 Lean 4.27，要么 PASS 要么 FAIL。

而 OpenAI 5 月 20 日那篇 "GPT-5.2 Pro 证伪 1946 planar-unit-distance 猜想"，没用 Lean。是自然语言证明。需要找审稿人读、找审稿人挑刺、等期刊接收。同样是当周大新闻，5 个月后能不能进 Annals of Mathematics 是另一回事——之前 OpenAI 前 VP Kevin Weil 宣称 GPT-5 "解了 10 道 Erdős" 那次，被陶哲轩等人发现其实只是"AI 在公开文献里检索到了已发表的解，重新表述了一遍"，后来 OpenAI 默默撤回。

这件事说明：**自然语言证明在 LLM 时代不再是有效凭证**。LLM 写得太流畅了，幻觉太自然，连"幻觉一个引理"都能写得像真的。审稿人需要花十倍时间挑出错。

而 Lean 不会被流畅说服。Lean 只认类型。

mathlib4 截至 2026 年 5 月 18 日：**274,045 条定理，130,791 条定义，772 位具名贡献者，超 200 万行 Lean 代码**。2026 年拿到了法国 Demailly 开放科学奖。mathlib 这套库是过去 6 年由全球数学家社区义务维护的——主要贡献者拿不到 Anthropic 的股权激励、不在 Google DeepMind 的 PIP（Performance Improvement Plan）名单上。

Lean 本身的故事更冷清。Lean 由 Leonardo de Moura（先在 Microsoft Research、后到 AWS）和 Sebastian Ullrich 在 2023 年 7 月共同创立 Lean FRO（Focused Research Organization），现在团队约 10 个人。2025 年拿了 ACM SIGPLAN 编程语言软件奖。

10 个人。一个非营利组织。

DeepMind 这次破 9 道 Erdős，靠的不是 Gemini 3.1 Pro 多聪明——Gemini 出错率高得很，否则也不会有 SafeVerify。**真正让这件事成立的，是 Lean 那个几千行的 kernel 加 200 万行的 mathlib**。

主角拿头条。配角拿名次。验证器拿了一句感谢。

Hassabis 那场 Axios 专访 7000 字，提 Lean 0 次。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：流程图
【副标题】：AlphaProof Nexus 的 Ralph loop 里，谁在猜、谁在判
【核心判断】：Gemini 负责猜，Lean 负责判——后者拒稿权才是这次系统能成的命门
【核心内容】：
  - 步骤1：父草稿池 P-UCB 采样
  - 步骤2：Gemini 3.1 Pro 多轮 CoT 改写
  - 步骤3：Lean 4.27 编译检查
  - 步骤4：SafeVerify 反 axiom 注入
  - 步骤5：通过则归档，失败则回滚重来</pre></details>
</div>

---

## 四、陶哲轩那张 wiki 表格里多了一行

数学社区怎么看这件事？看一手的——数学家自己写的字。

陶哲轩在 GitHub 上维护一份 wiki，地址是 `github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erdős-problems`，专门记录各家 AI 在 Erdős 问题上的真实贡献。表格里之前已经有：AlphaProof（2024 IMO）、Claude Opus 4.6 / 4.7、Gemini Deep Think、GPT-5.2 Thinking、GPT-5.4 Thinking、Seed 2.0 Pro。

2026 年 5 月底，表里加了一行 AlphaProof Nexus。

陶哲轩在 2026 年 1 月给出的基准判断是这样的：当时所有 LLM 加在一起，对公开 Erdős 问题的最大可处理比例约 1 - 2%。AlphaProof Nexus 这次 2.5%——比基准翻了一倍多一点，落在他给的"可能进步速度"区间内沿。

不是奇迹。是斜率改善。

陶哲轩本人在 Mastodon 上对这次具体怎么发帖，写稿截稿前没扒到原文（mathstodon.xyz 的 anti-bot 拦了几次）。能确认的是他在 wiki 上加了行字，没在博客上写专文。一个人对一件事的最大评价，是给它一行表格。

Timothy Gowers（高尔斯）的评价不一样。他是 Fields 奖得主、被 DeepMind 团队提前在论文发布前 brief 过，原话：

> 「The key word is verified. We're not talking about plausible arguments that might contain errors — these are machine-checked proofs of the same standard as any theorem in Lean's library.」
>
> 关键词是"被验证过的"。我们说的不是看起来合理可能有错的论证，是机器校验过、和 Lean 库里任何定理同等标准的证明。

> 「The fact that the hit rate is non-zero on genuinely hard problems changes the conversation.」
>
> 非零命中率本身就改变了对话。

Gowers 看到的也是 verified 这个词，不是 AI 那个词。同一周 OpenAI 那篇没经过 Lean 的"破解 1946 猜想"，他给的评价更短："a milestone"——一个里程碑，没说是不是数学里程碑。

Scott Aaronson 5 月那篇博客《Dispatches from the Possibly Last Days of Human Relevance》提了这次的 AlphaProof Nexus，提了一句他 UT Austin 同事 Swarat Chaudhuri 在 DeepMind 团队里、提了一句 Lean。标题里那个 "Possibly Last Days of Human Relevance" 是他的反讽——人类还没到无关紧要那天，但每次有这种新闻，他都得加一句 "possibly"，且要加越来越多。

三位有名有姓的数学家，三种反应。

陶哲轩——加一行表。

Gowers——强调 verified。

Aaronson——可能、可能、可能。

没有一个人欢呼。没有一个人焦虑。

数学家这周共识是：**有件事变了，但不是"AI 会做数学了"，是"人类终于有了一个不需要审稿人也能信任的 AI 输出"**。

这个共识里没有 AGI 三个字。

回到 Hassabis 那场专访。Axios 专访 7000 字，Hassabis 提了 AGI 大约 18 次，提了 Lean 0 次，提了 mathlib 0 次，提了 SafeVerify 0 次，提了陶哲轩 0 次，提了 Gowers 0 次。

提的最多的词是 "agentic"。

数学家们这周关心 Lean 4.27 那几千行 kernel 还能不能继续没 bug 地服役下去；CEO 这周关心 SB53 触发条款里"AGI" 这个词的定义到底由谁说了算。

这是两套完全不一样的语言体系。一套关心定理。一套关心估值和监管。中间那 9 道破了的 Erdős 难题，被两边各自挪用了一次——数学家拿它当 verifier 信任的证明，CEO 拿它当"我们离 AGI 还远但已经在彩排"的素材。

回到开头那个问题——这次真正的赢家是谁？

不是 Gemini 3.1 Pro。Gemini 出错率高、需要 SafeVerify 拦着；它只是 Ralph loop 里那个一直猜的小工。

不是 Hassabis。Hassabis 守住了 AGI 定义权的当下版本，但下次有新模型出来，他还得再画一遍线，下下次再画一遍。守门人没有终局。

不是 DeepMind 这次 11 万美元的实验预算。这点钱在 Google 内部不够付一位 staff engineer 一个月的工资。

赢家是 Lean 那个几千行的 kernel，是 mathlib 那 200 万行没人发奖金的代码，是 Leonardo de Moura 那 10 个人的非营利组织，是陶哲轩那张默默更新的 wiki 表格。

他们不出席发布会，不接受 Axios 专访，不参加白宫 AI 行政命令圆桌。他们安静地等下一次模型升级，把验证标准再卡紧一点。

整个 AI 行业用万亿美元估值、用「agent 时代彩排」、用「AGI 2029」这些话术，正在向一个本质上是数学家义务劳动的开源验证器要信用背书。

破 9 道难题是新闻。守住「这不是 AGI」是产品。

但真正在卖信用的，是 Lean。

而 Lean 没拿到一分钱。

就这。

## 数据来源

- [arXiv 2605.22763v1：Advancing Mathematics Research with AI-Driven Formal Proof Search](https://arxiv.org/abs/2605.22763)
- [arXiv 论文 HTML 版](https://arxiv.org/html/2605.22763v1)
- [GitHub：google-deepmind/alphaproof-nexus-results](https://github.com/google-deepmind/alphaproof-nexus-results)
- [Axios 专访：DeepMind CEO Demis Hassabis（2026-05-26，by Ina Fried）](https://www.axios.com/2026/05/26/deepmind-ceo-demis-hassabis)
- [Thomas Bloom 维护的 Erdős 公开问题清单](https://www.erdosproblems.com/)
- [Erdős 悬赏奖金档案](https://www.erdosproblems.com/prizes)
- [陶哲轩 GitHub wiki：AI Contributions to Erdős Problems](https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems)
- [Scott Aaronson 博客：Dispatches from the Possibly Last Days of Human Relevance](https://scottaaronson.blog/?p=9782)
- [DeepMind 官方博客：AI solves IMO problems at silver medal level（AlphaProof 2024）](https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/)
- [Nature 论文：AlphaProof（2025）](https://www.nature.com/articles/s41586-025-09833-y)
- [OpenAI：GPT-5.2 for Science and Math（2026-05-20）](https://openai.com/index/gpt-5-2-for-science-and-math/)
- [OpenAI Frontier Governance Framework（2026-05-29）](https://openai.com/index/openai-frontier-governance-framework/)
- [NIST CAISI 与 Google DeepMind / Microsoft / xAI 协议公告](https://content.govdelivery.com/accounts/USNIST/bulletins/415cadf)
- [mathlib4 仓库](https://github.com/leanprover-community/mathlib4)
- [mathlib 统计页](https://leanprover-community.github.io/mathlib_stats.html)
- [Lean 4 GitHub releases](https://github.com/leanprover/lean4/releases)
