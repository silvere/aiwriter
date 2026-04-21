# Meta花了140亿，买了个"不用再装开源理想主义"的许可证

> **发布日期**：2026-04-21 | **分类**：AI行业观察

## 核心观点

- Meta的"开源理想主义"从来不是信仰，是打不过OpenAI时的战术工具
- 140亿买Wang，一半买技术，一半买"我可以不再是开源派"的剧本切换费
- 谁在大声拥抱开源，翻译过来就是"目前我排不到第一梯队"

---

## 导语

4月8日，Meta发布了Muse Spark。

这是Alexandr Wang去年6月被扎克伯格用143亿美金抢到Meta、成立Meta Superintelligence Labs之后，9个月憋出来的第一个大动作。

这事儿听起来像个翻身仗——Llama 4去年翻了车，140亿买来一个28岁的小孩重做一遍，现在Intelligence Index从18分干到52分，排进全球前五。

但故事的真正核心不在这里。

事情的核心是：Meta发这个模型的第一件事，是把自己供奉了三年的开源神龛，悄悄拆了。

Muse Spark不开源。

三年前被Meta自己写了两千字檄文捧上天的"Open Source AI is the Path Forward"（完整翻译：开源AI是人类前进的道路），在2026年4月8日这一天，事先不通知粉丝，静默下架。

没有悼词，没有鞠躬，没有交代。

就这。

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>A dismantled wooden altar or shrine being quietly taken apart in the background, while a shiny new tech product is unveiled in the foreground spotlight, flat design, minimalist illustration, tech style, blue and gray color palette, cinematic composition, no text, no labels, clean white background</pre></details>
</div>

---

## 一、三年前那篇"开源宣言"，究竟讲的是什么故事

要看懂这事儿，先得回到2023年。

那年2月，Meta悄悄把第一代Llama的权重"泄露"给了研究圈。几周后，社区反应起来了，Meta顺势承认：这就是我们的开源战略。2023年7月，Llama 2正式开源商用免费。

彼时，OpenAI的GPT-4已经把API价格抬到天上，Anthropic跟着闭源收费，Google还在用各种Gemini演示视频画大饼。

Meta的位置是什么？

Meta的位置是：自研模型追不上GPT-4，但我有Facebook、Instagram、WhatsApp三十亿日活——我手上有的是场景，缺的是别人已经跑在前面的模型能力。

这时候扎克伯格做了一件聪明的事：把"追不上"包装成"送给全世界"。

开源变成了一种叙事武器。你付费用GPT-4？我Llama 2免费给你。你想做企业落地？我开源你自己部署。你担心数据隐私？我权重下载到本地。

开发者很感动。学术圈很感动。监管部门很感动——"啊Meta是民主化AI的推动者"。

唯一不感动的是OpenAI，因为它的API生意被从下面挖墙脚。

这就是Meta开源战略的真实功能：**它是用"免费"把对手的收费模型打成"值不值"的选择题**。

2024年7月，扎克伯格写了一篇两千多字的公开信，标题叫"Open Source AI Is the Path Forward"。通篇讲开源对人类、对开发者、对美国创新生态多么重要。

写得情真意切，像个理想主义者。

但理想主义者不会在两年后，自己憋出一个更强的模型时，连招呼都不打就关门上锁。

战术家会。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：对比图
【核心内容】：Meta开源/闭源时间线
  - 2023年2月：Llama 1 权重泄露（被动开源）
  - 2023年7月：Llama 2 正式开源商用
  - 2024年4月：Llama 3 全线开源
  - 2024年7月：扎克伯格发《Open Source AI Is the Path Forward》
  - 2025年4月：Llama 4 开源，被指基准作弊
  - 2025年6月：143亿收购Scale AI 49%股权，挖走Wang
  - 2026年4月：Muse Spark 发布，闭源
【布局建议】：横向时间轴
【配色】：主色 #1A56DB，强调色 #F05252，背景 #FFFFFF</pre></details>
</div>

---

## 二、Llama 4 是那根压断信仰的稻草

2025年4月，Meta发布了Llama 4，包括Scout和Maverick两个版本。

发布时的宣传口径是：性能对标GPT-4o，开源，可商用，权重全放。

