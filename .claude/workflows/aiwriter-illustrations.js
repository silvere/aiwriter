export const meta = {
  name: 'aiwriter-illustrations',
  description: 'AIWriter Step 5 配图：每张图一个代理，写 HTML → 渲染 PNG → 看图过验收闸 → 最多修 2 轮',
  whenToUse: 'aiwriter 技能 Step 5，Opus 出完配图设计简报之后',
  phases: [{ title: '出图', detail: '每张图独立：生成+渲染+视觉自查+修复' }],
}

// args: { briefs: [{ id, anchor, difficulty, work, caption, points, form }], workdir?: string }
if (!args || !Array.isArray(args.briefs) || !args.briefs.length) throw new Error('需要 args.briefs（配图设计简报数组）')
const workdir = args.workdir || '/tmp/aiwriter-ill'

const IMG_SCHEMA = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    escapedHtml: { type: 'string', description: '最终 .illustration HTML 片段，已做 HTML 转义（< → &lt; 等）' },
    qaPassed: { type: 'boolean' },
    rounds: { type: 'integer', description: '实际渲染轮数' },
    notes: { type: 'string', description: '未通过项或权衡说明，≤80 字' },
  },
  required: ['id', 'escapedHtml', 'qaPassed', 'notes'],
}

phase('出图')
const results = await pipeline(
  args.briefs,
  (brief) => agent(
    `你负责为公众号文章产出一张「理解图」，走完 生成→渲染→自查→修复 全回路。\n\n` +
    `第一步，Read skills/templates/illustration-spec.md —— 必须读全：§1 高大上铁律、§2 难点→形态词表、` +
    `§3 反模式清单、§4 统一 CSS 约定与视觉组件、§4.5 验收闸、§6 ECharts 多序列图。\n\n` +
    `配图简报：\n${JSON.stringify(brief)}\n\n` +
    `第二步，写 .illustration HTML 片段：把想法画成形状/关系/对比，禁止把要点排成文字列表；` +
    `只用 §4 约定的 class，不自带 <style>；单一强调色、留白、有视觉焦点；` +
    `真·多序列数据才用 §6 ECharts（SVG 渲染器 + fonts.ready 后 setOption + animation:false），≤4 个数据点用大数字/比例条。\n\n` +
    `第三步，渲染并亲眼看：\n` +
    `  mkdir -p ${workdir} && 把片段存为 ${workdir}/${brief.id}.html，然后\n` +
    `  python3 skills/scripts/render_illustration.py ${workdir}/${brief.id}.html ${workdir}/${brief.id}.png --width 1100 --scale 2\n` +
    `  用 Read 打开 PNG，过 §4.5 验收闸：遮住文字还剩信息吗？一图一主张吗？另查：文字溢出/截断、对齐、中文是否方块、图例是否可读。\n\n` +
    `第四步，不合格就改 HTML 重渲染，**最多再修 2 轮**（共渲染 ≤3 次）。仍不完美就在 notes 里说明取舍。\n\n` +
    `⛔ 硬约束：严禁调用 Agent/Task 派生子代理；不要联网搜索（一切素材来自简报与 spec）。\n\n` +
    `返回：id、最终片段的 HTML 转义版本（escapedHtml）、qaPassed、rounds、notes。`,
    { label: `图:${brief.id}`, phase: '出图', model: 'sonnet', effort: 'medium', agentType: 'general-purpose', schema: IMG_SCHEMA }
  )
)

const ok = results.filter(Boolean)
const failed = args.briefs.filter((b, i) => !results[i])
if (failed.length) log(`⚠ ${failed.length} 张图的代理失败：${failed.map(b => b.id).join(', ')}（主控需补做或改用 concept 占位）`)
log(`完成 ${ok.length}/${args.briefs.length} 张，其中验收闸通过 ${ok.filter(r => r.qaPassed).length} 张`)

return { images: ok, failedIds: failed.map(b => b.id) }
