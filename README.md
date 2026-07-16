# AI 面试模拟官

一个面向大学生和求职新人的模拟面试 Web 应用。用户可以选择目标岗位和面试类型，逐题提交回答，获得四维评分、改进建议、参考表达和可下载的 Markdown 练习报告。

项目提供两种运行方式：

- 演示模式：不需要 API Key，使用内置题库和透明的规则评分，适合第一次运行和功能展示。
- 大模型模式：调用 OpenAI 兼容接口，根据岗位和个人背景生成题目与反馈。

## 功能

- 支持 AI 应用开发、Python 后端、前端、数据分析、产品经理等岗位
- 支持自定义岗位、难度、面试类型和题目数量
- 根据个人背景生成个性化面试题
- 逐题回答并获得岗位相关性、表达清晰度、案例与证据、思考深度评分
- 提供优点、改进建议、参考表达和面试官追问
- 展示面试总分与逐题回顾
- 下载完整 Markdown 面试报告
- API Key 通过环境变量或 Streamlit Secrets 管理

## 技术栈

- Python 3.11
- Streamlit
- OpenAI-compatible API
- python-dotenv
- unittest

## 项目结构

```text
ai-interview-coach/
|-- app.py                       # Streamlit 页面和答题流程
|-- interview_engine.py          # 题目生成、评分和报告逻辑
|-- tests/
|   `-- test_interview_engine.py # 核心逻辑测试
|-- .streamlit/
|   `-- config.toml              # 页面主题和服务配置
|-- .env.example                 # 环境变量示例
|-- .gitignore                   # Git 忽略规则
|-- requirements.txt             # Python 依赖
|-- runtime.txt                  # 部署使用的 Python 版本
|-- GITHUB_UPLOAD_GUIDE.md       # GitHub 上传和部署步骤
|-- LEARNING_GUIDE.md            # 新手阅读与练习路线
`-- LICENSE
```

## 本地运行

建议使用 Python 3.10 至 3.12。

```powershell
cd E:\github\ai-interview-coach
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

浏览器通常会自动打开 `http://localhost:8501`。第一次运行直接选择“演示模式”即可，不需要注册模型账号。

## 使用大模型模式

复制环境变量模板：

```powershell
Copy-Item .env.example .env
```

编辑 `.env`：

```env
AI_API_KEY=你的_API_Key
AI_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-4.1-mini
```

项目使用 OpenAI 兼容接口，也可以在网页侧边栏选择 DeepSeek、通义千问或填写其他兼容接口。模型名称和接口可能随服务商更新，请以对应服务商文档为准。

不要上传 `.env`、`.streamlit/secrets.toml` 或任何真实 API Key。

## 运行测试

```powershell
python -m unittest discover -s tests -v
```

## 核心流程

```text
填写面试配置
    -> 生成面试题
    -> 提交单题回答
    -> 获得结构化反馈
    -> 继续下一题
    -> 汇总评分并下载报告
```

## 项目亮点

- 使用 Session State 实现多步骤面试流程和答题记录管理
- 将界面与业务逻辑拆分，便于测试和后续扩展
- 使用 JSON 约束大模型输出，并提供解析、校验和兜底逻辑
- 对简历背景和面试回答增加提示词注入防护说明
- 演示模式不依赖外部服务，方便招聘者直接体验
- 使用环境变量和 Git 忽略规则保护 API Key

## 简历描述参考

> 独立开发 AI 面试模拟官，基于 Streamlit 构建多步骤 Web 交互流程，接入 OpenAI-compatible 大模型 API，实现岗位定制出题、回答四维评分、改进建议生成与 Markdown 报告导出；通过 JSON 输出约束、异常兜底和环境变量管理提升应用稳定性与安全性，并使用 unittest 覆盖核心业务逻辑。

## 面试时可以怎么介绍

1. 项目解决大学生缺少低成本面试陪练的问题。
2. `app.py` 管理页面和会话状态，`interview_engine.py` 管理题目、评分和报告。
3. 大模型输出不一定稳定，因此项目要求 JSON，并对字段、分数和缺失数据做校验。
4. 没有 API Key 时仍可通过演示模式体验完整流程。
5. 下一步可以增加语音面试、历史记录和岗位题库管理。

## 说明

本项目用于学习和面试练习。自动评分不能代表企业真实评价，请勿输入身份证号、手机号、未公开公司资料等敏感信息。
