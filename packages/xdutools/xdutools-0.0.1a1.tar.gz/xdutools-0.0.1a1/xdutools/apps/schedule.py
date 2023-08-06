import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from httpx import AsyncClient

E_HALL_NAME = "我的课表"
E_HALL_ID = "4770397878132218"
LESSONS_URL = "http://ehall.xidian.edu.cn/jwapp/sys/wdkb/modules/xskcb/xsllsykb.do"

WEEKDAY_MAPPING = " 一二三四五六日"


@dataclass
class Lesson(object):
    course: str
    teachers: list[str]
    weekday: int
    start_lesson: int
    end_lesson: int
    place: str
    weeks: list[int]

    @classmethod
    def by_data(cls, raw_data: dict):
        return cls(
            course=raw_data["KCM"],
            teachers=(raw_data["SKJS"] or "").split(","),
            weekday=raw_data["SKXQ"],
            start_lesson=raw_data["KSJC"],
            end_lesson=raw_data["JSJC"],
            place=raw_data["JASMC"],
            weeks=cls.process_week(raw_data["ZCMC"]),
        )

    @property
    def wake_up_record(self) -> dict[str, str]:  # python>=3.7保证字典有序
        return {
            "课程名称": self.course,
            "星期": self.weekday_char,
            "开始节数": str(self.start_lesson),
            "结束节数": str(self.end_lesson),
            "老师": self.teachers_str,
            "地点": self.place,
            "周数": "、".join(str(i) for i in self.weeks),
        }

    @property
    def weekday_char(self) -> str:
        return WEEKDAY_MAPPING[self.weekday]

    @property
    def teachers_str(self) -> str:
        return " ".join(self.teachers) if self.teachers else "未安排"

    @property
    def weeks_str(self) -> str:
        return " ".join(str(i) for i in self.weeks)

    @classmethod
    def process_week(cls, week_str: str) -> list[int]:
        rst: list = []
        for w in week_str.split(","):
            m = re.match(r"(\d+)-(\d+)周\([单双]\)$", w)
            if m:
                rst.extend(i for i in range(int(m.group(1)), int(m.group(2)) + 1, 2))
                continue
            m = re.match(r"(\d+)-(\d+)周$", w)
            if m:
                rst.extend(i for i in range(int(m.group(1)), int(m.group(2)) + 1))
            m = re.match(r"(\d+)周$", w)
            if m:
                rst.append(int(m.group(1)))
                continue
        return rst


async def get_lessons(client: "AsyncClient") -> list[Lesson]:
    res = await client.post(LESSONS_URL, data={"XNXQDM": "2020-2021-1"})
    return [Lesson.by_data(i) for i in res.json()["datas"]["xsllsykb"]["rows"]]


def save_lessons_as_wake_up(lessons: list[Lesson]):
    """保存为适合WakeUp课程表导入的格式(csv)
    课程名称,星期,开始节数,结束节数,老师,地点,周数
    """
    with open("./schedule-WakeUpSchedule.csv", "w", encoding="utf-8") as fo:
        fo.write("课程名称,星期,开始节数,结束节数,老师,地点,周数" + "\n")
        fo.writelines(",".join(i.wake_up_record.values()) + "\n" for i in lessons)
