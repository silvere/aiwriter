# 马斯克救 Anthropic？是两个落水的人在互相踩对方上岸

> **发布日期**：2026-05-18 | **分类**：AI 行业拆解

## 核心观点

- 5 月 6 日同一天发生四件事——Anthropic 拿下 SpaceX 的 22 万张 GPU、马斯克宣布 xAI 解散并入 SpaceXAI、马斯克在 X 说"恶人探测器没响"、三个月前他刚骂 Anthropic"恨西方文明"。中文媒体把这串戏剧性事件包装成"马斯克放下偏见、算力时代来临"——这是错的剧本
- Anthropic 不是赢家，是被 Claude Code 限速暴动逼到三月以来无路可走：Amazon、Google、Microsoft 的算力承诺加起来 $380B 起步，但全要 2027 年才能上线。能立刻上电的，只有马斯克手里那批闲置硅锭
- 马斯克也不是施舍，是 xAI 11 个共同创始人全跑光、SpaceX 下个月就要 IPO，Colossus 1 这块"账面包袱"必须在路演前换成 Fortune 估算的 $3-4B/年现金流。xAI 当天解散并入 SpaceXAI 这步法律重组，恰好让 Anthropic 可以假装"我租的是航天公司不是竞品"

---

## 一、马斯克的"恶人探测器"，三个月前刚把 Anthropic 测成"恨西方文明"

时间线先摆这里，别急着解读。

2 月 27 日，Anthropic CEO Dario Amodei 在公司博客上画了两条红线：不允许 Claude 被用于大规模国内监控，不允许用于无人类监督的自主武器。这是回应美国国防部一份要 Anthropic 同意"all lawful purposes"的合同模板。Anthropic 宁可丢合同，也不松口。

同一天，国防部副部长 Emil Michael 在 X 上指控 Anthropic 试图把 Claude 早期版本的"宪法"文档从互联网上抹掉。马斯克转发了那条贴，加了一句话——

> "Anthropic hates Western Civilization."

中文译过来叫"Anthropic 痛恨西方文明"。这不是嘴上抱怨，这是把一家 AI 公司贴上叛徒标签。在 2 月底之前的几周，马斯克在 X 上还多次说过 Anthropic 是"misanthropic and evil"——这一套话术在 Anthropic 拒绝 Pentagon 的窗口里密集打了好几发。

然后是 5 月初。5 月 1 日 CNN Business、5 月 3 日 Breaking Defense、5 月 4 日 gHacks 接力报道同一件事：美国国防部一口气和 8 家科技公司签 IL6/IL7 级别（最高机密网络）AI 部署协议——OpenAI、Google、Microsoft、AWS、Oracle、NVIDIA、SpaceX、Reflection AI——独独把 Anthropic 排在门外。理由是"供应链风险 + 合同纠纷"。Anthropic 转头起诉特朗普政府，加州联邦法官给了禁令，但禁令挡不住这种"事实上的不签"——Pentagon 不签就是不签，法院没法判 8 家公司必须取消合同腾出位子来。

到这一步，国防部已经替马斯克兑现了那句"hates Western Civilization"。Anthropic 被拉黑，SpaceX 进了榜。

5 月 6 日，Anthropic 官博出现了一行公告——SpaceX 把 Colossus 1 整个超算的算力全租给 Anthropic：22 万多张 NVIDIA GPU（H100、H200、还有下一代 GB200），超过 300 兆瓦电力，"在一个月内"交付。所有 Claude Code 用户的 5 小时配额翻倍，Pro 和 Max 取消峰值时段压制，Opus 系列 API 限速大幅放宽。

同一天，马斯克在 X 上贴了一段话——

> "Everyone I met was highly competent and cared a great deal about doing the right thing. No one set off my evil detector. So long as they engage in critical self-examination, Claude will probably be good."

翻译：我见的每一个人都能力很强、都很在乎把事情做对，没有人触发我的恶人探测器，只要他们持续做自我审查，Claude 大概率会是好东西。

