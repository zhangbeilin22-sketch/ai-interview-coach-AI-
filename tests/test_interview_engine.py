import unittest

from interview_engine import (
    _extract_json,
    average_score,
    build_markdown_report,
    evaluate_demo_answer,
    generate_demo_questions,
)


class InterviewEngineTests(unittest.TestCase):
    def test_demo_questions_match_requested_count(self):
        questions = generate_demo_questions("AI 应用开发实习生", 5)

        self.assertEqual(len(questions), 5)
        self.assertEqual(len({item["question"] for item in questions}), 5)
        self.assertTrue(all(item["focus"] for item in questions))

    def test_custom_role_uses_general_questions(self):
        questions = generate_demo_questions("量化研究实习生", 8)

        self.assertEqual(len(questions), 8)
        self.assertIn("自我介绍", questions[0]["focus"])

    def test_extract_json_accepts_code_fence(self):
        payload = _extract_json('```json\n{"score": 80}\n```')

        self.assertEqual(payload["score"], 80)

    def test_detailed_demo_answer_scores_higher(self):
        short_feedback = evaluate_demo_answer("介绍项目", "项目经验", "我做过一个项目。")
        detailed_feedback = evaluate_demo_answer(
            "介绍项目",
            "项目经验",
            (
                "首先，我负责一个课程项目的需求分析。其次，我使用 Python 和 Streamlit "
                "完成了页面设计与接口调用，并整理了 20 条测试数据。最后项目按时完成，"
                "核心流程可以稳定运行。因为早期提示词不稳定，我又增加了输出格式约束，"
                "后续还计划改进异常处理。"
            ),
        )

        self.assertGreater(detailed_feedback["score"], short_feedback["score"])
        self.assertEqual(set(detailed_feedback["dimensions"]), {"relevance", "clarity", "evidence", "depth"})

    def test_report_contains_summary_and_answers(self):
        feedback = evaluate_demo_answer("请介绍项目", "项目经验", "我负责完成了页面和接口。")
        records = [
            {
                "question": "请介绍项目",
                "focus": "项目经验",
                "answer": "我负责完成了页面和接口。",
                "feedback": feedback,
            }
        ]
        config = {"role": "AI 应用开发实习生", "level": "基础", "interview_type": "综合面试"}

        report = build_markdown_report(config, records)

        self.assertEqual(average_score(records), feedback["score"])
        self.assertIn("# AI 模拟面试报告", report)
        self.assertIn("AI 应用开发实习生", report)
        self.assertIn("我负责完成了页面和接口", report)


if __name__ == "__main__":
    unittest.main()
