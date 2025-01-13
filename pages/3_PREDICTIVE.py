if st.checkbox("Show feature importance for models"):
    # Dropdown for model selection
    selected_model = st.selectbox(
        "Select a model to display feature importance:",
        ['Random Forest', 'Decision Tree']
    )

    # Check if the selected model supports feature importance
    if selected_model in ['Random Forest', 'Decision Tree']:
        model = models[selected_model]  # Fetch the trained model
        feature_importances = model.feature_importances_  # Get feature importance
        feature_names = ['item_code', 'month', 'premise_type', 'district']

        # Plotly bar chart for feature importance
        fig_features = px.bar(
            x=feature_importances,
            y=feature_names,
            orientation='h',
            title=f'Feature Importance ({selected_model})',
            labels={'x': 'Importance', 'y': 'Feature'}
        )

        # Update layout for better aesthetics
        fig_features.update_layout(
            xaxis_title="Importance",
            yaxis_title="Feature",
            template="plotly_white"
        )

        # Display the chart
        st.plotly_chart(fig_features, use_container_width=True)
    else:
        st.write(f"{selected_model} does not support feature importance.")
