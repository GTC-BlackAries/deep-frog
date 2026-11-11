# 报告结构与视觉规范

> 本文同时规定报告的信息结构、Deep Frog 默认品牌视觉和交付检查。
> **默认皮肤为 Deep Frog Brand System（深色品牌入口 + 浅色阅读正文）**，不再使用旧版“纸面 + 墨 / 豆沙粉”皮肤。

## 一、视觉规范优先级

1. **用户明确提供的项目视觉规范优先。** 如果用户已有自己的 Logo、品牌色、排版规范或报告模板，沿用用户的规范，不要强行套用 Deep Frog 皮肤。
2. **没有用户专属规范时，使用 Deep Frog Brand System。** 以 `assets/deep-frog-logo.png` 为唯一官方品牌标识，按本文定义的色彩、组件和布局生成报告。
3. **不得自行创造第二套蛙 Logo。** 不要用 AI 重绘、替换、裁切、变形或改变官方 Logo 的主体颜色。缺少品牌资产时，不要假装已经放入 Logo；使用文字品牌名并在交付说明中披露。

品牌视觉分三层：

- **Brand / 品牌层**：深渊黑、薄荷绿、冷白。用于侧栏、报告 Hero、品牌入口和少量重点强调。
- **Reading / 阅读层**：冷雾白、纯白、墨绿黑。用于长篇正文、表格、说明和图表底板，保证长时间阅读舒适。
- **Data / 数据层**：薄荷绿、蓝、琥珀、红、灰。用于数据强调、证据等级、结论状态和风险语义，不作装饰性彩虹配色。

**不要把整份报告做成黑底荧光绿。** 深色只承担品牌识别；正文以浅色阅读为主。也不要将旧版暖奶油底、豆沙粉主色混入默认皮肤。

## 二、报告章节骨架

按研究任务裁剪和调整顺序，但完整决策型调研的核心章节不得缺失：

| # | 章节 | 必含内容 | 典型篇幅 |
|---|---|---|---|
| 0 | 一句话结论 | 核心判断 + 最反直觉的发现 + 当前判断边界 | 1–3 段 |
| 1 | 研究范围与定义 | 研究对象、边界、术语澄清、默认假设 | 中 |
| 2 | 需求侧 / 市场 | 规模、驱动、结构性变化、数字口径 | 大 |
| 3 | 供给侧 / 竞争 | 玩家矩阵、竞争格局、口径冲突表 | 大 |
| 4 | 证据与争议 | 证据分级、正反并列、被省略的另一半 | 大 |
| 5 | 政策与合规 | 能做什么 / 绝对不能碰 / 灰区 | 中 |
| 6 | 工具与产品形态 | 产品形态、收费、交付、变现 | 中 |
| 7 | 机会判断 | 每条包含参与者、未被满足原因、成立条件 | 大 |
| 8 | 风险与未解缺口 | 风险表 + 查不到的部分 + 后续核验建议 | 中 |
| 9 | **对存量资产的反哺** | 逐条对照用户已有文件的具体位置 | 中 |
| 10 | 参考文献 | 分组、按用途、可追溯出处 | 中 |

### 反哺清单的三段式

这是本 Skill 的差异化产出，**必须逐条对照到用户已有文件的具体位置**：

| 段 | 内容 | 示例 |
|---|---|---|
| 发现 | 客观事实 + 出处 | 某品类的国内风险排序与国际分类不同 |
| 意味着什么 | 对用户现有资产的影响 | 现有清单适合做标签，不适合直接充当本地优先级 |
| 建议动作 | 具体可执行 | 保留原分类，增加本地风险排序字段 |

**不要擅自改用户的文件**——医疗/法律/金融类内容改动需用户拍板。

## 三、品牌视觉 Token

以下颜色是 Deep Frog 默认皮肤的规范值。生成报告时优先通过 CSS variables 统一管理，不要在不同章节随意发明近似色。

```css
:root {
  /* Brand: 深色品牌区 */
  --deep: #050b0a;          /* 主深色 */
  --deep-2: #0a1512;        /* 次深色 */
  --deep-3: #10221c;        /* 深色层次 / 悬浮面 */
  --mint: #5be3b4;          /* 品牌薄荷绿 */
  --mint-strong: #20bd8b;   /* 薄荷绿强调 / 交互 */
  --mint-soft: #e3f6ee;     /* 浅绿提示底 */

  /* Reading: 浅色阅读区 */
  --paper: #f2f6f3;         /* 页面底色：冷雾白 */
  --surface: #ffffff;       /* 卡片 / 表格底 */
  --surface-2: #f7faf8;     /* 次级面 / 表头 */
  --ink: #18251f;           /* 正文主文字 */
  --ink-2: #53645b;         /* 次级文字 */
  --ink-3: #819087;         /* 辅助文字 */
  --line: #dfe8e2;          /* 浅色分隔线 */
  --line-dark: rgba(204,238,223,.12);

  /* Data: 语义辅助色 */
  --blue: #4f6d88;
  --blue-soft: #e9f0f6;
  --amber: #9a682a;
  --amber-soft: #fff3df;
  --red: #a64e49;
  --red-soft: #fbecea;

  /* Shape / depth */
  --shadow: 0 8px 28px rgba(23,49,36,.055);
  --radius: 16px;
  --radius-lg: 22px;
}
```

