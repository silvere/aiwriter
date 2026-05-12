# 99% 的零日漏洞没补，因为 Anthropic 还没决定让谁补

> **发布日期**：2026-05-12 | **分类**：AI 商业拆解

## 核心观点

- Project Glasswing 的 partner list 上没有 OpenSSL 维护者、没有 curl 维护者、没有 Debian Security Team——选门票的标准不是"软件多关键"，是"组织能不能签 enterprise NDA"
- Anthropic 自己公告页面写着"99% of the vulnerabilities have not yet been patched"，前面三个数字上头条，这个数字没人转
- 评估"safety-first AI"项目时，问的是"谁不在你们 partner list 里"——能力 demo 是产品，partner list 才是商业模式

---

## 导语

4 月 8 日，Anthropic 发了一份声明，叫 Project Glasswing。声明里塞了三个数字：thousands of zero-day vulnerabilities（挖出几千个零日漏洞）、every major operating system（每一个主流操作系统都有）、every major web browser（每一个主流浏览器都有）。

这三个数字上了全球科技媒体的头条。OpenBSD 一个 27 年没被发现的 SACK 漏洞、FreeBSD 17 年的 CVE-2026-4747——两个具体例子被引用了几千遍。Dario Amodei 不久前去白宫见了 Trump 团队。各家 CSO 内部群里转着同一个截图。

但同一份声明里还有第四个数字。位置很偏，写在 disclosure 政策那一段：

> **Over 99% of the vulnerabilities Mythos has found have not yet been patched.**

翻译过来：Mythos 找到的漏洞，超过 99% 还没修。这句没人转。

把这两组数字摆一块儿看个三分钟，整件事的形状才出得来。

<div class="img-placeholder concept">
  <div class="img-placeholder-icon">🎨</div>
  <div class="img-placeholder-label">概念图占位</div>
  <details><summary>生成 Prompt</summary><pre>A large vault door with the Anthropic logo, glowing keys hanging on a keychain held by a corporate executive's hand, dozens of smaller vault doors in the background labeled with operating system names locked tight, dramatic chiaroscuro lighting, financial corporate noir style, no text, no labels, clean composition, dark blue and gold palette</pre></details>
</div>

---

## 一、那张 partner list 上谁不在

Project Glasswing 的发起伙伴一共 12 家，名单如下：

AWS、Apple、Broadcom、Cisco、CrowdStrike、Google、JPMorganChase、Linux Foundation、Microsoft、NVIDIA、Palo Alto Networks，加 Anthropic 自己。

Anthropic 同时给了 40 多家"关键软件维护机构"扩展访问权限，具体名单没公开。

这张名单里有三类玩家：四大云厂商（AWS、Apple、Google、Microsoft）、四家网络安全上市公司（Cisco、CrowdStrike、Palo Alto、Broadcom）、一家半导体（NVIDIA）、一家银行（JPM）、一家法律实体（Linux Foundation）。

每家都能开 enterprise procurement，能让 GC 在两小时内 review 完 NDA。现在做个减法。

世界上跑得最多的开源软件维护者：OpenSSL 项目（Stephen Henson 那一批人）——不在。curl（Daniel Stenberg 一个人扛了 25 年）——不在。OpenBSD 项目——不在，讽刺的是 27 年那个 SACK bug 就是他们家的。Debian Security Team——不在。OWASP——不在。Postgres core team——不在。FFmpeg 维护者——不在，他们家的代码刚被 Mythos 扫了一遍。

