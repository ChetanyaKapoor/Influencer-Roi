import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page config
st.set_page_config(
    page_title="Influencer ROI Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Load data
@st.cache_data
def load_data():
    return pd.read_csv("Influencer Roi.csv")

df = load_data()

# 3. Sidebar filters
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

# 4. Tabs for macro and micro analytics
tab1, tab2 = st.tabs(["📊 Macro Analytics", "🔍 Micro Analytics"])

with tab1:
    st.header("Overview Metrics")

    st.markdown("**AdCred Score Distribution**")
    st.plotly_chart(px.histogram(filtered, x="AdCred_Score", nbins=20), use_container_width=True)

    st.markdown("**ROI Distribution**")
    st.plotly_chart(px.histogram(filtered, x="ROI", nbins=20), use_container_width=True)

    st.markdown("**Revenue by Week**")
    fig3 = px.line(filtered.groupby("Week")["Revenue"].sum().reset_index(), x="Week", y="Revenue", markers=True)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("**Impressions vs Clicks (Scatter Plot)**")
    fig4 = px.scatter(filtered, x="Impressions", y="Clicks")
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("**Avg Cart Value by Safety Bucket**")
    cart = filtered.groupby("Safety_Bucket")["Cart_Value_USD"].mean().reset_index()
    st.plotly_chart(px.bar(cart, x="Safety_Bucket", y="Cart_Value_USD"), use_container_width=True)

    st.markdown("**Platform Share**")
    plat = filtered["Platform"].value_counts().reset_index()
    plat.columns = ["Platform", "Count"]
    st.plotly_chart(px.pie(plat, names="Platform", values="Count"), use_container_width=True)

    st.markdown("**Correlation Matrix**")
    corr = filtered.select_dtypes("number").corr()
    st.plotly_chart(px.imshow(corr, text_auto=True), use_container_width=True)

with tab2:
    st.header("Detailed Insights")

    st.markdown("**Conversion Funnel**")
    funnel = filtered[["Clicked","Visited_Landing","Downloaded_Offer","Purchased"]].sum().reset_index()
    funnel.columns = ["Stage","Count"]
    st.plotly_chart(px.bar(funnel, x="Stage", y="Count"), use_container_width=True)

    st.markdown("**AdCred vs ROI (Scatter Plot)**")
    st.plotly_chart(px.scatter(filtered, x="AdCred_Score", y="ROI"), use_container_width=True)

    st.markdown("**ROI by Platform (Box Plot)**")
    st.plotly_chart(px.box(filtered, x="Platform", y="ROI"), use_container_width=True)

    st.markdown("**Top 10 Influencers by Avg ROI**")
    top10 = filtered.groupby("Influencer_Name")["ROI"].mean().nlargest(10).reset_index()
    st.plotly_chart(px.bar(top10, x="Influencer_Name", y="ROI"), use_container_width=True)

    st.markdown("**Sentiment Score Distribution**")
    st.plotly_chart(px.histogram(filtered, x="Sentiment_Score", nbins=20), use_container_width=True)

    st.markdown("**Fake Follower % vs ROI (Scatter Plot)**")
    st.plotly_chart(px.scatter(filtered, x="Fake_Follower_%", y="ROI"), use_container_width=True)

    st.markdown("**Avg Brand Safety Rating by Platform**")
    bs = filtered.groupby("Platform")["Brand_Safety_Rating"].mean().reset_index()
    st.plotly_chart(px.bar(bs, x="Platform", y="Brand_Safety_Rating"), use_container_width=True)

    st.markdown("**AdCred Score by Platform**")
    st.plotly_chart(px.box(filtered, x="Platform", y="AdCred_Score"), use_container_width=True)

    st.markdown("**Avg Story View Rate by Platform**")
    sv = filtered.groupby("Platform")["Story_View_Rate_%"].mean().reset_index()
    st.plotly_chart(px.bar(sv, x="Platform", y="Story_View_Rate_%"), use_container_width=True)

    st.markdown("**Content Match Score vs AdCred (Scatter Plot)**")
    st.plotly_chart(px.scatter(filtered, x="Content_Match_Score", y="AdCred_Score"), use_container_width=True)

    st.markdown("**Avg Posting Frequency by Platform**")
    pf = filtered.groupby("Platform")["Posting_Frequency"].mean().reset_index()
    st.plotly_chart(px.bar(pf, x="Platform", y="Posting_Frequency"), use_container_width=True)

    st.markdown("**Would Rehire?**")
    reh = filtered["Would_Rehire"].value_counts(normalize=True).reset_index()
    reh.columns = ["Would_Rehire", "Proportion"]
    st.plotly_chart(px.pie(reh, names="Would_Rehire", values="Proportion"), use_container_width=True)

    st.markdown("**Conversions by Week**")
    conv = filtered.groupby("Week")["Conversions"].sum().reset_index()
    st.plotly_chart(px.line(conv, x="Week", y="Conversions", markers=True), use_container_width=True)
