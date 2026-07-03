export const meta = {
  name: 'aiwriter-review',
  description: 'AIWriter Step 6 五刀审稿：角度/AI味/废话/读者/事实五刀并行 → 建议对抗校验 → 输出定稿修改清单',
  whenToUse: 'aiwriter 技能 Step 6 审稿（文章初稿完成后）',
  phases: [
    { title: '五刀', detail: '五个审稿视角并行读全文' },
    { title: '校验', detail: '对抗校验：驳回会把文章改差的建议' },
  ],
}

// args: { articlePath, title, platform, audience, coreClaim, styleCard }
if (!args || !args.articlePath) throw new Error('需要 args.articlePath（article.md 路径）')
const ctx =
  `文章文件：${args.articlePath}（用 Read 读全文）\n` +
  `标题：${args.title || '（见文件）'}\n平台：${args.platform || '微信公众号'}\n` +
  `目标读者画像：${args.audience || '（见文件导语推断）'}\n` +
  `核心判断：${args.coreClaim || '（从开篇提取）'}\n` +
  `风格备忘卡：${args.styleCard || '默认冷峻记者腔：具体事实优先、克制比喻、不替读者加戏'}\n`

const FINDINGS_SCHEMA = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          quote: { type: 'string', description: '问题段落的开头原句（精确抄写前 20 字，供定位）' },
          issue: { type: 'string', description: '问题是什么，≤60 字' },
          severity: { type: 'string', enum: ['高', '中', '低'] },
          action: { type: 'string', enum: ['砍段', '重写', '补论据', '删词', '改数据', '补桥句'] },
          suggestion: { type: 'string', description: '具体改法（重写类给出改后的方向，不用写全文）' },
        },
        required: ['quote', 'issue', 'severity', 'action', 'suggestion'],
      },
    },
    summary: { type: 'string', description: '本刀总评 ≤100 字' },
  },
  required: ['findings', 'summary'],
}

// 前三刀是质量核心 → 继承主控模型（不设 model）；读者/事实刀机械 → sonnet
const KNIVES = [
  {
    key: '角度刀',
    model: null,
    prompt: 'Read skills/templates/review-cuts.md 的「第一刀：角度刀」。重测核心判断的一刀测试三条（可证伪/反常识/行动含义），检查每节是否支撑核心判断，模拟 1 位领域专家读完是否会说"你没挡住我的刀"。',
  },
  {
    key: 'AI味刀',
    model: null,
    prompt: 'Read skills/templates/review-cuts.md 的「第二刀：AI 味刀」和 skills/templates/quotas.md 全文。做配额审计（比喻/加粗/段首路标词/一句话成段）、风格抽测 5 段（对照风格备忘卡，不像就整段判重写）、AI 味 2.0 特征扫描。',
  },
  {
    key: '废话刀',
    model: null,
    prompt: 'Read skills/templates/review-cuts.md 的「第三刀：废话刀」。逐节标出最弱的 20%（注水/重复/空过渡/空洞形容词），检查每 150 字至少 1 个新信息，总结式结尾判删。',
  },
  {
    key: '读者刀',
    model: 'sonnet',
    prompt: 'Read skills/templates/review-cuts.md 的「第四刀：读者刀」。扮演 3 类具体读者（核心共鸣/怀疑反驳/路人耐心薄）各读一遍，标 🚪想关掉/🪨想反驳/⏭️想跳过（必修）与 📤想转发/✏️想划线（保留项）。想关掉→重写，想反驳→补论据，想跳过→砍段。',
  },
  {
    key: '事实刀',
    model: 'sonnet',
    prompt: '你是事实核查员。把文中每个具体数字、人名、时间、事件逐一列出，对照文末「数据来源」链接（用 WebFetch 抽查）与独立 WebSearch 核验。对不上或查无出处的 → action=改数据，suggestion 里给出正确值或建议删除；夸大/过时的表述也算。只报事实问题，不管文笔。',
  },
]

phase('五刀')
const rounds = await parallel(KNIVES.map(k => () =>
  agent(
    `你是文章审稿员，只负责「${k.key}」这一个视角。\n${ctx}\n${k.prompt}\n` +
    `⛔ 硬约束：严禁调用 Agent/Task 派生子代理${k.key === '事实刀' ? '；WebSearch/WebFetch 合计 ≤10 次，到顶即停' : '；除 Read 模板与文章外不要联网'}。\n` +
    `只返回结构化 findings（quote 必须精确抄原文前 20 字），不要重复全文，不要改文。`,
    {
      label: `刀:${k.key}`, phase: '五刀', schema: FINDINGS_SCHEMA,
      agentType: 'general-purpose',
      ...(k.model ? { model: k.model, effort: 'medium' } : { effort: 'high' }),
    }
  )
))

// 汇总 + 按 quote 前 12 字去重（不同刀撞同一段时保留 severity 更高的）
const rank = { 高: 3, 中: 2, 低: 1 }
const byKey = {}
rounds.forEach((r, i) => {
  if (!r) { log(`⚠ ${KNIVES[i].key} 失败，本轮缺这一刀`); return }
  r.findings.forEach(f => {
    const key = f.quote.slice(0, 12)
    const item = { ...f, knife: KNIVES[i].key }
    if (!byKey[key] || rank[f.severity] > rank[byKey[key].severity]) byKey[key] = item
  })
})
const merged = Object.values(byKey)
log(`五刀共 ${merged.length} 条去重后建议`)

phase('校验')
// 对抗校验：只校验 高/中（低直接列为可选项）；上限 16 条控 token
const toVerify = merged.filter(f => f.severity !== '低').slice(0, 16)
const optional = merged.filter(f => f.severity === '低')
const VETO_SCHEMA = {
  type: 'object',
  properties: { refuted: { type: 'boolean' }, reason: { type: 'string', description: '≤60 字' } },
  required: ['refuted', 'reason'],
}
const vetoes = await parallel(toVerify.map(f => () =>
  agent(
    `你是"护稿人"，立场是尽量驳回没必要的修改。\n${ctx}\n` +
    `Read 文章后判断这条${f.knife}建议：定位「${f.quote}…」，问题「${f.issue}」，建议「${f.action}：${f.suggestion}」。\n` +
    `执行它文章会更好还是更差/无所谓？对照风格备忘卡与 skills/templates/quotas.md 的硬配额。` +
    `吹毛求疵、会伤害文气、或与配额冲突的 → refuted=true。真问题（事实错误、读者会关掉、明显注水）→ refuted=false。\n` +
    `⛔ 硬约束：严禁调用 Agent/Task 派生子代理；只 Read 文章与模板，不要联网。`,
    { label: `校验:${f.knife}`, phase: '校验', model: 'sonnet', effort: 'low', agentType: 'general-purpose', schema: VETO_SCHEMA }
  )
))
const confirmed = toVerify.filter((f, i) => vetoes[i] && !vetoes[i].refuted)
const rejected = toVerify.filter((f, i) => !vetoes[i] || vetoes[i].refuted)
  .map((f, idx) => ({ ...f, rejectReason: (vetoes[toVerify.indexOf(f)] || {}).reason || '校验失败' }))

log(`校验通过 ${confirmed.length} 条，驳回 ${rejected.length} 条，低优可选 ${optional.length} 条`)

return {
  mustFix: confirmed.sort((a, b) => rank[b.severity] - rank[a.severity]),
  optional,
  rejected,
  knifeSummaries: rounds.map((r, i) => (r ? { knife: KNIVES[i].key, summary: r.summary } : { knife: KNIVES[i].key, summary: '（本刀失败）' })),
}
