import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.express as px

st.set_page_config(layout="wide")
# Create three columns with the middle one containing the content
left_col, middle_col, right_col = st.columns([1,2,1])
st.title("Stelle Restaurant Analytics Dashboard")
st.markdown("### A data-driven approach to optimize operations and enhance customer experience")

user_profile = {
    "name": "Erica",
    "role": "Manager",
    "profile_picture": "./images.png"  # Replace with actual image path
}

# Sidebar Layout
st.sidebar.image("./FB_IMG_1737140832991.jpg", width=300)
st.sidebar.header("User  Profile")
st.sidebar.image(user_profile["profile_picture"], width=90)  # Profile Picture
st.sidebar.markdown(f"**{user_profile['name']}**")  # User Name
st.sidebar.markdown(f"*{user_profile['role']}*")  # User Role
menu = st.sidebar.selectbox("Select a Dashboard Section", [
    "Overview",
    "Demand Prediction",
    "Customer Insights",
    "Menu Performance",
    "Inventory Management",
    "Staff Optimization",
    "Customer Feedback"
])

# Load Sample Data (To be replaced with actual data)
def load_sample_data():
    data = {
        "Date": pd.date_range(start="2023-01-01", periods=365, freq="D"),
        "Sales": np.random.randint(500, 2000, 365),
        "Customers": np.random.randint(50, 200, 365),
        "Service Time": np.random.uniform(5, 15, 365),
        "Top Item": np.random.choice(["Burger", "Pizza", "Pasta", "Salad"], 365),
        "Staff Present": np.random.randint(4, 10, 365),
        "Service Type": np.random.choice(["Dine-in", "Takeaway", "Delivery"], 365)
    }
    return pd.DataFrame(data)

data = load_sample_data()

# Dynamic Filtering
st.sidebar.markdown("### Filters")
time_period = st.sidebar.selectbox("Select Time Period", ["Daily", "Weekly", "Monthly"])
menu_item_filter = st.sidebar.selectbox("Filter by Menu Item", ["All"] + list(data["Top Item"].unique()))

if menu_item_filter != "All":
    data = data[data["Top Item"] == menu_item_filter]

   # Theme Settings
st.sidebar.header("Theme Settings")
theme_option = st.sidebar.radio("Select Theme", ("Light Mode", "Dark Mode"))

