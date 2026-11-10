import streamlit as st
from pipeline import run_research_pipeline

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔎",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #6366f1, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-title { color: #94a3b8; margin-bottom: 1.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

STEP_NAMES = {
    1: "Search agent",
    2: "Reader agent",
    3: "Writer agent",
    4: "Critique agent",
}

if "history" not in st.session_state:
    st.session_state.history = []
if "selected" not in st.session_state:
    st.session_state.selected = None


# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 📚 Research History")
    if st.session_state.history:
        for idx in reversed(range(len(st.session_state.history))):
            item = st.session_state.history[idx]
            if st.button(f"📄 {item['topic'][:40]}", key=f"hist_{idx}", use_container_width=True):
                st.session_state.selected = idx
    else:
        st.caption("No research yet. Enter a topic to start.")

    st.divider()
    if st.button("🗑️ Clear history", use_container_width=True):
        st.session_state.history = []
        st.session_state.selected = None
        st.rerun()


# ---------- Header ----------
st.markdown('<div class="main-title">AI Research Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Search, read, write and critique, all automatically</div>',
    unsafe_allow_html=True,
)


# ---------- Input ----------
with st.form("research_form"):
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Impact of AI on healthcare in India",
    )
    submitted = st.form_submit_button("🚀 Start Research", use_container_width=True)


def show_results(item: dict):
    tab_report, tab_critique, tab_sources, tab_scraped = st.tabs(
        ["📝 Report", "🧐 Critique", "🔍 Search Results", "🌐 Scraped Content"]
    )

    with tab_report:
        st.markdown(item["report"])
        full_text = (
            f"# {item['topic']}\n\n{item['report']}\n\n"
            f"---\n\n## Critique\n\n{item['feedback']}"
        )
        st.download_button(
            "⬇️ Download report (Markdown)",
            data=full_text,
            file_name="research_report.md",
            mime="text/markdown",
        )

    with tab_critique:
        st.markdown(item["feedback"])

    with tab_sources:
        st.markdown(item["search_results"])

    with tab_scraped:
        st.text(item["scraped_content"])  # plain text, avoids markdown breaking on raw HTML-ish content


# ---------- Run pipeline ----------
if submitted:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        status_box = st.status("Researching...", expanded=True)

        def on_step(step, status, detail):
            if status == "running":
                status_box.write(f"⏳ **{STEP_NAMES[step]}** is working...")
            else:
                status_box.write(f"✅ **{STEP_NAMES[step]}** finished.")

        try:
            result = run_research_pipeline(topic.strip(), on_step=on_step)
            status_box.update(label="Research complete ✅", state="complete", expanded=False)

            st.session_state.history.append({
                "topic": topic.strip(),
                "report": result["report"],
                "feedback": result["feedback"],
                "search_results": result["search_results"],
                "scraped_content": result["scraped_content"],
            })
            st.session_state.selected = len(st.session_state.history) - 1
        except Exception as e:
            status_box.update(label="Something went wrong ❌", state="error")
            st.error(f"Pipeline error: {e}")


# ---------- Show selected result ----------
if st.session_state.selected is not None and st.session_state.history:
    current = st.session_state.history[st.session_state.selected]
    st.subheader(f"Topic: {current['topic']}")
    show_results(current)
else:
    st.info("Enter a topic above and click **Start Research** to begin.")