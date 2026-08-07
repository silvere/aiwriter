# 百年京张AI创新带 · 开源征集投稿包(待转投 open-city-ai/haidian)

本目录是为 [open-city-ai/haidian](https://github.com/open-city-ai/haidian) "百年京张AI创新带城市设计开源征集"
准备的完整 formal 投稿包,已在该仓库校验链路下通过全部自检:

```
Result: PASS · Package type: professional_design_package
Review status: formal-review-ready · Can enter formal review: YES
Deterministic / Spatial / Visual / Professional 四链路全部 PASS
```

## 如何提交 PR(本会话无法跨所有者 fork,需一步人工操作)

```bash
# 1. fork open-city-ai/haidian 到你的账号(网页点 Fork 或: gh repo fork open-city-ai/haidian --clone)
git clone https://github.com/silvere/haidian && cd haidian
git checkout -b submission/silvere-jingzhang-ai-belt-open-loop
# 2. 从本仓库本分支复制投稿目录(唯一允许修改的路径)
cp -r ../aiwriter/submissions/silvere/jingzhang-ai-belt-open-loop submissions/silvere/
# 3. 本地复验(可选)
python3 -m pip install -r requirements-review.txt
python3 scripts/self_check_submission.py submissions/silvere/jingzhang-ai-belt-open-loop --pr-author silvere
# 4. 提交并开 PR(PR 只包含 submissions/silvere/jingzhang-ai-belt-open-loop/,不要动 submissions-data.js)
git add submissions/silvere/jingzhang-ai-belt-open-loop
git commit -m "submission: 百年京张·开源智线——AI创新带开放共创城市设计方案 (silvere)"
git push -u origin submission/silvere-jingzhang-ai-belt-open-loop
```

或者:在 Claude Code 新建一个以 open-city-ai/haidian 为初始源的会话,让 agent 直接完成 fork/push/PR。