这就是过去 9 周的全部表演。

2 月 27 日：Anthropic 恨西方文明。  
5 月 4 日：国防部把 Anthropic 拉黑。  
5 月 6 日：Anthropic 大概率是好东西。  

中间也没发生什么具体的化解事件。Anthropic 还是那个 Anthropic，红线还是那两条红线。变的只是：5 月 6 日同一天马斯克宣布要把这 22 万张 GPU 租给对方。

恶人探测器是个很诚实的仪器——它对着合同条款会响，对着钱包不响。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：流程
【副标题】：从"恨西方文明"到"大概率是好东西"的 68 天
【核心内容】：
  - 02-27 Musk："恨西方文明"
  - 05-01 Pentagon 拉黑 Anthropic
  - 05-04 8 家 AI 大单签订
  - 05-06 SpaceX 租算力给 Anthropic
  - 05-06 Musk："恶人探测器没响"</pre></details>
</div>

---

## 二、Anthropic 不是赢了，是被 Claude Code 用户在 GitHub 上围攻三个月

中文媒体上关于 SpaceX 这单的所有叙事，都把 Anthropic 写成赢家——"AI 大女主拿下 22 万张 GPU"、"Claude 算力翻倍"。

要这么写也行，前提是你得跳过过去 9 周里 Claude Code 用户的 GitHub Issues 区。

3 月 23 日，Claude Code 的付费用户开始大规模在 Reddit、X、GitHub 上喊救命。MacRumors 3 月 26 日整理了一份用户投诉合集：单次 prompt 烧掉 3% 到 7% 的会话配额，原本号称 5 小时的会话窗口最快 19 分钟见底。Max 20x 这一档是 $200 一个月、Anthropic 卖给最重度用户的旗舰订阅——好几个用户在 GitHub Issue #41930 里贴出截图：从 21% 跳到 100%，中间只发了一个 prompt。

The Register 3 月 31 日跟进。一位安全研究员逆向了 Claude Code 的二进制，发现两个独立的 caching bug 把实际 token 消耗放大了 10 到 20 倍。本来应该从 cache 里读旧上下文、只对新 token 计费，bug 触发后每一轮都重算全部历史。一个 $100 的 Max 5x 用户在峰值时段被 throttle + caching bug 双杀，实际可用 token 量被压到接近免费用户。

Anthropic 没沉默，但回得很难听。3 月 26 日 Anthropic 工程师 Thariq Shihipar 在 X 上承认——

> "We are intentionally adjusting 5-hour session limits to manage growing demand."

翻译：我们正在故意调整 5 小时会话上限，因为需求涨太快了。

这是把"我们偷偷限速"这件事改名叫"故意管理需求"。"故意"是关键字——这不是 bug，是产品决定。付了 $200 的用户没法在条款里找到这条，但 Anthropic 在管理。

到 5 月 6 日，这场暴动已经烧了 6 个礼拜，GitHub Issue #41930 没关。

同一天，Dario Amodei 在一场公开活动上把账摊出来：Anthropic 2026 年第一季度按收入年化口径增长了 80 倍——原本规划的是 10 倍——这就是他的原话："we planned for 10x, we got 80x"。还有一句更要命的："it's just crazy"，"too hard to handle"。CNBC、VentureBeat、Cryptopolitan、Fortune 各自当天报道，引语一致。Anthropic 当时的收入 run rate 是 $300 亿一年。一年前的 1 月还是 $1 亿。这家公司在 12 个月里把收入跑出了 300 倍。

收入跑出 300 倍，配套的算力本来应该早就备好——但备好的速度，赶不上烧的速度。Anthropic 自己披露的算力承诺清单看着很长——

- **Amazon**：5 GW 上限，超过 $1000 亿，10 年期
- **Google + Broadcom**：5 GW，五年 $2000 亿，**2027 年开始上线**
- **Microsoft + NVIDIA**：$300 亿 Azure 算力
- **Fluidstack**：$500 亿美国 AI 基础设施
- **SpaceX Colossus 1**：300 兆瓦，**一个月内**

