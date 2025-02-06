import streamlit as st
import google.generativeai as genai

def get_gemini_response(prompt, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3
            )
        )
        return response.text
    except Exception as e:
        return f"Erro na API: {str(e)}"

def main():
    st.sidebar.title("Navegação")
    page = st.sidebar.radio("Menu", ["⚙️ Configuração", "📊 Análise"])
    
    if page == "⚙️ Configuração":
        st.header("Configuração do Google Gemini")
        st.markdown("""
        **Guia de Configuração:**
        1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Crie sua API Key
        3. Cole a chave abaixo:
        """)
        
        api_key = st.text_input("Chave API Gemini:", type="password")
        if api_key:
            st.session_state.gemini_api_key = api_key
            st.success("Chave configurada com sucesso!")
            
    elif page == "📊 Análise":
        st.header("Análise de Documentos")
        if 'gemini_api_key' not in st.session_state:
            st.error("Configure sua chave API na página de Configuração!")
            return
            
        user_input = st.text_area("Cole seu texto:", height=300)
        if st.button("Analisar"):
            with st.spinner("Processando..."):
                response = get_gemini_response(
                    f"Analise este documento em português e destaque:\n"
                    f"- Dados importantes\n- Possíveis erros\n- Valores relevantes\n\n{user_input}",
                    st.session_state.gemini_api_key
                )
                st.subheader("Resultado:")
                st.write(response)

if __name__ == "__main__":
    main()
