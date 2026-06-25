# AI 公司锁死了自己的电价，然后把涨价的账单寄给了你

> **发布日期**：2026-06-25 | **分类**：AI 观察 · 算力成本

## 导语

兄弟们，先看两个数字。

第一个：在美国最大的电网 PJM，有一笔叫「容量费」的钱——你可以先粗暴理解成整个电网为「保证未来随时有电」交的份子钱，跟你今天用了多少电没关系。它的拍卖清算价，从 **28.92 美元/MW·天** 一路涨到 **329.17**，顶到了监管批准的天花板，前后整整十一倍。

第二个：英伟达 2026 财年，光数据中心业务就卖了 **1937 亿美元**，同比涨 68%。

大多数人看到这两个数字，第一反应是——一个是美国电费，一个是 AI 卖铲子，八竿子打不着。

我个人感觉，这俩是同一件事。

更准确地说——

**第一个数字是你交的，第二个数字是它赚的。**

而最骚的地方在于：AI 公司一边把电吃成了行业增长引擎，一边用一纸合同，把自己从涨价的账单里，干干净净地摘了出去。

这篇文章，我们做一次电费账单的法医解剖。

---

## 一、你账单上涨的那笔，根本不叫「电价」

先纠正一个全网都在犯的错。

几乎所有中文报道都在说「AI 数据中心推高了电价」。

这话不能说错，但它把最关键的机制说糊了。涨得最猛的那笔，**不是你用一度电付的钱（电量电价），而是一笔叫「容量费」的押金。**

什么是容量费？

PJM 是北美最大的区域电网调度机构，管着美国东部 13 个州加华盛顿特区，6500 万用户。它每年办一场拍卖，叫「基础剩余容量拍卖」（BRA），让发电商提前三年竞标，保证未来电力够用。

你可以把它理解成整个电网交的一笔「份子钱」——不是买你今天用的电，是预定未来三年「随时有电可用」这个承诺。发电商中标的清算价，最后摊进每一个用电方的账单里。

现在看这笔份子钱这几年的报价（全部来自 PJM 官方拍卖报告，单位是美元/MW·天）：

- **2024/2025 交割年：28.92**
- **2025/2026 交割年：269.92**（大部分区域），暴涨 833%
- **2026/2027 交割年：329.17**，全区域统一，**顶到 FERC 批准的价格上限**
- **2027/2028 交割年：333.44**，再次顶到上限

看明白没有。

一笔保证「有电可用」的押金，一年之内涨了九倍多，然后连着两年贴着监管天花板走。

这不是电变贵了。这是**「保证有电」这件事本身变贵了**——因为电网突然发现，要喂饱一群胃口大到离谱的新客户。

<div class="img-placeholder understanding" data-caption="图注：你账单涨的那笔是「容量费」——一笔给未来三年电力产能交的押金，一年内从 28.92 飙到 329.17 美元/MW·天，顶到监管上限。">
  <div class="img-placeholder-icon">🧩</div>
  <div class="img-placeholder-label">理解图占位</div>
  <details><summary>理解图 HTML</summary><pre>
&lt;div class="illustration"&gt;
  &lt;h2&gt;涨的不是「电价」，是「容量费」&lt;/h2&gt;
  &lt;div class="sub"&gt;PJM 基础剩余容量拍卖（BRA）清算价 · 单位 美元/MW·天&lt;/div&gt;
  &lt;div class="bar-row"&gt;&lt;div class="name"&gt;2024/2025&lt;/div&gt;&lt;div class="bar" style="width:9%"&gt;&lt;/div&gt;&lt;div class="val"&gt;28.92&lt;/div&gt;&lt;/div&gt;
  &lt;div class="bar-row"&gt;&lt;div class="name"&gt;2025/2026&lt;/div&gt;&lt;div class="bar" style="width:81%"&gt;&lt;/div&gt;&lt;div class="val"&gt;269.92&lt;/div&gt;&lt;/div&gt;
  &lt;div class="bar-row"&gt;&lt;div class="name"&gt;2026/2027&lt;/div&gt;&lt;div class="bar" style="width:99%;background:var(--accent)"&gt;&lt;/div&gt;&lt;div class="val"&gt;329.17 ↑上限&lt;/div&gt;&lt;/div&gt;
  &lt;div class="bar-row"&gt;&lt;div class="name"&gt;2027/2028&lt;/div&gt;&lt;div class="bar" style="width:100%;background:var(--accent)"&gt;&lt;/div&gt;&lt;div class="val"&gt;333.44 ↑上限&lt;/div&gt;&lt;/div&gt;
  &lt;div class="note"&gt;一年涨九倍，然后连续两年贴着监管天花板走。这不是电变贵，是「保证有电」本身变贵了。&lt;/div&gt;
