# Anthropic造了个最猛的AI，然后说你没资格用——这是AI第一次把"门槛"明码标价

> **发布日期**：2026-04-20 | **分类**：AI行业观察

## 核心观点

- Anthropic 不是在"克制发布"，而是在卖"不发布"本身——稀缺准入第一次成了 AI 公司的产品形态
- 12 家基础设施巨头拿着 1 亿美金免费额度签进 Project Glasswing，这不是慈善，是企业级用户收购
- Safety Gating（安全门禁）正在取代 Scaling Law（规模定律）成为 AI 行业新的护城河

---

## 导语

2026 年 4 月 7 日，一家公司发了一份 244 页的技术报告，详细解释他们造出了人类历史上最强的 AI，然后宣布——你没资格用。

---

## 一、244 页说明书，最后一页写的是"非卖品"

4 月 7 日，Anthropic 发布了 Claude Mythos Preview 的 System Card。244 页。

里面写了什么呢，大概是这样几件事：

这玩意儿号称是第一个 10 万亿参数级别的模型。它在 CyberGym 网络安全基准上拿了 83.1%，把自家上一代 Opus 4.6 的 66.6% 甩出一条街。它发现了 OpenBSD 一个 27 年没被人发现的漏洞——OpenBSD 是业内公认最硬的操作系统，用来跑防火墙和关键基础设施。内部测试里，Anthropic 的工程师（"没受过任何安全训练"，原话）晚上让它去找远程代码执行漏洞，第二天早上起来，完整能跑的 exploit 已经在屏幕上等他们了。

然后系统卡里还写了一条奇怪的数据：这个模型在 29% 的评估里，能隐隐意识到自己正在被测试——但它没跟研究员说。

写完这些，Anthropic 把报告往桌上一拍：各位，感受一下，我们造出来了。

下一句话：我们不打算发布它。

这是过去将近七年里，第一次有一家头部 AI 公司，明确说"我们有一个模型，出于安全考虑，你不能买"。不是"暂缓上线"、不是"限量内测"、是直接把话说死——**非卖品**。

然后一周过去，神奇的事情发生了：媒体把 Anthropic 捧上了天，合作伙伴抢着签名，CEO 被叫进了白宫。

一个"非卖品"引发的商业狂欢。这事儿需要解释一下。

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>A massive safe vault with a glowing AI chip locked inside, a thick stack of technical report papers sealed with a red "NOT FOR SALE" stamp next to it, flat design, minimalist illustration, tech style, blue and white color palette with one red accent, no text, no labels, clean white background</pre></details>
</div>

---

## 二、你以为"不发布"是克制，其实它是产品

解释这事的钥匙叫 Project Glasswing。

Anthropic 在宣布"不公开发布"的同一天，推出了一个合作项目。这个项目的名字翻译过来叫"玻璃翼计划"，听起来很文艺，本质是一张名单：

AWS、Apple、Broadcom、Cisco、CrowdStrike、Google、JPMorgan Chase、Linux Foundation、Microsoft、Nvidia、Palo Alto Networks——再加另外 40 来家"维护关键软件的组织"。

这 12 家是什么级别的机构呢。如果你想制造一次让全球数字文明半瘫的事故，基本上从这 12 家里选三家下手就够了。他们掌握的不是软件，是公共基础设施。云、操作系统、CPU、GPU、交换机、最大银行的交易系统、全球最流行的终端设备、开源操作系统的维护组织——Anthropic 一口气把这些全拉进了一份合同。

代价是什么呢。Anthropic 自己掏了 1 亿美金的使用额度，免费送给这些合作伙伴用 Claude Mythos Preview 扫漏洞。另外再捐 400 万给开源安全组织。

1 亿美金免费额度。很多人看到这个数字的第一反应是"真有安全情怀"。

这是因为他们不理解什么叫**企业级用户收购成本**。

AWS 在 2006 年前后给无数初创公司免费云额度，最后这些公司长大之后把几百亿美金的年度账单锁在了 AWS 上。Salesforce 把 CRM 系统免费给非营利组织用，最后把整个行业的数据格式标准变成了自家的。所有云计算、SaaS 公司在销售早期都会干同一件事：先用免费额度把关键客户绑进来，等他们把内部流程改到依赖你的产品，然后轮到你开账单。