### 用色纪律

- 薄荷绿是**品牌强调色**，不是所有正确结论的默认背景色。用于关键词、关键指标、选中状态、细线和少量图标。
- 蓝色用于来源、方法、信息类辅助标记；琥珀色用于存疑、待确认、限制条件；红色仅用于证伪、重大风险和明确负面结论；灰色用于中性或较弱证据。
- **结论状态和证据等级必须分开理解**：
  - 结论状态：`CONFIRMED` 用绿色；`REFUTED` 用红色；`UNVERIFIABLE` 用琥珀色。
  - 证据等级：A 用绿色系，B 用蓝色系，C 用中性灰。证据等级不能代替结论状态，也不能暗示 A 级来源中的每个结论都已确证。
- 大面积页面不使用高饱和荧光绿；正文对比度至少 4.5:1。
- 不使用玫瑰粉、杏色作为默认品牌主色；除非用户明确要求沿用其自有皮肤。

## 四、布局与组件

### 桌面布局

```text
.layout { display:flex; min-height:100vh; }
├─ aside.sidebar
│   width:264px; flex:0 0 264px; position:sticky; top:0; height:100vh
│   深色渐变背景；顶部官方 Logo；品牌说明；目录；底部品牌签名
└─ main.content
    min-width:0; flex:1; max-width:1600px; margin:0 auto
    冷雾白页面底色；顶部面包屑 / 状态；深色 Hero；浅色正文
```

推荐基础样式：

```css
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font: 15px/1.78 var(--body);
  -webkit-font-smoothing: antialiased;
}
.layout { display: flex; min-height: 100vh; }
.sidebar {
  width: 264px; flex: 0 0 264px;
  position: sticky; top: 0; height: 100vh; overflow: auto;
  color: #eaf5ef;
  background: linear-gradient(180deg,var(--deep),#07100e 72%,#091713);
  border-right: 1px solid rgba(91,227,180,.12);
  padding: 24px 17px 20px;
  display: flex; flex-direction: column;
}
.content {
  min-width: 0; flex: 1;
  max-width: 1600px; margin: 0 auto;
  padding: 26px clamp(20px,4vw,58px) 72px;
}
.hero {
  position: relative; overflow: hidden; isolation: isolate;
  color: #f1f8f4; border-radius: var(--radius-lg);
  background:
    radial-gradient(ellipse at 83% 18%,rgba(45,183,137,.19),transparent 36%),
    linear-gradient(128deg,#07100e 0%,#0b1a15 55%,#10271f 100%);
  padding: 34px 38px 30px;
  box-shadow: 0 16px 42px rgba(7,22,15,.16);
}
.card {
  min-width: 0; background: var(--surface);
  border: 1px solid var(--line); border-radius: var(--radius);
  padding: 19px 20px; box-shadow: var(--shadow);
}
```

### 视觉层级

- **侧栏**：官方 Logo → `Evidence-first Research` 品牌副标 → 报告目录 → 品牌签名。侧栏目录保持清晰，不堆放无关装饰。
- **顶部状态栏**：显示报告路径 / 标题、生成日期、离线阅读提示（仅在确实无外部资源时使用）。
- **Hero 封面**：使用深色渐变、柔和的薄荷绿光晕或低对比度环形元素呼应 Logo。标题优先展示报告主题和核心结论，不重复堆叠 Logo。
- **正文**：以白色卡片、清晰的标题层级、克制的边框和留白组织内容。章节之间有明确节奏，不要每段都做成卡片。
- **指标卡**：数字可用墨绿或薄荷绿强调，单位、年份、地域、样本和统计口径紧邻呈现。
- **章节锚点**：每个主要章节使用带稳定 `id` 的 `<h2 id="section-id">`；侧栏目录 `href="#section-id"` 必须一一对应。该结构供 `audit_report.py` 检查内部链接，也供 `render_check.py` 分章截图。
- **表格**：表头使用 `--surface-2`，边线轻量；宽表格放入 `overflow-x:auto` 容器，正文表格建议 `min-width:620px`。
- **图表**：优先用薄荷绿作为主系列，蓝色和中性灰作为辅助。多个系列必须有图例和明确口径，不能仅凭颜色传达含义。
- **卡片**：允许少量深色卡片用于一句话结论、关键洞察或反例，但主体内容保持浅色。

