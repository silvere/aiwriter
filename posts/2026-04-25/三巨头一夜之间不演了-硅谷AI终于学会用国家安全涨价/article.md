# 三巨头一夜之间不演了：硅谷AI终于学会用"国家安全"涨价

> **发布日期**：2026-04-25 | **分类**：AI与产业

## 核心观点

- 美国三巨头不再相互厮杀，不是因为团结，是因为发现"管制"比"竞争"更赚钱
- 把 ToS 违约升级为"国家攻击"，是一次精准的话术工程——事实没变，叙事变了
- 下一阶段的 AI 护城河不是模型能力，是 API 的"持牌经营资格"

---

## 导语

OpenAI、Anthropic、Google——这三家公司平时干嘛？互相挖工程师，互相抢客户，互相在发布会上踩对方。结果上周，他们一起开了个会。然后白宫发了个备忘录。然后 Google 把 400 亿砸进 Anthropic 的怀里。然后 DeepSeek 把 V4 甩出来。三天，四件事，没一件是巧合。

---

## 一、三家死对头突然站到一起，时间凑得有点过分

我们先把过去 72 小时按时间排一下。

4 月 22 日：Anthropic 自家那个"太危险不能公开"的 Mythos 模型，被一个第三方供应商路径的私人论坛黑了。Anthropic 在博客里承认了。

4 月 23 日：白宫科技政策办公室发布备忘录 NSTM-4，标题是《对美国 AI 模型的对抗性蒸馏》（Adversarial Distillation of American AI Models），把 2 月 Anthropic 指控中国三家公司的事，正式升级为政府层面的姿态。

4 月 24 日上午：Google 官宣投资 Anthropic 100 亿美元现金、外加 300 亿条件追加，估值 3500 亿。这家公司自己有 Gemini，但它在花真金白银扶持自己的"竞争对手"。

4 月 24 日下午：DeepSeek 把 V4 推了出去。1M token 上下文，论文里大方写着："我们用了 On-Policy Distillation，从 10 个 teacher 模型学。"

四件事。三天。

孤立看任何一件，你都能找到一个解释。Mythos 被黑是个安全事故。白宫备忘录是个例行政策。Google 投 Anthropic 是个商业操作。DeepSeek 发 V4 是个产品发布。但把时间线拉开一点看，孤立的解释就站不住了。

从今年 2 月 Anthropic 公开点名 DeepSeek、Moonshot、MiniMax，到 4 月 7 日 OpenAI、Anthropic、Google 通过 Frontier Model Forum 宣布共享"攻击模式数据"，再到上周白宫拍板——三个月，从"一家公司发的博客"，变成"行业三巨头联防"，再变成"白宫文件"。

这是一条非常工整的话术升级路径。一件原本属于"商业纠纷"的事，被一步一步抬到了"国家安全"。

而最关键的一点是：在这个过程里，**三家平时互相拆台的公司，一句争吵都没有**。

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>Three corporate executives in suits standing together holding hands raised up like an alliance, behind them three different colored logos converging into one shield, dramatic lighting, flat design, minimalist illustration, tech style, blue and white color palette, no text, no labels, clean white background</pre></details>
</div>

---

## 二、同一件事，2024 年是违约，2026 年是国家攻击

来看一下 Anthropic 控诉的"蒸馏攻击"具体是个什么事。

2 月 23 日，Anthropic 发文点名 DeepSeek、Moonshot、MiniMax，说这三家用大约 2.4 万个虚假账号，跟 Claude 跑了 1600 万次对话，目的是从输出里反向提炼能力——这就是模型蒸馏。MiniMax 1300 万次最多，Moonshot 340 万次，DeepSeek 15 万次最少但最精准，专挑 Claude 在推理、工具使用、强化学习评分这些关键能力上的输出来薅。

听起来很严重。然后你去看 DeepSeek 的研究论文。

DeepSeek V3 的技术报告里就大大方方写着用了知识蒸馏。V4 的论文更进一步，介绍了 On-Policy Distillation（OPD）：让学生模型自己生成回答，然后让 10 个不同领域的"老师"逐 token 给反馈、调分布。论文公开发，代码部分开源，方法在 arXiv 上挂着。

这事不是中国独有。OpenAI 自己用蒸馏训练过 GPT-4 Turbo。Anthropic 用蒸馏从 Opus 蒸出 Sonnet 和 Haiku。Google 用蒸馏出 Gemini Flash。任何一家做大模型的，蒸馏都是标配。

