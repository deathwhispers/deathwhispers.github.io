#!/usr/bin/env python3
"""Normalize tags/categories for Jekyll posts.

Goals:
- unify tag casing and aliases
- reduce tag explosion by controlled vocabulary
- enforce two-level, series-oriented categories
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.S)

ACRONYMS = {
    "ai": "AI",
    "llm": "LLM",
    "nlp": "NLP",
    "jvm": "JVM",
    "sql": "SQL",
    "http": "HTTP",
    "https": "HTTPS",
    "tcp": "TCP",
    "udp": "UDP",
    "jwt": "JWT",
    "sso": "SSO",
    "ddd": "DDD",
    "gcp": "GCP",
    "cpa": "CPA",
    "capa": "CAPA",
    "mcp": "MCP",
    "cra": "CRA",
    "aio": "AIO",
    "bio": "BIO",
    "nio": "NIO",
    "poi": "POI",
    "spi": "SPI",
}

TAG_ALIAS = {
    # generic
    "笔记": None,
    "note": None,
    "notes": None,
    # core casing
    "mysql": "MySQL",
    "redis": "Redis",
    "mongodb": "MongoDB",
    "db2": "DB2",
    "cassandra": "Cassandra",
    "java": "Java",
    "java8": "Java",
    "java9": "Java",
    "java10": "Java",
    "java11": "Java",
    "java16": "Java",
    "javanio": "NIO",
    "synchronized": "Concurrency",
    "concurrent": "Concurrency",
    "jmm": "JMM",
    "aqs": "AQS",
    "spring": "Spring",
    "spring boot": "SpringBoot",
    "springboot": "SpringBoot",
    "spring 框架": "Spring",
    "spring 源码解析": "SpringSourceCode",
    "mybatisplus": "MyBatisPlus",
    "mybatis": "MyBatis",
    "dubbo": "Dubbo",
    "netty": "Netty",
    "kafka": "Kafka",
    "flink": "Flink",
    "spark": "Spark",
    "spark sql": "SparkSQL",
    "spark streaming": "SparkStreaming",
    "hbase": "HBase",
    "hive": "Hive",
    "hadoop": "Hadoop",
    "hdfs": "HDFS",
    "storm": "Storm",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "go": "Go",
    "python": "Python",
    "c/c++": "Cpp",
    "c_c++": "Cpp",
    "rust": "Rust",
    "designpatterns": "DesignPatterns",
    "distributed system": "DistributedSystem",
    "分布式系统": "DistributedSystem",
    "分布式": "DistributedSystem",
    "分布式事物": "DistributedSystem",
    "系统设计": "SystemDesign",
    "计算机网络": "Network",
    "network": "Network",
    "poll": "OperatingSystem",
    "epoll": "OperatingSystem",
    "select": "OperatingSystem",
    # front-end
    "vue3": "Vue3",
    "前端工程化": "FrontendEngineering",
    "工程化": "FrontendEngineering",
    "前后端协作": "FrontendCollaboration",
    "pinia": "Pinia",
    "状态管理": "StateManagement",
    "工程实践": "EngineeringPractice",
    "实战": "EngineeringPractice",
    "旧项目改造": "LegacyRefactor",
    "学习路线": "LearningPath",
    "学习方法": "LearningMethod",
    # AI
    "deepseek": "DeepSeek",
    "agent": "Agent",
    "llm": "LLM",
    "大模型": "LargeModel",
    "生成式ai": "GenerativeAI",
    "transformer": "Transformer",
    "attention": "Transformer",
    "机器学习": "MachineLearning",
    "深度学习": "DeepLearning",
    "卷积神经网络": "ComputerVision",
    "目标检测": "ComputerVision",
    "神经网络": "NeuralNetwork",
    "多模态": "Multimodal",
    "vlm": "VLM",
    "rag": "RAG",
    "ai发展史": "AIHistory",
    # IoT
    "jetlinks": "JetLinks",
    "thingsboard": "ThingsBoard",
    "httpclient": "HttpClient",
    # personal / others
    "效率": "Efficiency",
    "课表": "Course",
    "科研修炼手册": "Research",
    "研究生科学道德与学术规范": "Research",
    "工程数学基础": "MasterLearn",
    "数据仓库与数据挖掘": "BigData",
    "武汉": "Travel",
    "东湖": "Travel",
    "落雁岛": "Travel",
    "江西": "Travel",
    "黄陂": "Travel",
    "孝感": "Travel",
    "新疆": "Travel",
    "神农架": "Travel",
    "黄石": "Travel",
    "青龙山": "Travel",
    "珠港澳": "Travel",
    "动物园": "Travel",
    "life": "Life",
    "blog": "Blog",
    "geek": "Geek",
    "github pages": "GitHubPages",
    "google search console": "GoogleSearchConsole",
    "virtualization": "Virtualization",
    "hardware": "Hardware",
    "security": "Security",
    "penetration": "Security",
    "graph database": "GraphDatabase",
    "graph neural network": "GNN",
    "gnn": "GNN",
    "computer vision": "ComputerVision",
    "cv": "ComputerVision",
    "natural language": "NLP",
    "timeSeries": "TimeSeries",
    "timeseries": "TimeSeries",
    "recommendation system": "Recommendation",
    "financial stocks": "Finance",
    "biopharmaceuticals": "ClinicalResearch",
    "监查": "ClinicalMonitoring",
    "临床研究": "ClinicalResearch",
    "临床试验": "ClinicalTrial",
    "职业发展": "Career",
    "职业规划": "Career",
    "职业技能": "Career",
    "风险管理": "RiskManagement",
    "绩效管理": "Performance",
    "sponsor": "Sponsor",
    "cro": "CRO",
}

DROP_TAGS = {
    "my all",
    "song",
    "japanese song",
}

# Keep tag set compact and stable.
ALLOWED_TAGS = {
    "AI",
    "AIHistory",
    "Agent",
    "Algorithms",
    "AQS",
    "BigData",
    "Blog",
    "CAPA",
    "Career",
    "Cassandra",
    "ClinicalMonitoring",
    "ClinicalResearch",
    "ClinicalTrial",
    "ComputerVision",
    "Concurrency",
    "Cpp",
    "CRO",
    "DB2",
    "DDD",
    "DeepLearning",
    "DeepSeek",
    "DesignPatterns",
    "DistributedSystem",
    "Docker",
    "Dubbo",
    "Efficiency",
    "EngineeringPractice",
    "Finance",
    "Flink",
    "FrontendCollaboration",
    "FrontendEngineering",
    "GCP",
    "Geek",
    "GenerativeAI",
    "Git",
    "GitHubPages",
    "GNN",
    "Go",
    "GoogleSearchConsole",
    "GraphDatabase",
    "Hadoop",
    "HBase",
    "HDFS",
    "Hardware",
    "Hive",
    "HttpClient",
    "IoT",
    "Java",
    "JetLinks",
    "JMM",
    "JVM",
    "Kafka",
    "Kubernetes",
    "LLM",
    "LargeModel",
    "LearningMethod",
    "LearningPath",
    "LegacyRefactor",
    "Life",
    "MachineLearning",
    "MasterLearn",
    "MCP",
    "MongoDB",
    "Multimodal",
    "MyBatis",
    "MyBatisPlus",
    "MySQL",
    "Netty",
    "Network",
    "NeuralNetwork",
    "NIO",
    "NLP",
    "OperatingSystem",
    "Pinia",
    "Python",
    "RAG",
    "Recommendation",
    "Redis",
    "Research",
    "RiskManagement",
    "Security",
    "Spark",
    "SparkSQL",
    "SparkStreaming",
    "Spring",
    "SpringBoot",
    "SpringSourceCode",
    "StateManagement",
    "Storm",
    "SystemDesign",
    "ThingsBoard",
    "TimeSeries",
    "Tooling",
    "Transformer",
    "Travel",
    "Virtualization",
    "VLM",
    "Vue3",
}

# Prefer stable ordering inside each series.
SERIES_TAG_PRIORITY = {
    "AI": [
        "AI",
        "LLM",
        "Agent",
        "MCP",
        "DeepSeek",
        "Transformer",
        "GenerativeAI",
        "AIHistory",
        "ComputerVision",
        "MachineLearning",
        "DeepLearning",
        "Multimodal",
        "VLM",
        "RAG",
        "NLP",
        "GNN",
        "LargeModel",
    ],
    "Framework": [
        "Spring",
        "SpringBoot",
        "MyBatis",
        "MyBatisPlus",
        "EngineeringPractice",
        "DesignPatterns",
        "SystemDesign",
        "Tooling",
    ],
    "IoT": ["IoT", "JetLinks", "ThingsBoard", "HttpClient", "Network"],
    "Learning": [
        "Java",
        "Spring",
        "SpringBoot",
        "SpringSourceCode",
        "Concurrency",
        "JVM",
        "MySQL",
        "Redis",
        "Database",
        "SQL",
        "MongoDB",
        "Cassandra",
        "DB2",
        "Dubbo",
        "DistributedSystem",
        "Netty",
        "Network",
        "Algorithms",
        "OperatingSystem",
        "Docker",
        "Kubernetes",
        "Flink",
        "Spark",
        "HBase",
        "Hive",
        "Storm",
        "Hadoop",
        "Python",
        "Go",
        "Cpp",
        "Vue3",
        "FrontendEngineering",
        "Pinia",
        "StateManagement",
        "EngineeringPractice",
    ],
    "Personal": ["MasterLearn", "Research", "Travel", "Life", "Efficiency", "Career"],
    "Practicing": ["EngineeringPractice", "Tooling", "Redis", "DeepSeek", "Network", "Spring"],
    "Resources": [
        "Tooling",
        "ComputerVision",
        "MachineLearning",
        "DeepLearning",
        "NLP",
        "LLM",
        "Python",
        "Cpp",
        "Rust",
        "Security",
        "Virtualization",
        "Hardware",
        "GraphDatabase",
        "Recommendation",
        "TimeSeries",
    ],
    "Other": ["Tooling", "Git", "EngineeringPractice", "Life"],
    "CleanCode": ["EngineeringPractice", "Java"],
    "Misc": ["Tooling", "EngineeringPractice"],
}

SERIES_BASE_TAGS = {
    ("AI", "General"): ["AI"],
    ("AI", "LargeModel"): ["AI", "LLM"],
    ("AI", "ComputerVision"): ["AI", "ComputerVision"],
    ("AI", "DeepSeek"): ["AI", "DeepSeek"],
    ("Framework", "Backend"): ["Spring"],
    ("IoT", "General"): ["IoT"],
    ("IoT", "JetLinks"): ["IoT", "JetLinks"],
    ("IoT", "ThingsBoard"): ["IoT", "ThingsBoard"],
    ("Learning", "General"): ["EngineeringPractice"],
    ("Learning", "Java"): ["Java"],
    ("Learning", "Spring"): ["Spring"],
    ("Learning", "Database"): ["Database"],
    ("Learning", "BigData"): ["BigData"],
    ("Learning", "Dubbo"): ["Dubbo"],
    ("Learning", "Network"): ["Network"],
    ("Learning", "DesignPatterns"): ["DesignPatterns"],
    ("Learning", "Interview"): ["Java", "Network"],
    ("Learning", "Algorithms"): ["Algorithms"],
    ("Learning", "Distributed"): ["DistributedSystem"],
    ("Learning", "Docker"): ["Docker"],
    ("Learning", "JVM"): ["JVM"],
    ("Learning", "Cpp"): ["Cpp"],
    ("Learning", "SystemDesign"): ["SystemDesign"],
    ("Learning", "Go"): ["Go"],
    ("Learning", "OperatingSystem"): ["OperatingSystem"],
    ("Learning", "Japanese"): [],
    ("Learning", "Python"): ["Python"],
    ("Learning", "Vue"): ["Vue3", "FrontendEngineering"],
    ("Learning", "Netty"): ["Netty"],
    ("Personal", "MasterLearn"): ["MasterLearn"],
    ("Personal", "Travel"): ["Travel"],
    ("Personal", "Life"): ["Life"],
    ("Personal", "Efficiency"): ["Efficiency"],
    ("Practicing", "General"): ["EngineeringPractice"],
    ("Resources", "Collection"): ["Tooling"],
    ("Other", "General"): ["Tooling"],
    ("CleanCode", "Naming"): ["EngineeringPractice", "Java"],
    ("Misc", "General"): ["Tooling"],
}


@dataclass
class Stats:
    scanned: int = 0
    changed: int = 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize taxonomy in markdown front matter")
    parser.add_argument("paths", nargs="*", default=["_posts"], help="files or directories to scan")
    parser.add_argument("--check", action="store_true", help="check only, do not write")
    parser.add_argument("--max-tags", type=int, default=4, help="max tags kept per post")
    return parser.parse_args()


def iter_markdown(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_file() and p.suffix.lower() == ".md":
            files.append(p)
        elif p.is_dir():
            files.extend(sorted(p.rglob("*.md")))
    return files


def split_front_matter(text: str) -> tuple[dict[str, Any], str, str]:
    if not text.startswith("---\n"):
        return {}, "", text
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return {}, "", text
    raw = m.group(1)
    body = text[m.end() :]
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        data = {}
    return data, raw, body


def render(meta: dict[str, Any], body: str) -> str:
    yaml_text = yaml.safe_dump(
        meta,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        indent=2,
    )
    normalized_body = body.lstrip("\n").rstrip("\n")
    return f"---\n{yaml_text}---\n\n{normalized_body}\n"


def norm_key(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).lower()


def title_case_token(token: str) -> str:
    if not token:
        return token
    lower = token.lower()
    if lower in ACRONYMS:
        return ACRONYMS[lower]
    if token.isupper() and len(token) <= 6:
        return token
    return token[0].upper() + token[1:].lower()


def fallback_format_tag(tag: str) -> str:
    if re.search(r"[\u4e00-\u9fff]", tag):
        return tag.strip()
    words = re.split(r"[\s_\-]+", tag.strip())
    words = [title_case_token(w) for w in words if w]
    if not words:
        return ""
    return "".join(words) if len(words) == 1 else "".join(words)


def normalize_tag(raw: Any) -> str | None:
    tag = str(raw).strip()
    if not tag:
        return None
    key = norm_key(tag)
    if key in DROP_TAGS:
        return None
    if key in TAG_ALIAS:
        return TAG_ALIAS[key]
    formatted = fallback_format_tag(tag)
    if not formatted:
        return None
    if formatted in ALLOWED_TAGS:
        return formatted
    # Chinese long-tail tags are folded by topic to keep taxonomy small.
    if re.search(r"[\u4e00-\u9fff]", formatted):
        if any(x in formatted for x in ["面试", "八股"]):
            return "EngineeringPractice"
        if any(x in formatted for x in ["网络", "TCP", "HTTP"]):
            return "Network"
        if any(x in formatted for x in ["并发", "线程", "锁"]):
            return "Concurrency"
        if any(x in formatted for x in ["数据库", "索引", "事务"]):
            return "Database"
        if any(x in formatted for x in ["算法", "树", "数组"]):
            return "Algorithms"
        if any(x in formatted for x in ["学习", "教程", "入门"]):
            return "LearningMethod"
        return None
    return None


def category_from_path(path: Path) -> list[str]:
    parts = path.parts
    if not parts or parts[0] != "_posts":
        return ["Misc", "General"]

    rel = parts[1:]
    if not rel:
        return ["Misc", "General"]

    root = rel[0].lower()

    if root == "ai":
        sub = rel[1].lower() if len(rel) > 2 else (rel[1].lower() if len(rel) > 1 and rel[1].endswith(".md") is False else "")
        mapping = {
            "bigmodel": "LargeModel",
            "computervision": "ComputerVision",
            "deepseek": "DeepSeek",
        }
        return ["AI", mapping.get(sub, "General")]

    if root == "framework":
        return ["Framework", "Backend"]

    if root == "iot":
        sub = rel[1].lower() if len(rel) > 2 else (rel[1].lower() if len(rel) > 1 and rel[1].endswith(".md") is False else "")
        mapping = {"jetlinks": "JetLinks", "thingsboard": "ThingsBoard"}
        return ["IoT", mapping.get(sub, "General")]

    if root == "learning":
        sub = rel[1].lower() if len(rel) > 2 else (rel[1].lower() if len(rel) > 1 and rel[1].endswith(".md") is False else "")
        mapping = {
            "java": "Java",
            "spring": "Spring",
            "database": "Database",
            "bigdata": "BigData",
            "dubbo": "Dubbo",
            "network": "Network",
            "designpatterns": "DesignPatterns",
            "interview": "Interview",
            "algorithms": "Algorithms",
            "distributed": "Distributed",
            "docker": "Docker",
            "jvm": "JVM",
            "c_c++": "Cpp",
            "sysdesign": "SystemDesign",
            "go": "Go",
            "os": "OperatingSystem",
            "japanese": "Japanese",
            "python": "Python",
            "vue": "Vue",
            "netty": "Netty",
            "numpy": "Python",
        }
        return ["Learning", mapping.get(sub, "General")]

    if root == "personal":
        sub = rel[1].lower() if len(rel) > 2 else (rel[1].lower() if len(rel) > 1 and rel[1].endswith(".md") is False else "")
        mapping = {
            "masterlearn": "MasterLearn",
            "travel": "Travel",
            "life": "Life",
            "efficiency": "Efficiency",
        }
        return ["Personal", mapping.get(sub, "Life")]

    if root == "practicing":
        return ["Practicing", "General"]

    if root == "resources":
        return ["Resources", "Collection"]

    if root == "other":
        return ["Other", "General"]

    if root == "cleancode":
        return ["CleanCode", "Naming"]

    return ["Misc", "General"]


def list_value(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            s = str(item).strip()
            if s:
                out.append(s)
        return out
    s = str(value).strip()
    return [s] if s else []


def order_tags(tags: list[str], series: str) -> list[str]:
    priority = SERIES_TAG_PRIORITY.get(series, [])
    ranking = {name: idx for idx, name in enumerate(priority)}
    return sorted(tags, key=lambda x: (ranking.get(x, 999), x))


def rebuild_tags(path: Path, meta: dict[str, Any], max_tags: int) -> list[str]:
    category = category_from_path(path)
    series = category[0]

    normalized: list[str] = []
    for raw in list_value(meta.get("tags")):
        t = normalize_tag(raw)
        if t and t in ALLOWED_TAGS and t not in normalized:
            normalized.append(t)

    base = SERIES_BASE_TAGS.get((category[0], category[1]), [])
    merged: list[str] = []
    for t in base + normalized:
        if t and t not in merged:
            merged.append(t)

    merged = order_tags(merged, series)
    if max_tags > 0:
        merged = merged[:max_tags]

    if not merged:
        merged = base[: max_tags or len(base)]
    if not merged:
        merged = ["EngineeringPractice"] if series in {"Learning", "Framework", "Practicing"} else ["Tooling"]

    return merged


def process_file(path: Path, check: bool, max_tags: int, stats: Stats) -> None:
    text = path.read_text(encoding="utf-8")
    meta, _, body = split_front_matter(text)
    if not meta:
        return

    stats.scanned += 1
    new_meta = dict(meta)
    new_meta["categories"] = category_from_path(path)
    new_meta["tags"] = rebuild_tags(path, meta, max_tags=max_tags)

    new_text = render(new_meta, body)
    if new_text != text:
        stats.changed += 1
        if check:
            print(f"NEED_UPDATE {path}")
        else:
            path.write_text(new_text, encoding="utf-8")


def main() -> int:
    args = parse_args()
    files = iter_markdown(args.paths)
    stats = Stats()
    for p in files:
        if "_site/" in str(p):
            continue
        try:
            process_file(p, check=args.check, max_tags=args.max_tags, stats=stats)
        except Exception as exc:
            print(f"ERROR {p}: {exc}")
            return 2

    mode = "CHECK" if args.check else "WRITE"
    print(f"{mode} scanned={stats.scanned} changed={stats.changed}")
    return 1 if args.check and stats.changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
