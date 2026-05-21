# AI 药监局开张那天，开源连排队的资格都没有

> **发布日期**：2026-05-09 | **分类**：AI · 监管 · 行业格局

## 核心观点

- Mythos 跑了那天，触发的不是惩罚，是一张比对手更早办下来的牌照
- CAISI 不是新建监管，是把五家公司的内部流程升级成行业入场券
- FDA 类比从结构上把开源排除——监管不需要禁令，只要让它扛不起合规风险

---

## 导语

四月七号，Anthropic 发了一个能在 Firefox 里挖出 271 个漏洞的模型。一个月后，白宫拿着这件事的灰，给 AI 行业糊了一座药监局。第一个进门的，正是当初点火的那家。

---

## 1. 一个月的剧本

事情得从四月七号说起。

那天 Anthropic 发了一个内部代号叫 Mythos 的模型。不是用来写小作文的，也不是用来做客服的——这玩意儿是用来挖洞的。在 Firefox 里挖出 271 个高危漏洞，自动写出 181 个能跑的 exploit；在 OpenBSD 里翻出一个躺了 27 年的安全 bug，没人发现；在 FFmpeg 里揪出一个埋了 16 年的雷。每一个，都是工业级速度。

Anthropic 不傻，发布的时候没一把撒到全网，搞了个项目叫 Glasswing，意思是"只发给守城的人"。听起来很美——把武器优先发给警察，匪徒就抢不到。

匪徒抢到了。

Anthropic 自己承认，发布后不久，Mythos 通过私有渠道被未授权访问。翻译过来就是：我们造了个工业级开锁工具，发给了一批我们认证的"防御者"，然后这工具被偷走了。具体被谁偷走、偷走之后做了什么，到现在没有公开答案。

四月底，副总统 Vance 开始给 CEO 们打电话，包括 Anthropic 的 Dario Amodei。五月二号，Pentagon 的 CTO 公开把 Mythos 称为更广义的"网络时刻"。五月五号，Commerce 部下属的 CAISI（AI 标准与创新中心）跟 Google DeepMind、Microsoft、xAI 签了发布前评估协议——OpenAI 和 Anthropic 早就签了，2024 年就在里面。第二天，国家经济委员会主任 Hassett 接受彭博采访，原话是："就像 FDA 管药一样，AI 也要在被证明安全之后再放进野外。"

一个月，五件事，一条直线：闯祸 → 失控 → 高层会议 → 拉拢同行 → FDA 比喻官方化。

你以为这是政府终于醒了。

不是。这是 Anthropic 赢了。

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>A regulatory building with a fancy front door, line of corporate logos waiting outside, one figure already inside holding a key, abstract editorial illustration, flat design, minimalist, tech style, blue and white color palette, no text, no labels, clean white background</pre></details>
</div>

---

## 2. Mythos 不是模型，是导火索

Mythos 不是 Anthropic 第一次发模型，但它是 Anthropic 第一次用一个模型把华盛顿吓到。

把数字摆在桌面上：271 个 Firefox 高危漏洞、181 个跑得起来的 exploit、一个躺了 27 年的 OpenBSD bug、一个埋了 16 年的 FFmpeg 雷。Anthropic 自己的红队在公开报告里写得很骄傲——"thousands of high-severity vulnerabilities, including some in every major operating system and web browser"。每一个主流操作系统、每一个主流浏览器，都被它扫过一遍，都留了血。

发布的时候，Anthropic 套了个项目叫 Glasswing。这个项目对外的宣传是：发给关键基础设施的防御者，让他们抢在攻击者之前把洞补上。听上去这是责任感，仔细一拆——它在结构上做了三件事。

第一，模型不开放权重，只给授权的合作伙伴用 API 访问。第二，参与方要签 NDA，签完才知道自己签的是什么。第三，所有"危险能力"的演示，最先看到的不是用户，是评估机构。

Anthropic 在 4 月 7 号把 Mythos Preview 文档发出来的时候，文档不是给开发者看的，是给政策官员看的。那份文档的副本，几乎同步出现在了 UK AISI 的评估博客里、出现在 Just Security 的政策分析里、出现在 Washington Post 4 月 24 号的头版。

然后 Mythos 被未授权访问了。

Anthropic 那边的措辞非常专业："正在调查潜在的未授权访问。"白宫的反应不专业——administration officials 直接要求 Anthropic 停止扩展 Mythos 的访问权限，把项目按住。国家网络主任 Sean Cairncross 被点名领头处理这事。

