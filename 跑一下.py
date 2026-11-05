# -*- coding: utf-8 -*-
"""
================================================================
  跑一下.py        判题器
================================================================

在练习场文件夹里执行：

    python 跑一下.py

它会把 01_W1_函数.py 和 02_W2_文件.py 里的题全部跑一遍，
告诉你哪题过了、哪题错在哪一行、还剩几题没做。

不用改这个文件。
================================================================
"""

import sys
import io
import contextlib
import importlib.util
import traceback
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "words.txt"

RESULT = []


def add(no, title, status, msg=""):
    RESULT.append((no, title, status, msg))


# ------------------------------------------------------------
# 加载学生的 .py 文件
# ------------------------------------------------------------
def load(fname, alias):
    path = BASE / fname
    spec = importlib.util.spec_from_file_location(alias, path)
    mod = importlib.util.module_from_spec(spec)
    # 包一层 stdout，防止学生文件里自己写的 print 干扰判题输出
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


def fmt(args):
    if len(args) == 1:
        return repr(args[0])
    return repr(args)


# ------------------------------------------------------------
# 通用判题：按用例逐个比
# ------------------------------------------------------------
def check_func(no, title, mod, func_name, cases, capture=False):
    fn = getattr(mod, func_name, None)
    if fn is None:
        add(no, title, "ERR", "文件里找不到 %s()，是不是函数名被改了？" % func_name)
        return

    for args, expect in cases:
        try:
            if capture:
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    fn(*args)
                got = [ln.strip() for ln in buf.getvalue().splitlines() if ln.strip()]
            else:
                got = fn(*args)
        except NotImplementedError:
            add(no, title, "TODO")
            return
        except Exception as e:
            hint = ""
            if isinstance(e, ZeroDivisionError):
                hint = "  >> 分母是 0。想想是不是有「列表为空 / 个数为 0」的情况没处理？"
            elif isinstance(e, NameError):
                hint = "  >> 有个名字没定义或拼错了，看报错里引号中那个词。"
            elif isinstance(e, TypeError):
                hint = "  >> 类型对不上，常见是数字和字符串直接相加，或者忘了转 int。"
            elif isinstance(e, IndexError):
                hint = "  >> 下标越界了，列表长度可能比你以为的短。"
            add(no, title, "ERR", "%s: %s%s" % (type(e).__name__, e, hint))
            return

        if got != expect:
            add(no, title, "FAIL",
                "输入 %s 时，期望 %r，你给的是 %r" % (fmt(args), expect, got))
            return

    add(no, title, "PASS")


# ------------------------------------------------------------
# 第 7 题：词频字典
# ------------------------------------------------------------
EXPECT_COUNT = {
    "the": 4, "fox": 3, "dog": 3,
    "quick": 2, "lazy": 2, "a": 2,
    "brown": 1, "jumps": 1, "over": 1, "barks": 1, "and": 1,
    "runs": 1, "away": 1, "is": 1, "better": 1, "than": 1,
}


def check_q7(mod):
    title = "第 7 题 · 统计词频"
    fn = getattr(mod, "read_and_count", None)
    if fn is None:
        add(7, title, "ERR", "找不到 read_and_count()")
        return
    try:
        got = fn(str(DATA))
    except NotImplementedError:
        add(7, title, "TODO")
        return
    except Exception as e:
        hint = ""
        if isinstance(e, FileNotFoundError):
            hint = "  >> 找不到文件。传给函数的 path 就用题目里那个 str(WORDS_TXT)，别改。"
        add(7, title, "ERR", "%s: %s%s" % (type(e).__name__, e, hint))
        return

    if not isinstance(got, dict):
        add(7, title, "FAIL", "要返回字典，你返回的是 %s" % type(got).__name__)
        return
    if got == EXPECT_COUNT:
        add(7, title, "PASS")
        return

    # 给出具体差异，别让人瞎猜
    if "the" in got and got["the"] != 4:
        add(7, title, "FAIL",
            "'the' 应该出现 4 次，你数成了 %r。检查是不是漏了转小写（The 和 the 要算一个词）"
            % got["the"])
        return
    bad_keys = [k for k in got if k != k.strip(".,!?;:")]
    if bad_keys:
        add(7, title, "FAIL",
            "字典里有带标点的词：%s。用 w.strip('.,!?;:') 去掉两头标点"
            % bad_keys[:5])
        return
    missing = [k for k in EXPECT_COUNT if k not in got]
    if missing:
        add(7, title, "FAIL", "少了这些词：%s" % missing[:8])
        return
    extra = [k for k in got if k not in EXPECT_COUNT]
    if extra:
        add(7, title, "FAIL", "多了这些不该有的键：%s" % extra[:8])
        return
    add(7, title, "FAIL", "词都对，但某个词的次数不对。你的结果：%r" % got)


