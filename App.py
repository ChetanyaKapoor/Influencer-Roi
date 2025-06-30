import streamlit as st
import pandas as pd
import plotly.express as px

# ─── 1. Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Influencer ROI Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── 2. Load data ───────────────────────────────────────────────────────────────
@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_csv("EA.csv")
    return df

df = load_data()

# ─── 3. Sidebar filters ─────────────────────────────────────────────────────────
st.sidebar.header("🔎 Filters")
platforms = st.sidebar.multiselect(
    "Platform", options=df["Platform"].unique(), default=df["Platform"].unique()
)
influencers = st.sidebar.multiselect(
    "Influencer", options=df["Influencer_Name"].unique(), default=df["Influencer_Name"].unique()
)
week_min, week_max = int(df["Week"].min()), int(df["Week"].max())
week_range = st.sidebar.slider("Week Range", week_min, week_max, (week_min, week_max))
adcred_min, adcred_max = float(df["AdCred_Score"].min()), float(df["AdCred_Score"].max())
adcred_range = st.sidebar.slider("AdCred Score", adcred_min, adcred_max, (adcred_min, adcred_max))

# Apply filters
filtered = df.query(
    "Platform in @platforms and Influencer_Name in @influencers and "
    "Week >= @week_range[0] and Week <= @week_range[1] and "
    "AdCred_Score >= @adcred_range[0] and AdCred_Score <= @adcred_range[1]"
)

# ─── 4. Tabs ────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📊 Macro Analytics", "🔍 Micro Analytics"])

with tab1:
    st.header("Overview Metrics")

    st.markdown("**AdCred Score Distribution** – shows how influencer credibility is spread.")
    fig1 = px.histogram(filtered, x="AdCred_Score", nbins=20)
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("**ROI Distribution** – understand profitability spread across campaigns.")
    fig2 = px.histogram(filtered, x="ROI", nbins=20)
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**Revenue by Week** – spot seasonality or spikes over time.")
    rev_week = filtered.groupby("Week")["Revenue"].sum().reset_index()
    fig3 = px.line(rev_week, x="Week", y="Revenue", markers=True)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("**Impressions vs Clicks** – more clicks per view indicates engagement.")
    fig4 = px.scatter(filtered, x="Impressions", y="Clicks", trendline="ols")
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("**Avg Cart Value by Safety Bucket** – transaction value by risk profile.")
    cart = filtered.groupby("Safety_Bucket")["Cart_Value_USD"].mean().reset_index()
    fig5 = px.bar(cart, x="Safety_Bucket", y="Cart_Value_USD")
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("**Platform Share** – which channels dominate your influencer mix.")
    plat = filtered["Platform"].value_counts().reset_index()
    plat.columns = ["Platform", "Count"]
    fig6 = px.pie(plat, names="Platform", values="Count")
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("**Correlation Matrix** – find strong positive/negative relationships.")
    corr = filtered.select_dtypes("number").corr()
    fig7 = px.imshow(corr, text_auto=True)
    st.plotly_chart(fig7, use_container_width=True)

with tab2:
    st.header("Detailed Insights")

    st.markdown("**Conversion Funnel** – drop-off from clicks → visits → downloads → purchases.")
    funnel = filtered[["Clicked","Visited_Landing","Downloaded_Offer","Purchased"]].sum().reset_index()
    funnel.columns = ["Stage","Count"]
    fig8 = px.bar(funnel, x="Stage", y="Count")
    st.plotly_chart(fig8, use_container_width=True)

    st.markdown("**AdCred vs ROI** – does credibility drive better returns?")
    fig9 = px.scatter(filtered, x="AdCred_Score", y="ROI", trendline="ols")
    st.plotly_chart(fig9, use_container_width=True)

    st.markdown("**ROI by Platform** – compare distributions across channels.")
    fig10 = px.box(filtered, x="Platform", y="ROI")
    st.plotly_chart(fig10, use_container_width=True)

    st.markdown("**Top 10 Influencers by Avg ROI** – spot your highest performers.")
    top10 = filtered.groupby("Influencer_Name")["ROI"].mean().nlargest(10).reset_index()
    fig11 = px.bar(top10, x="Influencer_Name", y="ROI")
    st.plotly_chart(fig11, use_container_width=True)

    st.markdown("**Sentiment Score Distribution** – gauge overall campaign tone.")
    fig12 = px.histogram(filtered, x="Sentiment_Score", nbins=20)
    st.plotly_chart(fig12, use_container_width=True)

    st.markdown("**Fake Follower % vs ROI** – see if inauthenticity hurts ROI.")
    fig13 = px.scatter(filtered, x="Fake_Follower_%", y="ROI", trendline="ols")
    st.plotly_chart(fig13, use_container_width=True)

    st.markdown("**Avg Brand Safety Rating by Platform** – compare content safety.")
    bs = filtered.groupby("Platform")["Brand_Safety_Rating"].mean().reset_index()
    fig14 = px.bar(bs, x="Platform", y="Brand_Safety_Rating")
    st.plotly_chart(fig14, use_container_width=True)

    st.markdown("**AdCred Score by Platform** – credibility variance per channel.")
    fig15 = px.box(filtered, x="Platform", y="AdCred_Score")
    st.plotly_chart(fig15, use_container_width=True)

    st.markdown("**Avg Story View Rate by Platform** – which channel has best engagement?")
    sv = filtered.groupby("Platform")["Story_View_Rate_%"].mean().reset_index()
    fig16 = px.bar(sv, x="Platform", y="Story_View_Rate_%")
    st.plotly_chart(fig16, use_container_width=True)

    st.markdown("**Content Match vs AdCred** – on-brand content → credibility?")
    fig17 = px.scatter(filtered, x="Content_Match_Score", y="AdCred_Score")
    st.plotly_chart(fig17, use_container_width=True)

    st.markdown("**Avg Posting Frequency by Platform** – posting cadence across channels.")
    pf = filtered.groupby("Platform")["Posting_Frequency"].mean().reset_index()
    fig18 = px.bar(pf, x="Platform", y="Posting_Frequency")
    st.plotly_chart(fig18, use_container_width=True)

    st.markdown("**Would Rehire?** – influencer satisfaction post-campaign.")
    reh = filtered["Would_Rehire"].value_counts(normalize=True).reset_index()
    reh.columns = ["Would_Rehire", "Proportion"]
    fig19 = px.pie(reh, names="Would_Rehire", values="Proportion")
    st.plotly_chart(fig19, use_container_width=True)

    st.markdown("**Conversions by Week** – campaign efficiency over time.")
    conv = filtered.groupby("Week")["Conversions"].sum().reset_index()
    fig20 = px.line(conv, x="Week", y="Conversions", markers=True)
    st.plotly_chart(fig20, use_container_width=True)