那 Anthropic 控诉的到底是什么？是 DeepSeek 用了 Claude 的输出去蒸——也就是用了别人家的 API 而没付钱（或者说没付到 Anthropic 觉得"够"）。这本质是 Terms of Service 违约。是商业纠纷。

2024 年，OpenAI 也指控过 DeepSeek 干同样的事。当时 OpenAI 怎么处理的？发了个声明，封了几个账号，然后没了下文。它没要求白宫介入，也没把这事拉到"国家安全"层面。

到了 2026 年，画风彻底变了。Anthropic 的措辞是"工业级蒸馏攻击"、"对抗性蒸馏"、"威胁国家安全"、"破坏出口管制"。然后 OpenAI 跟 Google 几乎同步背书。然后白宫备忘录跟上。

事实层面没有什么新东西。蒸馏在 2024 年是蒸馏，在 2026 年还是蒸馏。账号是假的——但 2024 年的假账号也是假的。变化的不是行为，是定性。

马斯克在 X 上贴脸开大："How dare they steal what Anthropic stole from human programmers."（他们怎么敢偷 Anthropic 从人类程序员那里偷来的东西。）这话糙理不糙——它戳破的不是中国清白，而是这套话术升级本身的滑稽。

Anthropic 拿全人类写的代码训练自己的模型，叫"开放科学"。DeepSeek 拿 Anthropic 模型的输出训练自己的模型，叫"对抗性国家威胁"。

这不是事实判断，这是叙事工程。

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>A symbolic illustration showing a large factory labeled with neural network patterns siphoning data from a globe, while a smaller factory siphons from the larger one - both factories are doing the same thing but only one is highlighted as a threat, flat design, minimalist illustration, tech style, blue and red contrast palette, no text, no labels, clean white background</pre></details>
</div>

---

## 三、三巨头不是在打中国，是在解决一个共同的麻烦

要理解为什么是这个时间点，要先看三家的财务。

Anthropic 4 月年化收入 300 亿美元，比 2025 年底的 90 亿翻了 3 倍。OpenAI 4 月月收入 20 亿美元，年化 240 亿，估值 8520 亿。xAI 每月烧 10 亿美元，刚被 SpaceX 用全股票交易吞下，合并体准备 6 月以 1.75 万亿估值在纳斯达克 IPO。

数字漂亮。但漂亮的数字下面，有一个所有人都不愿意公开承认的事——三家的产品差距正在收窄。

GPT-5.4、Claude Opus 4.6、Gemini 3.1 Pro 在主流 benchmark 上互有胜负，没有谁能甩开谁。API 价格呢？Claude Opus 4.6 每百万 token 输入 5 美元、输出 25 美元；GPT-5.4 是 2.5 美元和 15 美元。Sonnet 和 Haiku 跟 GPT-5.4 mini、Gemini Flash 之间，价格已经压到一两美元的差距。

这就是 OPEC 在 70 年代面对的局面。三家产品同质化，价格往下走，每家都在亏。继续打价格战，谁先撑不住谁先死，撑下来的也只剩一口气。

这种局面下，最理性的选择从来不是"团结对外"，是"集体涨价"。但赤裸的涨价同盟会被反垄断盯上——美国 FTC 在 2025 年刚审过一轮 AI 公司间的协调嫌疑。所以三家需要一个东西：一个能让"我们的 API 不卖给某些人"听上去正当的理由。

"国家安全"是一个完美的理由。

监管层喜欢——它让 AI 公司变成可控的政策杠杆。媒体喜欢——它让本来枯燥的产业新闻有了反派。投资人喜欢——它把 API 价格从"商业服务"变成"许可证商品"，许可证商品的毛利率永远比商业服务高。

而最重要的是，"国家安全"叙事完成之后，三家可以光明正大做这些事而不被追责：限制中国 IP 调用、要求企业客户走 KYC（了解你的客户）流程、设置敏感行业溢价、对"高风险"地区索取额外授权费。

这些动作的真名叫"价格歧视"。但披上"国家安全"外衣之后，它的名字叫"合规"。

Frontier Model Forum 不是一个反华联盟，它是一个 OPEC——只不过它卖的不是石油，是 token。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：对账图
【副标题】：三巨头烧的钱 vs 卖的钱
【单位】：亿美元
【核心判断】：产品差距在收窄，烧钱在加速——这种局面下，"对外联防"才是最理性的选择
【核心内容】：
  - Anthropic 年化收入 [流入]：300
  - OpenAI 年化收入 [流入]：240
  - xAI 年烧钱（月10亿×12）[流出]：120
  - OpenAI 最新一轮融资 [参照]：1220
  - Anthropic 最新Google加注 [参照]：400</pre></details>