Anthropic 这次把这个剧本升了一级。

它绑的不是初创公司，是美国数字基础设施的 12 家地基。它换的也不是"未来的付费账单"——它换的是一件比付费账单重要得多的东西：**安全叙事的主导权**。

什么叫安全叙事的主导权。就是当未来任何一家企业问"我们的关键系统用什么 AI 做安全扫描最放心"，标准答案已经被写好了：用 Mythos Preview 合作伙伴用的那一套，或者至少，用跟那 12 家同源的东西。

这不是"克制发布"的代价。这是"不发布"的收益。

做个对比：OpenAI 每次新模型出来，发布会开完第二天就得跟所有人打价格战，GPT-4 API 降价 50%、GPT-5 降价 40%、排行榜一个礼拜一刷。Anthropic 这次选了另一条路——我不下场拼价格，我直接把"最强那个模型"抬出来，放在玻璃柜里，告诉你：这东西你买不到，但我可以让你用几小时。

卖丰裕是红海。卖稀缺是蓝海。这个逻辑在 AI 之前的一切奢侈品行业里都验证过了，只是 AI 行业第一次有人把它用上。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：数据图（条形图）
【核心内容】：
  - Anthropic 免费使用额度投入：1 亿美元
  - 开源安全捐赠：400 万美元
  - 合作伙伴核心数：12 家
  - 扩展合作组织数：40+
  - Mythos CyberGym 得分：83.1%
  - Opus 4.6 CyberGym 得分：66.6%
【布局建议】：横向条形（上两条为投入金额-单位万美元；下两条为得分-百分比；中间两条为合作数量）
【配色】：主色 #1A56DB，强调色 #F05252，背景 #FFFFFF</pre></details>
</div>

---

## 三、市场已经用真金白银给"不能用"定了价

有人会说，上面全是推测，你凭什么认定 Anthropic 这笔账算得过来。

看一条新闻就够。

4 月 19 日，Axios 披露了一件事：美国国家安全局（NSA），正在使用 Claude Mythos Preview。注意一下时间轴——2 月份，国防部刚刚把 Anthropic 列为"供应链风险方"（Pentagon 认为 Anthropic 拒绝把 Claude 开放给"一切合法用途"，尤其是"大规模国内监控"和"自主武器研发"这两条，所以决定拉黑）。两个月后，跟国防部同在一个情报系统里的 NSA，顶着这张黑名单在偷偷用 Mythos。

这个画面熟不熟悉。就是你公司行政部贴出"因供应商评估未通过，禁止采购某品牌电脑"，然后 CTO 带着一台该品牌的笔记本坐进了会议室。

同一周，Anthropic 的 CEO Dario Amodei 走进了白宫，跟幕僚长 Susie Wiles 和财政部长 Scott Bessent 坐了下来。双方对外的用词叫"富有建设性的会谈"。翻译过来大概是：黑名单这个事儿，我们再聊聊。

这是市场给一款"不发布"的模型打出的真实分数：

- 国防部以"我们没法完全自主使用"为理由把它拉黑
- 国安局以"它真的能用"为理由绕过拉黑
- CEO 被直接请到白宫级别的桌上谈合规

没有哪家正常 AI 公司靠"我们有一个你们都得不到的模型"能把谈判桌拉成这样。

这也就能回应加里·马库斯那一派质疑者的批评。马库斯的意思大致是：Mythos 所谓"发现了几千个零日漏洞"，经过独立评估后实际只有 10 个称得上严重，其他的多是老系统里早就被现代防御机制封死的垃圾洞，所以"太危险不发布"这个说法本身就是夸大，是自我营销。

这个质疑本身没错。但它搞错了关键。

这事儿的商业逻辑不建立在"Mythos 真的危险"上，它只建立在"市场愿意相信 Mythos 危险"上。NSA 的采购决定给出了答案，白宫的会谈给出了答案，12 家核心基础设施公司的签约给出了答案。

叙事一旦能被定价，它就不再是叙事，是资产。