&lt;/div&gt;
</pre></details>
</div>

谁是那个胃口大到离谱的新客户，PJM 自己说得很清楚。

---

## 二、这笔押金，最后摊到了一个马里兰家庭头上

PJM 不藏着掖着。

它 2025 年的长期负荷预测里写：未来 15 年，夏季峰值负荷要从 150 GW 涨到 220 GW，多出来 70 GW。而 2024 到 2030 这一段，峰值要涨 32 GW——**其中 30 GW 来自数据中心。**

换句话说，电网未来要多扛的负荷，几乎全是数据中心一家贡献的。

PJM 的独立市场监控机构 Monitoring Analytics 把话说得更狠。它的措辞是：数据中心负荷增长，是「近期及预期容量市场几乎全部问题的根本原因」。它给了个数字——数据中心要为 2025/2026 那次拍卖涨价负 **63%** 的责任，折合 **93 亿美元**，会通过更高的电费，从所有用户身上收回来。

「所有用户」是谁？

是你。是我。是一个住在马里兰州、从来没听说过什么叫 BRA 拍卖的普通家庭。

这里有个一手数字，来自华盛顿特区和马里兰州的消费者顾问办公室（OPC，政府监管机构）2024 年的费率影响报告：在 Pepco 供电区，居民月均电费要涨 **21 美元**，**其中约 10 美元，直接来自容量市场价格的飙升。**

10 美元一个月，120 美元一年。

听着不多？这只是一个区、一年的数字，而且这笔钱里没有一度电是这个家庭多用的。他家的灯没多开一盏，空调没多吹一度，账单凭空多出来一栏，理由是几百公里外有人要盖一片他这辈子都不会进去的机房。

全国层面 EIA 的数据也在往同一个方向走：美国居民电价从 2019 年的每度 13.01 美分，涨到 2024 年的 16.5 美分，2025 年 7 月已经摸到 17.47 美分。五年涨了快 27%，跑赢了通胀。

兄弟们，到这一步，故事还只是「AI 很费电，电网很紧张，大家一起多掏钱」。

听上去像个无人作恶的系统性悲剧。

但接下来这一节，你会看到这个系统里，有人提前给自己买好了雨衣。

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>high voltage power transmission lines glowing at dusk leading toward a massive humming data center, streams of electricity flowing along the wires, moody blue twilight atmosphere, flat design, minimalist illustration, tech style, blue and white color palette, no text, no labels, clean background</pre></details>
</div>

---

## 三、AI 公司是怎么把自己摘出去的

现在请记住一个词：**PPA，购电协议。**

微软、谷歌、亚马逊、Meta 这些超大规模厂商，绝大部分电不是在现货市场上现买现用的。它们跟发电商签长期购电协议，一锁就是 15 到 20 年，价格提前谈死。

2025 年，全球企业级清洁能源 PPA 的交易量（按彭博新能源财经 BNEF 的统计口径），这四家就占了 **49%**。光微软一家，累计签约容量到 2025 年 9 月已经堆到 **34.7 GW**。

锁价意味着什么？

意味着当现货电价上蹿下跳的时候，这些公司锁定的那部分电价**纹丝不动**——它们在十年前、五年前就把数字焊死了。

这里得说句精确的，免得被懂行的抓住把柄：PPA 锁的主要是「电量价格」，不是「容量费」本身；大用户在 PJM 里通常还得另外持有或购买容量信用，容量这部分到底怎么分摊，因合同而异。

但方向是清楚的——有本事签 15 年、20 年长约的玩家，能把自己的价格暴露大幅对冲掉；而电网里那些签不起长约的人——居民、小商户、中小工厂，对着一年涨九倍的容量费，只能照单全收。也就是上一节那个马里兰家庭。

你可能会说，那 AI 公司至少在账面上是个用电大户，财报里总该看得见它扛了多少电费成本吧。

我去翻了。翻不到。

谷歌母公司 Alphabet 2025 财年的 10-K（向美国 SEC 提交的年报），把能源成本埋进了一个叫「其他营收成本」的科目里，原文是这么写的——「technical infrastructure operations costs, including **energy**, equipment, and network capacity costs」（技术基础设施运营成本，包括能源、设备和网络容量成本）。

