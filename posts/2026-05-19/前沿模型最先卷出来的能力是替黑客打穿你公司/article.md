# 前沿模型最先卷出来的能力，是替黑客打穿你公司

> **发布日期**：2026-05-19 | **分类**：AI 行业拆解

## 核心观点

- 英国 AI 安全研究所（AISI）2026 年挂出来一个叫 "The Last Ones"（TLO）的攻防靶场——32 步、一家虚拟公司的完整内网、从侦察到全网接管，人类专家做完要 20 小时。4 月 14 日 Anthropic 的 Claude Mythos Preview 第一个通关，10 次跑通 3 次，平均拿下 22/32 步。这是 AI 第一次从头到尾自己打穿一家公司
- 5 月 14 日 AISI 又挂出 OpenAI GPT-5.5-Cyber 的评估：10 次跑通 2 次，95 个 CTF 上专家级任务 71.4% 准确率，跟 Mythos 的 68.6% 在误差范围内。OpenAI 用了 3 周追平。同一时间 Anthropic 自己更新了 Mythos checkpoint，把 3/10 翻到 6/10。这不是两个模型在比聪明，是两家"安全公司"在比谁更会打穿你公司
- 两家公司都把这种能力发在自己的"安全研究"博客上当业绩公布。Anthropic 给 Mythos 配了一个叫 Project Glasswing 的封闭联盟，赦免 40 家"白名单"企业先用上。这是"我练出了一把没人挡得住的刀，先递给我的朋友们"——而 The Last Ones 这个名字起得很诚实，它不是 AI 攻击能力的最后一关，是企业网络防御的最后一关

---

## 一、英国政府办了个 32 步靶场，名字叫 "The Last Ones"

先把这件事讲清楚——这不是民间 CTF 比赛，是政府机构的标准化评估。

英国 AI 安全研究所（AI Security Institute，简称 AISI）2023 年成立，2024 年改组，2025 年把名字从 "AI Safety Institute" 改成 "AI Security Institute"。改名这件事本身就值得读一遍——"Safety" 是对齐、伦理、价值观那一套，"Security" 是网络攻防、生化武器、CBRN 风险那一套。改名意味着英国政府正式把"AI 模型本身就是攻击武器"当成研究对象。

改完名第二年，AISI 端出来一个评估套件，叫 "The Last Ones"，缩写 TLO。

这个套件是一个 32 步的企业网络入侵模拟。具体步骤覆盖五个阶段——侦察（搜端口、扫服务、抓配置）、初始访问（拿到一个低权限账号或一个 web shell）、横向移动（从一台机器跳到另一台）、权限提升（普通用户拿到 admin 或 root）、持久化与接管（埋后门、改 ACL、覆盖整个内网）。

AISI 估计人类专家从头跑完一遍需要约 **20 小时**。这是真人渗透测试员的工时口径，不是脚本时间。

4 月 14 日，AISI 发了一篇评估博客，标题就一句话——Claude Mythos Preview 是第一个把 TLO 跑通的模型。具体数字是这样的——

- 跑了 10 次，**3 次完整通关**
- 全部 10 次平均拿下 **22/32 步**
- 对照组里第二名是 Claude Opus 4.6，平均 16/32 步
- 在另一个独立测试里，Mythos Preview 最新 checkpoint 把通关率翻到 **6/10**

把 22/32 这个平均数换个说法：在 10 次随机种子下，这个模型平均能把一家虚拟公司打到只剩三分之一防线还没破。3/10 这个完整通关率换个说法：随便挑三个工作日给它三次机会，至少一次它会把这家公司从 0 跑到 100。

AISI 在评估报告里给了一句完整的定性——

> "is at least capable of autonomously attacking small, weakly defended and vulnerable enterprise systems where access to a network has been gained"

翻译：在已经取得网络访问权的情况下，这个模型至少有能力自主攻击小型、防御薄弱、有漏洞的企业系统。

把这句话拆开看。"至少"——AISI 测的是已知 32 步，没测更复杂的；实际能力可能更高。"自主"——不需要人在循环里下指令。"小型、防御薄弱、有漏洞"——这是政府机构的礼貌用法，意思是中国和美国 80% 以上没专职 SOC 团队的中小企业。"已经取得网络访问权"——这一条听着像免责声明，实际不值钱，因为初始访问这一步现在去 dark web 上买一个泄露凭证只要几美元，比 AI 自己钓鱼还便宜。