# Apply theme based on user selection
if theme_option == "Dark Mode":
    st.markdown("""
        <style>
            .stApp {
                background-color: #2E2E2E;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

if menu == "Overview":
    st.header("Overview Dashboard")
    
    # Custom CSS for better card styling
    st.markdown("""
        <style>
        div[data-testid="stMetricValue"] {
            font-size: 24px;
            color: #0066cc;
        }
        div.stMetricLabel {
            font-size: 16px;
            color: #666666;
        }
        div[data-testid="metric-container"] {
            background-color: #ffffff;
            border: 1px solid #e6e6e6;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        </style>
    """, unsafe_allow_html=True)

    # Top metrics section - 3 columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        today_revenue = data['Sales'].iloc[-1]
        st.metric(
            label="Today's Revenue",
            value=f"${today_revenue:,.2f}",
            delta=f"{((today_revenue/10000)*100):.1f}% of target"
        )

    with col2:
        today_orders = data['Customers'].iloc[-1]
        st.metric(
            label="Today's Orders",
            value=f"{today_orders:,}",
            delta=f"{((today_orders/300)*100):.1f}% of target"
        )

    with col3:
        avg_service_time = data['Service Time'].mean()
        st.metric(
            label="Avg Service Time",
            value=f"{avg_service_time:.1f} min",
            delta=f"{(10-avg_service_time):.1f} min to target"
        )

    # Performance charts section - 2 columns
    st.subheader("Performance Analytics")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # Revenue trend
        fig_revenue = px.line(
            data,
            x="Date",
            y="Sales",
            title="Daily Revenue Trend",
            labels={"Sales": "Revenue ($)", "Date": "Date"}
        )
        fig_revenue.update_layout(margin=dict(t=30))
        st.plotly_chart(fig_revenue, use_container_width=True)

    with chart_col2:
        # Customer traffic
        hourly_traffic = pd.DataFrame({
            "Hour": list(range(6, 23)),
            "Customers": np.random.randint(10, 50, 17)
        })
        fig_traffic = px.bar(
            hourly_traffic,
            x="Hour",
            y="Customers",
            title="Customer Traffic by Hour",
            labels={"Customers": "Customer Count", "Hour": "Hour of Day"}
        )
        fig_traffic.update_layout(margin=dict(t=30))
        st.plotly_chart(fig_traffic, use_container_width=True)

    # Revenue breakdown and performance indicators - 2 columns
    st.subheader("Business Insights")
    insight_col1, insight_col2 = st.columns(2)

    with insight_col1:
        service_revenue = data.groupby("Service Type")["Sales"].sum().reset_index()
        fig_service = px.pie(
            service_revenue,
            names="Service Type",
            values="Sales",
            title="Revenue by Service Type"
        )
        fig_service.update_layout(margin=dict(t=30))
        st.plotly_chart(fig_service, use_container_width=True)

    with insight_col2:
        # Performance table
        st.markdown("#### Sales Performance")
        performance_data = pd.DataFrame({
            "Item": ["Burger", "Pizza", "Pasta", "Salad"],
            "Sales": [300, 250, 200, 100],
            "Profit": [1200, 1500, 800, 600]
        })
        st.dataframe(
            performance_data.style.background_gradient(
                subset=['Sales', 'Profit'],
                cmap='Blues'
            ),
            use_container_width=True
        )

    # Alerts and inventory section
    st.subheader("Alerts & Inventory")
    alert_col1, alert_col2 = st.columns(2)

    with alert_col1:
        st.warning("⚠️ Low Inventory Items")
        inventory_alerts = pd.DataFrame({
            "Item": ["Tomatoes", "Cheese", "Lettuce"],
            "Stock": [10, 5, 2],
            "Threshold": [20, 15, 10]
        })
        st.dataframe(
            inventory_alerts.style.apply(
                lambda x: ['background-color: #ffebee' if x.Stock < x.Threshold else '' for _ in x],
                axis=1
            ),
            use_container_width=True
        )

    with alert_col2:
        # Sales vs Profit comparison
        fig_sales_profit = px.bar(
            performance_data,
            x='Item',
            y=['Sales', 'Profit'],
            title="Sales vs. Profit Comparison",
            barmode='group'
        )
        fig_sales_profit.update_layout(margin=dict(t=30))
        st.plotly_chart(fig_sales_profit, use_container_width=True)
   

elif menu == "Demand Prediction":
    st.header("Demand Prediction")
    fig = px.line(data, x="Date", y="Sales", title="Sales Over Time")
    st.plotly_chart(fig)

    st.markdown("### Predicted Sales for Next 7 Days")
    future_dates = pd.date_range(start=data['Date'].iloc[-1] + pd.Timedelta(days=1), periods=7)
    future_sales = np.random.randint(500, 2000, 7)
    future_df = pd.DataFrame({"Date": future_dates, "Predicted Sales": future_sales})
    st.table(future_df)
if menu == "Demand Prediction":
    st.header("Demand Prediction Dashboard")

    # Create a modern layout with cards
    st.markdown("""
        <style>
            .card {
                background-color: #f0f2f5;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
        </style>
    """, unsafe_allow_html=True)

    # Input for selecting prediction date
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Select Prediction Date")
    prediction_date = st.date_input("Choose a date for prediction", value=datetime.today())
    st.markdown("</div>", unsafe_allow_html=True)

    # Generate predictions based on the selected date
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Predicted Sales for Next 7 Days")
    
    # Simulate future sales predictions
    future_dates = pd.date_range(start=prediction_date, periods=7)
    future_sales = np.random.randint(500, 2000, 7)  # Simulated sales data
    future_df = pd.DataFrame({"Date": future_dates, "Predicted Sales": future_sales})

    # Display the predictions in a table
    st.table(future_df)
    st.markdown("</div>", unsafe_allow_html=True)

    # Visualization of predicted sales
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Predicted Sales Line Chart")
    fig_predicted_sales = px.line(future_df, x="Date", y="Predicted Sales", title="Predicted Sales Over Next 7 Days", labels={"Predicted Sales": "Sales ($)", "Date": "Date"})
    st.plotly_chart(fig_predicted_sales, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Additional Insights
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Insights and Recommendations")
    st.text("- Consider increasing staff during predicted peak sales days.")
    st.text("- Monitor inventory levels to meet expected demand.")
    st.text("- Analyze historical data for similar patterns.")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Customer Insights":
       # Customer Traffic by Hour
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Customer Traffic by Hour")
    hourly_traffic = pd.DataFrame({"Hour": list(range(6, 23)), "Customers": np.random.randint(10, 50, 17)})
    fig_customer_traffic = px.bar(hourly_traffic, x="Hour", y="Customers", title="Customer Traffic by Hour", labels={"Customers": "Customer Count", "Hour": "Hour of Day"})
    st.plotly_chart(fig_customer_traffic, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Most Ordered Items
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Most Ordered Items")
    top_items = data['Top Item'].value_counts().head(5)
    fig_top_items = px.bar(top_items, x=top_items.index, y=top_items.values, title="Top 5 Most Ordered Items", labels={"x": "Menu Item", "y": "Order Count"})
    st.plotly_chart(fig_top_items, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

 # Insights and Recommendations
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Insights and Recommendations")
    st.text("- Most ordered item: Burger")
    st.text("- Customer retention rate: 70%")
    st.text("- Popular days: Weekends")
    st.markdown("</div>", unsafe_allow_html=True)

    # Customer Retention Rate
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Customer Retention Rate")
    retention_rate = 70  # Example retention rate
    st.metric(label="Customer Retention Rate", value=f"{retention_rate}%", delta="5%", delta_color="normal")
    st.markdown("</div>", unsafe_allow_html=True)

    # Customer Feedback Sentiment Analysis
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Customer Feedback Sentiment Analysis")
    sentiment_data = pd.DataFrame({
        "Sentiment": ["Positive", "Neutral", "Negative"],
        "Count": [120, 45, 25],
    })
    fig_sentiment = px.pie(sentiment_data, names="Sentiment", values="Count", title="Customer Sentiment Distribution", hole=0.4)
    st.plotly_chart(fig_sentiment, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


    
elif menu == "Menu Performance":
    st.header("Menu Performance Dashboard")

    # Create a modern layout with cards
    st.markdown("""
        <style>
            .card {
                background-color: #f0f2f5;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
        </style>
    """, unsafe_allow_html=True)

    # Menu Profitability
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Menu Profitability")
    menu_data = pd.DataFrame({
        "Item": ["Burger", "Pizza", "Pasta", "Salad"],
        "Profitability": [1200, 1500, 800, 600],
        "Sales Frequency": [300, 250, 200, 100],
    })
    fig_menu_profitability = px.bar(menu_data, x="Item", y="Profitability", title="Menu Profitability", labels={"Profitability": "Profit ($)", "Item": "Menu Item"})
    st.plotly_chart(fig_menu_profitability, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Sales Frequency
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Sales Frequency")
    fig_sales_frequency = px.bar(menu_data, x="Item", y="Sales Frequency", title="Sales Frequency by Menu Item", labels={"Sales Frequency": "Number of Sales", "Item": "Menu Item"})
    st.plotly_chart(fig_sales_frequency, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Performance Comparison
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Performance Comparison")
    fig_performance_comparison = px.line(menu_data, x="Item", y=["Profitability", "Sales Frequency"], title="Performance Comparison", labels={"value": "Amount ($)", "Item": "Menu Item"}, markers=True)
    st.plotly_chart(fig_performance_comparison, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Insights and Recommendations
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Insights and Recommendations")
    st.text("- Focus on promoting high-profit items like Pizza.")
    st.text("- Consider revising the menu to improve sales frequency for lower-performing items.")
    st.text("- Analyze customer feedback to enhance menu offerings.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    


elif menu == "Inventory Management":
    st.header("Inventory Management Dashboard")

    # Create a modern layout with cards
    st.markdown("""
        <style>
            .card {
                background-color: #f0f2f5;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
        </style>
    """, unsafe_allow_html=True)

    # Critical Stock Alerts
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Critical Stock Alerts")
    inventory_data = pd.DataFrame({
        "Ingredient": ["Tomatoes", "Cheese", "Lettuce", "Chicken"],
        "Stock Level": [50, 20, 10, 30],
        "Threshold": [40, 30, 15, 25]
    })
    low_stock_alerts = inventory_data[inventory_data['Stock Level'] < inventory_data['Threshold']]
    if not low_stock_alerts.empty:
        st.warning("Low inventory items detected.")
        st.table(low_stock_alerts)
    else:
        st.success("All inventory levels are sufficient.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Inventory Levels Visualization
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Inventory Levels Visualization")
    fig_inventory_levels = px.bar(inventory_data, x="Ingredient", y="Stock Level", title="Current Inventory Levels", labels={"Stock Level": "Quantity", "Ingredient": "Ingredient"})
    st.plotly_chart(fig_inventory_levels, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Historical Inventory Trends
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Historical Inventory Trends")
    # Simulating historical data for demonstration
    historical_data = pd.DataFrame({
        "Date": pd.date_range(start="2023-01-01", periods=30, freq="D"),
        "Tomatoes": np.random.randint(20, 60, 30),
        "Cheese": np.random.randint(10, 40, 30),
        "Lettuce": np.random.randint(5, 25, 30),
        "Chicken": np.random.randint(15, 50, 30)
    })
    fig_historical_trends = px.line(historical_data, x="Date", y=["Tomatoes", "Cheese", "Lettuce", "Chicken"], title="Historical Inventory Trends", labels={"value": "Stock Level", "Date": "Date"})
    st.plotly_chart(fig_historical_trends, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Insights and Recommendations
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Insights and Recommendations")
    st.text("- Monitor stock levels regularly to avoid shortages.")
    st.text("- Consider automating inventory alerts for low stock items.")
    st.text("- Analyze usage trends to optimize ordering schedules.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Alert Section
    st.markdown("### Alerts")
    low_inventory_alerts = inventory_data[inventory_data['Stock Level'] < inventory_data['Threshold']]
    if not low_inventory_alerts.empty:
        st.warning("Low inventory items detected.")
        st.table(low_inventory_alerts)


elif menu == "Staff Optimization":
    st.header("Staff Optimization Dashboard")

    # Create a modern layout with cards
    st.markdown("""
        <style>
            .card {
                background-color: #f0f2f5;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
        </style>
    """, unsafe_allow_html=True)

    # Staff Schedule Optimization
    st.header("Staff Optimization Dashboard")

    # Create a modern layout with cards
    st.markdown("""
        <style>
            .card {
                background-color: #f0f2f5;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
            .ai-bot {
                background-color: #e7f3fe;
                border-left: 5px solid #2196F3;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
            }
            .alert-table {
                border-collapse: collapse;
                width: 100%;
            }
            .alert-table th, .alert-table td {
                border: 1px solid #ddd;
                padding: 8px;
            }
            .alert-table th {
                background-color: #2196F3;
                color: white;
            }
            .alert-table tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            .alert-table tr:hover {
                background-color: #ddd;
            }
        </style>
    """, unsafe_allow_html=True)

    # Staff Schedule Optimization
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Staff Schedule Optimization")
    schedule_data = pd.DataFrame({
        "Shift": ["Morning", "Afternoon", "Evening"],
        "Staff Required": [5, 7, 8],
    })
    fig_schedule = px.bar(schedule_data, x="Shift", y="Staff Required", title="Staff Required by Shift", labels={"Staff Required": "Number of Staff", "Shift": "Shift"})
    st.plotly_chart(fig_schedule, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Staff Presence Overview
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Staff Presence Overview")
    staff_presence = pd.DataFrame({
        "Date": pd.date_range(start="2023-01-01", periods=30, freq="D"),
        "Staff Present": np.random.randint(4, 10, 30)
    })
    fig_staff_presence = px.line(staff_presence, x="Date", y="Staff Present", title="Staff Presence Over the Month", labels={"Staff Present": "Number of Staff", "Date": "Date"})
    st.plotly_chart(fig_staff_presence, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Staff Alerts
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Staff Alerts")
    staff_alerts = staff_presence[staff_presence['Staff Present'] < 5]
    
    if not staff_alerts.empty:
        st.markdown("<div class='ai-bot'>", unsafe_allow_html=True)
        st.markdown("🤖 **AI Assistant:** Low staff presence detected on the following days:")
        st.markdown("</div>", unsafe_allow_html=True)

        # Create a table for alerts
        st.table(staff_alerts.style.set_table_attributes('class="alert-table"'))
    else:
        st.success("Staff levels are adequate.")
    
    st.markdown("</div>", unsafe_allow_html=True)

    # AI Insights and Recommendations
    st.markdown("<div class='card ai-bot'>", unsafe_allow_html=True)
    st.markdown("### AI Insights and Recommendations")
    
    # Simulated AI-generated insights
    st.markdown("🤖 **AI Assistant:** Based on the current staffing data, here are some recommendations:")
    
    # Example insights based on data
    if staff_presence['Staff Present'].mean() < 6:
        st.text("- It seems that the average staff presence is below optimal levels. Consider increasing staff during peak hours.")
    else:
        st.text("- Staff levels are generally adequate, but monitor for any upcoming events that may require additional staffing.")
    
    if staff_alerts.shape[0] > 0:
        st.text("- Review the days with low staff presence to identify patterns and adjust schedules accordingly.")
    
    st.text("- Consider cross-training staff to ensure coverage during peak hours.")

elif menu == "Customer Feedback":
    st.header("Customer Feedback Analysis Dashboard")

    # Create a modern layout with cards
    st.markdown("""
        <style>
            .card {
                background-color: #f0f2f5;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
            .feedback-table {
                border-collapse: collapse;
                width: 100%;
            }
            .feedback-table th, .feedback-table td {
                border: 1px solid #ddd;
                padding: 8px;
            }
            .feedback-table th {
                background-color: #2196F3;
                color: white;
            }
            .feedback-table tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            .feedback-table tr:hover {
                background-color: #ddd;
            }
        </style>
    """, unsafe_allow_html=True)

    # Sentiment Analysis
    st.header("Customer Feedback Analysis Dashboard")

    # Create a modern layout with cards
    st.markdown("""
        <style>
            .card {
                background-color: #f0f2f5;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
            .feedback-table {
                border-collapse: collapse;
                width: 100%;
            }
            .feedback-table th, .feedback-table td {
                border: 1px solid #ddd;
                padding: 8px;
            }
            .feedback-table th {
                background-color: #2196F3;
                color: white;
            }
            .feedback-table tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            .feedback-table tr:hover {
                background-color: #ddd;
            }
            .ai-bot {
                background-color: #e7f3fe;
                border-left: 5px solid #2196F3;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Sentiment Analysis
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Customer Sentiment Analysis")
    sentiment_data = pd.DataFrame({
        "Sentiment": ["Positive", "Neutral", "Negative"],
        "Count": [120, 45, 25],
    })
    fig_sentiment = px.pie(sentiment_data, names="Sentiment", values="Count", title="Customer Sentiment Distribution", hole=0.4)
    st.plotly_chart(fig_sentiment, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Common Feedback
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Most Common Feedback")
    common_feedback = pd.DataFrame({
        "Feedback": [
            "Great service!",
            "Loved the pizza!",
            "Wait time was a bit long.",
            "Friendly staff.",
            "The ambiance was nice."
        ]
    })
    st.table(common_feedback.style.set_table_attributes('class="feedback-table"'))
    st.markdown("</div>", unsafe_allow_html=True)

    # Feedback Trends Over Time
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Feedback Trends Over Time")
    feedback_trends = pd.DataFrame({
        "Date": pd.date_range(start="2023-01-01", periods=30, freq="D"),
        "Positive": np.random.randint(5, 20, 30),
        "Neutral": np.random.randint(1, 10, 30),
        "Negative": np.random.randint(0, 5, 30)
    })
    fig_feedback_trends = px.line(feedback_trends, x="Date", y=["Positive", "Neutral", "Negative"], title="Customer Feedback Trends Over Time", labels={"value": "Number of Feedbacks", "Date": "Date"})
    st.plotly_chart(fig_feedback_trends, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # AI Insights and Recommendations
    st.markdown("<div class='card ai-bot'>", unsafe_allow_html=True)
    st.markdown("### AI Insights and Recommendations")
    
    # Simulated AI-generated insights
    st.markdown("🤖 **AI Assistant:** Based on the customer feedback data, here are some insights:")
    
    # Example insights based on data
    st.text("- It seems that customers appreciate the service but have concerns about wait times.")
    st.text("- The most common positive feedback is about the pizza, indicating it is a popular item.")
    st.text("- Consider addressing the wait time issue to improve overall customer satisfaction.")
    st.text("- Regularly monitor feedback trends to identify any emerging issues.")
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Analytics Dashboard powered by Stelle Restaurant's data insights.")
