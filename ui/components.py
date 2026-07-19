import streamlit as st


def hero(title: str, subtitle: str):
    st.container(border=True)

    st.markdown(
        f"""
        <h1 style='margin-bottom:0;'>{title}</h1>
        <p style='font-size:18px;color:gray;margin-top:5px;'>
            {subtitle}
        </p>
        """,
        unsafe_allow_html=True,
    )


def metric_card(column, label, value, help_text=None):
    with column:
        st.metric(
            label=label,
            value=value,
            help=help_text,
        )


def section(title):
    st.markdown(f"### {title}")


def success(message):
    st.success(message)


def info(message):
    st.info(message)


def warning(message):
    st.warning(message)


def quick_action(label, icon="🚀"):
    return st.button(
        f"{icon} {label}",
        use_container_width=True,
    )