加总一下，过去 12 个月披露的算力承诺是 $3800 亿以上量级。对照收入 run rate $300 亿——Anthropic 用未来 5 到 10 年的合同，覆盖了今年 12 倍的开销。这本身已经够魔幻，但更魔幻的是：Amazon 那笔上限 5 GW、Google 那笔 5 GW，全要 2027 年才开始通电；Microsoft 那笔走 Azure，Azure 自己今年也吃紧；Fluidstack 那笔还在规划阶段。

所以 Anthropic 在 5 月初手里能立刻吃到嘴里的算力，是 0。

不是少，是 0。

5 月 6 日同一天交付（"在一个月内"）的，只有马斯克手里那批闲着烧折旧的硅锭。

这就是这单交易的真实形状——Anthropic 不是在选合作伙伴，是只有一家可选。马斯克手里这 22 万张 GPU 是 2025 年下半年才点亮的，规模在那个时间点全球第一，xAI 自己训 Grok 4 / Grok 4.3 用不完，整套 Colossus 1 一停转就要烧电费、烧折旧、烧人工。Anthropic 是唯一愿意把它整个吃下来的人——OpenAI 当然不会，因为 OpenAI 是马斯克的诉讼对手；Google、Meta 各自有 TPU / MTIA；中型 AI 公司吃不下 300 兆瓦。剩下 Anthropic 一个。

把 9 周的时间线拉直你就看清楚了——

3 月 23 日 Anthropic 限速暴动开始，3 月 26 日 Anthropic 自己工程师在 X 承认是"故意调"。  
5 月 6 日 Anthropic 拿到 SpaceX 整个超算，当天宣布所有付费档限速翻倍、峰值压制取消、Opus API 限速大幅放宽。

这不叫"算力时代来临"，这叫"我们用最后一根稻草把暴动压回去了"。

Anthropic 这单不是赢，是续了一口气。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：条形
【副标题】：Anthropic 算力承诺 vs 当前收入 run rate
【单位】：十亿美元
【核心判断】：3800 亿美元承诺只有 300 亿美元收入接住，且 2027 前能上线的只有 300 兆瓦
【核心内容】：
  - Google + Broadcom 五年承诺：200
  - Amazon 十年承诺：100
  - Fluidstack 基建合作：50
  - Microsoft + NVIDIA 承诺：30
  - 2026 收入 run rate [参照]：30
【备注】：单位均为十亿美元；除 SpaceX 外其他承诺均要 2027 起才能上线</pre></details>
</div>

---

## 三、马斯克也不是施舍，是 xAI 烧不动了、SpaceX 下个月要 IPO

5 月 6 日同一天还发生了第三件事。

马斯克在 X 上回复 Sawyer Merritt 一条问"xAI 怎么办"的帖，写了一句话——

> "xAI will be dissolved as a separate company, so it will just be SpaceXAI, the AI products from SpaceX."

翻译：xAI 作为独立公司将被解散，以后就叫 SpaceXAI，是 SpaceX 旗下的 AI 产品。

后面跟了一句更狠的：

> "xAI was not built right first time around, so is being rebuilt from the foundations up."

翻译：xAI 第一次没建对，所以现在从地基往上重建。

这是马斯克本人亲口说的。今年 2 月 2 日 SpaceX 全股票收购 xAI 时估值 $2500 亿，三个月后老板自己出来说"第一次没建对"。这种话从他嘴里说出来，是一种事后追认。追认什么？追认 xAI 已经死了。

3 月 28 日是个关键时间点。媒体当天盘点 xAI 的共同创始人——11 人全部离开，只剩马斯克一个。这是 11 走 11，不是 5 走 6 那种逐步流失。包括 Greg Yang、Igor Babuschkin、Christian Szegedy、Jimmy Ba 这一长串 2024 年高调一起出来"对抗 OpenAI 的封闭"的名字，2026 年初全跑光了。

