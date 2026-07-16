# GitHub 上传与部署指南

下面的步骤适合第一次上传项目。上传之前，先在演示模式下完整答完一轮面试。

## 第一步：检查项目

进入项目目录：

```powershell
cd E:\github\ai-interview-coach
```

运行测试：

```powershell
python -m unittest discover -s tests -v
```

检查 `.env` 没有被 Git 追踪：

```powershell
git status
```

`.env` 不应该出现在待上传文件列表中。

## 第二步：在 GitHub 创建仓库

1. 登录 GitHub。
2. 点击右上角 `+`，选择 `New repository`。
3. Repository name 填写 `ai-interview-coach`。
4. Description 可以填写：`A beginner-friendly AI mock interview coach built with Streamlit.`
5. 选择 `Public`。
6. 不勾选 `Add a README file`、`.gitignore` 或 License，因为本地已经准备好了。
7. 点击 `Create repository`。

## 第三步：使用命令上传

在项目目录依次运行：

```powershell
git init
git add .
git status
git commit -m "feat: build AI interview coach"
git branch -M main
git remote add origin https://github.com/你的用户名/ai-interview-coach.git
git push -u origin main
```

把命令里的“你的用户名”换成自己的 GitHub 用户名。

如果 `git commit` 提示没有配置身份，只需要在电脑上执行一次：

```powershell
git config --global user.name "你的 GitHub 用户名"
git config --global user.email "你的 GitHub 邮箱"
```

然后重新执行提交和推送命令。

## 第四步：补一张项目截图

1. 本地打开应用并完成一次面试。
2. 截取“本题反馈”或“模拟面试完成”页面。
3. 在仓库中新建 `docs` 文件夹，把图片命名为 `preview.png`。
4. 在 README 的项目介绍后添加：

```markdown
![项目截图](docs/preview.png)
```

截图中不要出现 API Key、手机号、真实简历或其他隐私信息。

## 第五步：部署到 Streamlit Community Cloud

1. 打开 `https://share.streamlit.io/`，使用 GitHub 登录。
2. 点击 `Create app`，选择仓库 `ai-interview-coach`。
3. Branch 选择 `main`。
4. Main file path 填写 `app.py`。
5. 点击部署。

演示模式不需要设置任何 Secret，部署后就能运行。

如果需要大模型模式，在应用设置的 Secrets 中填写：

```toml
AI_API_KEY = "你的 API Key"
AI_BASE_URL = "https://api.openai.com/v1"
AI_MODEL = "gpt-4.1-mini"
```

不要把上面的真实值写进 GitHub 文件。

## 第六步：完善仓库首页

部署成功后，把下面两行加到 README 标题下方，并替换链接：

```markdown
[在线体验](https://你的应用地址.streamlit.app/)

![项目截图](docs/preview.png)
```

最后在 GitHub 仓库右侧 About 区域填写：

- Description：`AI mock interview coach for students and junior job seekers`
- Website：你的 Streamlit 在线地址
- Topics：`python`、`streamlit`、`llm`、`ai-application`、`interview`

做到这里，项目就已经可以放进简历了。