### 推荐组件语义

| 组件 | 样式方向 | 用途 |
|---|---|---|
| `.hero` | 深色渐变 + 低强度薄荷光晕 | 报告首屏 / 一句话结论 |
| `.card` | 白底、细边线、柔和阴影 | 普通内容容器 |
| `.card.dark` | 深墨绿底、浅色文字 | 少量强调洞察 |
| `.metric` | 大号 tabular 数字 | 市场规模、样本、价格等 |
| `.callout` | 浅薄荷绿底 + 左侧强调线 | 已证实的重要结论 / 方法说明 |
| `.callout.amber` | 浅琥珀底 | 口径限制、存疑和待确认事项 |
| `.pill-a / .pill-b / .pill-c` | 绿 / 蓝 / 灰 | 证据等级 |
| `.pill-unknown / .pill-refuted` | 琥珀 / 红 | 无法验证 / 已证伪 |

不要仅为了好看增加无意义的 glow、网格、粒子、动画或装饰线。品牌感主要来自 Logo、配色、深色品牌区和稳定的信息层级。

## 五、官方 Logo 与品牌资产

官方 Logo 位于：`assets/deep-frog-logo.png`（512 × 512 PNG）。

使用规则：

1. 将该 PNG 原样放在侧栏顶部，推荐桌面端显示尺寸约 132–148px，窄屏约 76–84px；保持 1:1 比例，使用 `object-fit:contain`。
2. Logo 自带近黑色背景和光效，因此只放在深色侧栏 / 深色品牌容器内。不要直接放在纯白正文中，也不要给它额外加白色底框。
3. 为保持报告单文件图像资源可用，生成 HTML 时将 PNG 转成 `data:image/png;base64,...` 内嵌到 `img src`；不要用相对路径引用 `assets/`，也不要使用远程图片地址。
4. `alt` 使用 `深蛙 Deep Frog 标志`。不要拉伸、裁切蛙眼与环形主体，不要重绘文字，不要更换为另一个 AI 生成的青蛙图。
5. Logo 文件缺失时不得自行仿制。可以用纯文字 `深蛙 · DEEP FROG` 临时替代，并在交付说明中注明。
6. Logo / 品牌标识是项目品牌资产，不因 Skill 主体采用 MIT License 就自动意味着 Logo 可被第三方作为自己的品牌使用；分发时应保留作者和品牌来源说明。

## 六、字体

```css
--display: "Quicksand","DengXian","PingFang SC","Microsoft YaHei",sans-serif;
--body: "Nunito","DengXian","PingFang SC","Microsoft YaHei","Helvetica Neue",sans-serif;
--mono: "SFMono-Regular",Consolas,"Liberation Mono",monospace;
```

- Quicksand 用于西文标题、编号和数字；Nunito 用于西文正文和辅助信息。
- 中文字体不嵌入，使用系统字体栈（等线 / 苹方 / 微软雅黑 / Noto Sans CJK SC）。
- 字体文件来自 `fonts/`，按 `fonts/fonts-baby.css` 声明本地 `@font-face`，不得调用 Google Fonts 或其他线上字体 CDN。
- 报告交付时必须连同 `fonts/` 目录一起分发，不能只交付 HTML；详见 `fonts/FONT-LICENSE.md`。

## 七、滚动条

```css
* { scrollbar-width: thin; scrollbar-color: rgba(32,189,139,.42) transparent; }
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
  background: rgba(32,189,139,.34); border-radius: 999px;
  border: 3px solid transparent; background-clip: content-box;
}
::-webkit-scrollbar-thumb:hover {
  background: rgba(32,189,139,.58); background-clip: content-box;
}
```

轨道透明、滑块磨圆。Firefox 必须同时写 `scrollbar-width` 与 `scrollbar-color`。

## 八、窄屏与打印

断点以实际内容为准，默认参考：

```css
@media (max-width:1050px) {
  .sidebar { width:228px; flex-basis:228px; }
  .content { padding:22px 24px 60px; }
  .grid-3 { grid-template-columns:repeat(2,minmax(0,1fr)); }
}
@media (max-width:760px) {
  .layout { display:block; }
  .sidebar {
    position:relative; width:100%; height:auto; max-height:none;
    padding:12px 14px 13px;
  }
  .logo-wrap { justify-content:flex-start; padding:0; margin:0; }
  .logo { width:82px; height:82px; }
  .nav { display:flex; flex-direction:row; overflow-x:auto; gap:5px; }
  .nav a { white-space:nowrap; }
  .side-bottom { display:none; }
  .content { padding:18px 14px 42px; }
  .grid-3,.grid-2 { grid-template-columns:1fr; }
  .sample-layout { grid-template-columns:1fr; }
  .section-head { align-items:flex-start; flex-direction:column; }
}
@media print {
  body { background:#fff; }
  .sidebar,.topbar .top-right { display:none !important; }
  .layout { display:block; }
  .content { padding:0; max-width:none; }
  .hero,.card { box-shadow:none; break-inside:avoid; }
  .hero { print-color-adjust:exact; -webkit-print-color-adjust:exact; }
  h2,h3,h4 { break-after:avoid; }
}
```