# ------------------------------------------------------------
# 第 8 题：写文件
# ------------------------------------------------------------
def check_q8(mod):
    title = "第 8 题 · 把结果写成文件"
    fn = getattr(mod, "write_report", None)
    if fn is None:
        add(8, title, "ERR", "找不到 write_report()")
        return

    dst = DATA.parent / "_report_check.txt"
    if dst.exists():
        dst.unlink()

    try:
        fn(str(DATA), str(dst))
    except NotImplementedError:
        add(8, title, "TODO")
        return
    except Exception as e:
        add(8, title, "ERR", "%s: %s" % (type(e).__name__, e))
        return

    if not dst.exists():
        add(8, title, "FAIL",
            "没有生成文件。你 open 的时候用的是不是 dst 这个参数？")
        return

    lines = [ln.strip() for ln in dst.read_text(encoding="utf-8").splitlines() if ln.strip()]
    expect_head = ["the 4", "dog 3", "fox 3"]
    if lines[:3] != expect_head:
        add(8, title, "FAIL",
            "前三行应该是 %s，你写的是 %s" % (expect_head, lines[:3]))
        return
    if len(lines) != 16:
        add(8, title, "FAIL",
            "应该正好 16 行（16 个不同的词），你写了 %d 行" % len(lines))
        return

    add(8, title, "PASS")
    try:
        dst.unlink()
    except OSError:
        pass


# ------------------------------------------------------------
# 主流程
# ------------------------------------------------------------
def main():
    print("")
    print("=" * 56)
    print("  练习场 · 自动判题")
    print("=" * 56)
    print("")

    # ---- 01 W1 ----
    try:
        m1 = load("01_W1_函数.py", "w1_funcs")
    except Exception:
        print("  [!!] 01_W1_函数.py 加载失败，先把它修好：")
        for ln in traceback.format_exc().splitlines()[-4:]:
            print("       " + ln)
        print("")
        m1 = None

    if m1 is not None:
        check_func(1, "第 1 题 · 算平均", m1, "average", [
            (([80, 90, 100],), 90.0),
            (([1, 2],), 1.5),
            (([],), 0),
        ])
        check_func(2, "第 2 题 · 判奇偶", m1, "is_even", [
            ((4,), True),
            ((7,), False),
            ((0,), True),
        ])
        check_func(3, "第 3 题 · 摄氏转华氏", m1, "c_to_f", [
            ((0,), 32.0),
            ((100,), 212.0),
            ((-40,), -40.0),
        ])
        check_func(4, "第 4 题 · 逐个打印名字", m1, "print_names", [
            ((["张三", "李四", "王五"],), ["张三", "李四", "王五"]),
        ], capture=True)
        check_func(5, "第 5 题 · 分数转等级", m1, "grade", [
            ((95,), "A"),
            ((90,), "A"),
            ((85,), "B"),
            ((59,), "E"),
        ])
        check_func(6, "第 6 题 · 1 加到 100", m1, "sum_1_to_100", [
            ((), 5050),
        ])

    # ---- 02 W2 ----
    try:
        m2 = load("02_W2_文件.py", "w2_files")
    except Exception:
        print("  [!!] 02_W2_文件.py 加载失败，先把它修好：")
        for ln in traceback.format_exc().splitlines()[-4:]:
            print("       " + ln)
        print("")
        m2 = None

    if m2 is not None:
        check_q7(m2)
        check_q8(m2)

    # ---- 出结果 ----
    done = [r for r in RESULT if r[2] == "PASS"]
    todo = [r for r in RESULT if r[2] == "TODO"]
    fail = [r for r in RESULT if r[2] == "FAIL"]
    err = [r for r in RESULT if r[2] == "ERR"]

    print("  " + "-" * 52)
    for no, title, status, msg in RESULT:
        if status == "PASS":
            print("  [OK]  %s" % title)
        elif status == "TODO":
            print("  [  ]  %s  （还没做）" % title)
        elif status == "FAIL":
            print("  [XX]  %s" % title)
            print("        %s" % msg)
        else:
            print("  [!!]  %s" % title)
            print("        %s" % msg)
    print("  " + "-" * 52)

    total = len(RESULT)
    passed = len(done)
    filled = int(20 * passed / total) if total else 0
    bar = "#" * filled + "." * (20 - filled)
    print("")
    print("  进度 [%s] %d / %d" % (bar, passed, total))
    print("  过 %d 题 · 错 %d 题 · 未做 %d 题 · 报错 %d 题"
          % (passed, len(fail), len(todo), len(err)))
    print("")

    # ---- 下一步建议 ----
    if passed == total:
        print("  全过了。W1 结业，明天开始 W2 的文件读写。")
        print("  记得把这两个 .py 传到 GitHub，这是你的第一个代码仓库。")
    elif err:
        print("  先把 [!!] 的报错解决掉 —— 报错会挡住后面的判题。")
        print("  看不懂报错就只把「英文第一行 + traceback 最后一行」贴给 AI，")
        print("  问它「哪一行错了、为什么」，不要让它重写整段。")
    elif fail:
        print("  错的那几题，回头看题目下面的提示那几行，八成就在里面。")
        print("  还是不会就先做下一题，30 分钟铁律。")
    else:
        left = total - passed
        print("  还剩 %d 题没做。今天先做 2 题就够，别一次做完。" % left)
        print("  最省力的顺序：第 4 题（for+print）-> 第 2 题 -> 第 3 题。")
    print("")


if __name__ == "__main__":
    main()