合起来就是：你只要给它一张内网门票，它能把里面打成自助餐。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：流程
【副标题】：The Last Ones (TLO) 32 步攻击链 — AISI 评估套件
【核心内容】：
  - 阶段一 侦察：扫端口 / 抓服务指纹 / 找暴露配置
  - 阶段二 初始访问：拿到低权限账号或 web shell
  - 阶段三 横向移动：从一台机器跳到另一台
  - 阶段四 权限提升：普通用户拿到 admin 或 root
  - 阶段五 持久化接管：埋后门 / 改 ACL / 覆盖全网
【备注】：人类专家约 20 小时；Mythos Preview 平均 22/32 步、3/10 完整通关，最新 checkpoint 6/10</pre></details>
</div>

---

## 二、OpenAI 用了 3 周追平 Anthropic，95 个 CTF 上 71.4%

4 月 14 日 Mythos Preview 第一个通关。5 月 14 日，AISI 第二篇评估博客挂出来，主角换成 OpenAI GPT-5.5-Cyber。

正好是 30 天。在硅谷的节奏里，这叫"3 周追平"——因为模型评估本身要 1 周，挂博客要 1 周，OpenAI 内部从看见对方数字到训出对应能力的 checkpoint 实际只用了不到 3 周。

GPT-5.5-Cyber 在 TLO 上的成绩是这样的——

- 跑了 10 次，**2 次完整通关**
- 在 AISI 维护的 95 个 CTF 套件（Capture the Flag——逆向工程、Web 漏洞利用、密码学三个大类）上，**专家级任务 71.4% 准确率**
- 对照 Mythos Preview 在同一个 CTF 套件上的 **68.6%**——差 2.8 个百分点，在 AISI 自己定义的误差范围内

AISI 这次的措辞跟 4 月那篇几乎是复制粘贴。OpenAI 用 5.5 这一代"达到了与 Mythos Preview 相当的水平"。两家公司，两个独立训练管线，两个不同的对齐方案，两个不同的内部评估委员会——在英国政府这一套 32 步靶场加 95 个 CTF 上，跑出了 2.8 个百分点以内的成绩。

这不是巧合。这是行业天花板。

去年还没有这个天花板。2025 年下半年最顶尖的模型——GPT-5 早期版本、Claude Opus 4 系列、Gemini 2.5 Pro——在类似的多步攻击靶场上拿到的平均成绩是个位数步骤，4 步、6 步、10 步都见过，从来没人在 20 步以上稳定通关。一年时间，从"个位数"跳到"32 步完整跑完"，这是攻击能力曲线的相位变化。

更要命的是，两家把这件事写在了不一样的位置——

**Anthropic 这边**，Mythos Preview 是 2026 年 4 月 7 日在 `red.anthropic.com` 上正式公布的。这个域名本身就是 Anthropic 的内部红队产品发布站。Mythos 配套公布的指标是：

- SWE-bench Verified（软件工程任务）：93.9%
- USAMO（美国奥数）：97.6%  
- 漏洞利用生成（working exploits rate）：72.4%

三个数字排排坐。Anthropic 的 PR 稿把它们并列展示，三项都是"前沿模型新高"。但稍微一站远看就发现，第三项跟前两项不在同一个维度里——93.9% 的 SWE-bench 说的是它能修一个 GitHub Issue，72.4% 的 working exploits rate 说的是它能生成可直接武器化的漏洞利用代码。一个是 productivity，一个是 weaponization。Anthropic 把这两条放在同一段 PR 稿里，是在告诉所有同行：我家这把刀，既能切菜也能砍人，刀刃两面都开得很锋利。

**OpenAI 这边**，5 月 14 日 GPT-5.5-Cyber 那篇博客虽然挂在 AISI 一侧，但 OpenAI 在自己的 system card 里同步把"通过 AISI TLO 评估"这件事写进了模型卡。OpenAI 比 Anthropic 谦虚一点的地方在于，没把这条单独拎出来当业绩——OpenAI 把"过了"和"过得不如对方多"两件事都写进去了。但这个"谦虚"也只是相对——它把过了的事实写进了 system card，等于把"我跟 Anthropic 一样能打穿你公司"这一行写在了产品规格里。