</div>

---

## 四、下一阶段不是"卡中国"，是"持牌运营"

这盘棋的下一步不难推。

把"蒸馏"重新定义成"对抗性蒸馏"——已经走完。白宫的 NSTM-4 备忘录目前还只是姿态，没有新的法律，但备忘录里那句"未来执法行动可能跟进"是钉子，钉子已经下去了。大概率在 2026 年下半年，会出现 API 访问的实质性管制：高级模型 API 调用要走 KYC 审查，敏感行业要单独许可证，对"受关注国家和地区"默认拒绝接入。这套东西早就有现成模板，叫 EAR（出口管制条例），过去管的是芯片和加密技术。

之后是行业洗牌。能拿到许可证的公司变成"持牌 AI 运营商"，毛利率向公用事业靠拢。拿不到的中小模型公司被挤出顶级合规客户市场。开源模型继续可用，但企业敢不敢用是另一回事——HR 和法务部门会用脚投票。

对在中国写代码、用 AI 的人来说，这意味着两件具体的事。

技术栈选型逻辑要变。"用最好的模型"这个标准会被"用合规的模型"覆盖。海外 API 的可用性会从默认稳定，变成默认不稳定。国内大模型的真实价值不在跑分多高，而在它不会因为某天的政策变化突然断供。

另一件事——别再期待这场"蒸馏争议"会有一个事实层面的真相裁决。它不需要真相。它需要的是叙事胜利。美国三巨头要的不是 DeepSeek 道歉，是把 API 访问权变成可以收牌照费的东西。

OpenAI 嘴上说的是 AI 安全。Anthropic 嘴上说的是负责任地部署。Google 嘴上说的是开放生态。它们心里算的是同一个东西——以后这门生意，不许新人随便进来。

欢迎来到 AI 的牌照时代。你以为你在选模型，其实模型在选你。

## 数据来源

- [Bloomberg：OpenAI, Anthropic, Google Unite to Combat Model Copying in China（2026-04-06）](https://www.bloomberg.com/news/articles/2026-04-06/openai-anthropic-google-unite-to-combat-model-copying-in-china)
- [CNBC：Anthropic accuses DeepSeek, Moonshot and MiniMax of distillation attacks on Claude（2026-02-24）](https://www.cnbc.com/2026/02/24/anthropic-openai-china-firms-distillation-deepseek.html)
- [Defense One：China has 'deliberate, industrial-scale campaigns' to steal US AI models, White House says（2026-04-23）](https://www.defenseone.com/threats/2026/04/china-steal-ai-models/413103/)
- [TechCrunch：Google to invest up to $40B in Anthropic in cash and compute（2026-04-24）](https://techcrunch.com/2026/04/24/google-to-invest-up-to-40b-in-anthropic-in-cash-and-compute/)
- [Asia Times：US sounds alarm on China's AI distillation as DeepSeek V4 debuts（2026-04）](https://asiatimes.com/2026/04/us-sounds-alarm-on-chinas-ai-distillation-as-deepseek-v4-debuts/)
- [Euronews：Hackers breach Anthropic's 'too dangerous to release' Mythos AI model（2026-04-22）](https://www.euronews.com/next/2026/04/22/hackers-breach-anthropics-too-dangerous-to-release-mythos-ai-model-report)
- [Fortune：Anthropic claims 3 Chinese companies ripped it off（2026-02-24）](https://fortune.com/2026/02/24/anthropic-china-deepseek-theft-claude-distillation-copyright-national-security/)
- [SaaStr：Anthropic Just Passed OpenAI in Revenue（2026-04）](https://www.saastr.com/anthropic-just-passed-openai-in-revenue-while-spending-4x-less-to-train-their-models/)
- [The Hacker News：Anthropic Says Chinese AI Firms Used 16 Million Claude Queries to Copy Model](https://thehackernews.com/2026/02/anthropic-says-chinese-ai-firms-used-16.html)
- [White House OSTP NSTM-4: Adversarial Distillation of American AI Models（2026-04-23）](https://rits.shanghai.nyu.edu/ai/white-house-memo-targets-adversarial-distillation-of-u-s-ai-models)
