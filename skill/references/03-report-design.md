# 报告结构与视觉

## 一、优先级原则

> **如果用户的存量 skill 已规定视觉规范，一律沿用用户的，不要套用本文默认值。**
> 例如用户为某个母婴类 skill 选定了"只有一套皮肤"（母婴侧栏版）——
> 那是用户亲自选定的，套别的皮肤是倒退。

本文提供的是**没有既有规范时的默认解**。

## 二、章节骨架

按重要性调整，但**四项不得缺**：

| # | 章节 | 必含 | 典型篇幅 |
|---|---|---|---|
| 0 | 一句话结论 | 核心判断 + 最反直觉的发现 | 1–3 段 |
| 1 | 赛道坐标与定义 | 研究对象、边界、术语澄清 | 中 |
| 2 | 需求侧 | 规模、驱动、结构性变化 | 大 |
| 3 | 供给侧 | 玩家矩阵、竞争格局、口径冲突表 | 大 |
| 4 | 证据与争议 | 分级、正反并列、被省略的另一半 | 大 |
| 5 | 政策与合规 | 能做什么 / 绝对不能碰 / 灰区 | 中 |
| 6 | 工具与形态 | 产品形态、收费、变现 | 中 |
| 7 | 机会判断 | 每条三要素 | 大 |
| 8 | 风险与未解缺口 | 风险表 + 查不到的部分 | 中 |
| 9 | **对存量资产的反哺** | 逐条对照到具体位置 | 中 |
| 10 | 参考文献 | 分组、按用途 | 中 |

### 反哺清单的三段式

这是本 skill 的差异化产出，**必须逐条对照到用户已有文件的具体位置**：

| 段 | 内容 | 示例 |
|---|---|---|
| 发现 | 客观事实 + 出处 | 「花生在中国过敏原排序仅第 8（4%），芒果占 15% 且不在国际八大类内」 |
| 意味着什么 | 对用户现有资产的影响 | 「「致敏食物清单.md」用的是国际八大类口径。作为标签合规没问题，作为引入优先级就偏了」 |
| 建议动作 | 具体可执行 | 「保留八大类不动，另加一节『中国实际风险排序』；把芒果从『其他常见致敏食物』提级」 |

**不要擅自改用户的文件**——医疗/法律/金融类内容改动需用户拍板。

## 三、视觉 token（默认皮肤：纸面 + 墨）

浅色底一律低彩度。深色主题另配一套，**不要把浅色底的颜色加深了当深色用**。

```css
--paper:#fdf8f4;      /* 奶白底 */
--card:#fffdfc;       /* 卡片近白 */
--card-2:#fbf3ee;     /* 次级面 / 表头 */
--ink:#3b3330;        /* 暖墨棕，不用纯黑 */
--ink-2:#6e615c; --ink-3:#a4948e;
--line:rgba(150,110,100,.13); --line-2:rgba(150,110,100,.07);
--rose:#c4878f;       /* 主色（大色块/顶边/圆点） */
--rose-ink:#9a5f68;   /* 小字用，对比 ≥4.5:1 */
--rose-soft:#f8e8ea;
--peach:#e2a077; --peach-ink:#a05c33; --peach-soft:#fbe9dd;   /* 判定/提示 */
--sage:#6d8a72; --sage-ink:#4f6b55; --sage-soft:#e7efe7;      /* 通过/正面 */
--berry:#b3564f; --berry-soft:#f9e7e4;                          /* 红线专用 */
--indigo:#5b6b8c; --indigo-ink:#44516b; --indigo-soft:#e9ecf3; /* 信息/证据 */
--sh-1:0 1px 2px rgba(150,110,100,.04),0 4px 14px rgba(150,110,100,.05);
--r-s:10px; --r-m:16px; --r-l:22px;
```

**用色纪律**：
- **红色只给红线/负面结论**，不用于装饰
- 绿=已确证/通过、琥珀=判定/存疑、靛蓝=证据/信息、豆沙=中性强调
- 表格里的证据等级徽章：A 用 sage、B 用 peach、C 用中性灰、不可用用 berry

## 四、布局骨架