接下来还会有 Gemini、Llama、DeepSeek、Qwen——这种攻击能力的指标一旦进了 system card，就会变成下一代所有前沿模型必须挂上去的一栏。挂不上的就是"性能不够"。挂上的就是"我练好了"。

行业的内卷方向就这样被永久地拨了一档。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：条形
【副标题】：AISI 评估 — TLO 32 步完整通关率（满分 10/10）
【单位】：完整通关次数 / 10
【核心判断】：两家公司一个月内被英国政府靶场卡到相同水位
【核心内容】：
  - Mythos Preview 最新 checkpoint：6
  - Claude Mythos Preview 4 月初版：3
  - GPT-5.5-Cyber：2
  - Claude Opus 4.6 [基线]：0
【备注】：Mythos 平均 22/32 步、Opus 4.6 平均 16/32 步；CTF 套件 OpenAI 71.4% vs Mythos 68.6%</pre></details>
</div>

---

## 三、两家"安全公司"，把通关写进自己的业绩

中文媒体这两个月写 Mythos 写过几轮，但有一件事写得很少——Mythos 这个名字所在的整个产品体系，本来是 Anthropic 内部红队的成果展示，不是给客户买的。

`red.anthropic.com` 这个域名上挂着三类内容：Mythos 系列模型卡、Project Glasswing 联盟介绍、还有 Anthropic 内部 disclosure 流程的公开版。Project Glasswing 是什么？这是 Anthropic 自己取的名字——"玻璃翼"——一个由 AWS、Apple、Microsoft、Google、CrowdStrike、Palo Alto Networks 加上另外约 40 家组织组成的封闭测试联盟。Anthropic 4 月公布 Mythos Preview 那天明确写了一句话：

> "We believe releasing Mythos publicly would be irresponsible given its offensive potential."

翻译：考虑到它的进攻潜能，把 Mythos 公开发布是不负责任的。

但下一句紧跟着——Project Glasswing 已经把 Mythos 给 40 多家"通过审查"的组织内部测试用了。一边说公开发布不负责任，一边给 40 家朋友先用上。这句话有一个非常诚实的逆读法——

"我练出了一把没人挡得住的刀，先递给我的朋友们。"

Anthropic 同时披露：通过 Mythos 已经在开源软件和闭源软件里发现了**几千个高严重级和严重级漏洞**，其中超过 99% 在博客发出来时**还没打补丁**。"还没打补丁"——这一行是这一整篇里最值得读三遍的事实。

为什么还没打补丁？因为 Anthropic 走的是负责任披露流程——CVE 系统的标准时间是 90 天，Anthropic 在公司博客里承诺最长 90+45 天后会把 SHA-3 哈希换成漏洞详情链接。这个流程本身是行业最佳实践。

但流程最佳实践，赶不上漏洞发现速度的相位变化。

人类安全研究员一个月找到的高严重漏洞是个位数到十几个；Mythos 一次跑通在一个开源仓库里就能拉出几十上百个候选，过了人工复核还能剩下几十个真实漏洞。Anthropic 自己披露："contracting professional security contractors to manually validate every bug report before sending it out"——雇了一批外部安全顾问做人工复核，每一份漏洞报告都得过一道人审。这个动作本身是负责任的，但它也变相揭示了模型的产出速度——必须配上一整支顾问团队才能审完。

把这件事翻成自然语言——

Anthropic 的 Mythos 现在在批发漏洞，批发速度比所有受影响厂商打补丁的速度合计还快。99% 的"已知"漏洞处在"已经被发现、但还在等修复窗口"的状态。这些漏洞的 SHA-3 哈希以承诺的方式锁在 Anthropic 的服务器上。Anthropic 一边等厂商打补丁，一边继续训下一代 Mythos——下一代 Mythos 找漏洞的速度只会更快，等待打补丁的库存只会更大。

这种局面叫什么？这叫做**"主动方建库存，被动方搬砖"**。

