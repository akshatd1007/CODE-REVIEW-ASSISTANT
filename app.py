import streamlit as st
from huggingface_hub import InferenceClient
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Code Review Assistant",
    page_icon="🔍",
    layout="wide"
)

# Hugging Face API Configuration
HF_API_KEY = "YOURKEY"  # Replace with your actual API key

# Initialize Hugging Face Inference Client
@st.cache_resource
def get_hf_client():
    return InferenceClient(token=HF_API_KEY)

# Initialize session state for storing reviews
if 'reviews' not in st.session_state:
    st.session_state.reviews = []

def analyze_code_with_hf(code, language):
    """
    Analyze code using Hugging Face Inference API
    """
    try:
        client = get_hf_client()
        
        # Construct detailed prompt for code review
        system_message = "You are an expert code reviewer with deep knowledge of software engineering best practices, security, and performance optimization."
        
        user_message = f"""Analyze the following {language} code and provide a comprehensive review.

Code to review:
```{language}
{code}
```

Please provide a structured review covering:
1. **Code Quality Score** (0-10)
2. **Readability Analysis**: How clear and understandable is the code?
3. **Best Practices**: Does it follow language-specific conventions?
4. **Potential Bugs**: Any logical errors or edge cases not handled?
5. **Security Issues**: Any security vulnerabilities?
6. **Performance**: Any optimization opportunities?
7. **Modularity**: Is the code well-structured and modular?
8. **Specific Improvements**: List concrete suggestions with line references if possible.

Format your response clearly with headers and bullet points."""

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        # Use chat completion with auto provider selection
        response = client.chat_completion(
            messages=messages,
            model="meta-llama/Llama-3.2-3B-Instruct",
            max_tokens=2000,
            temperature=0.7,
        )
        
        return response.choices[0].message.content
            
    except Exception as e:
        error_msg = str(e)
        if "is currently loading" in error_msg:
            return "⏳ Model is currently loading. Please wait 20-30 seconds and try again."
        elif "Authorization header is invalid" in error_msg or "Invalid token" in error_msg:
            return "❌ Error: Invalid API key. Please check your Hugging Face API key in the code."
        elif "Rate limit" in error_msg or "rate limit" in error_msg:
            return "⏳ Rate limit reached. Please wait a moment and try again."
        else:
            return f"❌ Error during analysis: {error_msg}"

def save_review(filename, language, code, analysis):
    """Save review to session state"""
    review = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'filename': filename,
        'language': language,
        'code': code,
        'analysis': analysis
    }
    st.session_state.reviews.insert(0, review)
    
    # Keep only last 10 reviews
    if len(st.session_state.reviews) > 10:
        st.session_state.reviews = st.session_state.reviews[:10]

# Check if API key is configured
api_configured = HF_API_KEY != "your_huggingface_api_key_here"

# Main UI
st.title("🔍 Code Review Assistant")
st.markdown("### Automated code analysis powered by AI")

if not api_configured:
    st.error("⚠️ **API Key Not Configured!** Please update the `HF_API_KEY` variable in the code with your Hugging Face API token.")
    st.info("Get your API key from: https://huggingface.co/settings/tokens")
    st.stop()

# Sidebar for settings and stats
with st.sidebar:
    st.header("⚙️ Settings")
    
    st.success("✅ API Key Configured")
    
    st.markdown("---")
    st.markdown("### 📊 Statistics")
    st.metric("Total Reviews", len(st.session_state.reviews))
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info("""
    This tool analyzes your code for:
    - Readability
    - Best practices
    - Potential bugs
    - Security issues
    - Performance optimization
    - Code modularity
    """)
    
    st.markdown("---")
    st.markdown("### 🤖 Model Info")
    st.caption("Using: Llama-3.2-3B-Instruct")
    st.caption("Fast & efficient for code analysis")

