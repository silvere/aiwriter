export const meta = {
  name: 'aiwriter-research',
  description: 'AIWriter Step 2 深度研究：5 视角并行扫描 → 关键数字交叉核验 → 综合成研究报告',
  whenToUse: 'aiwriter 技能 Step 2 深度研究（微信公众号/小红书文章前期调研）',
  phases: [
    { title: '扫描', detail: '5 个视角并行搜集，各自带来源' },
    { title: '核验', detail: '关键数字交叉核验（≤8 条）' },
    { title: '综合', detail: '合成 8 节研究报告 + 竞品扫描 + 专家建议' },
  ],
}

// args: { topic: string, refs?: string, depth?: string, extra?: string }
if (typeof args === 'string') { try { args = JSON.parse(args) } catch (e) {} }  // 兜底：args 有时以 JSON 字符串传入
if (!args || !args.topic) throw new Error('需要 args.topic（研究主题）')
const topic = args.topic
const refs = args.refs || '无'
const depth = args.depth || '快速了解'
const extra = args.extra || ''

const FACTS_SCHEMA = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          fact: { type: 'string', description: '一条具体事实/观点/案例，含数字、名字、时间' },
          source: { type: 'string', description: '来源名称' },
          url: { type: 'string' },
          isKeyNumber: { type: 'boolean', description: '是否为文章可能引用的关键数字' },
        },
        required: ['fact', 'source'],
      },
    },
    angleNotes: { type: 'string', description: '该视角下值得写的角度建议，≤150 字' },
  },
  required: ['findings', 'angleNotes'],
}

const LENSES = [
  { key: '背景机制', brief: '背景历史与运作机制：这件事怎么来的、底层机制是什么、关键转折点' },
  { key: '动态数据', brief: '最新动态与硬数据：近 3 个月进展、可引用的关键数字（务必带出处与时间）' },
  { key: '竞品扫描', brief: '同题竞品：搜近期同主题中文爆款/热门文章 3-5 篇，记录每篇的核心判断 + 常用类比（用于差异化）' },
  { key: '专家反方', brief: '专家与反方：该领域 3 位真实顶级专家（产业/技术/社会三视角）的公开观点，以及对主流叙事最强的反对意见' },
  { key: '案例故事', brief: '具体案例与故事素材：有名有姓有时间的案例、场景细节、当事人原话' },
]

phase('扫描')
const sweeps = await parallel(LENSES.map(l => () =>
  agent(
    `用 WebSearch / WebFetch 研究主题「${topic}」。\n` +
    `你的视角（只做这一个视角，别的视角有别人负责）：${l.brief}\n` +
    `参考链接：${refs}\n研究深度：${depth}\n${extra ? '补充要求：' + extra + '\n' : ''}` +
    `⛔ 硬约束（最高优先级）：严禁调用 Agent/Task 等任何派生子代理的工具（嵌套曾炸出 100+ 代理）；` +
    `WebSearch ≤8 次、WebFetch ≤6 次，到顶即停、用已有材料返回；同一数字核实一次就够。\n` +
    `要求：每条事实必须带来源；文章可能直接引用的关键数字标 isKeyNumber=true；` +
    `拿不到一手来源的传闻不要收。不要写文章，只返回结构化事实。`,
    { label: `研究:${l.key}`, phase: '扫描', model: 'sonnet', effort: 'medium', agentType: 'general-purpose', schema: FACTS_SCHEMA }
  )
))

const all = sweeps.filter(Boolean)
if (!all.length) throw new Error('全部研究视角失败，检查网络/搜索工具')

phase('核验')
const keyNums = all.flatMap(s => s.findings).filter(f => f.isKeyNumber).slice(0, 8)
log(`关键数字 ${keyNums.length} 条进入交叉核验（上限 8 条）`)
const VERDICT_SCHEMA = {
  type: 'object',
  properties: { confirmed: { type: 'boolean' }, note: { type: 'string', description: '≤60 字：核验依据或存疑原因' } },
  required: ['confirmed', 'note'],
}
const verdicts = await parallel(keyNums.map(f => () =>
  agent(
    `交叉核验这条关键数据是否属实、出处是否可靠：「${f.fact}」（来源：${f.source} ${f.url || ''}）。\n` +
    `用独立的 WebSearch 验证（换关键词、找第二来源）。找不到第二来源或数字对不上 → confirmed=false。拿不准也算 false。\n` +
    `⛔ 硬约束：严禁调用 Agent/Task 派生子代理；WebSearch ≤3 次、WebFetch ≤2 次，到顶即停按现有证据下结论。`,
    { label: '核验', phase: '核验', model: 'sonnet', effort: 'low', agentType: 'general-purpose', schema: VERDICT_SCHEMA }
  )
))
const checked = keyNums.map((f, i) => ({ fact: f.fact, source: f.source, ...(verdicts[i] || { confirmed: false, note: '核验失败' }) }))

phase('综合')
const report = await agent(
  `把以下多视角研究材料综合成一份研究报告（中文，约 2000 字），按 aiwriter-research 的 8 节标准格式：\n` +
  `①主题速览 ②背景与机制 ③最新动态 ④关键数据（只用核验通过的） ⑤关键案例 ⑥争议与风险 ⑦竞品扫描（每篇核心判断+类比） ⑧写作角度建议 + 专家挑选建议（3 位真实专家：产业/技术/社会）。\n` +
  `核验结果里 confirmed=false 的数据必须弃用或明确标注「存疑」。所有数字保留来源。\n\n` +
  `【多视角材料】\n${JSON.stringify(all)}\n\n【关键数字核验】\n${JSON.stringify(checked)}\n\n` +
  `⛔ 硬约束：只基于给定材料综合，不要调用任何搜索或子代理工具。\n` +
  `只返回报告正文，不要客套话。`,
  { label: '综合报告', phase: '综合', effort: 'high' }
)

return {
  report,
  verifiedNumbers: checked.filter(c => c.confirmed),
  droppedNumbers: checked.filter(c => !c.confirmed),
}