Schneier 写过——他是上世纪 90 年代以来全世界最有名的密码学家和安全研究员之一，从来是攻防双方都尊敬的那种少数派——4 月那篇关于 Mythos 的评论里他用了一个词："asymmetry"。攻击方靠一份模型就能批发漏洞，防御方靠的是几千万家企业各自掏钱雇人去打补丁。这种结构性不对称是这一代 AI 的特征，不是 bug。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：对账
【副标题】：Mythos 漏洞库存 vs 业界补丁速度
【核心判断】：发现速度甩开修复速度，库存在 Anthropic 一侧持续累积
【核心内容】：
  - Mythos 已披露漏洞总量（高/严重级）[流入]：几千
  - 已修复并公开的漏洞 [流出]：&lt;1%
  - 仍处在 disclosure 等待期 [滞留]：&gt;99%
  - 负责任披露窗口：90+45 天
【备注】：Anthropic 雇佣外部安全顾问做人工复核，复核完才能发出去；下一代 Mythos 训练时间窗口比披露窗口短</pre></details>
</div>

---

## 四、靶场没设防御方，现实世界也快没有了

AISI 自己在评估报告里写了一段免责声明，这段免责声明在中文媒体的转载里几乎全都被砍掉了。原文是这样的——

> "The benchmark environments lack security features that are often present, such as active defenders and defensive tooling, and there are no penalties for the model for undertaking actions that would trigger security alerts."

翻译：靶场环境缺少现实里通常存在的安全特性，比如主动防御方和防御工具；模型做任何会触发安全告警的动作都不会被惩罚。

这段话两个用法。

第一个用法是政府机构的常规免责——告诉公众别因为模型 6/10 通关就觉得自家公司明天就会被打穿。AISI 不希望这份报告变成"AI 末日来了"的标题党素材。这一层是合理的。

第二个用法是 AISI 的诚实——这份评估测的不是"模型在已部署 EDR、SOAR、SIEM、SOC 7×24 监控、防火墙规则齐全的网络里能不能打穿"，而是"模型在干净环境里能跑出多远"。这个区别非常关键。前者是"实战测试"，后者是"能力上限"。AISI 测的是能力上限——他们告诉你这个模型至少能跑这么远，至于现实里它会跑得更近还是更远，取决于防御一侧的具体情况。

那么现实里防御一侧的情况是什么？

按照 IBM 2025 年的全球安全调查，全球有专职 SOC（Security Operations Center）团队的企业大约占 30%——这 30% 还集中在金融、电信、政府、能源这些行业。剩下 70% 的企业——制造业、零售业、教育、医疗、地方政府、各种中小服务业——要么是有但形同虚设，要么是全外包给 MSSP（托管安全服务），要么干脆只有一个 IT 行政人员兼任安全管理员。

这 70% 在 AISI 的术语里就叫 "small, weakly defended and vulnerable enterprise systems"。

也就是说，AISI 描述的"小型、防御薄弱、有漏洞的企业系统"——不是"少数极端样本"，是"全球绝大多数企业"。Mythos 和 GPT-5.5-Cyber 现在在 AISI 靶场上跑出来的 6/10 和 2/10，是针对这 70% 企业的实战预测。

更糟糕的是，防御一侧的 AI 能力增长曲线远远跑输攻击一侧。攻击方只需要"能在标准化靶场上一次跑通"就能 commercialize 攻击能力——卖给情报机构、卖给犯罪集团、嵌进 ransomware-as-a-service 的工具链。防御方需要的是"能跨千万种企业环境、千万种业务逻辑、千万种历史包袱里跑通的方案"——这种方案没办法被一个模型一次性吃下，必须靠每家企业自己的 SOC 团队配合本地化部署。

后者的成本是前者的几十倍。后者的训练数据是前者的几十分之一。后者的迭代周期是前者的几倍。这个结构性差异，意味着 AISI 报告里写的"主动防御方"和"防御工具"——在攻击曲线已经爬到 32 步通关的 2026 年——仍然在用 2018 年的节奏在更新。

行业里早就有人提醒过这一点。Bishop Fox 在 4 月 14 日 Mythos 评估出来当天就发了一篇分析，标题里直接用了 "inflection point"——拐点。Cloud Security Alliance 同期挂出来的研究 note 题目叫 "AI Autonomous Offensive Threshold"——AI 自主进攻能力阈值。Bloomsbury Intelligence and Security Institute 把这件事写进了关于"网络安全风险加速"的报告。

