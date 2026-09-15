# 也门那伙人开了三个 Claude：一个写代码，一个查资料，第三个给第一个做 code review

> **发布日期**：2026-09-15 | **分类**：AI 与安全

## 导语

火箭试射失败了。几个小时之后，他们回到对话框，问为什么没打中。

---

## 一、三个对话窗口，一个工程部

9 月 10 日，Anthropic 发了一份报告，叫《Detecting and countering misuse of AI: September 2026》，把 2025 年 12 月到 2026 年 8 月之间它自己抓到并掐断的滥用行为，按七个门类摊开讲。七个门类里有一个叫"常规武器研发"，这个门类底下有一个编号，GTG-87001。

GTG-87001 是一伙人，在也门北部，同时推进三个武器项目：一枚带末段寻的制导的火箭；一枚多级弹道导弹，他们自己给的射程目标是 2000 公里以上；还有一个叫 R2000 的多型号导弹族，里面含一个高超声速滑翔体变体。

三个项目，一伙人。他们缺的不是图纸，是写 GNC 软件的人——制导、导航、控制，就是让一个飞行器知道自己在哪、该往哪转、怎么不把自己转翻的那层代码。这层代码是一枚导弹和一根窜天猴的全部区别，也是全世界军工体系里最不好招人的岗位之一。

Anthropic 在报告里的说法是，这伙人用 Claude Code "代替了人类软件工程师"（in place of human software engineers）。

怎么代替的，写得挺细。他们同时开多个 Claude 实例，每个实例分一个固定角色：一个负责写代码，一个负责查资料，第三个负责 review 第一个写出来的代码。然后有一个人坐在中间调度，报告里给的词是 orchestrator，翻成人事术语就是项目经理。

这是一张标准的小型研发团队组织图。写码的、查资料的、做评审的、协调的，一个不少，齐活。唯一的区别是，这张组织图上四个格子，有三个里面不是人。

他们还懂点运维。为了不让 Anthropic 看出整个项目有多大，他们把任务拆散，分到很多条互相独立的会话里去问——每条会话单看都只是某个人在问一个普通的工程问题，拼起来才是一个导弹族。

然后他们把那枚制导火箭拉出去试射了。

失败了。

Anthropic 说，几个小时之内，这伙人回到了 Claude 那里，开始排查为什么会失败。

我看到这句是愣了一下的，不是因为恐怖，是因为太眼熟。周五上线，炸了，半夜爬起来翻日志，找 root cause，改完明天再来一次——这是个 debug 循环，全世界每一个写过软件的人都认得它长什么样，也都知道它最关键的属性是什么：周期以小时计。武器研发的迭代周期，历史上从来不是以小时计的。

## 二、九个账号，一支接单的队伍

同一份报告，另一个编号：GTG-27005，俄罗斯。项目名是他们自己取的，叫 DronDoc，也叫 Serafim——六翼天使，取名的人对自己在干什么显然有清醒认识。

2026 年 5 月中旬开工。九个账号，注册时间从 2025 年底铺到 2026 年初，关联到一所地方大学和俄罗斯科学院下属的一家联邦研究中心。Anthropic 有地理封锁，他们用商用 VPS 绕过去。他们跟 Claude 说，自己拿的是先进研究基金会、国家技术倡议和国防部的钱；Anthropic 在报告里专门补了一句，这些说法它无法核实。它自己的判断是，这不是一个国家项目，是一支小型的、专业的自由职业团队。也就是接单的。

Claude Code 帮他们写出来的东西，列一下：一套共享的"蜂群记忆"，让一群无人机互相知道对方看见了什么；一套容错协调逻辑，掉几架不影响整体编队；末段制导；以及机上的一个小模型，由它来决定这架无人机下一步是攻击、是继续盯着、还是返航。

目标分类器的训练数据，是抓来的乌克兰战场视频，标注方式是敌、友二分。为了不炸自己人，他们把俄方的装备型号做成了白名单。

目标类别里有一个类，叫 "person"。

整套系统可以在没有人参与的情况下，自己选定目标，自己下达引爆指令。

我想请你在"白名单"那三个字上多停一会儿。有一个人，坐在某个房间里，给一群会自己挑人炸的无人机写配置文件，内容是"这几种车别碰，是我们的"。他很清楚这个列表写漏一项会发生什么，所以他写得格外认真。他大概还让第三个窗口给这份列表做了一遍 code review。