energy 这个词，跟设备、网络挤在一个口袋里，**没有单独的一行。**

也就是说，一家一年烧掉的电够好几个中等国家用的公司，你从它的法定财报里，**抠不出它到底为电付了多少钱。**

这就是这件事最干净利落的一手——

AI 公司不是没付电费。它付的是锁了价、提前焊死、还在财报里没有名字的电费。而涨出来的那部分，份子钱一样，摊给了所有签不起长约的人。

<div class="img-placeholder understanding" data-caption="图注：大厂用 15-20 年 PPA 把自家电价焊死、波动风险甩给电网其他人；居民只能在现货+容量费里随行就市，替它扛涨价。">
  <div class="img-placeholder-icon">🧩</div>
  <div class="img-placeholder-label">理解图占位</div>
  <details><summary>理解图 HTML</summary><pre>
&lt;div class="illustration"&gt;
  &lt;h2&gt;同一张电网，两种命运&lt;/h2&gt;
  &lt;div class="sub"&gt;容量费暴涨时，谁锁了价、谁在裸奔&lt;/div&gt;
  &lt;div class="vs"&gt;
    &lt;div class="fact"&gt;&lt;div class="tag fact"&gt;AI 超大规模厂商&lt;/div&gt;
      &lt;div class="desc"&gt;15-20 年 PPA 锁死电价&lt;br/&gt;四大厂占全球企业 PPA 49%&lt;br/&gt;微软累计签约 34.7 GW&lt;br/&gt;财报里「能源」无单独一行&lt;br/&gt;&lt;b&gt;波动风险 → 甩出去&lt;/b&gt;&lt;/div&gt;
    &lt;/div&gt;
    &lt;div class="think"&gt;&lt;div class="tag think"&gt;居民 / 小商户&lt;/div&gt;
      &lt;div class="desc"&gt;签不起长约，随行就市&lt;br/&gt;容量费一年涨九倍照单全收&lt;br/&gt;马里兰 Pepco 月账单 +21 美元&lt;br/&gt;其中约 10 美元来自容量市场&lt;br/&gt;&lt;b&gt;波动风险 → 自己扛&lt;/b&gt;&lt;/div&gt;
    &lt;/div&gt;
  &lt;/div&gt;
  &lt;div class="note"&gt;PPA 不是阴谋，是合法的风险管理工具。问题是：被甩出去的风险，总得有人接住。&lt;/div&gt;
&lt;/div&gt;
</pre></details>
</div>

按半佛的剧本，下面该接一段「资本吃人」的高潮收尾了。

但我不打算这么写。因为就此打住，我跟那些只会喊口号的人就没区别了。

下一节，我要把刀对准我自己的论点。

---

## 四、先别急着骂——把被夸大的部分，我自己砍掉

一个诚实的拆穿，必须包含「哪些部分其实赖不到 AI 头上」。

网上流传最广的一个数字是：数据中心密集的弗吉尼亚州，电价五年涨了 267%。这个数字我**不用**，因为我顺着它查到 EIA 原始数据时，对不上号。一个对不上一手出处的数字，再爆炸也是哑弹。

更要命的是反方证据。

能源咨询公司 E3 在 2026 年 5 月出了份白皮书，分析了十多项量化研究后给出的结论是：PJM 2025/2026 那次容量价格暴涨里，大约 **一半** 不是数据中心干的，而是来自市场设计变化——一个叫 ELCC 的新计费规则（一种重新评估风电、光伏到底能提供多少「可靠容量」的机制），单这一项就把拍卖收入推高了 49.1%，折合 44 亿美元；再加上老旧发电机退役、供给侧收紧。

还有更扎心的：E3 对全球最大数据中心市场弗吉尼亚做历史分析，**没找到证据**表明数据中心已经把成本转嫁给了居民。亚马逊的数据中心案例里，平均每个站点向电网净缴 **340 万美元**——它给电网交的钱，比它占用的服务成本还多。

（这里要说句公道话：E3 这份研究部分由亚马逊委托，屁股在哪儿你心里有数。但它引用的市场设计、天然气这些因素，是独立可查的。）

天然气也得算一份。EIA 的数据，2025 年天然气价格每百万英热 3.52 美元，比 2024 年的 2.21 涨了 56%，这是 2025 年批发电价上涨的一个独立大头，跟 AI 一点关系没有。

UC Berkeley 的能源经济学家 Severin Borenstein 把这事说得最清楚：数据中心对电价的威胁「真实存在，但好的政策设计可以把需求增长变成更低的电价，而不是更高」。关键要分清两件事——**数据中心在容量市场上的成本外部化**（这个确实在发生，尤其在 PJM），和**把全国零售电价上涨全赖给数据中心**（这个证据弱得多）。