然后独立研究员开始跑基准测试，发现了一个小问题——Meta在LMArena上送测的Maverick版本，和给开发者下载的版本，不是同一个。

送测的那份经过了专门的对话格式优化。通俗的说法叫"应试微调"。不通俗的说法叫作弊。

社区一夜之间从欢迎变成嘲讽。Reddit的r/LocalLLaMA板块开始流行一句话："Meta的基准分，除以2再用。"

这不是Meta第一次被骂，但这是第一次Meta的"开源人设"被骂。

**因为开源的道德制高点，是建立在"不装X"这个前提上的。**

你闭源收费，用户不会骂你作弊，因为用户不知道你里面是什么——反正花钱买产品，体感不行就不续费。

你开源免费，全世界都能审查你的权重、你的训练方式、你的测评流程。作弊一次，信仰崩一半。

Llama 4的故事真正吓到扎克伯格的，可能不是"我们模型不够强"，而是"我们连'开源'这张牌都打不干净了"。

开源本来是Meta在AI竞赛里握着的一张"道德牌+用户牌"。打赢的时候它是护城河，打输的时候它是抽血机——因为越开源越多人发现你不行。

这时候扎克伯格面临一道选择题：

A. 继续做开源，死磕Llama 5，把道德牌攥到发烂。  
B. 从"我们开源"切换到"我们有钱"，换个故事重来一遍。

他选B。

2025年6月，143亿美金砸进Scale AI，49%非投票股权，顺便把28岁的Alexandr Wang抢过来，给了他一个连Meta都没设过的新头衔：Chief AI Officer。

与此同时，Meta AI被重组。Yann LeCun领导的FAIR被边缘化（几个月后LeCun也宣布离职）。一个全新的部门"Meta Superintelligence Labs"凭空出现。

所有跟Llama过去相关的人和事，被装进了旧抽屉。

换人、换部门、换命名体系（从动物系的Llama换到文艺系的Muse），换叙事（从"开源民主化AI"换到"personal superintelligence"）。

这一整套动作，翻译成大白话是：我们要开始讲一个新故事了，之前那个不算数了。

143亿，付的主要不是工资，是这张故事切换的许可证费。

---

## 三、Muse Spark的真实水位：从掉队追到打平手

数据放一下（来自独立第三方Artificial Analysis）：

- Muse Spark 在Intelligence Index上拿52分
- Gemini 3.1 Pro Preview：57分
- GPT-5.4 Thinking：57分
- Claude Opus 4.6：53分
- Llama 4 Maverick（Meta自家上一代）：18分

9个月时间，Meta从18分跑到52分，这是真涨。但跑到52分之后，它还是第四名。

Health领域有亮点：HealthBench Hard 42.8分，确实全球第一——Meta花钱请了1000多位医生参与训练，垂直领域堆人堆出来的。

但在ARC AGI 2这种纯抽象推理测试上，Muse Spark只有42.5分。对面Gemini 3.1 Pro 76.5，GPT-5.4 76.1。差了三分之一。

这个模型的真实评价，不是"翻身"，是"终于进场"。

一个"刚刚能打"的模型，为什么第一件事是闭源？

这是整个故事最关键的那个问题。

答案不复杂：**开源作为战术，只在你追不上的时候有用。**

追不上的时候，你送给世界免费用，至少能挖对手的墙角、挖对手的收费模式、挖对手的开发者生态。这时候你的模型弱一点没关系，你的定位是"免费大礼包"。

追上来了——哪怕只是追到打平手——继续开源就开始亏了。

因为你现在的模型每免费放出去一个权重，都是在给自己的下游竞争对手（做API转卖的、做部署服务的、做垂直小模型的）送子弹。你自己辛辛苦苦训出来的能力，别人拿去收钱，你还要倒贴GPU。

更重要的是：当你的模型能跟GPT-5.4打个七七八八的时候，闭源的API收入预期才终于有了算术意义。

Meta 2026年AI资本开支指引：1150-1350亿美金。

接近上一年的两倍。