Linux Foundation 在名单上，但 Linux Foundation 是一个法律实体，它不写代码。写 Linux 内核 RCU 那个模块的 Paul McKenney？不在。

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：对账图
【副标题】：Project Glasswing 的 partner list 选了谁，缺了谁
【单位】：家
【核心判断】：12 家 enterprise + 1 个法律实体，0 个真正写代码的开源维护者
【核心内容】：
  - 云厂商 (AWS/Apple/Google/Microsoft) [流入]：4
  - 安全上市公司 (Cisco/CrowdStrike/Palo Alto/Broadcom) [流入]：4
  - 其他企业 (NVIDIA/JPM) [流入]：2
  - 法律实体 (Linux Foundation) [流入]：1
  - 独立开源维护者 (OpenSSL/curl/OpenBSD/Debian/OWASP) [流出]：0
  - FFmpeg/Postgres/Nginx 等被扫软件的核心 maintainer [流出]：0</pre></details>
</div>

这名单的选择标准不是"软件多关键"。

12 家发起伙伴管理的代码总行数，加起来都不一定比 Debian 一个发行版多。OpenSSL 跑在世界上 80% 的 HTTPS 服务器上，curl 装在地球上每一台 Linux 机器和大半台 Windows 机器上——按"关键软件"排序，它们应该在第一行。

但它们没法签 enterprise NDA。Daniel Stenberg 一个人没法跟 Anthropic legal 来回过 12 版合同；OpenBSD 项目没有可以挂在合同抬头上的法律实体；OWASP 是会员制非营利，理事会决议过不了"接受单方面访问限制"这一条。

partner list 真正的筛选条件，是 **能不能跟 Anthropic 签字**。

这跟"关键基础设施"是两回事。

---

## 二、99% 没补，是处理瓶颈，还是发牌优势

Anthropic 自己在 disclosure 政策那一段，把没补的原因解释得很标准：Coordinated vulnerability disclosure 是行业惯例，周期 90 天 + 45 天宽限期，加起来 135 天，Mythos 一次扫出几千个，量大、人类 triager 处理不过来，所以 99% 还卡在流程里。

短期看，这个解释合理。但你把它跟另外几组数据摆在一起，画风就开始变了。

第一组：被披露的几个具体例子，全是 17 年起步、最远 27 年。OpenBSD 那个 SACK bug 在仓库里趴了 27 年没人发现，那不是一个漏洞，那是几代人 review 过的代码。Mythos 找一个，需要不到一小时。

第二组：Anthropic 给的 Linux 内核 benchmark。100 个 2024–2025 年的内存破坏类 CVE，Mythos 标了 40 个"看起来可继续利用"。换句话说，**已经打过补丁的洞，它还能从同一份代码里再翻出新的 exploit 路径**。

第三组：Vidoc Security Lab 4 月底做的复现实验——只用市场上人人能买到的 GPT-5.4 和 Claude Opus 4.6，跑一套标准化的 chunked security review，FreeBSD、Botan、OpenBSD 三类样本全部复现 Mythos 的核心发现；FFmpeg 和 wolfSSL 部分复现。

把三组数据合并：挖一个 0day 的边际成本，已经低到一台 MacBook 加一个月度订阅。攻击方的迭代周期，按小时算。

那 135 天的 disclosure 窗口在守护谁？

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：对账图
【副标题】：Anthropic 持有的 0day 库存周期 vs 攻击者迭代周期
【单位】：小时
【核心判断】：补丁周期按月算，复现周期按天算，攻击周期按小时算
【核心内容】：
  - Anthropic 标准 disclosure 周期 (90+45 天) [流出]：3240
  - 顶级安全研究员手工挖一个 0day 平均周期 [流出]：720
  - Vidoc 用公开模型复现 Mythos 发现 [流入]：48
  - 攻击者拿到漏洞细节后写 exploit [流入]：24
  - Lapsus$ 通过 Mercor 泄露猜出 Anthropic 文件命名 [流入]：12</pre></details>
</div>

99% 没补，意味着这 99% 的漏洞所有权——至少是"在补丁公开发布之前，谁知道这个漏洞"的所有权——握在 Anthropic 内部档案里。