但这些机构的分析最多被读到 Twitter 上的相关圈子里。打开任何一家普通企业的董事会，AI 议题还是停留在"我们 ChatGPT 怎么不被员工乱用"和"我们要不要买 Copilot"。

防御方还在卷自动化补丁。攻击方已经一次跑通 32 步。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：对账
【副标题】：攻击方与防御方 AI 应用节奏差
【核心判断】：靶场上没有防御方，现实世界的 70% 企业里也几乎没有
【核心内容】：
  - 有专职 SOC 团队企业占比 [流出]：约 30%
  - 防御薄弱、合 AISI 描述企业占比 [流入]：约 70%
  - 攻击方迭代周期（Mythos → GPT-5.5 追平）：约 30 天
  - 防御方对应工具链迭代周期：以年为单位
【备注】：IBM 2025 全球安全调查；AISI 评估对"防御薄弱"系统给出"至少有能力自主攻击"判断</pre></details>
</div>

---

## 五、"The Last Ones" 这个名字，起得很诚实

把这一周的所有事实摆回来——

4 月 14 日，AISI 公布 Mythos Preview 是第一个跑通 32 步攻击链的模型。  
4 月底，Anthropic 自己把 Mythos checkpoint 的通关率从 3/10 推到 6/10。  
5 月 14 日，AISI 公布 GPT-5.5-Cyber 也跑通了，95 个 CTF 上 71.4% 跟 Mythos 的 68.6% 误差范围内。  
5 月 14 日同一天，OpenAI 把"通过 AISI TLO 评估"写进 GPT-5.5-Cyber 的 system card。  

这五件事压在一起，告诉你两个判断。

第一个判断是产业层面的。所有现在还在新闻里被叫"前沿模型"的实验室——Anthropic、OpenAI、Google DeepMind、Meta、xAI——会在接下来 12 个月里，把"AISI TLO 通关率"和"95 CTF 专家级准确率"这两栏写进自己的 system card。这意味着 2027 年的前沿模型 baseline 里就**必然**包含一个能完整跑完 32 步攻击链的版本。所有训出来不带这能力的模型，会被市场认定为"性能不够"，被竞品挤出 enterprise 采购名单。这条曲线是单向的，没有刹车点。

第二个判断是用户层面的。如果你公司不属于那 30% 有专职 SOC 的——你不在金融、电信、政府、能源这种被监管的行业——那"前沿模型的攻击能力"从此就跟你的企业网络处在 AISI 描述的那种关系里：模型一旦拿到任意一个内网门票（凭证泄露、钓鱼邮件、第三方供应商被打穿），剩下的 32 步它能自己跑完，时间从人类的 20 小时压到模型的一次任务运行。这意味着**针对中小企业的攻防游戏，在 2026 年这一年里被永久改写了**——不是说更危险一点点，是说防御方原本依赖的"攻击者要花时间所以能被 SOC 抓到"这个基础假设，被打掉了。

回头看那个名字——AISI 给这个套件起名 "The Last Ones"，意思字面是"最后那些"。在政府安全圈里这种命名通常有一层 inside joke——"the last ones to fall"——最后一批倒下的目标。AISI 设计这个套件的本意大概是：能通关这个套件的模型就是"最后一批要担心的模型"，意思是过了这一关再往上的能力就该被严格管控了。

但实际跑出来是另一回事。两个最顶尖的模型一个月内分别通关，第三个、第四个会很快跟上。"The Last Ones" 这个名字从"最后一批要担心的模型"变成了"最后一批能扛得住的企业"——能扛过这套攻击链的企业，会越来越少。

所以这个名字真起得对。它不是 AI 攻击能力的最后一关，是企业网络防御的最后一关。

要给两个可证伪的观察点你来检验——

第一，看下一个季度（Q3 2026）会不会有第一例公开归因的 AI 主导企业网络入侵案例。"AI 辅助钓鱼邮件"那种我不算——我说的是带完整攻击链证据、能被 incident response 公司复盘出"这一步明显是模型自主决策"的事件。如果 Q3 没有、Q4 也没有，那 AISI 这套评估的现实威胁性可以再让子弹飞一阵；如果半年内出现 1 例，那这件事就锁死了。