为什么跑？看模型迭代节奏就懂。Grok 4 / Grok 4.3 在 2026 年的上线节奏明显跟不上 GPT-5 系列和 Claude Opus 4.6 / 4.7。Anthropic 5 月发 Opus 4.7、OpenAI 那边走自己的 GPT-5.x 路线，xAI 这边声音越来越小。没有共同创始人愿意留下来给一个声音越来越小的项目当殉葬品。

Colossus 1 这块超算就是在这个背景下变成"账面包袱"的。

这块超算 2025 年下半年点亮时是世界第一规模，22 万张 H100 / H200 / GB200，300 兆瓦电力。每天什么都不干都在烧电——按工业电价 $0.06/kWh、满负载 24h 算，光电费一天就是 $43 万，一个月 $1300 万；再加 22 万张 GPU 的折旧（H100 单卡 $30k 起、按 4 年折）、冷却、人工、维护，养这块超算的口径月成本进 $1 亿是合理估算。原本算盘是用它把 Grok 训出来追上 OpenAI 和 Anthropic，结果一年下来 Grok 没追上，超算还得养。这是教科书"沉没成本"。

然后 SpaceX 自己有另一件大事压头上——IPO。Axios 5 月 7 日的报道里直接写了一句：SpaceX IPO 预期在"下个月"。Stocktwits 5 月 8 日的标题更明白："SpaceXAI Takes Off: Elon Musk Consolidates AI Empire Ahead Of Massive IPO"。Musk 整合 AI 业务、压低 xAI 那个泡沫估值、把烧钱的超算变成"年化收入资产"，是给 SpaceX 招股书做账。

Fortune 5 月 7 日估算这单租给 Anthropic 的合同，能给 SpaceX 带来 $30 亿到 $40 亿一年的收入，毛利率高到现金利润超过 $25 亿。当然这是 Fortune 估的，不是合同披露的——Anthropic 和 SpaceX 双方都没披露总价、合同期。但即使打折一半，对一家航天公司来说，这笔钱意味着招股书可以新增一行"AI 算力业务"，估值乘数能直接往上跳一档。

把这三件事放一起看——

xAI 烧不动了 + SpaceX 要 IPO 了 + 全球只有 Anthropic 一家肯出这个价。

这不是"马斯克放下偏见拥抱对手"。这是马斯克在路演前把仓库里最大的一块库存出清。

最妙的还是 xAI 解散这一步法律重组。如果不解散，Anthropic 是没法租 xAI 那块超算的——直接竞品互供算力，合规过不去，董事会也过不去。但 xAI 一旦解散并入 SpaceX，房东就变成"私营航天公司"。SpaceX 不卖大模型给企业，Anthropic 卖；SpaceX 客户群是政府和卫星运营商，Anthropic 客户群是开发者和企业。两家在主营上不竞争，租算力天经地义。

至于 SpaceXAI 内部还在做 Grok、Anthropic 租来的 GPU 上跑的是 Claude——这件事所有人都假装看不见。

公司治理上有个词叫"换马甲签合同"。这单子是这个词的活体演示。

但换马甲只是第一层 PPT。这单合同里还藏着第二层——面向二级市场基金经理那一层。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：流程
【副标题】：xAI 解散 + Anthropic 接盘的法律白手套
【核心内容】：
  - 02-02 SpaceX $2500 亿全股票收购 xAI
  - 03-28 11 位共同创始人全部离开
  - 05-06 xAI 解散并入 SpaceXAI
  - 05-06 Anthropic 租走 Colossus 1
  - 下月 SpaceX IPO 路演启动</pre></details>
</div>

---

## 四、"数 GW 太空算力"，是给 SpaceX 投资人写的 PPT