被发到 maintainer 邮箱的，是被选中的那批：时间窗口外、被高严重性 triager 标过 P0、且 partner 名单内有人能"对接"维护方的那批。OpenBSD 那个 27 年 bug 之所以补了，是因为 Linux Foundation 在桌上，OpenBSD 项目通过 Linux Foundation 的 OpenSSF 渠道间接接到了 patch。

其他 99% 长什么样？不知道。Anthropic 自己也说："per our coordinated vulnerability disclosure process"，我们不公开细节。

这话从 Project Zero 嘴里说出来，很 OK——Google 的 Project Zero 每个 90 天到期就公开 CVE 编号、写 blog 详解、再开 OffensiveCon 上去做演讲，全套披露动作做满。

从 Anthropic 嘴里说出来，是另一回事——它压根没有公开 CVE 计数器、没有自己的漏洞 advisory 序号空间、没有 deadline 到期后的"自动公开"承诺。99% 没补，下一步是什么？是某天 Anthropic legal 觉得披露时机合适，挑一批发给挑中的 partner。

补丁本身是公共物品；但**谁先拿到补丁、谁能在补丁发布前先把内网防御调整好，这是私有物品**。99% 这个数字越大，私有物品的存货就越多。

这不是"处理瓶颈"，这是"发牌优势"。

---

## 三、"太危险所以不公开"，问题是它已经不那么稀缺了

Anthropic 不公开 Mythos 的理由，是 capability dangerous to release——能力太危险，公开会被滥用。听上去很负责任。但市场告诉我们另一件事。

4 月底，一家叫 Vidoc Security Lab 的安全公司发了一篇技术博客。他们没拿到 Mythos 的访问权，partner list 上也没他们。他们做的事很简单：把 Anthropic 公开的几个 case study——FreeBSD CVE-2026-4747、OpenBSD SACK bug、Botan 的几处弱点——做成 reproducible workflow，喂给 GPT-5.4 和 Claude Opus 4.6（一个月 20 美金谁都能开），看公开模型能不能找到同样的漏洞。

结论是三类样本完全复现，两类部分复现。

翻译过来：你说"太危险"的那个能力，80% 已经在月度订阅级别的公开模型里。Anthropic 自己 4 月 8 日的声明里也写得很清楚——Mythos 在内部 cyber benchmark 上比 Claude Opus 4.6 强 1.5–2 倍。强 1.5–2 倍是真的，但 Opus 4.6 不是零分，是 100 分里拿了 40 分，Mythos 拿到 80 分。

40 分够干嘛？够把 Mythos 找到的"thousands"复现一大半。

那么"太危险不公开"在防的是谁？

不是国家级 APT。一个 APT 团队按硅谷价位招 20 个安全研究员，工资成本一年 1000 万美元，找一个 0day 边际成本 50 万。给他们一台 GPT-5.4，边际成本砍到 5 万。Mythos 砍到 1 万。从 50 万降到 5 万和从 5 万降到 1 万，对 APT 来说没什么差别——预算和招人门槛早就跨过临界点。

它防的是中间那批人——不在 partner list 上、但有合规要求的企业内 red team。它防的是想要复现"thousands of 0day"这条头条但没钱开 enterprise 合同的二三线安全公司。它防的是开源生态里那些做 vulnerability research 一辈子的研究员，他们曾经能跟 Project Zero 平起平坐发现 bug，现在被关在门外。

而真正最该被防的——攻击方——已经能用公开工具做出 60%+ 的工作。

如果觉得这还不够反讽，再加一个镜头。4 月 21 日，TechCrunch 报道：一个 Anthropic 第三方承包商的员工，用 Mercor 数据泄露里抓到的内部文件命名规则（Mercor 是另一家 AI feedback 公司，4 月初被 Lapsus$ 通过 LiteLLM 这个开源工具的漏洞拿下了），猜出 Mythos 在 Anthropic 内部受限环境的部署路径，进去看了一眼，又把同事拉进来一起看。

Anthropic 自己投资建的"安全访问环境"，被 contractor 用一次开源工具漏洞泄露 + 文件命名规则猜测就破了。

