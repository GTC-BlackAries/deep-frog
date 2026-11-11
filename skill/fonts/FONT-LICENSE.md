# 字体授权说明（Font Licensing）

本目录下的全部字体文件均为**开源字体**，采用 **SIL Open Font License, Version 1.1 (OFL-1.1)** 授权。
OFL-1.1 允许：**免费商用、允许嵌入到网页/文档/软件、允许再分发**（含随产品一同分发）。
唯一限制：**不得单独售卖字体本身**、不得以字体名为由单独分发字体文件、修改后的字体不得使用保留字体名（Reserved Font Name）。

---

## 一、字体清单与授权

| 文件 | 字体 | 字重/样式 | 授权 | 版权声明 | 许可证全文 |
|---|---|---|---|---|---|
| `quicksand-latin.woff2`<br>`quicksand-latin-ext.woff2` | **Quicksand** | 300–700 可变 | OFL-1.1 | Copyright 2019 The Quicksand Project Authors, with Reserved Font Name "Quicksand" | `LICENSE-quicksand.txt` |
| `nunito-latin.woff2`<br>`nunito-latin-ext.woff2`<br>`nunito-latin-italic.woff2`<br>`nunito-latin-ext-italic.woff2` | **Nunito** | 200–1000 可变 + 斜体 | OFL-1.1 | Copyright 2014 The Nunito Project Authors | `LICENSE-nunito.txt` |

所有 `LICENSE-*.txt` 均包含该字体的**版权声明行 + SIL OFL 1.1 许可证全文**，满足 OFL「随字体分发时必须附带许可证副本」的要求。
`manifest.json` 记录了每个文件的 SHA-256 前 16 位，便于校验。

---

## 二、为什么本地打包，而不是用线上 CDN

线上字体 CDN 在国内不可靠或极慢，且会产生第三方请求。
因此最终方案：**字体文件随报告一起打包**（`fonts/` 目录），HTML 用相对路径引用。
好处：① 国内完全无障碍，离线秒开；② 字体随报告走，拷到手机/平板/别的电脑照样显示；③ 不加载外部字体 = 没有第三方请求 = 更安全，也更快（无 FOUT 字形跳动）。

---

## 三、中文字体为什么不用嵌入

中文字体体积大（完整字库 5–20 MB），且**可授权嵌入的中文字体版权条款更复杂**（多数商用需单独授权）。
因此中文字体一律走**系统字体栈**，不随报告分发：

- 标题中文：`DengXian`（等线，Windows 自带）→ `PingFang SC`（macOS）→ `Microsoft YaHei` → 通用 sans-serif
- 正文中文：同上

嵌入的西文字体（Quicksand / Nunito）负责**数字、日期、英文单位**——正是报告里最需要圆润感、也最常被读到的部分。

> 注：Windows 自带的「**幼圆**」字形很圆润、很适合母婴场景，但**字体文件存在（`C:\Windows\Fonts\SIMYOU.TTF`）而系统未注册该字体族**，CSS 写 `"幼圆"` 或 `"YouYuan"` 均不生效（已实测，全部回落黑体）。因此本项目改用**等线**——比苹方柔和，又不像儿童字体那么幼态。

---

## 四、使用规则

1. 生成的 HTML 必须**连同 `fonts/` 目录一起分发**，不要只发 HTML（否则字体会回落系统字体，版式观感变化）。
2. **不得**单独售卖本目录中的字体文件；**不得**移除 `LICENSE-*.txt`。
3. 若要换字体，只换 OFL-1.1 或其他允许商用+嵌入+再分发的字体，并同步更新本说明与许可证副本。
4. 字体文件来源：Google Fonts（`fonts.googleapis.com` / `fonts.gstatic.com`）与 `@fontsource` npm 包。