```
.wrap { display:flex; align-items:flex-start; }
├─ aside.side   268–288px，sticky top:0 height:100vh
│                顺序：标题 → 目录 → 关键锚点 → 折叠区（必读/纠错/前提）→ 免责
└─ main          flex:1 1 auto; min-width:0; padding:32px 38px 90px
                 **不锁页面宽度**，宽屏由内容填充
```

- **入口类信息放侧栏常驻**（目录、关键数字锚点）；**叙述类信息放宽栏正文**
- 板块按重要性分配面积，同排卡片**等高**
- 次要信息默认**收起**（`<details>` 折叠），不是删除
- 表格外层 `overflow-x:auto`，正文 `table{min-width:560px}`

### 窄屏（≤980px）

侧栏转顶部。**必须改多列，不能整条拉满**，否则左右两端会被甩到屏幕两边：

```css
@media (max-width:980px){
  .wrap{flex-direction:column}          /* ← 漏这行会导致侧栏被压成窄条 */
  .side{width:100%;flex:1 1 auto;min-width:0;height:auto;position:static;
        display:grid;grid-template-columns:repeat(auto-fit,minmax(min(232px,100%),1fr));
        gap:0 26px;align-items:start;padding:22px 18px 20px}
  .side .brand,.side .brand-sub,.side .toc,.side .side-foot{grid-column:1/-1}
}
```

坑：`flex:none` 会让 flex item 按 **max-content** 算宽度 → 侧栏撑出视口。
必须 `flex:1 1 auto;min-width:0`。

## 五、字体（不许用线上 CDN）

```css
--display:"Quicksand","DengXian","PingFang SC","Microsoft YaHei",sans-serif;
--body:"Nunito","DengXian","PingFang SC","Microsoft YaHei","Helvetica Neue",sans-serif;
```

- **Quicksand/Nunito 走本地打包**（skill 包根目录的 `fonts/`，SIL OFL 1.1 可商用可再分发）
- **中文字体不嵌入**，走系统栈（等线/苹方/雅黑）
- 理由：Google Fonts 国内常被墙，`fonts.loli.net` 超时，`font.im` 慢；
  本地打包后完全离线可用、无第三方请求、无 FOUT

## 六、滚动条（默认灰粗条必须改）

```css
*{scrollbar-width:thin;scrollbar-color:rgba(196,135,143,.42) transparent}
::-webkit-scrollbar{width:10px;height:10px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:rgba(196,135,143,.34);border-radius:999px;
  border:3px solid transparent;background-clip:content-box}
::-webkit-scrollbar-thumb:hover{background:rgba(196,135,143,.58);background-clip:content-box}
```

轨道透明、滑块磨圆、`background-clip:content-box` + 透明 border 让滑块更细。
Firefox 必须同时写 `scrollbar-width/color`（Chrome 不认）。

## 七、打印与窄屏

```css
@media print{
  body::before{display:none}
  .side{display:none}
  .card,.tw,.note,.opp{break-inside:avoid;box-shadow:none}
  h2,h3,h4{break-after:avoid}
}
@media (max-width:620px){
  thead{display:none}
  tbody tr{display:block;border-bottom:1px solid var(--line);padding:9px 0}
  tbody tr td{display:flex;justify-content:space-between;gap:14px;border:none;padding:3px 13px}
  tbody tr td::before{content:attr(data-l);font-weight:700;color:var(--ink-3);flex:none}
}
```

窄屏下表格转块级时，`td` 要加 `data-l="列名"` 才有标签。

## 八、其他硬性要求

- **不外链任何资源**（字体走本地，图片一律内联 SVG/CSS）→ 离线可读
- 数字一律 `font-variant-numeric: tabular-nums`
- 正文对比度 ≥ 4.5:1，交互元素 ≥ 44×44px，`:focus-visible` 可见描边
- 进场动效包在 `@media (prefers-reduced-motion:no-preference)` 内
- 聊天正文只留 3–5 行摘要 + 文件路径，**长表格放 HTML**
- `audit_report.py` 会检查：外部资源依赖、缺窄屏适配、缺打印样式、窄屏块内无 `flex-direction`

## 九、交付前

```bash
python scripts/audit_report.py {报告路径}     # ERROR 必须清零
python scripts/render_check.py {报告路径}     # 分章截图，桌面+窄屏
```

两个脚本都**不需要联网**，可直接跑。