注意：

- 窄屏时侧栏应转为顶部品牌区与横向目录，不能被压成窄条。
- 表格外层 `overflow-x:auto`；正文表格设置合理的 `min-width`，不要撑破页面。
- 窄屏表格如转为块级卡片，每个 `td` 必须有 `data-l="列名"`，用 `td::before` 显示字段名；若表格本身可横向滚动，则不必强制转换。
- 打印时隐藏侧栏和纯交互导航，保留关键结论、表格、来源与必要的深色 Hero；避免卡片跨页断裂。
- `render_check.py` 的窄屏基准为 560px，不要用低于此宽度的无头截图判断布局是否溢出。

## 九、可访问性与离线要求

- 不外链资源：不使用线上 CSS、JS、字体、图片或 iframe。官方 Logo 使用 data URI；字体使用随包提供的本地文件；图表优先使用内联 SVG / CSS。
- 正文对比度至少 4.5:1，交互元素点击区域至少 44×44px，`:focus-visible` 必须有可见描边。
- 数字统一使用 `font-variant-numeric:tabular-nums`。
- 进场动效必须包在 `@media (prefers-reduced-motion:no-preference)` 内；默认无动效也完全可读。
- 颜色不能成为唯一的信息编码方式：状态徽章同时显示文字（已确证 / 已证伪 / 无法验证）。
- 聊天正文只留 3–5 行摘要 + 文件路径，长表格放 HTML。

## 十、报告尾部的品牌引导区（固定环节）

每份默认皮肤报告的**参考文献之后**，放一个固定收尾组件（`.dossier-footer`），引导读者回到项目本身。规则：

- 浅色区收尾（不做第二个深色块，避免与侧栏/Hero 抢层级）；小字号、居中、细上边线与正文分隔。
- **必须如实**：只有当报告确实由深蛙生成且使用默认皮肤时才放；用户指定自有品牌规范时，此区**整体省略**，不得套用。
- 文案固定如下（中英各一行 + 一行链接），不得扩写成广告，不得加二维码以外的引流物：

```html
<footer class="dossier-footer">
  <p>本报告由 <b>深蛙 · Deep Frog</b> 调研纪律生成 —
     口径先于数字 · 冲突不调和 · 查不到就写查不到</p>
  <p>觉得有用？给项目一个 Star 是最直接的支持：<br>
     <a href="https://github.com/GTC-BlackAries/deep-frog">github.com/GTC-BlackAries/deep-frog</a> ⭐</p>
</footer>
```

```css
.dossier-footer {
  margin-top: 56px; padding: 28px 20px 8px; text-align: center;
  border-top: 1px solid var(--line);
  color: var(--ink-2); font-size: 14px; line-height: 1.9;
}
.dossier-footer a { color: var(--mint-strong); font-weight: 700; text-decoration: none; }
.dossier-footer a:hover { text-decoration: underline; }
@media print { .dossier-footer { margin-top: 24px; } }
```

- 打印时保留（链接仍有传播价值），但去掉颜色依赖，纯文字即可。

## 十一、交付前检查

```bash
python scripts/audit_report.py {报告路径}     # ERROR 必须清零
python scripts/render_check.py {报告路径}     # 分章截图，桌面 + 窄屏
```

两个脚本都不需要联网，可直接运行。`audit_report.py` 负责数字、引用、必备章节、外部资源、内部链接和 CSS 的静态检查；`render_check.py` 负责分章节截图。脚本不负责判断品牌审美，也不证明研究事实正确。

最终人工检查还需确认：

- [ ] 首屏侧栏使用官方深蛙 Logo，未变形、未被裁切，图片已内嵌。
- [ ] 深色只用于侧栏和 Hero 等品牌区，正文仍是浅色阅读区。
- [ ] 薄荷绿使用克制，蓝 / 琥珀 / 红 / 灰各自保持语义，不混淆证据等级与结论状态。
- [ ] 桌面、560px 窄屏和打印预览均可读；没有水平溢出、空白区或文字重叠。
- [ ] 若用户明确指定了其他视觉规范，已遵循用户规范，而不是强行使用 Deep Frog 默认皮肤。