所以，把断言收窄到它真正站得住的地方：

**在 PJM 容量市场这个特定机制里，数据中心是价格飙升的首要驱动力之一；而 AI 公司用 PPA 锁价，绕开了自己本该承担的那一份波动。**

这句话，每一个字都有一手数据顶着。比「AI 让全美电费暴涨」那种爽文口号，弱了一截。

但它是真的。

而一个真的、收窄过的判断，比一个爆炸的、站不住的口号，杀伤力大得多——因为前者你反驳不了。

<div class="img-placeholder understanding" data-caption="图注：把 2025/2026 容量涨价拆开看，数据中心约占一半，另一半是 ELCC 机制改革、电厂退役、天然气涨 56%。骂 AI 之前，先把账算干净。">
  <div class="img-placeholder-icon">🧩</div>
  <div class="img-placeholder-label">理解图占位</div>
  <details><summary>理解图 HTML</summary><pre>
&lt;div class="illustration"&gt;
  &lt;h2&gt;容量费暴涨，到底几成赖 AI&lt;/h2&gt;
  &lt;div class="sub"&gt;两家机构的归因之争（2025/2026 拍卖）&lt;/div&gt;
  &lt;div class="bar-row"&gt;&lt;div class="name"&gt;Monitoring Analytics&lt;br/&gt;（PJM 独立市场监控）&lt;/div&gt;&lt;div class="bar" style="width:63%;background:var(--accent)"&gt;&lt;/div&gt;&lt;div class="val"&gt;数据中心占 63%&lt;/div&gt;&lt;/div&gt;
  &lt;div class="bar-row"&gt;&lt;div class="name"&gt;E3 白皮书&lt;br/&gt;（部分受亚马逊委托）&lt;/div&gt;&lt;div class="bar" style="width:50%;background:var(--primary)"&gt;&lt;/div&gt;&lt;div class="val"&gt;数据中心约占 50%&lt;/div&gt;&lt;/div&gt;
  &lt;div class="note"&gt;另一半：ELCC 机制改革（单项 +49%/44 亿美元）、发电机退役、天然气涨 56%。诚实地砍掉夸大，剩下的才钉得死。&lt;/div&gt;
&lt;/div&gt;
</pre></details>
</div>

---

## 五、这事跟你家电表，到底有没有关系

你可能想：PJM 在美国东部，离我十万八千里，关我什么事。

关系在机制，不在地理。

中国信通院的官方报告写得明白：到 2023 年底，全国在用的 810 万标准机架，一年耗电 **1500 亿千瓦时**，占全社会用电量 **1.6%**。这个比例还在往上走。

只不过，中美把这笔成本外部化的方向，正好相反。

美国是**市场机制**无意中把成本摊给了全体用户——容量费涨了，大家一起分。中国走的是另一条路：「东数西算」把大型智算中心引到内蒙、宁夏、贵州、甘肃这些电价洼地，用政策电价和补贴把电费压下去。

（注：关于西部枢纽具体补贴比例，网上流传一个「最高减免 50%」的说法，我没能从发改委一手文件里核实到这个精确数字，这里只说方向，不报这个数。）

方向相反，本质一样——

**算力的电费成本，没有一家是自己全额扛的。美国摊给全体用电方，中国摊给财政和纳税人。**

只不过中国这条路更隐蔽：它不出现在你的电费账单上，而是出现在不显眼的公共支出里。你感受不到，不代表你没付。

那么，作为一个普通人，看完这篇你能做一件什么不一样的事？

不是去骂 AI，也不是关掉 ChatGPT 省那几瓦电——那没用，也搞错了对象。

是下次拿到电费账单时，**别只看总数，去看它的结构。** 美国账单上那栏叫「capacity / delivery charge」，中国工商业账单上那栏叫「基本电费」或「容量电价」。当有人告诉你「电费又涨了」，你要能分清：涨的是你用的电，还是你替别人垫的那笔「保证有电」的押金。

然后，把火力对准真正能解决问题的地方——

支持那种「让大用户为自己造成的容量成本单独买单」的电价改革（在美国这叫「大用户专用费率类别」，宾夕法尼亚已经有人在推）。让吃电的为吃掉的电付费，而不是让全网替它分摊。