这是 Project Glasswing 启动两周后的事。

防外人，没防住自己。

---

## 四、Schneier 在博客上写的那一段

Bruce Schneier 在 4 月底自己的博客上发了一篇短文，标题叫《On Anthropic's Mythos Preview and Project Glasswing》。

这位是密码学界过去三十年最有发言权的人之一。文章不长，一千字左右，但里面有一句话特别值得抄下来：

> "A private company can unilaterally classify a capability as too dangerous for the public, grant selective access to the largest incumbents in the affected industry, and construct a parallel disclosure regime outside any democratic accountability structure."

我把它翻成中文，再拆三段：

第一段：**一家私人公司，单方面**判定某项能力"对公众太危险"。

第二段：把访问权**有选择地**发给"受影响行业里最大的几家在位玩家"。

第三段：在 CVE、CISA、ENISA、CERT 这一整套官方漏洞披露体系之外，**另起炉灶搭一套平行的披露机制**，绕开所有民主问责结构。

Schneier 同一段里还有一句更狠的："This is very much a PR play by Anthropic."

这是不是新东西？不全是。90 天披露规则不是 Anthropic 发明的，Google Project Zero 2014 年就这么干了——当年 Project Zero 找了苹果一个 macOS 内核 bug，90 天到期苹果没补，Project Zero 当天发 CVE 详解，整个安全行业为这条规则的合法性吵了三年。

Project Zero 干完一件事就把它公开化：CVE 编号公开、技术细节公开、PoC 公开。它的"单方面"是写在台面上的——我现在就告诉所有人这个 bug 的细节，谁先用看本事，Apple 不补是 Apple 自己的事，Project Zero 不会替它保密。

Anthropic 的"单方面"是关着门的：我不告诉所有人 bug 在哪，我告诉 partner list 里 12 家。我不公开 CVE，我让 partner 之间内部通报。我不发 PoC，我把 PoC 写进 Mythos 模型本身，partner 想要 PoC，向我申请就有。

Project Zero 是公开标准。

Anthropic 在做**私有标准**。

公开标准的合法性来自 transparency——所有人都能看到、所有人都能挑战。私有标准的合法性来自——好像也就只能来自 Anthropic 自己声称"我们是 safety-first lab"。

Schneier 不买这个账，所以他说这是 PR play。

我也不买这个账。但我比他更冷漠一点：Anthropic 不是在做 PR play，**Anthropic 在做产品**。

产品名字叫 Glasswing。SKU 是 partner 资格。定价是签 enterprise NDA + 接受单方面披露规则。客单价：你的内网先得到 0day 预警，外网晚 135 天。

PR 是副产品。

---

## 五、最后一把要挂上去的钥匙

partner list 现在 12 家，但这串钥匙上还差一把。

5 月初，美国联邦 CIO Gregory Barbaccia 在白宫管理预算办公室（OMB）发了一份内部通告，准备授权一个修改版的 Mythos 模型给联邦机构使用，原话里说 OMB 正在"and ensure the appropriate guardrails and safeguards are in place before potentially releasing a modified version of the model to agencies"。

往前回放几周——Anthropic CEO Dario Amodei 去白宫见过 Trump 团队。议程外界看不到，但白宫之后陆续发的几份关于 AI 的行政命令里，cyber capability evaluation 部分明显加重了。CAISI（Center for AI Standards and Innovation）4 月底跟 Google DeepMind、Microsoft、xAI 也签了 pre-deployment evaluation 协议——但 Anthropic 不在那批，因为 Anthropic 跟 CAISI 早在 2024 年就签过单独协议，已经是 inside player。

挂上去之后这串钥匙长什么样：

- 4 家美国云厂商
- 4 家美国安全上市公司
- 1 家半导体、1 家银行、1 个法律实体
- 40+ 家美国关键基础设施维护机构（具体名单不公开）
- 美国联邦政府