这个时间点上，Anthropic 失去了对自己造的工具的控制权。但它收获了别的东西。

Mythos 之前，AI 风险在华盛顿是个抽象命题——很多场会、很多份报告、没人真的怕。Mythos 之后，"AI 能在 60 秒内黑掉一个银行"成了一个可以放进国会听证会的具体威胁。Anthropic 没有写过这句话，但它发了一个能让这句话成立的模型。

四月底，VP Vance 打电话约谈 CEO 圈。会议没有公开纪要，但有公开结果——五月五号，CAISI 的协议清单上，从 OpenAI / Anthropic 两家，扩到了五家。

Mythos 在 Glasswing 里被关住没？没。在用户手里发挥了"防御者"作用没？暂时没有。但它替 Anthropic 完成了一件最贵的事：把"AI 风险"从空气变成了铁条。

铁条做出来之后，下一步是把别人也圈进去。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary>【图类型】：条形图
【副标题】：Mythos Preview 在主流软件里挖出的洞
【单位】：个
【核心判断】：发布一个工业级挖洞工具，比写一万份政策报告有效
【核心内容】：
  - Firefox 高危漏洞 [流出]：271
  - Firefox 已写出 exploit [流出]：181
  - OpenBSD 沉睡漏洞年限 [参照]：27
  - FFmpeg 沉睡漏洞年限 [参照]：16</pre></details>
</div>

---

## 3. CAISI 不是 FDA，是 VIP 通道

外面在传 CAISI 是"AI 版 FDA"。这个定位害人。

CAISI 全名 Center for AI Standards and Innovation，挂在商务部下面，是 NIST AI Safety Institute 在 Trump 政府里的更名版。它在五月五号宣布的事是这样的——已经完成了 40 多次模型评估，包括对未公开的前沿系统的评估；现在跟 Google DeepMind、Microsoft、xAI 三家签了新协议，给政府发布前的访问权。

CAISI 内部之前是谁？OpenAI 和 Anthropic。2024 年就在里面了。

把这两件事放在一起看，你就会发现一个很有意思的细节：CAISI 不是被 Mythos 倒逼出来的。它早就存在。它一直在跑评估。它只是在 Mythos 之后，把会员名单从两家扩到了五家，然后给这件事配了一个 FDA 的故事。

这五家，全部是闭源前沿大厂。

CAISI 评估怎么跑？文件原文是这样写的：developers frequently hand over versions of their models with safety guardrails stripped back so the centre can probe for national security risks。翻译一下：开发者主动交出"卸了护栏"的模型，让中心去试它最危险的能力。

这件事本身就值得多看两眼。

一个普通公司不会把自家产品的"卸甲版"主动交给政府。一个汽车厂不会把刹车系统拆掉给监管员开。一个药厂不会主动把降低剂量的安全冗余拆掉，让 FDA 去试一下三倍剂量会不会死人。但 AI 公司会。为啥？

因为这件事的功能不是"让监管知道你危险"，而是"让监管确认只有你能让自己不危险"。

你卸下护栏给政府看一眼——看，没有我，这玩意儿能干这些坏事。然后你把护栏装回去——所以你需要我，我会负责任地把它装回去。这是一次反向广告。监管是观众，不是裁判。

CAISI 现在做了 40 多次评估。每一次评估的输出，是一份机密文件，是一次安全签证，是一张"这家公司有能力管住自己的模型"的盖章。这张章，在五月五号之前，只有两家有；五月五号之后，多了三家；总共五家。

这五家，加在一起，覆盖了美国前沿 AI 几乎全部的产业能力。

剩下的呢？开源社区——Mistral、DeepSeek、Llama 家族、Qwen 家族——他们不在名单里。不是被禁，是没接口。CAISI 的工作流是"开发者交模型 → 中心评估 → 出报告"。开源权重一旦发布到 Hugging Face，就没有"开发者交"这一步了。它在你那儿，也在所有人那儿，没有"提交"这个动作。

所以"CAISI 评估"这件事，对开源是个空概念。

监管框架默认你能交模型。开源默认你不需要交。两者直接错过。

错过的结果是：CAISI 评估这张章，开源拿不到。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary>【图类型】：对账图
【副标题】：CAISI 入场名单 vs 没接口的玩家
【核心判断】：监管不需要禁开源，它只要发只有闭源能拿的牌照
【核心内容】：
  - 闭源·已在 CAISI（2024）[流入]：2
  - 闭源·新加入（2026/5/5）[流入]：3
  - CAISI 已完成评估次数 [流入]：40
  - 开源·能交闭源版给政府的 [流出]：0
  - 开源·全球可下载的前沿模型家族 [流出]：5</pre></details>