这比在评论区骂英伟达，管用一万倍。

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>an ordinary person sitting at a kitchen table at night looking with quiet worry at a rising electricity bill, a small glowing data center visible through the window in the far distance, warm domestic lighting contrasted with cold blue outside, flat design, minimalist illustration, tech style, blue and white color palette, no text, no labels, clean background</pre></details>
</div>

---

兄弟们，回到开头那两个数字。

英伟达数据中心业务的 1937 亿，和你账单上那栏涨了十一倍的容量费，确实是同一件事的两端。

但这件事的真相，不是「AI 抢走了你的电」这种爽文。

真相要冷得多，也精确得多：

AI 公司把自己的电价用合同焊死，把成本埋进财报里没有名字的科目，然后让一群签不起长约的普通人，替它接住了涨价的那部分波动。

这不违法。PPA 是合法工具，容量市场是合法设计，财报科目是合规披露。

每一步都合规，合起来，就是一笔没有人需要为之负责的账单，悄悄寄到了你家。

而你能做的，不是愤怒。

是先看懂账单，再把账，算到该算的那个人头上。

## 数据来源

- [PJM 2024/2025 Base Residual Auction Report（官方）](https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2024-2025/2024-2025-base-residual-auction-report.ashx)
- [PJM 2025/2026 Base Residual Auction Report（官方，2024-07-30）](https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2025-2026/2025-2026-base-residual-auction-report.pdf)
- [PJM 2026/2027 拍卖新闻稿：329.17 触及上限（官方，2025-07-22）](https://www.pjm.com/-/media/DotCom/about-pjm/newsroom/2025-releases/20250722-pjm-auction-procures-134311-mw-of-generation-resources-supply-responds-to-price-signal.pdf)
- [PJM 2027/2028 拍卖新闻稿（官方，2025-12-17）](https://www.pjm.com/-/media/DotCom/about-pjm/newsroom/2025-releases/20251217-pjm-auction-procures-134479-mw-of-generation-resources.pdf)
- [PJM 2025 长期负荷预测报告（官方）](https://www.pjm.com/-/media/DotCom/library/reports-notices/load-forecast/2025-load-report.pdf)
- [PJM Inside Lines：拍卖回应价格信号（官方博客）](https://insidelines.pjm.com/pjm-auction-procures-134311-mw-of-generation-resources-supply-responds-to-price-signal/)
- [Monitoring Analytics 归因 63% / 93 亿（经 Utility Dive 报道）](https://www.utilitydive.com/news/data-centers-pjm-capacity-auction-market-monitor/801780/)
- [马里兰 / DC 消费者顾问办公室费率影响报告（政府，2024-08）](https://opc.maryland.gov/Portals/0/Files/Publications/RMR%20Bill%20and%20Rates%20Impact%20Report_2024-08-14%20Final.pdf)
- [NVIDIA FY2026 Q4 财报 8-K（SEC 原文）](https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000019/q4fy26pr.htm)
- [NVIDIA FY2027 Q1 财报 8-K（SEC 原文）](https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000051/q1fy27pr.htm)
- [Alphabet FY2025 10-K：能源成本无单独披露（SEC 原文）](https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000018/goog-20251231.htm)
- [EIA 电价月度数据（官方）](https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=table_5_03)
- [IEA《Energy and AI》报告（官方，2025）](https://www.iea.org/reports/energy-and-ai/executive-summary)
- [LBNL《2024 美国数据中心能耗报告》（官方）](https://eta.lbl.gov/publications/2024-lbnl-data-center-energy-usage-report)
- [E3：电价驱动因素与数据中心角色白皮书（2026-05）](https://www.ethree.com/electricity-rate-drivers-data-center-role-2026/)
- [Severin Borenstein：数据中心会对你的电费做什么（UC Berkeley Haas，2025-09-29）](https://energyathaas.wordpress.com/2025/09/29/what-will-data-centers-do-to-your-electric-bill/)
- [中国信通院《中国绿色算力发展研究报告（2024）》（官方 PDF）](https://www.caict.ac.cn/kxyj/qwfb/ztbg/202407/P020240711551514828756.pdf)

> 注：本文核心数据均追溯至一手来源（PJM 官方拍卖报告、SEC 财报原文、政府监管机构报告、IEA/LBNL/信通院原始报告）。Monitoring Analytics 的 63% 归因经独立市场监控机构统计、由 Utility Dive 报道；弗吉尼亚州「电价五年涨 267%」与中国西部「电费减免 50%」两个流传数字因无法核实一手出处，本文不予采用。容量价格单位为 美元/MW·天（UCAP，非强制容量）。

