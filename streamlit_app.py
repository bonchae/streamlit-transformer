import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="Self-Attention Demo",
    page_icon="🧠",
    layout="wide"
)

# Lightweight CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .word-box {
        background-color: #f0f2f6;
        border: 2px solid #ddd;
        border-radius: 8px;
        padding: 8px 12px;
        margin: 3px;
        display: inline-block;
        font-weight: bold;
        font-size: 14px;
    }
    .selected-word {
        background-color: #ff6b6b;
        color: white;
        border-color: #ff4757;
    }
    .attending-word {
        background-color: #4ecdc4;
        color: white;
        border-color: #26d0ce;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# Simplified data - no complex caching
EXAMPLES = {
    "Business": {
        "words": ["Our", "company", "reported", "strong", "quarterly", "profits", "and", "the", "stock", "price", "surged"],
        "attention": {
            "stock": ["company", "profits", "surged"],
            "profits": ["company", "quarterly", "strong"],
            "surged": ["profits", "stock", "strong"],
            "company": ["Our", "profits", "stock"]
        }
    },
    "Technology": {
        "words": ["The", "new", "AI", "model", "processes", "language", "better", "than", "previous", "versions"],
        "attention": {
            "model": ["AI", "new", "processes"],
            "processes": ["model", "language", "AI"],
            "language": ["processes", "model", "better"],
            "AI": ["model", "new", "processes"]
        }
    }
}

def create_simple_heatmap(words, selected_word, attention_dict):
    """Create a simple attention heatmap"""
    n = len(words)
    matrix = np.full((n, n), 0.1)  # Base attention
    
    # Set diagonal (self-attention) to 1.0
    np.fill_diagonal(matrix, 1.0)
    
    # Fill attention scores
    if selected_word.lower() in attention_dict:
        selected_idx = words.index(selected_word)
        for target_word in attention_dict[selected_word.lower()]:
            if target_word in words:
                target_idx = words.index(target_word)
                matrix[selected_idx][target_idx] = 0.8
    
    fig = px.imshow(
        matrix,
        x=words,
        y=words,
        color_continuous_scale="Reds",
        title=f"Attention Pattern for '{selected_word}'"
    )
    
    fig.update_layout(height=400, width=500)
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">🧠 Self-Attention Demo</h1>', unsafe_allow_html=True)
    st.markdown("**Understand how AI processes language context**")
    
    # Simple sidebar
    st.sidebar.header("🎮 Controls")
    
    selected_example = st.sidebar.selectbox("Choose Example:", list(EXAMPLES.keys()))
    
    # Get data
    current_data = EXAMPLES[selected_example]
    words = current_data["words"]
    attention_dict = current_data["attention"]
    
    # Word selection
    available_words = [w for w in words if w.lower() in attention_dict]
    selected_word = st.sidebar.selectbox("Select Word:", available_words)
    
    # Main content
    st.subheader("📝 Interactive Sentence")
    
    # Display sentence
    sentence_html = ""
    attending_words = attention_dict.get(selected_word.lower(), [])
    
    for word in words:
        if word == selected_word:
            css_class = "word-box selected-word"
        elif word in attending_words:
            css_class = "word-box attending-word"
        else:
            css_class = "word-box"
        sentence_html += f'<span class="{css_class}">{word}</span> '
    
    st.markdown(sentence_html, unsafe_allow_html=True)
    
    # Explanation
    if attending_words:
        st.markdown(f"""
        <div class="insight-box">
        💡 <strong>"{selected_word}"</strong> pays attention to: <strong>{', '.join(attending_words)}</strong><br>
        These words provide crucial context for understanding "{selected_word}" in this sentence.
        </div>
        """, unsafe_allow_html=True)
    
    # Simple visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔥 Attention Heatmap")
        try:
            fig = create_simple_heatmap(words, selected_word, attention_dict)
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Visualization error: {e}")
            st.info("The demo is working, just visualization issues.")
    
    with col2:
        st.subheader("📊 Attention List")
        if attending_words:
            for word in attending_words:
                st.write(f"• **{word}** - High attention")
        else:
            st.write("No strong attention patterns for this word.")
    
    # Business context
    st.subheader("💼 Why This Matters")
    st.markdown("""
    **Self-attention is the breakthrough behind ChatGPT, BERT, and modern AI:**
    
    - 🚀 **Parallel Processing**: All words analyzed simultaneously
    - 🎯 **Long-range Connections**: Links words across entire documents  
    - 💡 **Context Understanding**: Knows "stock surged" relates to "company profits"
    - 🔧 **Business Applications**: Customer service, document analysis, translation
    """)
    
    # Simple explanation
    with st.expander("🤔 How does this work?"):
        st.markdown("""
        **The Simple Version:**
        1. Each word looks at every other word
        2. Calculates how "relevant" each word is
        3. Focuses more on highly relevant words
        4. Combines information based on relevance scores
        
        **Why it's powerful:**
        - No information loss over long distances
        - Finds relationships humans might miss
        - Processes everything in parallel (fast!)
        """)

if __name__ == "__main__":
    main()
