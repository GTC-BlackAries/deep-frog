<div align="center">

<img src="assets/logo.png" width="160" alt="深蛙 Logo"/>

# 深蛙 Deep Frog

**凡是要下注的问题，先把证据收拾干净。**
*Clean up the evidence before you bet on an answer.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](skill/LICENSE)
[![Platform](https://img.shields.io/badge/Platform-WorkBuddy%20Skill-3E5A33)](skill/SKILL.md)

</div>

---

## 这是什么 · What it is

**中文**
深蛙（`deep-frog`）是一个 AI Agent 技能（skill）：把"要不要投入 / 要不要信 / 要不要买或签"这类**要下注的问题**，做成一份可信的调研档案。名字取自"深挖"的谐音——而且**蛙会叫**：查不到、有冲突、拿不准的时候，它必须出声。一只闷头挖、什么都不吭声的鼹鼠，恰恰是调研最怕的样子。

**English**
Deep Frog is an AI-agent skill that turns "bet-worthy questions" — should I enter this market, should I trust this claim, should I sign this vendor — into a trustworthy research dossier. The name is a pun on "deep dive" in Chinese; the frog also *croaks*: when something can't be found, conflicts, or is uncertain, it says so out loud. A mole that digs in silence is exactly what research should not be.

---

## ⏱️ 跑之前要知道的成本 · Read this before running

**一个话题的挖掘深度和交叉核验会做得比较深，一次完整调研约需 30–60 分钟，token 消耗较大。** 实测参考：本仓库 `examples/` 里的「社区电子产品回收」案例，在 WorkBuddy Hy4 模型上跑了约 **40 分钟**，产出 13 章自包含 HTML 报告 + 独立 critic 挑刺记录 + 40 条人工复核的审计警告。

它不适合"快速问一嘴"，适合**真的要用结论做决定**的时刻：投不投一个赛道、信不信一个流传的数字、签不签一家供应商。轻量场景请直接问你的 AI，不必动用深蛙。

> **Cost up front:** a full run goes deep on one topic — cross-verification included — and typically takes **30–60 minutes with substantial token usage**. The example dossier in `examples/` took ~40 min on WorkBuddy's Hy4 model. Use it when the answer is worth a decision, not for quick lookups.

---

## 四条不可协商的纪律 · Four non-negotiable rules

| | 中文 | English |
|---|---|---|
| 1 | **口径先于数字**：任何数字必须带口径（统计方法/年份/样本量/零售还是出厂）。没口径的数字不许写进正文 | **Caliber before figure**: every number carries its statistical caliber (method, year, sample, retail vs. ex-factory). No caliber, no body text |
| 2 | **冲突不调和**：来源打架就并列摆出，不挑顺眼的、不取平均、不写"约"。打架本身就是信息 | **Never reconcile conflicts**: clashing sources are shown side by side with calibers. The clash itself is information |
| 3 | **查不到就写查不到**：列入"未解缺口"，绝不用估算填。缺一个数字，比错一个数字安全 | **Say "not found"**: gaps are listed explicitly, never filled with estimates. A missing number is safer than a wrong one |
| 4 | **冲突必须先问人**：结论与用户已知事实打架时停下来问，绝不静默改掉用户的基准；核验器自身故障记 unverifiable，不记"已证伪" | **Conflicts go to the human first**: never silently overwrite the user's baseline; a crashed verifier yields *unverifiable*, not *refuted* |

## 交付物 · Deliverable

一份**自包含单文件 HTML 调研档案**（离线可开、可转 PDF）：证据 A/B/C 分级、口径冲突表、误引追查结果、未解缺口清单、独立 critic 原文（未经删改）、以及对你已有资产的可执行反哺建议。附带两个纯标准库 Python 自检脚本（`audit_report.py` 数字与引用静态审计 / `render_check.py` 双视口渲染核验）。

---

## 真实案例 · A real dossier

[`examples/community-electronics-recycling/`](examples/community-electronics-recycling/) —— 「社区电子产品二手回收值不值得进」：

- 结论：旧手机回收不是独立生意，是别人闭环里的一环；流传的"7,000 亿"是流转 GMV 不是社区盘子；"2% 正规回收率"多源旧数据口径互打架；**单位经济数据（单点月单量/单台毛利/合规成本）全部查不到，报告拒绝用估算填**
- 对抗核验：独立 critic 9 条判定 **5 条 REFUTED**，原文未经删改全部收录
- 审计：0 ERROR / 40 WARN（启发式误报逐条人工复核并如实说明）
- 这就是纪律 3 长出来的样子——**它敢把"不知道"印在交付物上**

## 怎么用 · How to use

**WorkBuddy 用户**：技能市场搜「**深蛙**」安装，然后直接说——

```
帮我深挖一下这个赛道，值不值得进
这个市场规模 80 亿的说法靠谱吗，帮我核一下出处和口径
帮我盘一下我们公司该不该接这个供应商
```

**其他 Agent 环境**：把 `skill/` 目录放进你的 skills 路径（SKILL.md 为通用格式，兼容 Claude Code / Codex / Cursor 等支持 skill 的环境），触发方式同上。

## 来源与原创性 · Provenance

本 skill 独立编写，未复制任何现有 skill 的文字、结构模板或代码。它的纪律从一次真实调研事故里倒推而来；公共范式内我们只主张一处原创（数字带统计口径），其余如实标注为跟随或取舍——详见 **[REFERENCES.md](REFERENCES.md)**（这份文件本身，就是纪律 2、3 对 README 的用法）。

## 许可 · License

- 主体：[MIT](skill/LICENSE)（Copyright © 2026 GTC黑羊 · ToolRadar.cc）
- `skill/fonts/` 字体不在 MIT 内：SIL Open Font License 1.1（见 `skill/fonts/FONT-LICENSE.md`）

---

<div align="center">

**蛙会叫。** · *The frog croaks.*

</div>
