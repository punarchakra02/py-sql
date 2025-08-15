import streamlit as st
import os

st.title("🚂 Railway Deployment Test")

st.write("✅ Streamlit is working!")
st.write("✅ Python is working!")

# Show environment info
st.subheader("Environment Information")
st.write(f"Python version: {os.sys.version}")
st.write(f"PORT environment variable: {os.environ.get('PORT', 'Not set')}")

# Show all environment variables (for debugging)
st.subheader("Environment Variables")
env_vars = dict(os.environ)
for key, value in list(env_vars.items())[:10]:  # Show first 10 only
    if 'password' not in key.lower() and 'secret' not in key.lower():
        st.write(f"{key}: {value}")

st.write("🎉 If you see this, the deployment is working!")
