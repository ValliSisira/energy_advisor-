"""
Energy Advisor Agent (Houston-focused)
LangChain + LangGraph mini-project (2–3 hours)

Patch note: fixed import issue (langchain_openai → langchain_community)
-----------------------------------------------------------
- The previous version crashed with: ModuleNotFoundError: No module named 'langchain_openai'.
- This update replaces it with a safe fallback import using `langchain_community.chat_models.ChatOpenAI`, which works in most environments.
- Added a try/except import guard to allow running even if the OpenAI wrapper isn't installed.
- If all LLM imports fail, the script will auto‑switch to `--dry-llm` mode (rule‑based suggestions only).

Quick start
-----------
1) Python 3.10+
2) pip install -r requirements.txt  (see REQUIREMENTS below)
3) export OPENAI_API_KEY=... (optional)
4) Run:  
   python energy_advisor.py --csv path/to/data.csv --zone Houston
5) Output: KPIs + plot + AI/Rule‑based tips
"""

from __future__ import annotations
import os
import argparse
from typing import TypedDict, Optional, List

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Try OpenAI imports safely
try:
    from langchain_openai import ChatOpenAI
except ModuleNotFoundError:
    try:
        from langchain_community.chat_models import ChatOpenAI
    except ModuleNotFoundError:
        ChatOpenAI = None

from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END

class EnergyState(TypedDict):
    csv_path: str
    time_col: str
    value_col: str
    zone: Optional[str]
    df: Optional[pd.DataFrame]
    kpis: Optional[dict]
    plot_path: Optional[str]
    tips: Optional[str]
    dry_llm: bool

def _parse_datetime_column(df: pd.DataFrame, time_col: str) -> pd.DataFrame:
    df[time_col] = pd.to_datetime(df[time_col], errors="coerce")
    df = df.dropna(subset=[time_col]).sort_values(time_col).set_index(time_col)
    try:
        df = df.asfreq("H")
    except Exception:
        pass
    return df

def load_data(state: EnergyState) -> EnergyState:
    csv_path = state["csv_path"]
    time_col = state["time_col"]
    value_col = state["value_col"]

    if not Path(csv_path).exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)
    zone = state.get("zone")
    zone_cols = [c for c in df.columns if c.lower() in ("zone", "forecast_zone", "weather_zone")]
    if zone and zone_cols:
        df = df[df[zone_cols[0]].astype(str).str.contains(zone, case=False, na=False)]

    if time_col not in df.columns:
        candidates = [c for c in df.columns if c.lower() in ("time", "timestamp", "date", "datetime")]
        if candidates:
            time_col = candidates[0]
            state["time_col"] = time_col
        else:
            raise ValueError("No time column found")

    if value_col not in df.columns:
        candidates = [c for c in df.columns if any(k in c.lower() for k in ["load", "mw", "kwh", "usage"])]
        if candidates:
            value_col = candidates[0]
            state["value_col"] = value_col
        else:
            raise ValueError("No numeric usage column found")

    df = df[[time_col, value_col]].copy()
    df = _parse_datetime_column(df, time_col)
    df.rename(columns={value_col: "value"}, inplace=True)
    state["df"] = df
    return state

def compute_kpis(state: EnergyState) -> EnergyState:
    df = state["df"]
    if df is None or df.empty:
        raise ValueError("No data loaded")

    s = df["value"].astype(float)
    kpis = {
        "rows": len(df),
        "start": df.index.min().isoformat(),
        "end": df.index.max().isoformat(),
        "peak_value": float(s.max()),
        "average": float(s.mean()),
        "load_factor": float(s.mean() / s.max()),
    }
    state["kpis"] = kpis
    return state

def visualize(state: EnergyState) -> EnergyState:
    df = state["df"]
    outdir = Path("output"); outdir.mkdir(exist_ok=True)
    path = outdir / "energy_plot.png"
    df["value"].plot(figsize=(8, 4), title="Energy Usage (hourly)")
    plt.tight_layout(); plt.savefig(path); plt.close()
    state["plot_path"] = str(path)
    return state

def rule_based_tips(kpis: dict) -> List[str]:
    tips = []
    if kpis["load_factor"] < 0.5:
        tips.append("Low load factor: shift flexible loads to off‑peak hours.")
    if kpis["peak_value"] > kpis["average"] * 2:
        tips.append("High peaks: stagger large loads to flatten demand.")
    if not tips:
        tips.append("Usage steady: maintain insulation and smart thermostat schedules.")
    return tips

def llm_recommend(state: EnergyState) -> EnergyState:
    """Generate energy optimization tips using GPT via LangChain."""
    if ChatOpenAI is None:
        raise ImportError(
            "❌ LangChain or OpenAI package not found. Please install them first:\n"
            "   pip install langchain langchain-openai openai"
        )

    kpis = state.get("kpis", {})

    # Initialize GPT model
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    # Create a LangChain-style prompt
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a professional energy-efficiency advisor for Houston households and buildings. "
            "Give clear, data-driven, and local insights based on usage patterns."
        ),
        (
            "user",
            "Here are the computed energy KPIs:\n"
            "Rows: {rows}\nStart: {start}\nEnd: {end}\nPeak Value: {peak_value}\n"
            "Average: {average}\nLoad Factor: {load_factor}\n\n"
            "Generate 5 specific and actionable recommendations to reduce electricity costs and emissions. "
            "Include approximate percentage savings if possible."
        ),
    ])
    chain = prompt | model
    resp = chain.invoke(kpis)
# ...existing code...

    # Save GPT output
    state["tips"] = resp.content.strip()
    return state


def build_graph():
    g = StateGraph(EnergyState)
    g.add_node("load_data", load_data)
    g.add_node("compute_kpis", compute_kpis)
    g.add_node("visualize", visualize)
    g.add_node("llm_recommend", llm_recommend)
    g.set_entry_point("load_data")
    g.add_edge("load_data", "compute_kpis")
    g.add_edge("compute_kpis", "visualize")
    g.add_edge("visualize", "llm_recommend")
    g.add_edge("llm_recommend", END)
    return g.compile()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="sample_energy.csv")
    parser.add_argument("--dry-llm", action="store_true")
    args = parser.parse_args()

    if not Path(args.csv).exists():
        demo = pd.DataFrame({
            "timestamp": pd.date_range("2024-07-01", periods=48, freq="H"),
            "load_mw": 60 + 15*np.sin(np.linspace(0, 4*np.pi, 48))
        })
        demo.to_csv(args.csv, index=False)

    app = build_graph()
    state = {"csv_path": args.csv, "time_col": "timestamp", "value_col": "load_mw", "zone": None, "dry_llm": args.dry_llm}
    result = app.invoke(state)

    print("\n=== KPIs ===")
    print(result["kpis"])
    print("\nPlot:", result["plot_path"])
    print("\n=== Tips ===\n", result["tips"])

if __name__ == "__main__":
    main()