花这种钱做出来的东西，免费发到Hugging Face上？这不是理想主义，这是财务事故。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：数据图（条形图）
【核心内容】：Intelligence Index 2026年4月
  - Gemini 3.1 Pro Preview：57
  - GPT-5.4 Thinking：57
  - Claude Opus 4.6：53
  - Muse Spark：52
  - Llama 4 Maverick（Meta上一代）：18
【布局建议】：横向条形
【配色】：主色 #1A56DB，强调色 #F05252，背景 #FFFFFF</pre></details>
</div>

---

## 四、谁在拥抱开源，谁在装睡——一张产业位次表

这事儿真要看清楚，你得把2026年几个头部玩家的开源姿势摊开看。

**从不开源的：OpenAI、Anthropic。**

它们从GPT-3、Claude 1开始就闭源。市场领头位置，不需要用"免费"做叙事，API收入扎实得很。没装过理想，也不用切换。

**一直开源的：DeepSeek、Qwen、Mistral的部分模型。**

DeepSeek V4依然放权重。Qwen3.6系列继续开源。这些玩家现在的位置，恰好类似2023年的Meta——模型能力在追赶期，开源是它们挖美国对手墙角最好用的那把铲子。等到有一天它们真的追上了头部，我几乎可以打包票：开源这把铲子会被收回抽屉。

**从开源转闭源的：Meta。**

Llama三年，Muse Spark一步。转的时机踩得精准——不早不晚，在"终于能打"但"还没领先"的那个刻度上。

**从闭源偶尔开源的：Google。**

Gemma系列开源，Gemini正主闭源。这是"一脚在门里一脚在门外"的标准动作——Gemma让学术圈有面子，Gemini给股东有收入。

四种姿势，背后是同一个规律：**开源不是价值观，是位置报表。**

你看一家公司在某个时间点开不开源，大概率能倒推出它在这个赛道的自我定位——不是领先，就是认了。

所以下次再看到某家大厂的CEO在主旨演讲里放出一张slide，上面写着"We embrace open source as a core value"，先不用感动，先掏手机查它最新一代模型的Benchmark。

要是前三，这是做公益。  
要是前十，这是卖广告。  
要是三十名开外，这是找同伴。

---

## 五、结尾

Muse Spark不是Meta堕落，是Meta终于可以不装了。

143亿买的不是一个28岁CEO，是一个"剧本切换"的许可证。Llama的开源神龛被悄悄拆走，不是因为Meta变坏了，是因为Meta终于不需要"免费"这条护城河了——它的钱烧到了每年一千三百亿美金这个量级，再讲情怀讲不过去。

真正该警惕的不是"Meta闭源"这件事，是下一次有某个科技巨头站在台上，深情地告诉你"开源是AI民主化的未来"。

别感动。

先问他：你今年第几名。

## 数据来源

- [Meta debuts Muse Spark model - TechCrunch (2026-04-08)](https://techcrunch.com/2026/04/08/meta-debuts-the-muse-spark-model-in-a-ground-up-overhaul-of-its-ai/)
- [Meta unveils Muse Spark - Fortune (2026-04-08)](https://fortune.com/2026/04/08/meta-unveils-muse-spark-mark-zuckerberg-ai-push/)
- [Muse Spark benchmarks - Artificial Analysis](https://artificialanalysis.ai/models/muse-spark)
- [Goodbye Llama - VentureBeat (2026-04)](https://venturebeat.com/technology/goodbye-llama-meta-launches-new-proprietary-ai-model-muse-spark-first-since)
- [Meta's Muse Spark is closed source - The Register (2026-04-08)](https://www.theregister.com/2026/04/08/meta_muse_spark/)
- [Meta debuts first major AI model since $14B Scale AI deal - CNBC (2026-04-08)](https://www.cnbc.com/2026/04/08/meta-debuts-first-major-ai-model-since-14-billion-deal-to-bring-in-alexandr-wang.html)
- [Scale AI's Alexandr Wang confirms departure - CNBC (2025-06)](https://www.cnbc.com/2025/06/12/scale-ai-founder-wang-announces-exit-for-meta-part-of-14-billion-deal.html)
- [Meta's Muse Spark AI Model - Built In](https://builtin.com/articles/meta-muse-spark-ai-model)