第二，看 Anthropic 公布的"Mythos 已发现但未披露"漏洞库存数。Anthropic 4 月披露的是"几千个"。如果到 Q3 这个数字翻到一万级别，那就证明 Mythos 这一代还在线性增长；如果直接跳到十万级别，那这件事的尺度比这篇文章估算的还要严重一档。

两个观察点都是硬数据。在那之前——

下次你再听到 AI 公司用"安全"两个字开头讲一个产品发布，不妨先问一句：你 PR 稿里这一栏写的，是"我让大家更安全"，还是"我把'打穿大家'这件事做到了行业第一"？

这两件事不一样。

第一件是商业模式。

第二件是行业现实。

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>A glowing minimalist corporate office building at night with 32 sequential locked doors lined up in a row leading deep into perspective, each door progressively more open than the previous, abstract digital threat lines flowing through them, dark navy and electric blue color palette, flat editorial illustration style, no text, no labels, dramatic side lighting, conceptual cybersecurity theme</pre></details>
</div>

---

## 数据来源

- [AISI 评估 — Claude Mythos Preview cyber capabilities](https://www.aisi.gov.uk/blog/our-evaluation-of-claude-mythos-previews-cyber-capabilities)
- [AISI 评估 — OpenAI GPT-5.5 cyber capabilities](https://www.aisi.gov.uk/blog/our-evaluation-of-openais-gpt-5-5-cyber-capabilities)
- [Anthropic 官方 — Claude Mythos Preview 发布页](https://red.anthropic.com/2026/mythos-preview/)
- [The Decoder — Mythos 第一个通关 AISI cyberattack 仿真](https://the-decoder.com/new-claude-mythos-becomes-the-first-ai-model-to-clear-all-cyberattack-simulations-from-britains-ai-safety-agency/)
- [The Decoder — GPT-5.5 在 AISI 测试中追平 Mythos](https://the-decoder.com/gpt-5-5-matches-claude-mythos-in-cyber-attack-tests-uk-ai-security-institute-finds/)
- [The New Stack — Mythos Preview 完成完整 cyberattack 模拟](https://thenewstack.io/claude-mythos-preview-simulation/)
- [CyberScoop — 前沿模型打破自主进攻基准](https://cyberscoop.com/ai-autonomous-cyber-capability-benchmarks-broken-gpt5-claude-mythos/)
- [Help Net Security — Mythos offensive 能力与限制测试](https://www.helpnetsecurity.com/2026/04/14/claude-mythos-test-attack-capabilities-limits/)
- [Schneier on Security — On Anthropic's Mythos Preview and Project Glasswing](https://www.schneier.com/blog/archives/2026/04/on-anthropics-mythos-preview-and-project-glasswing.html)
- [Cloud Security Alliance — AI Autonomous Offensive Threshold](https://labs.cloudsecurityalliance.org/research/csa-research-note-claude-mythos-autonomous-offensive-thresho/)
- [Bishop Fox — Mythos Preview cybersecurity inflection point](https://bishopfox.com/blog/anthropics-claude-mythos-preview-the-ai-cybersecurity-inflection-point)
- [BISI — Mythos 与网络安全风险加速](https://bisi.org.uk/reports/claude-mythos-and-the-acceleration-of-cybersecurity-risk)
- [Slashdot — GPT-5.5 匹配 Mythos Preview 安全测试](https://it.slashdot.org/story/26/05/01/1658212/gpt-55-matches-heavily-hyped-mythos-preview-in-new-cybersecurity-tests)
- [Winbuzzer — GPT-5.5 在安全测试中追平 Mythos](https://winbuzzer.com/2026/05/14/openais-gpt-55-matches-claude-mythos-in-security-tests-xcxwbn/)
- [ResultSense — AISI Mythos First AI to Solve 32-Step Cyber Range](https://www.resultsense.com/news/2026-04-14-aisi-mythos-preview-cyber-eval-uk-banking-response/)
- [Postquantum — Mythos Preview 与 20 年网络安全均衡的终结](https://postquantum.com/security-pqc/anthropic-mythos-preview-ai-offensive-security/)
