import os
from typing import Any

import streamlit as st
from dotenv import load_dotenv

from interview_engine import (
    DIMENSION_LABELS,
    ROLE_QUESTION_BANK,
    average_score,
    build_markdown_report,
    dimension_averages,
    evaluate_ai_answer,
    evaluate_demo_answer,
    generate_ai_questions,
    generate_demo_questions,
)


load_dotenv()

st.set_page_config(
    page_title="AI 面试模拟官",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="expanded",
)


PROVIDER_PRESETS = {
    "OpenAI": {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4.1-mini",
    },
    "DeepSeek": {
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat",
    },
    "通义千问 / Qwen": {
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-plus",
    },
    "自定义 OpenAI 兼容接口": {
        "base_url": os.getenv("AI_BASE_URL", "https://api.openai.com/v1"),
        "model": os.getenv("AI_MODEL", "gpt-4.1-mini"),
    },
}


def read_setting(name: str, default: str = "") -> str:
    env_value = os.getenv(name)
    if env_value:
        return env_value
    try:
        return str(st.secrets.get(name, default))
    except Exception:
        return default


def initialise_state() -> None:
    defaults: dict[str, Any] = {
        "interview_started": False,
        "interview_complete": False,
        "questions": [],
        "current_index": 0,
        "current_feedback": None,
        "records": [],
        "interview_config": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_interview() -> None:
    for key in [
        "interview_started",
        "interview_complete",
        "questions",
        "current_index",
        "current_feedback",
        "records",
        "interview_config",
    ]:
        st.session_state.pop(key, None)
    initialise_state()


def apply_provider_preset() -> None:
    selected_provider = st.session_state.provider_select
    selected_preset = PROVIDER_PRESETS[selected_provider]
    st.session_state.base_url_input = selected_preset["base_url"]
    st.session_state.model_input = selected_preset["model"]


def show_feedback(feedback: dict[str, Any]) -> None:
    st.subheader("本题反馈")
    score_col, dimensions_col = st.columns([1, 3])
    with score_col:
        st.metric("本题得分", f"{feedback['score']} / 100")
    with dimensions_col:
        dimension_columns = st.columns(4)
        for column, (key, label) in zip(dimension_columns, DIMENSION_LABELS.items()):
            column.metric(label, feedback["dimensions"][key])

    strengths_col, improvements_col = st.columns(2)
    with strengths_col:
        st.markdown("#### 做得不错")
        for item in feedback["strengths"]:
            st.markdown(f"- {item}")
    with improvements_col:
        st.markdown("#### 下一步改进")
        for item in feedback["improvements"]:
            st.markdown(f"- {item}")

    with st.expander("查看参考表达", expanded=True):
        st.write(feedback["better_answer"])
    st.info(f"面试官追问：{feedback['follow_up']}")


initialise_state()

if "provider_select" not in st.session_state:
    st.session_state.provider_select = "OpenAI"
if "base_url_input" not in st.session_state:
    st.session_state.base_url_input = PROVIDER_PRESETS["OpenAI"]["base_url"]
if "model_input" not in st.session_state:
    st.session_state.model_input = PROVIDER_PRESETS["OpenAI"]["model"]
if "api_key_input" not in st.session_state:
    st.session_state.api_key_input = read_setting(
        "AI_API_KEY", read_setting("OPENAI_API_KEY")
    )

st.title("AI 面试模拟官")
st.caption("选择目标岗位，逐题练习并获得结构化反馈。")

with st.sidebar:
    st.header("运行模式")
    mode = st.radio(
        "选择模式",
        ["演示模式", "大模型模式"],
        help="演示模式免费且无需 API Key；大模型模式会生成个性化题目与评价。",
        disabled=st.session_state.interview_started,
    )

    provider = st.selectbox(
        "模型服务商",
        list(PROVIDER_PRESETS),
        key="provider_select",
        on_change=apply_provider_preset,
        disabled=mode == "演示模式" or st.session_state.interview_started,
    )
    api_key = st.text_input(
        "API Key",
        type="password",
        key="api_key_input",
        disabled=mode == "演示模式" or st.session_state.interview_started,
    )
    base_url = st.text_input(
        "Base URL",
        key="base_url_input",
        disabled=mode == "演示模式" or st.session_state.interview_started,
    )
    model = st.text_input(
        "模型名称",
        key="model_input",
        disabled=mode == "演示模式" or st.session_state.interview_started,
    )

    st.divider()
    if st.session_state.interview_started:
        running_mode = st.session_state.interview_config.get("mode", mode)
        st.caption(f"本轮面试：{running_mode}")
        if st.button("结束本轮面试", use_container_width=True):
            reset_interview()
            st.rerun()
    else:
        st.caption("建议第一次先用演示模式跑完整个流程。")


if not st.session_state.interview_started:
    st.subheader("创建模拟面试")
    with st.form("interview_setup"):
        first_col, second_col = st.columns(2)
        with first_col:
            role_option = st.selectbox(
                "目标岗位",
                list(ROLE_QUESTION_BANK) + ["自定义岗位"],
            )
            custom_role = st.text_input(
                "自定义岗位",
                placeholder="选择自定义岗位时填写，例如：Java 开发实习生",
            )
            level = st.select_slider(
                "面试难度",
                options=["基础", "进阶", "挑战"],
                value="基础",
            )
        with second_col:
            interview_type = st.selectbox(
                "面试类型",
                ["综合面试", "技术面试", "项目面试", "行为面试"],
            )
            question_count = st.slider("题目数量", min_value=3, max_value=8, value=5)
            background = st.text_area(
                "个人背景（可选）",
                placeholder="例如：会 Python、Streamlit，做过 AI 简历优化助手。请勿填写身份证号等敏感信息。",
                height=118,
            )

        start = st.form_submit_button(
            "开始模拟面试",
            type="primary",
            use_container_width=True,
        )

    if start:
        role = custom_role.strip() if role_option == "自定义岗位" else role_option
        if not role:
            st.error("请填写自定义岗位名称。")
        elif mode == "大模型模式" and not api_key.strip():
            st.error("大模型模式需要 API Key。也可以先切换到演示模式。")
        else:
            with st.spinner("正在准备面试题..."):
                try:
                    if mode == "大模型模式":
                        questions = generate_ai_questions(
                            api_key=api_key.strip(),
                            base_url=base_url.strip(),
                            model=model.strip(),
                            role=role,
                            level=level,
                            interview_type=interview_type,
                            count=question_count,
                            background=background.strip(),
                        )
                    else:
                        questions = generate_demo_questions(role, question_count)
                except Exception as exc:
                    st.error(f"生成题目失败：{exc}")
                    questions = []

            if questions:
                st.session_state.questions = questions
                st.session_state.interview_config = {
                    "role": role,
                    "level": level,
                    "interview_type": interview_type,
                    "question_count": question_count,
                    "background": background.strip(),
                    "mode": mode,
                }
                st.session_state.interview_started = True
                st.rerun()


elif not st.session_state.interview_complete:
    questions = st.session_state.questions
    index = st.session_state.current_index
    current = questions[index]
    records = st.session_state.records
    config = st.session_state.interview_config

    progress_col, score_col, role_col = st.columns([1, 1, 2])
    progress_col.metric("答题进度", f"{index + 1} / {len(questions)}")
    score_col.metric("当前均分", f"{average_score(records) or '-'}")
    role_col.metric("目标岗位", config["role"])
    completed_fraction = (index + (1 if st.session_state.current_feedback else 0)) / len(questions)
    st.progress(completed_fraction)

    with st.container(border=True):
        st.caption(f"第 {index + 1} 题 · 考察点：{current['focus']}")
        st.subheader(current["question"])

    if st.session_state.current_feedback is None:
        with st.form(f"answer_form_{index}"):
            answer = st.text_area(
                "你的回答",
                placeholder="建议按照：背景 → 任务 → 行动 → 结果 来组织，尽量写出你自己的具体贡献。",
                height=220,
            )
            submit_answer = st.form_submit_button(
                "提交回答",
                type="primary",
                use_container_width=True,
            )

        if submit_answer:
            if len(answer.strip()) < 10:
                st.warning("回答有点短，请至少写 10 个字再提交。")
            else:
                with st.spinner("正在分析你的回答..."):
                    try:
                        if config["mode"] == "大模型模式":
                            feedback = evaluate_ai_answer(
                                api_key=api_key.strip(),
                                base_url=base_url.strip(),
                                model=model.strip(),
                                role=config["role"],
                                question=current["question"],
                                focus=current["focus"],
                                answer=answer.strip(),
                            )
                        else:
                            feedback = evaluate_demo_answer(
                                question=current["question"],
                                focus=current["focus"],
                                answer=answer.strip(),
                            )
                    except Exception as exc:
                        st.error(f"分析回答失败：{exc}")
                        feedback = None

                if feedback:
                    st.session_state.records.append(
                        {
                            "question": current["question"],
                            "focus": current["focus"],
                            "answer": answer.strip(),
                            "feedback": feedback,
                        }
                    )
                    st.session_state.current_feedback = feedback
                    st.rerun()
    else:
        show_feedback(st.session_state.current_feedback)
        is_last_question = index == len(questions) - 1
        button_label = "查看面试总结" if is_last_question else "进入下一题"
        if st.button(button_label, type="primary", use_container_width=True):
            if is_last_question:
                st.session_state.interview_complete = True
            else:
                st.session_state.current_index += 1
                st.session_state.current_feedback = None
            st.rerun()


else:
    records = st.session_state.records
    config = st.session_state.interview_config
    score = average_score(records)
    dimensions = dimension_averages(records)

    st.subheader("模拟面试完成")
    summary_columns = st.columns(5)
    summary_columns[0].metric("综合得分", f"{score} / 100")
    for column, (key, label) in zip(summary_columns[1:], DIMENSION_LABELS.items()):
        column.metric(label, dimensions[key])

    if score >= 80:
        st.success("整体表现扎实。下一步可以缩短表达，并继续补充更具体的数据和取舍。")
    elif score >= 65:
        st.info("已经具备基本表达框架。建议优先重练得分最低的题目。")
    else:
        st.warning("先别着急背答案。选一道题，用真实经历补齐背景、行动和结果。")

    st.markdown("#### 逐题回顾")
    for index, record in enumerate(records, start=1):
        with st.expander(
            f"第 {index} 题 · {record['feedback']['score']} 分 · {record['question']}"
        ):
            st.markdown("**你的回答**")
            st.write(record["answer"])
            st.markdown("**主要建议**")
            for item in record["feedback"]["improvements"]:
                st.markdown(f"- {item}")

    report = build_markdown_report(config, records)
    download_col, restart_col = st.columns(2)
    with download_col:
        st.download_button(
            "下载 Markdown 面试报告",
            data=report.encode("utf-8"),
            file_name="interview-report.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with restart_col:
        if st.button("重新开始", use_container_width=True):
            reset_interview()
            st.rerun()

    st.caption("评分用于练习参考。大模型可能出错，请结合真实岗位要求判断。")
