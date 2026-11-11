#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调研报告的「数字与引用」自检。

为什么需要这个脚本：
一份调研报告最贵的错误不是写错观点，而是**把一个口径不对的数字、
一个不存在的文献、或一个被误引的结论**当成事实写进交付物。
观点错了读者会质疑，数字错了读者会照着做决策。

本脚本做三件事（纯静态检查，不需要联网）：
  1. 数字体检——抽出所有数字，检查是否带口径标注、是否成对出现冲突值；
  2. 引用体检——检查文献引用是否有 DOI/PMID/年份，是否出现"存疑"标记；
  3. 交付前红线——检查免责声明、证据分级标记、未解缺口章节是否齐备。

用法：
    python audit_report.py <报告.html> [--json]

退出码：0 = 无 ERROR；1 = 有 ERROR（警告不阻断）。
"""

import os
import re
import sys
import json

ERROR = "ERROR"
WARN = "WARN"
INFO = "INFO"

# 这些标记意味着作者已经主动声明了不确定性，属于良好实践，不该报警。
HONEST_MARKERS = [
    "未查到", "不可用", "存疑", "证据不足", "未覆盖", "口径", "估算",
    "互相冲突", "不可调和", "无公开数据", "待观察", "本文不构成",
]

# 缺少这些就是硬伤。
REQUIRED_SECTIONS = [
    (r"口径", "口径说明章节"),
    (r"未解|缺口|未查到|待补", "未解缺口章节"),
    (r"免责|不构成.*建议|不构成.*诊断", "免责声明"),
    (r"证据|等级|已确证|已证实", "证据分级标记"),
]

# 常见的"伪精确"信号：一个数字带了过分的有效位数。
FAKE_PRECISION = re.compile(r"\d+\.\d{4,}")


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def strip_tags(html):
    html = re.sub(r"<script\b.*?</script>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<style\b.*?</style>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    html = (
        html.replace("&nbsp;", " ")
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
    )
    return re.sub(r"\s+", " ", html)


def check_numbers(text, issues):
    """找出裸数字：前面没有口径限定词的百分比/金额。"""
    # 常见口径限定词（出现在数字前 40 字内即视为已标注）
    qualifiers = [
        "口径", "占", "约", "达", "为", "是", "高达", "突破", "规模", "市场",
        "自报", "确诊", "激发", "队列", "随机", "证据", "研究中", "来自", "报告",
        "年复合", "CAGR", "同比", "环比", "占比", "增长", "下降", "上升", "第",
        "中国", "全国", "城市", "农村", "门诊", "住院", "合计", "总计", "余",
        "亿元", "百万", "万", "亿", "率", "人数", "家", "人", "项", "条", "款",
        "排行", "排序", "名单", "序列", "≥", "≤", "<", ">", "＝", "=",
    ]
    # 百分数与金额
    pattern = re.compile(r"(\d[\d,\.]*\s*(?:%|亿|万|元|人|户|个|项|条|款|倍))")
    naked = []
    for m in pattern.finditer(text):
        start = max(0, m.start() - 40)
        ctx = text[start : m.start()]
        if any(q in ctx for q in qualifiers):
            continue
        # 前文有"约/近/超/不足/逾"也算
        if re.search(r"[约近超不足逾]\s*$", ctx):
            continue
        # 枚举/串联语境：前文若以顿号/逗号连续列出同类项，视为同组已标注
        if re.search(r"[、，,]\s*[^、，,]{0,12}$", ctx):
            continue
        naked.append((m.group(1), ctx[-38:].strip()))

    for val, ctx in naked[:40]:
        issues.append(
            {
                "level": WARN,
                "type": "裸数字",
                "detail": "%s 附近缺少口径限定词 → 「…%s」" % (val, ctx),
            }
        )


def check_fake_precision(text, issues):
    """伪精确检测。

    排除 DOI（10.xxxx/...）与 PMID——它们天然多位小数，不是伪精确。
    真正的伪精确是"占比/率/规模"这类值带了 4 位以上小数。
    """
    # 先把 DOI 和 PMID 挖掉，避免误报
    scrubbed = re.sub(r"10\.\d{4,9}/[^\s，。）)]+", "DOI", text)
    scrubbed = re.sub(r"\bPMID[:：]?\s*\d{6,9}\b", "PMID", scrubbed)
    scrubbed = re.sub(r"https?://\S+", "URL", scrubbed)

    # 只在"率/占比/比例"语境下判伪精确
    context_pat = re.compile(
        r"(占比|比例|率|份额|渗透率|致死率|患病率|增长率|CAGR)\s*[:：]?\s*"
        r"(\d+\.\d{4,})"
    )
    for m in context_pat.finditer(scrubbed):
        issues.append(
            {
                "level": WARN,
                "type": "伪精确",
                "detail": "%s = %s 有效位数过多，检查是否把估算写成了实测"
                % (m.group(1), m.group(2)),
            }
        )



def check_citations(text, issues):
    """检查引用完整性：出现文献/研究名，但没有可追溯标识。

    只对"具体可考"的来源名报错——指南、共识、白皮书这类词在正文里
    常作泛指（如"符合指南精神"），只有紧邻具体名称时才值得追溯。
    """
    # 具体来源名（可考）
    specific = re.compile(
        r"(NEJM|Lancet|JAMA|Cochrane|BMJ|JACI|PMID|DOI|中华流行病学杂志|"
        r"中华儿科杂志|中华实用儿科临床杂志|中华预防医学杂志|白皮书)"
    )
    # 泛指词（不报错，除非带书名号/括号补全）
    generic = re.compile(r"(指南|共识|meta\s*分析|系统综述|研究|试验)")

    trace_pat = re.compile(
        r"(DOI|PMID|doi:|10\.\d{4,9}/\S+|PMC|https?://|\b(19|20)\d{2}\b)"
    )

    for m in specific.finditer(text):
        s = max(0, m.start() - 120)
        e = min(len(text), m.end() + 120)
        ctx = text[s:e]
        if not trace_pat.search(ctx):
            issues.append(
                {
                    "level": WARN,
                    "type": "引用不可追溯",
                    "detail": "提到「%s」但邻近无 DOI/PMID/年份/链接 → 「…%s…」"
                    % (m.group(1), ctx[:70].strip()),
                }
            )

    # 泛指词：只有在形如「XXX指南（2022）」这样带年份补全时才提示
    for m in generic.finditer(text):
        tail = text[m.end() : m.end() + 30]
        if re.match(r"\s*[（(]\s*(19|20)\d{2}\s*[)）]", tail):
            s = max(0, m.start() - 100)
            ctx = text[s : m.end() + 40]
            if not trace_pat.search(ctx):
                issues.append(
                    {
                        "level": WARN,
                        "type": "引用不可追溯",
                        "detail": "带年份的「%s」邻近无来源标识 → 「…%s…」"
                        % (m.group(1), ctx[:70].strip()),
                    }
                )



def check_claims_vs_evidence(text, issues):
    """抓'结论型数字'：这类数字如果证据等级缺失，风险最高。

    豁免：作者已主动标注存疑（如"存疑""未查到原始研究来源"），
    或者该宣称本身就带限定语（"宣称""声称""说法"）——那是在转述
    他人的主张，不是在背书。
    """
    strong = re.compile(r"(降低|减少|提升|下降|上升|改善|有效|预防|治愈|获益|风险)[^。；]{0,12}?(\d[\d\.]*\s*%)")
    ev = re.compile(r"(已确证|已证实|证据等级|A 级|A级|随机|对照试验|RCT|指南|共识|meta)")
    hedge = re.compile(r"(存疑|未查到|未找到|宣称|声称|说法|声称过|可能|据称|宣称不|疑似)")
    for m in strong.finditer(text):
        s = max(0, m.start() - 160)
        e = min(len(text), m.end() + 160)
        ctx = text[s:e]
        if ev.search(ctx) or hedge.search(ctx):
            continue
        issues.append(
            {
                "level": ERROR,
                "type": "结论型数字缺证据",
                "detail": "「%s」附近无证据等级/研究类型标注" % m.group(0).strip()[:40],
            }
        )


def check_effect_sizes(text, issues):
    """效应量必须紧邻研究名。

    RR / OR / HR / CI / P 值这类数字只有挂在具体研究上才有意义。
    裸奔的 "RR 0.49" 没有可追溯性——读者无法知道出自哪篇。
    """
    eff = re.compile(
        r"\b(RR|OR|HR|AUC|CI|NNT)\s*=?=?\*?\s*(\d\.\d+|\d+\.\d+%)"
    )
    # 研究标识：期刊名 + 年份，或 ITT/PP/n= 等设计词
    study = re.compile(
        r"(ITT|PP|队列|RCT|随机|对照|试验|meta|PMID|DOI|10\.\d{4,}/\S+)"
    )
    for m in eff.finditer(text):
        s = max(0, m.start() - 150)
        e = min(len(text), m.end() + 150)
        ctx = text[s:e]
        if not study.search(ctx):
            issues.append(
                {
                    "level": WARN,
                    "type": "效应量无出处",
                    "detail": "「%s」附近无研究标识（队列/RCT/PMID/DOI）" % m.group(0).strip(),
                }
            )




def check_required(text, issues):
    for pat, label in REQUIRED_SECTIONS:
        if not re.search(pat, text):
            issues.append(
                {
                    "level": ERROR,
                    "type": "必备内容缺失",
                    "detail": "未找到%s（正则 %s）" % (label, pat),
                }
            )


def check_offline(text, issues):
    """离线可用性：除 allowlist 外不得有外部**资源**引用。

    只检查真正会发起网络请求的属性（script src / link href / img src），
    不检查 <a href>——那是参考文献的超链接，不影响离线阅读。
    """
    allowed = ("cdnjs.cloudflare.com", "esm.sh", "cdn.jsdelivr.net", "unpkg.com")
    resource_pat = re.compile(
        r'<(?:script|img|iframe|source|video|audio)\b[^>]*\bsrc\s*=\s*["\'](https?://[^"\']+)["\']',
        re.I,
    )
    link_pat = re.compile(
        r'<link\b[^>]*\bhref\s*=\s*["\'](https?://[^"\']+)["\']', re.I
    )
    for pat in (resource_pat, link_pat):
        for m in pat.finditer(text):
            url = m.group(1)
            if not any(a in url for a in allowed):
                issues.append(
                    {
                        "level": ERROR,
                        "type": "外部依赖",
                        "detail": "引用了外部资源，离线不可用 → %s" % url,
                    }
                )



def check_internal_links(text, issues):
    """内部锚点链接：href="#x" 必须有对应 id="x"。"""
    ids = set(re.findall(r'id="([^"]+)"', text))
    for m in re.finditer(r'href="#([^"]+)"', text):
        if m.group(1) not in ids:
            issues.append(
                {
                    "level": WARN,
                    "type": "死链",
                    "detail": "锚点 #%s 无对应元素" % m.group(1),
                }
            )


def check_mobile_css(text, issues):
    """窄屏与打印：两个最容易漏的媒体查询。"""
    if not re.search(r"@media[^{]*max-width", text):
        issues.append(
            {
                "level": ERROR,
                "type": "缺窄屏适配",
                "detail": "未找到 max-width 媒体查询",
            }
        )
    if not re.search(r"@media[^{]*print", text):
        issues.append(
            {
                "level": WARN,
                "type": "缺打印样式",
                "detail": "未找到 @media print",
            }
        )
    # flex 容器转竖排的常见漏项
    for m in re.finditer(r"@media[^{]*max-width[^{]*\{(.*?)\n\}", text, re.S):
        block = m.group(1)
        if re.search(r"flex-direction", block) is None and re.search(r"display:\s*flex", text[:2000]):
            issues.append(
                {
                    "level": INFO,
                    "type": "窄屏检查",
                    "detail": "窄屏块内未见 flex-direction:column，确认侧栏转顶部是否生效",
                }
            )
            break


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    path = os.path.abspath(sys.argv[1])
    if not os.path.isfile(path):
        print("[FAIL] 找不到文件: %s" % path)
        return 1

    html = read_text(path)
    text = strip_tags(html)

    issues = []
    check_numbers(text, issues)
    check_fake_precision(text, issues)
    check_citations(text, issues)
    check_claims_vs_evidence(text, issues)
    check_effect_sizes(text, issues)
    check_required(text, issues)
    check_offline(html, issues)
    check_internal_links(html, issues)
    check_mobile_css(html, issues)

    errors = [i for i in issues if i["level"] == ERROR]
    warns = [i for i in issues if i["level"] == WARN]
    infos = [i for i in issues if i["level"] == INFO]

    if "--json" in sys.argv:
        print(json.dumps({"errors": errors, "warnings": warns, "info": infos}, ensure_ascii=False, indent=2))
    else:
        for lvl, items in ((ERROR, errors), (WARN, warns), (INFO, infos)):
            if not items:
                continue
            print("\n=== %s (%d) ===" % (lvl, len(items)))
            seen = set()
            for it in items:
                key = (it["type"], it["detail"][:60])
                if key in seen:
                    continue
                seen.add(key)
                print("[%s] %s: %s" % (lvl, it["type"], it["detail"]))

    print("\n汇总: %d ERROR, %d WARN, %d INFO" % (len(errors), len(warns), len(infos)))
    if errors:
        print("[FAIL] 存在 ERROR，交付前必须处理。")
        return 1
    print("[PASS] 无 ERROR。警告项需人工确认——多数是提醒补口径，不是错误。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