</div>

---

## 4. FDA 类比里那个永远不会被讨论的 bug

把 Hassett 5 月 6 号的原话再贴一遍：

> "We're studying possibly an executive order to give a clear roadmap to everybody about how this is going to go and how future AIs that also potentially create vulnerabilities should go through a process so that they're released to the wild after they've been proven safe, just like an FDA drug."

"like an FDA drug"。

很多人听到这话，第一反应是：这挺好啊，至少安全标准统一了。

把 FDA 拆开看一下。FDA 管药，靠的是三件具体的事——有一个固定的化合物分子式；有一个可量化的剂量；有一个明确的适应症。基于这三件事，你才能跑随机对照试验，你才能算副作用，你才能在事后召回——批号召回，因为药有批次，每一支药都有身份。

AI 模型有这三件事吗？

模型没有"分子式"。同一个 base model 上面叠几个微调，行为可以从写作家变成黑客。模型没有"剂量"。一个 prompt 跟另一个 prompt 之间，模型能力差几个数量级。模型没有"适应症"。Mythos 自己的官方定位是 general-purpose——通用模型，不是 cyber 模型。它做的事是"通用智能在 cyber 任务上的副作用"。

FDA 那一套审查方法论，套在 AI 上是个空架子。AEI（美国企业研究所）5 月 6 号的政策评论说得直白：白宫的 AI 审查提案是 bad policy，因为它假设了一个根本不存在的"通过/失败"的分界线。

但请注意，AEI 反对的是政策合理性。这跟我说的不是一件事。

这个类比的"bug"恰恰是它的功能。

第一，它好懂。FDA 是美国人最熟的监管机构之一。把 AI 套进 FDA，普通人立刻有了一个心智模型——"哦，就跟管药一样"。这是一个公关上的胜利，比写十份白皮书有效。

第二，它把焦点引向"模型本身安全不安全"，而不是"谁有权决定模型上市"。FDA 的争议永远在某种药要不要批；FDA 不会被讨论"为什么这家药厂能交申请、那家不能"——这部分被默认了。AI 套上 FDA 之后，公众讨论被同样地默认到了"评估流程"上，而把"谁有资格被评估"这个真正的市场结构问题，悄悄留在了门外。

第三，也是最关键的——FDA 有召回权，AI"FDA"没有。

一个药品出问题，FDA 可以批号召回，不许再卖。一个 AI 模型一旦权重开放出去，全世界已经下载到本地了，没有任何机构有"召回"权——下载发生的那一瞬间，模型就脱离了任何政府的物理触达范围。

这件事的政策含义是：AI"FDA"对开放权重模型不仅没接口，而且没意义。它评估完了也没法收回。

所以政策必然滑向另一个方向——把"未经评估的模型用于关键基础设施"定为责任标准。这不是禁止开源，是给开源的部署方算合规账。一个银行用 Llama 做内部 agent，律师就要算：万一出事，监管那边会问，你用的模型走 CAISI 流程没？没走？那就是疏忽。

到这一步，监管不需要明文禁开源，开源就在企业市场被定价定到关门。

AEI 说这是 bad policy。它说得对。但这个"坏"不是一个 bug，是商业上想要的 feature。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary>【图类型】：流程图
【副标题】：FDA 三件套 vs AI"FDA"
【核心判断】：FDA 类比之所以被白宫挑中，正是因为它在 AI 上对不上号
【核心内容】：
  - FDA 步骤1：固定化合物分子式
  - FDA 步骤2：剂量与适应症明确
  - FDA 步骤3：随机对照试验可证伪
  - FDA 步骤4：批号可召回
  - AI"FDA"步骤1：模型权重不固定（微调即变）
  - AI"FDA"步骤2：能力随 prompt 浮动
  - AI"FDA"步骤3：评估只能采样不能穷举
  - AI"FDA"步骤4：开放权重永不可召回</pre></details>
</div>

---

## 5. 闯祸的人不会被罚，只会被发牌照

回头看 Anthropic 在这一个月里的处境。

它造的 Mythos 跑了。它被白宫点名要求暂停扩展访问。它的 CEO 被 VP 约谈。它在 Pentagon 那边吃了闭门羹——Pentagon CTO 公开说 Mythos 是个"cyber moment"，明确不打算跟 Anthropic 和解。