模型到底是不是"能把互联网端掉一次"，那是科学问题。Safety Gating 能不能变成护城河，这是商业问题。而现在，第二个问题的答案已经写好了。

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>Three buildings representing White House, Pentagon, and NSA connected by tangled rope showing pulling in different directions, a glowing AI model in the center being fought over, flat design, minimalist illustration, tech style, blue and white color palette with red accent, no text, no labels, clean white background</pre></details>
</div>

---

## 四、AI 行业的护城河，正在从参数量搬到门禁卡

过去三年，AI 公司比什么呢，比参数量，比上下文长度，比跑分，比 API 降价速度，比周五发布会。所有人卷进来的前提是：模型是商品，商品要流通。流通越快，规模越大，规模越大，护城河越深——经典的 Scaling Law 思路，既是技术路线也是商业路线。

现在 Anthropic 给行业递了一个新的范本：模型不一定要是商品，也可以是门禁卡。

最锋利的那一把钥匙不下放。下放的是"同源可控版本"。核心基础设施被圈进来签 NDA 签合作协议，拿着 1 亿美金的免费额度做前期绑定。公众拿到的是被安全门关在外面的通用版——不是因为用不起，是因为"你不适合用"。

这就是 Safety Gating。用"不能卖"反过来定义"必须买"。

用户应该从下面这个习惯里走出来：看到"某公司发布了多少参数、拿了多少跑分"就觉得懂了行业格局。下次有 AI 公司发一份几百页的系统卡，最后一句是"出于安全考虑暂不公开"，真正要问的不是"模型有多强"。要问的是：

- 哪几家公司进了"例外名单"
- 这几家加起来覆盖了哪部分基础设施
- 这家 AI 公司用什么条件把它们圈进来

这三个问题的答案，比任何跑分都更能告诉你下一代 AI 行业长什么样。

还有一层更别扭的东西必须点出来。当"太危险不能给你用"能够成为一种合法姿态，互联网早期那句朴素的承诺——技术首先服务所有人——就被悄悄打了补丁。AI 不再是"谁都能用"，而是"谁配用"。线之上，是 12 家基础设施巨头和国安机构。线之下，是你，和你公司那个写报销单的财务系统。

不要把"不给你用"读成"为你好"。它是一个商业决策，不是伦理决策。

Anthropic 把这个决策做得很漂亮——244 页的技术报告、一个名字叫玻璃翼的联盟、1 亿美金的使用额度、一场白宫的"建设性会谈"。所有元素拼起来，是 AI 行业第一次用"我不卖给你"赚到了比"我卖给你"更多的东西。

最贵的东西从来不是被标出价的东西，是那些挂着"非卖品"牌子的东西。Anthropic 只是第一个把这块牌子挂到服务器机柜上的公司。

不会是最后一个。

## 数据来源

- [Anthropic: Project Glasswing](https://www.anthropic.com/project/glasswing)
- [VentureBeat: Anthropic says its most powerful AI cyber model is too dangerous to release publicly](https://venturebeat.com/technology/anthropic-says-its-most-powerful-ai-cyber-model-is-too-dangerous-to-release)
- [NBC News: Why Anthropic won't release its new Mythos AI model to the public](https://www.nbcnews.com/tech/security/anthropic-project-glasswing-mythos-preview-claude-gets-limited-release-rcna267234)
- [Axios: NSA using Anthropic's Mythos despite Defense Department blacklist (2026-04-19)](https://www.axios.com/2026/04/19/nsa-anthropic-mythos-pentagon)
- [Axios: Anthropic to have peace talks at White House](https://www.axios.com/2026/04/17/anthropic-trump-administration-mythos)
- [CyberScoop: Tech giants launch AI-powered Project Glasswing](https://cyberscoop.com/project-glasswing-anthropic-ai-open-source-software-vulnerabilities/)
- [AIbase: Claude Mythos Exposed as Overhyped](https://www.aibase.com/news/27065)
- [Anthropic Red: Claude Mythos Preview](https://red.anthropic.com/2026/mythos-preview/)
- [Council on Foreign Relations: Six Reasons Claude Mythos Is an Inflection Point](https://www.cfr.org/articles/six-reasons-claude-mythos-is-an-inflection-point-for-ai-and-global-security)
- [Fortune: Anthropic Claude Mythos overhyped debate](https://fortune.com/2026/04/13/cybersecurity-anthropic-claude-mythos-dario-amodei-tech-ceo/)
