def display_prediction_results(prediction, historical_data, features_used):
    """Display prediction results without matplotlib"""
    
    st.markdown("---")
    st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"<h2 style='text-align: center; color: #1f77b4;'>🔮 Next Day Prediction</h2>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center; color: #2e86ab; font-size: 3rem;'>{prediction:,.0f} Wh</h1>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Find energy column
    energy_col = None
    energy_indicators = ['energy', 'prev_day', 'consumption', 'usage', 'target', 'value']
    for col in historical_data.columns:
        if any(indicator in col.lower() for indicator in energy_indicators):
            energy_col = col
            break
    
    if energy_col is None and len(historical_data.columns) > 0:
        energy_col = historical_data.columns[0]
    
    if energy_col:
        # Metrics and comparison
        col1, col2, col3, col4 = st.columns(4)
        
        recent_data = historical_data[energy_col].tail(7)
        recent_avg = recent_data.mean()
        recent_max = recent_data.max()
        recent_min = recent_data.min()
        
        with col1:
            st.metric("📊 Recent Average", f"{recent_avg:,.0f} Wh")
        with col2:
            st.metric("📈 Recent Maximum", f"{recent_max:,.0f} Wh")
        with col3:
            st.metric("📉 Recent Minimum", f"{recent_min:,.0f} Wh")
        with col4:
            change_pct = ((prediction - recent_avg) / recent_avg) * 100
            st.metric("🔄 vs Average", f"{change_pct:+.1f}%")
        
        # Visualization using Streamlit native charts
        st.subheader("📈 Historical Trends & Prediction")
        
        # Line chart for trend
        trend_data = historical_data[energy_col].tail(min(30, len(historical_data)))
        st.line_chart(trend_data)
        
        # Bar chart for recent pattern
        st.subheader("Last 7 Days Pattern")
        recent_df = pd.DataFrame({
            'Days Ago': ['6 days', '5 days', '4 days', '3 days', '2 days', '1 day', 'Today'],
            'Energy (Wh)': recent_data.values
        })
        st.bar_chart(recent_df.set_index('Days Ago'))