5 月 6 日 Anthropic 那篇官博里，有一句话被中文媒体疯狂转发——Anthropic 和 SpaceX 表达了"合作开发数 GW（multiple gigawatts）级轨道 AI 算力"的意向。

中文圈把这句话翻译成"AI 算力进入太空时代"、"星际算力大决战"、"Anthropic 要把数据中心送上轨道"。一夜之间各家公众号又有了一个十年题材。

要不要查一下，2026 年 5 月人类把多少张 H100 送上了轨道。

Starcloud 是目前唯一一家把 GPU 真送上轨道的公司。Starcloud-1 卫星 2025 年 11 月发射，载荷是**一张** H100，做的事情是训了一个 NanoGPT 莎士比亚全集。NanoGPT 是 Andrej Karpathy 用来教学的玩具模型，参数量 1000 万级别，能跑通就算成功。Starcloud-2 计划 2026 年 10 月发射，载荷是**一张** H100 加**一张** Blackwell B200，外加一块 AWS 服务器刀片——顺带挖比特币，免得卫星上电没事干。

这是 2026 年人类在轨 AI 算力的全部家底。一张 H100 满载 700 瓦，两张加一起约 1.5 千瓦。Anthropic 官博里说的"数 GW"是至少 20 亿瓦——从 1.5 千瓦到 20 亿瓦，差约 130 万倍。

中间隔着至少四件基础物理问题：真空环境靠辐射散热（GW 级热量散热板面积比数据中心本体大几倍）、低轨高能粒子让民用 H100 MTBF 短一个数量级、星间激光链路单链 100 Gbps 比张量同步带宽差三个数量级、20 亿瓦太阳能板平摊到低轨要 30 平方公里。任意一件都是 10 年以上的工程问题，加起来超出 2030 年代上半段的可行范围。

Anthropic 的官博文案撰稿人不会不知道。马斯克更不会不知道。这句话本来就不是写给工程师看的——这句话是写给二级市场基金经理看的。

SpaceX 招股书一旦递出去，"我们已经和顶级 AI 公司就 GW 级轨道算力达成意向"这一行，可以给整个估值模型加上一个"未来 10 年新业务"的 multiple。

300 兆瓦是真金白银的 2026 年合同。GW 级是写给 PPT 的 2030 年代愿景。两个数字放一起，前面那个像真的，后面那个就不像假的了——用兑现的小承诺，包装一个永远不用兑现的大承诺。

中文媒体喜欢把后面那个数字单拎出来当头条。这是免费给 SpaceX IPO 打广告。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：对账
【副标题】：300 兆瓦地面 vs 数 GW 太空，前者是合同，后者是 PPT
【单位】：瓦
【核心判断】：差约 130 万倍，且四个基础物理问题都没解
【核心内容】：
  - Colossus 1 已交付 [流入]：300000000
  - Starcloud-1 在轨 [流出]：700
  - Starcloud-2 计划 [流出]：1500
  - 数 GW 太空算力意向 [流入]：2000000000
【备注】：在轨 GPU 当前合计 1.5 千瓦，距离 GW 级差约 130 万倍</pre></details>
</div>

---

## 五、两个落水的人，互相把对方踩成救命稻草

把 5 月 6 日同一天的四件事按时间顺序对照——

早上，Anthropic 官博：我们拿下 SpaceX Colossus 1 整套算力，付费用户限速翻倍。这一条把"我快撑不住了"包装成"我又收获了"。

接近中午，SpaceX 这边配合：是的我们租给 Anthropic 了。这一条把"我有块烧钱包袱要变现"包装成"我又签了个大客户"。

下午，马斯克在 X 上贴"恶人探测器没响"。这一条把"我前几周还在喊它恨西方文明"包装成"我一直是开明的人"。

晚上，马斯克再补一条：xAI 解散并入 SpaceXAI。这一条把"我一年花 $2500 亿建的公司死了 11 个创始人"包装成"我在做战略整合"。

四件事各自都是告急。四件事拼起来，被媒体写成"AI 行业新格局诞生"。