<div class="img-placeholder diagram">
  <div class="img-placeholder-icon">📊</div>
  <div class="img-placeholder-label">信息图占位</div>
  <details><summary>规格卡</summary><pre>【图类型】：饼图
【副标题】：Mythos 的访问权按地域分布
【单位】：%
【核心判断】：一家美国 AI 公司的 partner list，决定了全球操作系统漏洞何时披露
【核心内容】：
  - 美国企业/政府/机构：99
  - 其他地区 (欧洲/亚洲/拉美/非洲)：1</pre></details>
</div>

那不在这串钥匙上的人是谁？

欧盟的安全机构——不在。日本的 JPCERT——不在。中国的 CNCERT——不在，可以理解。印度 CERT-In、巴西 CERT.br——不在。德国 BSI、英国 NCSC——不在。

所有这些机构维护的、保护本国关键基础设施的、被 Mythos 扫过的那些操作系统、浏览器、数据库——补丁什么时候到？取决于 Anthropic 把哪几个 0day 排进下一批 disclosure，取决于 Anthropic 的 partner list 上有没有人有动机推这个 patch。

LSE Media 5 月 11 号有一篇博客，标题叫《Claude Mythos and the Myth of Containment》。里面有一段话：

> If this knowledge remains restricted to a limited number of states and private actors, it will do little to contain the risks associated with models like Claude Mythos.

把它再往下推一步：restricting 不是 contain 的工具，restricting 本身就是这套商业模型的产品。

Mythos 越被宣传成"危险的"，partner 名单的稀缺性越高。越稀缺，能签 enterprise NDA + 接受单方面规则的门槛越值钱。99% 没补的库存越大，"先得到补丁"的预警价值越高。整个 Glasswing 项目，看着像是 cyber defense，按经济学逻辑跑下来，是 cyber subscription——而且是只发给会员的 subscription。

会员之外的世界，凑合用。

会员之外的 maintainer，凑合等。

会员之外的人，需要补丁的时候，找 Anthropic 申请会员。

这是产品。

不是项目。

---

## 数据来源

- [Anthropic 官方公告 Project Glasswing](https://www.anthropic.com/project/glasswing)
- [Anthropic 红队公告 Claude Mythos Preview](https://red.anthropic.com/2026/mythos-preview/)
- [Schneier on Security：On Anthropic's Mythos Preview and Project Glasswing](https://www.schneier.com/blog/archives/2026/04/on-anthropics-mythos-preview-and-project-glasswing.html)
- [Vidoc Security Lab：We Reproduced Anthropic's Mythos Findings With Public Models](https://blog.vidocsecurity.com/blog/we-reproduced-anthropics-mythos-findings-with-public-models)
- [TechCrunch：Unauthorized group has gained access to Anthropic's exclusive cyber tool Mythos](https://techcrunch.com/2026/04/21/unauthorized-group-has-gained-access-to-anthropics-exclusive-cyber-tool-mythos-report-claims/)
- [Tom's Hardware：How a cavalcade of blunders gave unauthorized users access to Claude Mythos](https://www.tomshardware.com/tech-industry/cyber-security/how-a-cavalcade-of-blunders-gave-unauthorized-users-access-to-claude-mythos-restricted-model-accessed-by-third-parties-thanks-to-knowledge-from-data-breach)
- [Help Net Security：Anthropic's new AI model finds and exploits zero-days across every major OS and browser](https://www.helpnetsecurity.com/2026/04/08/anthropic-claude-mythos-preview-identify-vulnerabilities/)
- [CSO Online：White House moves to give federal agencies access to Anthropic's Claude Mythos](https://www.csoonline.com/article/4160303/white-house-moves-to-give-federal-agencies-access-to-anthropics-claude-mythos.html)
- [LSE Media：Claude Mythos and the Myth of Containment](https://blogs.lse.ac.uk/medialse/2026/05/11/claude-mythos-and-the-myth-of-containment/)
