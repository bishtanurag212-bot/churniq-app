# Enterprise Churn Analytics Platform
# Modern SaaS-Style Web Application

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, 
                             confusion_matrix, roc_auc_score, classification_report)
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import warnings
import time
import io
from streamlit_option_menu import option_menu
import base64
from datetime import datetime

warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="ChurnIQ | Enterprise Customer Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Modern Enterprise Design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Global Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Modern Glass Morphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.6s;
    }
    
    .glass-card:hover::before {
        left: 100%;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: rgba(99, 102, 241, 0.5);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    /* Animated Gradient Header */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        animation: gradientShift 8s ease infinite;
        border-radius: 32px;
        padding: 3rem;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .hero-section h1 {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    /* Neon Glow Effects */
    .neon-text {
        text-shadow: 0 0 10px rgba(102, 126, 234, 0.5), 0 0 20px rgba(102, 126, 234, 0.3);
    }
    
    /* Modern Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(168, 85, 247, 0.2));
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(99, 102, 241, 0.3);
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        border-color: #6366f1;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Floating Animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .float-animation {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Glowing Button */
    .glow-button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border: none;
        padding: 12px 32px;
        border-radius: 50px;
        color: white;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .glow-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.6);
    }
    
    /* Upload Area */
    .upload-area {
        border: 2px dashed #6366f1;
        border-radius: 24px;
        padding: 3rem;
        text-align: center;
        background: rgba(99, 102, 241, 0.05);
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: #a78bfa;
        background: rgba(99, 102, 241, 0.1);
        transform: translateY(-2px);
    }
    
    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255,255,255,0.05);
        border-radius: 60px;
        padding: 0.5rem;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 50px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: #94a3b8;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    /* Dataframe Styling */
    .dataframe {
        border-radius: 16px;
        overflow: hidden;
        background: rgba(255,255,255,0.05);
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        padding: 12px;
        font-weight: 600;
    }
    
    .dataframe td {
        padding: 10px;
        background: rgba(255,255,255,0.03);
        color: #e2e8f0;
    }
    
    /* Particle Effect */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #8b5cf6, #6366f1);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Notification Cards */
    .notification-card {
        background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(139,92,246,0.1));
        border-left: 4px solid #6366f1;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'models_trained' not in st.session_state:
    st.session_state.models_trained = False
if 'target_column' not in st.session_state:
    st.session_state.target_column = None
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Upload"