这种集体性的"把告急包装成胜利"，是 AI 大厂这一年的标准动作。Anthropic 半年里把 $3800 亿算力承诺写进官博、把 80 倍年化增长说成"crazy"——背后是收入接不住、用户在 GitHub 围攻。马斯克半年里把 xAI 卖给 SpaceX 时挂 $2500 亿估值、三个月后亲口承认"第一次没建对"——背后是创始人跑光、模型掉队。两边都在用一套"我赢了"的修辞，给一份"我快撑不住"的财务表打掩护。

二级市场吃这一套。一级市场上 Anthropic 估值奔万亿、SpaceX IPO 准备路演——背后的逻辑是"既然两家都说自己赢了，那一定都在赢"。Bernstein 分析师 Stacy Rasgon 已经公开质疑过 NVIDIA-OpenAI-Microsoft 那条循环交易链，Anthropic 这边的链更长：NVIDIA 投钱给 Anthropic 让它买 NVIDIA GPU，Amazon / Google 投钱给 Anthropic 让它买 AWS / GCP，SpaceX 现在直接租算力把收入做进 IPO 估值。所有 AI 估值都建在"对方付钱给我"的双向承诺上，所有的双向承诺都建在"未来融资覆盖未来开销"的滚动预期上，所有的滚动预期都建在"两家都在赢"的市场共识上。任何一环 default，整张网都会快速塌。

5 月 6 日这一天，这张网又加固了一圈。

但加固和塌方在表面上是一回事。一根绳上多打两个结，绳本身没变粗。多打的那两个结只是给路过的人看，让他们以为绳能再承重一吨。

具体怎么检验我说的对不对，给你两个可证伪的观察点——

第一，看 Q3 Anthropic Claude Code 会不会再涨价。今年 5 月 14 日 Anthropic 已经把第三方 Agent 调用从订阅里剥离出去单独按 API 计费——那是 5 月 14 日。如果 SpaceX 这单算力够用，5 月 14 日那刀就是最后一刀。如果 Q3 又来一刀（更高的月费、更紧的配额、更多的剥离），就证明 22 万张 GPU 也接不住 80 倍增长。

第二，看 SpaceX 招股书里 AI 算力收入占总收入的比重。如果占比是个位数，那这 22 万张 GPU 对 SpaceX 来说就是"路过的额外收入"，Fortune 估算的 $3-4B 大概率掺水。如果占比上两位数，那 SpaceX 就是真把火箭公司当 AI 房东在卖——你愿不愿意按"火箭 + 算力"组合估值，是另一个问题。

两个观察点都很硬。前者最快 Q3 出结论，后者最快下个月递招股书。

在那之前，"马斯克救 Anthropic"这种叙事可以再洗一波——洗稿的人是真心相信、还是收钱配合、还是单纯没看时间线，每个公众号自己挑。我这一行的观察是：当一个剧本所有当事人都在出力演、所有围观媒体都在出力捧、所有信息差都被精心维护——

通常剧本本身就是台词。

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>Two business people stranded in deep water clutching each other shoulders, each desperately stepping on the other's shoulders trying to push themselves higher above the waterline, viewed from side angle, dark blue ocean background, flat design, minimalist illustration, no text, no labels, dramatic lighting, conceptual editorial style</pre></details>
</div>

---

## 数据来源