按"出事"的标准看，这是一个完美的危机。

按结果看，它是一次升级。

CAISI 的协议清单从两家扩到五家——Anthropic 是那两家之一。FDA 类比是 Hassett 在彭博的采访里讲出来的——讲的时候 Anthropic 已经在那个体系里两年。EO 草案要做的事，是把"未经评估的模型"挡在关键基础设施之外——Anthropic 的所有模型，从 Mythos 到 Claude Code，都在评估之内。

它没被罚。它没被禁。它甚至没被收税。它得到的处罚是：被多发了一张其他人没有的会员卡。

新加入的三家是 Google DeepMind、Microsoft、xAI。看起来像是被拉进来分享荣誉，实际上是被拉进来一起举牌。这五家手里举着的牌写着同一个字——"合规"。这个字在 5 月 5 号之前是公司的内部口号，5 月 5 号之后会变成政府采购合同里的一行硬性要求。

开源社区不在这五家里面。开源社区也进不来——CAISI 的工作流默认你能交一个闭源版本，开源社区交不出来。它只能被这套监管框架包绕，绕到企业不敢买它，绕到关键基础设施不敢用它，绕到风投不敢投它。

监管的尽头不是约束，是发牌照。这件事，每一个被监管过的行业都见过——出租车牌、医生资格证、银行牌照、电视台执照。每一次套上一个"安全"的故事，最先受益的都是已经在里面的人。

Mythos 跑掉那天，Anthropic 失去了一个模型。Anthropic 拿回来的，是一张比对手更早办下来的牌照——而办这张牌照的衙门，是它自己出事那一天才被白宫想起来的那个。

写完 EO 那天，开源排在门外，连排队的资格都没有。

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>An ornate license certificate with embossed seal lying on a desk under warm lamplight, an open empty doorway leading to a long line of figures in the dark outside, abstract editorial illustration, flat design, minimalist, tech style, blue and gold color palette, no text, no labels, clean white background</pre></details>
</div>

## 数据来源

- [CNBC: Trump admin moves further into AI oversight (2026.5.5)](https://www.cnbc.com/2026/05/05/ai-oversight-trump-google-microsoft-xai.html)
- [The Hill: White House may review AI models 'like an FDA drug' (2026.5.6)](https://thehill.com/policy/technology/5866292-white-house-ai-evaluation-process/)
- [Bloomberg: White House Preps Order to Boost AI Security, Hassett Says (2026.5.6)](https://www.bloomberg.com/news/articles/2026-05-06/white-house-preps-order-to-boost-ai-security-hassett-says)
- [Anthropic Red: Claude Mythos Preview](https://red.anthropic.com/2026/mythos-preview/)
- [UK AISI: Evaluation of Claude Mythos Preview's cyber capabilities](https://www.aisi.gov.uk/blog/our-evaluation-of-claude-mythos-previews-cyber-capabilities)
- [Washington Post: AI hacking fears jolt Washington as Anthropic unveils Mythos (2026.4.24)](https://www.washingtonpost.com/technology/2026/04/24/anthropic-mythos-ai-washington-cybersecurity-hacking-risk/)
- [The Hill: Pentagon CTO rules out resolution with Anthropic, calls Mythos a broader 'cyber moment'](https://thehill.com/policy/technology/5868214-pentagon-anthropic-mythos/)
- [CNN: Microsoft, Google and xAI will let the government test their AI models before launch (2026.5.5)](https://www.cnn.com/2026/05/05/tech/microsoft-google-xai-government-test-ai-models)
- [CNBC: Anthropic's Mythos set off a cybersecurity 'hysteria' (2026.5.8)](https://www.cnbc.com/2026/05/08/anthropic-mythos-ai-cybersecurity-banks.html)
- [Fortune: Trump administration suddenly embraces AI oversight ideas it once rejected (2026.5.6)](https://fortune.com/2026/05/06/trump-administration-embraces-ai-oversight-policies-it-once-rejected-anthropic-mythos-caisi/)
- [AEI: White House AI Vetting Proposal Is Bad Policy](https://www.aei.org/technology-and-innovation/white-house-ai-vetting-proposal-is-bad-policy/)
- [The Register: Trump jumps from 'anything goes' to 'strict regulation' AI policy (2026.5.8)](https://www.theregister.com/ai-and-ml/2026/05/08/trump-jumps-from-anything-goes-to-strict-regulation-ai-policy/5234687)