# Main content area
tab1, tab2, tab3 = st.tabs(["📝 New Review", "📚 Review History", "📖 Guide"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Upload Code for Review")
        
        # File upload option
        uploaded_file = st.file_uploader(
            "Upload a code file",
            type=['py', 'js', 'java', 'cpp', 'c', 'go', 'rs', 'rb', 'php', 'ts', 'jsx', 'tsx', 'html', 'css'],
            help="Supported formats: Python, JavaScript, Java, C++, C, Go, Rust, Ruby, PHP, TypeScript, HTML, CSS"
        )
        
        # Manual input option
        st.markdown("**Or paste your code below:**")
        
        language = st.selectbox(
            "Programming Language",
            ["Python", "JavaScript", "TypeScript", "Java", "C++", "C", "Go", "Rust", "Ruby", "PHP", "JSX", "TSX", "HTML", "CSS"]
        )
        
        code_input = st.text_area(
            "Paste your code here",
            height=300,
            placeholder="# Paste your code here...\ndef example():\n    pass"
        )
    
    with col2:
        st.subheader("Review Options")
        
        focus_areas = st.multiselect(
            "Focus Areas",
            ["Readability", "Performance", "Security", "Best Practices", "Bug Detection"],
            default=["Readability", "Best Practices", "Bug Detection"]
        )
        
        severity_filter = st.select_slider(
            "Issue Severity Level",
            options=["Low", "Medium", "High", "Critical"],
            value="Medium"
        )
        
        st.info("💡 **Tip:** Keep code under 500 lines for best results")
    
    # Process the code
    if uploaded_file is not None:
        code_to_review = uploaded_file.read().decode('utf-8')
        filename = uploaded_file.name
        # Auto-detect language from file extension
        ext_to_lang = {
            'py': 'Python', 'js': 'JavaScript', 'java': 'Java',
            'cpp': 'C++', 'c': 'C', 'go': 'Go', 'rs': 'Rust',
            'rb': 'Ruby', 'php': 'PHP', 'ts': 'TypeScript',
            'jsx': 'JSX', 'tsx': 'TSX', 'html': 'HTML', 'css': 'CSS'
        }
        ext = filename.split('.')[-1]
        detected_language = ext_to_lang.get(ext, language)
    else:
        code_to_review = code_input
        filename = f"code.{language.lower()}"
        detected_language = language
    
    st.markdown("---")
    
    # Review button
    if st.button("🚀 Analyze Code", type="primary", use_container_width=True):
        if not code_to_review or code_to_review.strip() == "":
            st.error("⚠️ Please upload a file or paste code to review")
        else:
            with st.spinner(f"🔄 Analyzing {detected_language} code... This may take 10-30 seconds..."):
                analysis = analyze_code_with_hf(code_to_review, detected_language)
                
                if not analysis.startswith("❌") and not analysis.startswith("⏳"):
                    save_review(filename, detected_language, code_to_review, analysis)
                    st.success("✅ Code review completed!")
                    
                    # Display results
                    st.markdown("## 📋 Review Report")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("File", filename)
                    with col2:
                        st.metric("Language", detected_language)
                    with col3:
                        st.metric("Lines", len(code_to_review.split('\n')))
                    
                    st.markdown("---")
                    
                    # Display code
                    with st.expander("📄 View Code", expanded=False):
                        st.code(code_to_review, language=detected_language.lower())
                    
                    # Display analysis
                    st.markdown("### 🔍 Analysis Results")
                    st.markdown(analysis)
                    
                    # Download button
                    report = f"""# Code Review Report
**File:** {filename}
**Language:** {detected_language}
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Lines of Code:** {len(code_to_review.split('\n'))}

## Code
```{detected_language.lower()}
{code_to_review}
```

## Analysis
{analysis}
"""
                    st.download_button(
                        "📥 Download Report",
                        report,
                        file_name=f"review_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
                else:
                    st.error(analysis)
                    if "loading" in analysis.lower():
                        st.info("💡 The AI model is warming up. Please wait a moment and click 'Analyze Code' again.")

with tab2:
    st.subheader("📚 Review History")
    
    if len(st.session_state.reviews) == 0:
        st.info("No reviews yet. Start by analyzing some code in the 'New Review' tab!")
    else:
        # Add clear all button
        col1, col2 = st.columns([6, 1])
        with col2:
            if st.button("🗑️ Clear All"):
                st.session_state.reviews = []
                st.rerun()
        
        st.markdown("---")
        
        for idx, review in enumerate(st.session_state.reviews):
            with st.expander(f"📄 {review['filename']} - {review['timestamp']}", expanded=(idx == 0)):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.markdown(f"**Language:** {review['language']}")
                with col2:
                    st.markdown(f"**Date:** {review['timestamp']}")
                with col3:
                    if st.button("🗑️ Delete", key=f"del_{idx}"):
                        st.session_state.reviews.pop(idx)
                        st.rerun()
                
                st.markdown("#### Code")
                st.code(review['code'], language=review['language'].lower())
                
                st.markdown("#### Analysis")
                st.markdown(review['analysis'])
                
                # Download individual report
                report = f"""# Code Review Report
**File:** {review['filename']}
**Language:** {review['language']}
**Date:** {review['timestamp']}

## Code
```{review['language'].lower()}
{review['code']}
```

## Analysis
{review['analysis']}
"""
                st.download_button(
                    "📥 Download This Report",
                    report,
                    file_name=f"review_{review['filename']}_{review['timestamp'].replace(':', '-').replace(' ', '_')}.md",
                    mime="text/markdown",
                    key=f"download_{idx}"
                )

with tab3:
    st.subheader("📖 How to Use")
    
    st.markdown("""
    ### Getting Started
    
    1. **Configure API Key** (One-time setup)
       - Open the code file
       - Replace `your_huggingface_api_key_here` with your actual API key
       - Get your key from [Hugging Face Settings](https://huggingface.co/settings/tokens)
    
    2. **Upload or Paste Code**
       - Upload a code file (multiple languages supported)
       - Or paste your code directly in the text area
       - Select the appropriate programming language
    
    3. **Configure Review** (Optional)
       - Choose focus areas
       - Set severity level
    
    4. **Analyze**
       - Click "Analyze Code"
       - Wait 10-30 seconds for results
       - First run may take longer as model loads
    
    5. **Review Results**
       - View comprehensive analysis
       - Download report as Markdown
       - Access history in "Review History" tab
    
    ### Supported Languages
    
    - Python
    - JavaScript / TypeScript
    - Java
    - C / C++
    - Go
    - Rust
    - Ruby
    - PHP
    - JSX / TSX
    - HTML / CSS
    
    ### What Gets Analyzed
    
    ✅ **Code Quality** - Overall score and assessment  
    ✅ **Readability** - Code clarity and documentation  
    ✅ **Best Practices** - Language-specific conventions  
    ✅ **Bug Detection** - Potential errors and edge cases  
    ✅ **Security** - Vulnerability identification  
    ✅ **Performance** - Optimization opportunities  
    ✅ **Modularity** - Code structure and organization  
    
    ### Tips for Best Results
    
    - 📏 Keep code snippets under 500 lines for faster analysis
    - 💬 Include comments in your code for better context
    - 🎯 Specify the correct language for accurate analysis
    - 🔄 Review multiple small files rather than one large file
    - ⏱️ Be patient on first run - model needs to load
    
    ### Troubleshooting
    
    **"Model is loading" error:**
    - Wait 20-30 seconds and try again
    - The model needs to warm up on first use
    
    **"Invalid API key" error:**
    - Check if you replaced the placeholder key
    - Ensure token has read permissions
    - Verify token is still valid
    
    **Timeout or slow response:**
    - Code might be too long
    - Try splitting into smaller chunks
    - Check your internet connection
    
    ### Installation
    
    ```bash
    pip install streamlit huggingface_hub
    ```
    
    ### Running the App
    
    ```bash
    streamlit run app.py
    ```
    """)
    
    st.markdown("---")
    st.markdown("### 🔧 Technical Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Backend:**
        - Streamlit for UI
        - Hugging Face Hub for inference
        - In-memory storage for reviews
        """)
    
    with col2:
        st.markdown("""
        **AI Model:**
        - Llama-3.2-3B-Instruct
        - Fast inference
        - Max tokens: 2000
        """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🔍 Code Review Assistant | Powered by Hugging Face & Streamlit</p>
        <p style='font-size: 0.8em;'>Made with ❤️ for better code quality</p>
    </div>
    """,
    unsafe_allow_html=True
)