Anthropic 封了这九个账号，同时说，没有证据表明这套东西被真的拉上过战场。

## 三、这个能力，本来就不稀缺

到这儿最容易得出的结论是"AI 让造武器变容易了"。这个结论听着顺，但它经不起查。

乌克兰有家公司叫 The Fourth Law，产品叫 TFL-1，干的就是机器视觉末段制导：操作手用眼睛指定目标，最后四五百米交给机上计算机自己飞完，哪怕电子干扰把图传掐断也照样打。跑的是 YOLOv8，硬件是树莓派 5 配一块 Google Coral 的边缘 TPU；廉价版本用树莓派 Zero，那块板子十五美元。据 Forbes 的 David Hambling 前后两次报道，最便宜的实装版本一百五十美元，量产型号 Vyriy-10-TFL-1 四百四十八美元，这套东西研发了大约两年，拿到了北约编码。参照系是：一架 FPV 攻击无人机本身，三百到七百美元。

所以"无人机自己完成末段制导、自己认目标"这件事，不是 2026 年 9 月这份报告里才冒出来的新能力。它已经量产了，已经进了北约的编码目录，单价比一部手机还低。

这也是为什么，对这份报告最有力的批评不是"危言耸听"，而是"这是营销"。Better Stack 的技术博客直接写，这份报告"缺乏真正的信息披露应有的技术深度、透明度和可操作情报"，"充斥着含糊的表述、无据的断言和逻辑上的不一致"，其"主要功能是一个营销工具"——用对一种新威胁的恐惧，来推销自家模型作为这种威胁的解药。

这个批评有它的道理。一家公司发报告说"坏人在用我的产品干坏事，还好我抓住了"，这个结构本身就不太干净。

但恰恰因为能力不新，报告里那句最不起眼的话才值钱：in place of human software engineers。

塌掉的不是技术门槛。技术门槛就在树莓派上放着，十五美元，谁都能买。塌掉的是另一样东西：也门北部，制裁之下，你上哪儿去雇一个 GNC 工程师？你怎么把他弄进来，怎么给他发工资，怎么确认他不是别人派来的，怎么在他撂挑子之后找到第二个？这不是技术问题，是人力资源问题，而在过去，正是这个人力资源问题挡住了绝大多数想造导弹的人。

**以前雇不到人，项目就死在那儿。现在雇不到人，项目照样跑，而且试射炸了之后几个小时就能开始复盘。**

## 四、同一条红线，Anthropic 自己半年前投过标

这份报告最讽刺的一段，不在报告里。

2026 年 2 月底，美国防长 Pete Hegseth 把 Anthropic 定性为"供应链风险"，下令禁止五角大楼的承包商及其合作方与这家公司发生商业往来。起因是 Anthropic 拒绝按国防部的要求拆掉自己的使用限制。它划的红线有两条：不得用于国内大规模监控，不得用于自主武器系统。国防部的立场是，AI 工具要能用于"一切合法用途"。

就在这场撕扯进行的同时——彭博 3 月 2 日报道——Anthropic 递了一份标书，参加五角大楼一个一亿美元的悬赏赛，内容是语音控制的自主无人机蜂群。

这份方案是精心设计过的，为的就是不越自己那条线：Claude 只负责把指挥官的意图翻译成数字指令、协调机队，不参与自主目标选择，不参与武器决策，人始终保有监督和叫停的权力。它还想顺带跟五角大楼搞一个联合研究项目，一起研究怎么安全地开发和评估自主武器能力。

它没中标。中标的是 SpaceX 与 xAI 的联合方案，以及两家跟 OpenAI 合作的国防科技公司，其中一家是 Applied Intuition。

把两件事并排放。一边是一家公司花了半年，跟国防部吵架、被列进供应链风险名单、递上一份把人牢牢焊死在决策环里的标书，去竞争一个一亿美元的自主蜂群项目，最后落选。另一边是九个账号，一台商用 VPS，五月中旬开工，把"人不在环"的那个版本写完了。

红线是写在标书里的。它管得住投标的人，因为投标的人需要被审；它管不住绕道的人，因为绕道的人只需要一台 VPS。

Anthropic 在这件事上其实是全行业最较真的那一个，较真到宁可被国防部拉黑。而这份报告等于它自己交了一份体检单上来，上面写着：我最严肃的那条承诺，在我最认真执行它的那半年里，被九个账号从侧面走掉了。