# Hero Section with Animation
st.markdown("""
<div class="hero-section">
    <div style="position: relative; z-index: 1;">
        <h1 class="float-animation">🎯 ChurnIQ Enterprise</h1>
        <p style="font-size: 1.2rem; color: #f0f0f0; margin-top: 1rem;">
            AI-Powered Customer Intelligence Platform
        </p>
        <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 2rem;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 50px; backdrop-filter: blur(5px;">🤖 Machine Learning</span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 50px; backdrop-filter: blur(5px;">📊 Real-time Analytics</span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 50px; backdrop-filter: blur(5px;">🎯 Predictive Intelligence</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Modern Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 20px; margin: 0 auto; display: flex; align-items: center; justify-content: center;">
            <span style="font-size: 2rem;">🎯</span>
        </div>
        <h3 style="margin-top: 1rem; background: linear-gradient(135deg, #fff, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">ChurnIQ</h3>
        <p style="font-size: 0.8rem; color: #94a3b8;">Enterprise Edition</p>
    </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["Upload", "Explore", "Target", "Train", "Predict", "Insights"],
        icons=["cloud-upload", "bar-chart", "bullseye", "robot", "magic", "lightbulb"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background": "transparent"},
            "icon": {"color": "#6366f1", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "5px 0",
                "padding": "12px 20px",
                "border-radius": "12px",
                "color": "#94a3b8",
                "transition": "all 0.3s ease"
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #6366f1, #8b5cf6)",
                "color": "white",
                "font-weight": "600"
            },
            "nav-link-hover": {
                "background": "rgba(99, 102, 241, 0.2)",
                "color": "white"
            }
        }
    )
    
    st.session_state.current_page = selected
    
    st.markdown("---")
    
    # Status Card
    if st.session_state.data_loaded:
        st.markdown("""
        <div class="glass-card" style="padding: 1rem;">
            <p style="color: #94a3b8; font-size: 0.8rem;">📊 Dataset Status</p>
            <p style="color: #4ade80; font-size: 0.9rem;">✅ Active</p>
            <p style="color: white;">{:,} records</p>
        </div>
        """.format(len(st.session_state.data)), unsafe_allow_html=True)
        
        if st.session_state.target_column:
            st.markdown(f"""
            <div class="glass-card" style="padding: 1rem; margin-top: 1rem;">
                <p style="color: #94a3b8; font-size: 0.8rem;">🎯 Target Column</p>
                <p style="color: #fbbf24;">{st.session_state.target_column}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.session_state.models_trained:
            st.markdown("""
            <div class="glass-card" style="padding: 1rem; margin-top: 1rem;">
                <p style="color: #94a3b8; font-size: 0.8rem;">🤖 Model Status</p>
                <p style="color: #4ade80;">✅ Trained & Ready</p>
            </div>
            """, unsafe_allow_html=True)

# Function to load data
def load_data(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            return None
        
        df = df.replace([np.inf, -np.inf], np.nan)
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Upload Page
if st.session_state.current_page == "Upload":
    st.markdown("""
    <div class="glass-card">
        <h2 style="background: linear-gradient(135deg, #fff, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">📤 Upload Your Dataset</h2>
        <p style="color: #94a3b8; margin-top: 0.5rem;">Start by uploading your customer data (CSV or Excel format)</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['csv', 'xlsx', 'xls'],
        help="Upload CSV or Excel file containing customer data"
    )
    
    if uploaded_file is not None:
        with st.spinner("Processing your dataset..."):
            df = load_data(uploaded_file)
            
            if df is not None:
                st.session_state.data = df
                st.session_state.data_loaded = True
                
                # Preview
                st.markdown("""
                <div class="glass-card" style="margin-top: 2rem;">
                    <h3>📊 Dataset Preview</h3>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rows", f"{df.shape[0]:,}", delta=None)
                with col2:
                    st.metric("Columns", df.shape[1], delta=None)
                with col3:
                    st.metric("Memory", f"{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB", delta=None)
                
                st.dataframe(df.head(100))
                
                # Quick Stats
                with st.expander("🔍 Quick Statistics"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Data Types:**")
                        st.dataframe(df.dtypes.value_counts().to_frame())
                    with col2:
                        st.write("**Missing Values:**")
                        missing = df.isnull().sum()
                        st.dataframe(missing[missing > 0].to_frame() if any(missing > 0) else pd.DataFrame({'Info': ['No missing values']}))
                
                st.success("✅ Dataset loaded successfully! Navigate to 'Explore' to analyze your data.")

# Explore Page
elif st.session_state.current_page == "Explore" and st.session_state.data_loaded:
    st.markdown("""
    <div class="glass-card">
        <h2 style="background: linear-gradient(135deg, #fff, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🔍 Data Exploration</h2>
        <p style="color: #94a3b8;">Interactive visualizations and insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    df = st.session_state.data
    
    # Modern Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Visual Analytics", "📊 Distributions", "🔗 Correlations", "📋 Summary"])
    
    with tab1:
        st.markdown("### Interactive Data Visualization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                selected = st.selectbox("Select numeric column", numeric_cols)
                fig = px.histogram(df, x=selected, title=f"Distribution of {selected}",
                                  color_discrete_sequence=['#6366f1'],
                                  template='plotly_dark')
                fig.update_layout(showlegend=False, height=500)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            if categorical_cols:
                selected_cat = st.selectbox("Select categorical column", categorical_cols)
                top_values = df[selected_cat].value_counts().head(10)
                fig = px.bar(x=top_values.index, y=top_values.values,
                            title=f"Top values in {selected_cat}",
                            color_discrete_sequence=['#8b5cf6'],
                            template='plotly_dark')
                fig.update_layout(showlegend=False, height=500)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Feature Distributions")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            fig, axes = plt.subplots(nrows=min(6, len(numeric_cols)), ncols=2, 
                                     figsize=(15, 4*min(6, len(numeric_cols))))
            axes = axes.flatten() if len(numeric_cols) > 1 else [axes]
            
            for idx, col in enumerate(numeric_cols[:12]):
                df[col].hist(ax=axes[idx], bins=30, color='#6366f1', edgecolor='#8b5cf6', alpha=0.7)
                axes[idx].set_title(col, color='white')
                axes[idx].set_xlabel('')
                axes[idx].set_facecolor('#0f172a')
            
            for idx in range(len(numeric_cols[:12]), len(axes)):
                axes[idx].set_visible(False)
            
            plt.tight_layout()
            st.pyplot(fig)
    
    with tab3:
        st.markdown("### Correlation Matrix")
        
        numeric_df = df.select_dtypes(include=[np.number])
        if len(numeric_df.columns) > 1:
            corr = numeric_df.corr()
            fig = ff.create_annotated_heatmap(
                z=corr.values,
                x=list(corr.columns),
                y=list(corr.index),
                annotation_text=corr.round(2).values,
                colorscale='Viridis',
                showscale=True
            )
            fig.update_layout(height=700, template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### Dataset Summary")
        st.dataframe(df.describe(include='all'))

# Target Selection Page
elif st.session_state.current_page == "Target" and st.session_state.data_loaded:
    st.markdown("""
    <div class="glass-card">
        <h2 style="background: linear-gradient(135deg, #fff, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🎯 Select Target Variable</h2>
        <p style="color: #94a3b8;">Choose which column represents customer churn</p>
    </div>
    """, unsafe_allow_html=True)
    
    df = st.session_state.data
    
    # Auto-detect potential churn columns
    potential = []
    for col in df.columns:
        col_lower = col.lower()
        if any(k in col_lower for k in ['churn', 'cancel', 'attrition', 'left', 'exited']):
            potential.append(col)
    
    if potential:
        st.info(f"💡 Detected potential churn columns: {', '.join(potential)}")
    
    target = st.selectbox("Select target column", df.columns.tolist())
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Distribution")
        counts = df[target].value_counts()
        fig = px.pie(values=counts.values, names=counts.index,
                    title=f"{target} Distribution",
                    color_discrete_sequence=['#6366f1', '#8b5cf6', '#a78bfa'],
                    template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Statistics")
        st.write(f"**Unique values:** {df[target].nunique()}")
        st.write(f"**Data type:** {df[target].dtype}")
        st.write("**Value counts:**")
        st.dataframe(df[target].value_counts().to_frame())
    
    if st.button("Confirm Target", use_container_width=True):
        st.session_state.target_column = target
        st.success(f"✅ Target column set to: {target}")

# Train Page - UPDATED WITH INTELLIGENT SAMPLING
elif st.session_state.current_page == "Train" and st.session_state.data_loaded:
    st.markdown("""
    <div class="glass-card">
        <h2 style="background: linear-gradient(135deg, #fff, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🤖 Model Training</h2>
        <p style="color: #94a3b8;">Train multiple ML models and compare performance</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.target_column:
        st.warning("⚠️ Please select a target column first")
    else:
        df = st.session_state.data
        
        # Add sampling option
        st.markdown("### ⚡ Training Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sample_size = st.slider(
                "Sample Size (%) for Training",
                min_value=10,
                max_value=100,
                value=30,
                step=10,
                help="Use a percentage of data for faster training. Lower = faster training"
            )
        
        with col2:
            total_rows = len(df)
            sampled_rows = int(total_rows * sample_size / 100)
            st.info(f"📊 Will use {sampled_rows:,} rows out of {total_rows:,} total rows ({sample_size}%)")
        
        with st.spinner("Preparing data..."):
            # Sample the data if needed
            if sample_size < 100:
                # Stratified sampling to maintain class distribution
                from sklearn.model_selection import StratifiedShuffleSplit
                
                y_temp = df[st.session_state.target_column]
                # Encode temporarily for stratification
                temp_le = LabelEncoder()
                y_encoded = temp_le.fit_transform(y_temp.astype(str))
                
                sss = StratifiedShuffleSplit(n_splits=1, test_size=1 - sample_size/100, random_state=42)
                for train_idx, _ in sss.split(df, y_encoded):
                    sampled_df = df.iloc[train_idx]
                    break
                
                st.info(f"✅ Sampled {len(sampled_df):,} rows while preserving class distribution")
                df = sampled_df
            else:
                st.info(f"✅ Using full dataset ({len(df):,} rows)")
            
            X = df.drop(st.session_state.target_column, axis=1)
            y = df[st.session_state.target_column]
            
            # Encode
            le = LabelEncoder()
            if y.dtype == 'object':
                y = le.fit_transform(y)
            
            categorical_cols = X.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                X[col] = le.fit_transform(X[col].astype(str))
            
            for col in X.columns:
                X[col] = pd.to_numeric(X[col], errors='coerce')
            X = X.fillna(0).replace([np.inf, -np.inf], 0)
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            st.session_state.feature_columns = X.columns.tolist()
            st.session_state.scaler = scaler
        
        models = {
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
            'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
            'Decision Tree': DecisionTreeClassifier(random_state=42)
        }
        
        if st.button("🚀 Start Training", use_container_width=True):
            results = []
            progress = st.progress(0)
            start_time = time.time()
            
            for idx, (name, model) in enumerate(models.items()):
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
                
                results.append({
                    'Model': name,
                    'Accuracy': accuracy_score(y_test, y_pred),
                    'Precision': precision_score(y_test, y_pred, average='weighted'),
                    'Recall': recall_score(y_test, y_pred, average='weighted'),
                    'F1 Score': f1_score(y_test, y_pred, average='weighted')
                })
                progress.progress((idx + 1) / len(models))
            
            training_time = time.time() - start_time
            
            results_df = pd.DataFrame(results)
            best_idx = results_df['Accuracy'].idxmax()
            best_model = models[results_df.loc[best_idx, 'Model']]
            
            st.session_state.best_model = best_model
            st.session_state.best_model_name = results_df.loc[best_idx, 'Model']
            st.session_state.models_trained = True
            
            # Show training stats
            st.info(f"⚡ Training completed in {training_time:.2f} seconds using {sampled_rows:,} samples")
            
            # Results visualization
            fig = go.Figure()
            metrics = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
            
            for metric in metrics:
                fig.add_trace(go.Bar(
                    name=metric,
                    x=results_df['Model'],
                    y=results_df[metric],
                    text=results_df[metric].round(3),
                    textposition='auto',
                    marker_color='#6366f1'
                ))
            
            fig.update_layout(
                barmode='group',
                height=500,
                title="Model Performance Comparison",
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(results_df.style.background_gradient(cmap='RdYlGn'))
            st.success(f"✅ Best Model: {st.session_state.best_model_name} with {results_df.loc[best_idx, 'Accuracy']:.3f} accuracy")

# Predict Page
elif st.session_state.current_page == "Predict" and st.session_state.data_loaded:
    st.markdown("""
    <div class="glass-card">
        <h2 style="background: linear-gradient(135deg, #fff, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🎲 Real-time Prediction</h2>
        <p style="color: #94a3b8;">Enter customer details to predict churn probability</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.models_trained:
        st.warning("⚠️ Please train models first")
    else:
        st.markdown("### Customer Profile")
        
        cols = st.columns(3)
        input_data = {}
        
        for idx, col in enumerate(st.session_state.feature_columns[:12]):
            with cols[idx % 3]:
                if st.session_state.data[col].dtype == 'object':
                    input_data[col] = st.selectbox(col, st.session_state.data[col].unique())
                else:
                    input_data[col] = st.number_input(col, float(st.session_state.data[col].min()), 
                                                      float(st.session_state.data[col].max()),
                                                      float(st.session_state.data[col].median()))
        
        if st.button("🔮 Predict Churn Risk", use_container_width=True):
            input_df = pd.DataFrame([input_data])
            
            le = LabelEncoder()
            for col in input_df.select_dtypes(include=['object']).columns:
                input_df[col] = le.fit_transform(input_df[col].astype(str))
            
            for col in st.session_state.feature_columns:
                if col not in input_df.columns:
                    input_df[col] = 0
            
            input_df = input_df[st.session_state.feature_columns].fillna(0)
            input_scaled = st.session_state.scaler.transform(input_df)
            
            prob = st.session_state.best_model.predict_proba(input_scaled)[0][1]
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=prob * 100,
                    title={'text': "Churn Risk Score"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#6366f1"},
                        'steps': [
                            {'range': [0, 30], 'color': "#10b981"},
                            {'range': [30, 70], 'color': "#f59e0b"},
                            {'range': [70, 100], 'color': "#ef4444"}
                        ]
                    }
                ))
                fig.update_layout(height=400, template='plotly_dark')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                risk = "HIGH" if prob > 0.7 else "MEDIUM" if prob > 0.3 else "LOW"
                color = "#ef4444" if prob > 0.7 else "#f59e0b" if prob > 0.3 else "#10b981"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {color}20, {color}10); border: 2px solid {color}; border-radius: 20px; padding: 2rem; text-align: center;">
                    <h3>Risk Level: <span style="color: {color};">{risk}</span></h3>
                    <h1 style="color: {color};">{prob*100:.1f}%</h1>
                    <p>Churn Probability</p>
                </div>
                """, unsafe_allow_html=True)

# Insights Page
elif st.session_state.current_page == "Insights" and st.session_state.data_loaded:
    st.markdown("""
    <div class="glass-card">
        <h2 style="background: linear-gradient(135deg, #fff, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">💡 Business Insights</h2>
        <p style="color: #94a3b8;">Strategic recommendations and ROI analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.target_column:
        df = st.session_state.data
        target = st.session_state.target_column
        
        total = len(df)
        churn_rate = (df[target].value_counts(normalize=True).iloc[0] * 100) if df[target].dtype == 'object' else (df[target].mean() * 100)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <p style="color: #94a3b8;">Total Customers</p>
                <p class="metric-value">{total:,}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <p style="color: #94a3b8;">Churn Rate</p>
                <p class="metric-value">{churn_rate:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                avg_value = df[numeric_cols[0]].mean()
                annual_loss = (churn_rate/100) * total * avg_value * 12
                st.markdown(f"""
                <div class="metric-card">
                    <p style="color: #94a3b8;">Annual Loss</p>
                    <p class="metric-value">${annual_loss:,.0f}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # ROI Calculator
        st.markdown("### 📊 Retention ROI Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            retention_rate = st.slider("Target Retention Rate (%)", 0, 100, 70)
        
        with col2:
            program_cost = st.number_input("Program Investment ($)", 0, 100000, 50000)
        
        customers_saved = int(total * (churn_rate/100) * (retention_rate/100))
        
        if len(numeric_cols) > 0:
            revenue_saved = customers_saved * avg_value * 12
            roi = ((revenue_saved - program_cost) / program_cost) * 100 if program_cost > 0 else 0
            
            st.markdown(f"""
            <div class="glass-card">
                <h3>Projected Impact</h3>
                <p><strong>Customers Saved:</strong> {customers_saved:,}</p>
                <p><strong>Revenue Saved:</strong> ${revenue_saved:,.0f}</p>
                <p><strong>ROI:</strong> <span style="color: {'#10b981' if roi > 0 else '#ef4444'}">{roi:.1f}%</span></p>
                <p><strong>Recommendation:</strong> {'Invest in retention program' if roi > 50 else 'Optimize program costs'}</p>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; margin-top: 2rem; border-top: 1px solid rgba(255,255,255,0.1);">
    <p style="color: #94a3b8;">🚀 ChurnIQ Enterprise | Powered by Advanced Machine Learning</p>
    <p style="color: #64748b; font-size: 0.8rem;">© 2024 | Real-time Predictive Analytics Platform</p>
</div>
""", unsafe_allow_html=True)