- [Anthropic 官方公告 - SpaceX 算力合作](https://www.anthropic.com/news/higher-limits-spacex)
- [CNBC - Anthropic, SpaceX announce compute deal](https://www.cnbc.com/2026/05/06/anthropic-spacex-data-center-capacity.html)
- [CNBC - Dario Amodei 80x growth quote](https://www.cnbc.com/2026/05/06/anthropic-ceo-dario-amodei-says-company-crew-80-fold-in-first-quarter.html)
- [VentureBeat - Anthropic $30B run rate 80x growth](https://venturebeat.com/technology/anthropic-says-it-hit-a-30-billion-revenue-run-rate-after-crazy-80x-growth)
- [Tom's Hardware - 220k GPUs and 300 MW deal](https://www.tomshardware.com/tech-industry/artificial-intelligence/musks-spacex-has-rented-out-access-to-its-supercomputers-220-000-nvidia-gpus-and-300-megawatts-of-ai-compute-power-to-rival-anthropic-musk-says-no-one-set-off-my-evil-detector-antrhropic-also-interested-in-orbital-data-centers)
- [Fortune - 马斯克成 Anthropic 数据房东](https://fortune.com/2026/05/07/spacex-anthropic-deal-elon-musk-ai-landlord-evil/)
- [Fortune - Anthropic 80x growth rents Musk data center](https://fortune.com/2026/05/08/anthropic-80fold-growth-quarter-renting-elon-musk-data-center/)
- [Gizmodo - Musk Teams Up With Anthropic Called Evil](https://gizmodo.com/elon-musk-teams-up-with-anthropic-a-company-hes-called-evil-2000755254)
- [The News - Musk 骂 Anthropic 恨西方文明](https://www.thenews.com.pk/latest/1393975-elon-musk-slams-anthropic-as-hater-of-western-civilization-over-pentagon-ai-military-snub)
- [CNBC - Trump 政府拉黑 Anthropic](https://www.cnbc.com/2026/02/27/trump-anthropic-ai-pentagon.html)
- [gHacks - Pentagon 8 家 AI 大单排除 Anthropic](https://www.ghacks.net/2026/05/04/pentagon-signs-ai-deals-with-openai-google-microsoft-nvidia-and-others-cutting-out-anthropic/)
- [Breaking Defense - Pentagon IL6/IL7 AI 部署清单](https://breakingdefense.com/2026/05/pentagon-clears-7-tech-firms-to-deploy-their-ai-on-its-classified-networks/)
- [CNN - Pentagon shuns Anthropic strikes 8 Big Tech deals](https://www.cnn.com/2026/05/01/tech/pentagon-ai-anthropic)
- [MacRumors - Claude Code rate limit drain bug](https://www.macrumors.com/2026/03/26/claude-code-users-rapid-rate-limit-drain-bug/)
- [The Register - Anthropic admits Claude Code quotas drain](https://www.theregister.com/2026/03/31/anthropic_claude_code_limits/)
- [GitHub Issue #41930 - Claude Code 限速暴动](https://github.com/anthropics/claude-code/issues/41930)
- [Musk X 推文 - xAI 解散并入 SpaceXAI](https://x.com/elonmusk/status/2052105373621121284)
- [Not a Tesla App - Musk 宣布 xAI 解散](https://www.notateslaapp.com/news/4116/elon-musk-announces-xai-will-dissolve-form-spacexai-subdivision)
- [SpaceXAI Wikipedia](https://en.wikipedia.org/wiki/SpaceXAI)
- [Axios - Musk Anthropic SpaceX compute SpaceX IPO](https://www.axios.com/2026/05/07/musk-anthropic-compute-spacex-ai)
- [Stocktwits - SpaceXAI Consolidates AI Empire Ahead of IPO](https://stocktwits.com/news-articles/markets/equity/spacexai-takes-off-elon-musk-consolidates-ai-empire-ahead-of-massive-ipo/cZQzjOQReOD)
- [The New Stack - Anthropic SpaceX Claude limits](https://thenewstack.io/anthropic-spacex-claude-limits/)
- [xAI 官方公告 - Anthropic 算力合作](https://x.ai/news/anthropic-compute-partnership)
- [The News Pravda - Anthropic 拒 Pentagon 引发 Musk 评论](https://news-pravda.com/world/2026/02/27/2102428.html)
- [Euronews - Musk 给"woke"对手供电](https://www.euronews.com/next/2026/05/11/musk-once-called-anthropic-evil-he-is-now-powering-his-woke-competitors-ai-expansion)
