# 新手学习指南

这个项目不要求你一次看懂全部代码。先运行，再按照下面顺序阅读和修改。

## 先理解四个概念

1. Streamlit：把 Python 代码快速变成网页。
2. Session State：保存当前题目、历史回答和面试进度。
3. Prompt：告诉大模型扮演谁、输入是什么、应该按什么格式输出。
4. JSON：让模型按照固定字段返回数据，程序才能稳定读取分数和建议。

## 按顺序阅读文件

### 1. `app.py`

先搜索 `st.title`，这是页面入口。然后重点看三个分支：

- `if not st.session_state.interview_started`：创建面试。
- `elif not st.session_state.interview_complete`：逐题回答。
- 最后的 `else`：显示总结和下载报告。

### 2. `interview_engine.py`

先看 `generate_demo_questions` 和 `evaluate_demo_answer`，它们不调用大模型，最容易理解。

再看 `build_question_prompt` 和 `build_feedback_prompt`，这里定义大模型的任务和 JSON 格式。

最后看 `_normalise_questions` 与 `_normalise_feedback`，它们负责检查模型返回值，避免页面因为缺少字段而报错。

### 3. `tests/test_interview_engine.py`

每一个 `test_` 函数都在检查一条规则。例如：题目数量是否正确、详细回答是否比过短回答得分高、报告是否包含岗位和回答。

## 第一次修改练习

按照难度从低到高，可以依次完成：

1. 在 `ROLE_QUESTION_BANK` 中增加“Java 开发实习生”题库。
2. 把默认题目数量从 5 改成 3。
3. 在总结页增加“最高分题目”。
4. 在 Markdown 报告中加入每道题的优点。
5. 增加一个新的评分维度，例如“技术准确性”。

每完成一个修改，都运行：

```powershell
python -m unittest discover -s tests -v
```

## 七天练习安排

- 第 1 天：运行项目，体验演示模式。
- 第 2 天：看懂页面的三个状态。
- 第 3 天：修改一个岗位题库。
- 第 4 天：配置 API Key，体验大模型模式。
- 第 5 天：阅读 Prompt 和 JSON 解析代码。
- 第 6 天：补截图、README 和在线部署。
- 第 7 天：练习用两分钟介绍项目，并上传 GitHub。

目标不是背下全部代码，而是能回答三个问题：项目解决什么问题、数据怎样在页面与模型之间流动、模型返回异常时程序怎样处理。