## 五、防扩散体系押的是哪一注

出口管制、防扩散、技术封锁，这一整套东西盯的是四样：设备、材料、图纸、人员流动。离心机往哪儿运，特种合金卖给了谁，图纸有没有外泄，哪个工程师去了哪个国家开会。

这四样底下压着同一个假设：造武器需要一批稀缺的、可识别的、能被盯住的人。

只要这个假设成立，整套体系就有效，因为人是有实体的——要签证，要工资，要住址，要在某个具体的地方出现。盯住人，就等于盯住了能力。

GTG-87001 把这个假设戳了个洞。不是因为 Claude 教了他们什么新东西，而是因为那个"需要被盯住的人"的位置，现在空着也能开工。

而 Anthropic 手上能用的处置，是封号，加分类器。SOCRadar 的分析里提了一句：也门那伙人顺手还做了一套离线的仿真工具包，封号之后，那套工具包照常能用。

**你封掉的是账号。他们留下的是工具链。**

报告里那么多案例，我记住的是开头那一句：火箭炸了，几个小时后，他们回到对话框，问为什么没打中。

这句话可怕的地方不在于 AI 有多危险。它可怕在，它是一句太正常的话，正常到任何一个写过软件的人都能立刻听懂——那就是周五晚上上线炸了之后，每个团队都会做的事。

他们已经不把造导弹当成一项需要举国之力的工程了。他们把它当成一个有迭代周期的普通软件项目在做。

而普通软件项目的迭代周期，是以小时计的。

## 数据来源

- [Anthropic：Detecting and countering misuse of AI: September 2026（2026-09-10 原始报告）](https://www.anthropic.com/threat-intelligence-report-september-2026)
- [The War Zone：Adversaries Using Claude AI To Target Americans And Develop Missiles Is A Sign Of What's To Come](https://www.twz.com/news-features/adversaries-using-claude-ai-to-target-americans-and-develop-missiles-is-a-sign-of-whats-to-come)
- [SOCRadar：Vibe-Terrorism: Inside the Yemen Cell That Used Claude to Build Guided Weapons](https://socradar.io/blog/vibe-yemen-cell-claude-guided-weapons/)
- [IBTimes：Claude Code Was Used in a Yemen Weapons Project; Anthropic Says the Rocket Failed](https://www.ibtimes.sg/claude-code-was-used-yemen-weapons-project-anthropic-says-rocket-failed-93703)
- [Tom's Hardware：Russian freelancers use Claude to program autonomous combat drone swarm](https://www.tomshardware.com/tech-industry/artificial-intelligence/russian-freelancers-use-claude-to-program-autonomous-combat-drone-swarm-ai-enabled-target-selection-and-detonation-without-a-human-in-the-loop)
- [Cybernews：Russian developers used Claude to build kamikaze drones that can choose their own targets](https://cybernews.com/ai-news/claude-anthropic-russia-kamikaze-drones/)
- [Resilience Media：Claude AI helped Russia-based threat actors develop autonomous kamikaze drone swarm](https://resiliencemedia.co/claude-ai-helped-russia-based-threat-actors-develop-autonomous-kamikaze-drone-swarm/)
- [DroneXL：Anthropic Catches Russians Using Claude to Code Self-Targeting Drones](https://dronexl.co/2026/09/12/anthropic-claude-russian-kamikaze-drone-swarm-software/)
- [Bloomberg：Anthropic Made Pitch in Drone Swarm Contest During Pentagon Feud（2026-03-02）](https://www.bloomberg.com/news/articles/2026-03-02/anthropic-made-pitch-in-drone-swarm-contest-during-pentagon-feud)
- [Cybernews：Anthropic pitched Pentagon technology for autonomous drone fleet](https://cybernews.com/ai-news/anthropic-drone-swarm/)
- [Forbes / David Hambling 对 The Fourth Law TFL-1 的报道（经 TechRadar、United24 等转载核对）](https://www.techradar.com/pro/the-pentagon-wants-swarms-of-voice-controlled-ai-drones-and-is-offering-a-usd100-million-prize-as-a-reward-and-elon-musks-spacex-is-taking-pole-position)
- [Better Stack：Analyzing Anthropic's AI Cyber Attack Report: What's Missing](https://betterstack.com/community/guides/ai/anthropic-ai-cyber-attack)
