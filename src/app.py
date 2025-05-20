import streamlit as st
import time
import streamlit.components.v1 as components
import random
from services.gemini_teste_perfil import analisar_respostas

def read_html():
    with open("./src/static/index.html") as f:
        return f.read()

def main():
    st.set_page_config(
        page_title="Perfil de Investimento",
        initial_sidebar_state="expanded",
        page_icon="🏦",
        layout="centered",
    )

    questions = [
        "Como você se sente em relação a investimentos com retorno demorado?",
        "Qual sua reação a possíveis perdas temporárias em seus investimentos?",
        "Você se sente atraído por promoções e descontos?",
        "Como você se sente em relação a correr riscos para obter possíveis ganhos maiores?",
        "O quanto você valoriza manter seu dinheiro seguro, mesmo que isso signifique retornos menores?",
        "Como você reage quando vê o valor dos seus investimentos caindo?",
        "O que você acha de investimentos que oferecem retornos rápidos, mesmo que sejam mais arriscados?",
        "Como você se sente sobre acompanhar o mercado financeiro e tomar decisões ativas sobre seus investimentos?",
        "O que você pensa sobre investir em algo considerado arriscado, como ações ou criptomoedas?",
        "Como você se sente sobre diversificar seus investimentos em diferentes tipos de ativos?",
        "Ter uma renda estável e previsível ao em vez da chance de ganhos altos te atrai?",
        "Deixar seus investimentos a longo prazo sem ficar verificando frequentemente é algo que você gosta?",
        "Você gosta da ideia dos seus investimentos serem focados em proteger seu dinheiro da inflação?",
        "Guiar suas escolhas de investimento com um objetivo financeiro de longo prazo, como aposentadoria, te interessa?",
        "Buscar orientação profissional antes de tomar decisões de investimento te interessa?",
        "A ideia de vender rapidamente seu investimento quando ele perde valor te agrada?",
        "Ter liquidez (acesso rápido ao dinheiro) é mais importante para você do que potenciais ganhos futuros?"
    ]

    col1, col2 = st.columns([1, 7])
    with col2:
        st.markdown("<h1 style='color: #f08671;'>Descubra seu Perfil de Investimento</h1>", unsafe_allow_html=True)
    with col1:
        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
        st.markdown("<h1 style='color: #f08671;'>💰</h1>", unsafe_allow_html=True)
    st.markdown(
    f"Responda a algumas perguntas rápidas e descubra, **com o apoio da Inteligência Artificial**, qual o seu **perfil de investimento**. O teste é composto por **{len(questions)} perguntas** e pode ser realizado quantas vezes você quiser! **Vamos começar?**")
    st.write("")

    if 'test_started' not in st.session_state:
        st.session_state.test_started = False
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.session_state.randomized_questions = random.sample(questions, len(questions))

    if not st.session_state.test_started:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("Iniciar o teste", use_container_width=True, type="primary"):
                st.session_state.test_started = True
                st.rerun()
    else:
        progress = st.session_state.current_question / len(questions)
        st.progress(progress)
        
        if st.session_state.current_question < len(questions):
            question = st.session_state.randomized_questions[st.session_state.current_question]
            st.write(f"### {question}")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            options = {
                "Detesto": ":material/sentiment_sad:",
                "Prefiro evitar": ":material/sentiment_dissatisfied:",
                "Indiferente": ":material/sentiment_neutral:",
                "Gosto": ":material/sentiment_satisfied:",
                "Amo": ":material/sentiment_very_satisfied:"
            }
            
            selected = None
            for i, (text, emoji) in enumerate(options.items()):
                with [col1, col2, col3, col4, col5][i]:
                    if st.button(f"{text}\n\n{emoji}", key=f"q_{st.session_state.current_question}_{i}", use_container_width=True, type="secondary"):
                        st.session_state.answers[question] = text
                        st.session_state.current_question += 1
                        st.rerun()
                        
        else:
            st.success("Teste concluído! Analisando suas respostas...")
            
            formatted_answers = "\n".join([f"{q}: {a}" for q, a in st.session_state.answers.items()])
            
            with st.status("Gerando resposta...", expanded=True):
                st.write("Analisando respostas...")
                time.sleep(3)
                st.write("Procurando investimentos...")
                time.sleep(3)
                analysis = analisar_respostas(formatted_answers)
                st.write("Formatando resposta...")
                time.sleep(3)
                
            with st.container(border=True):
                st.markdown("### 💰 Sua Análise de Perfil de Investimento")
                st.markdown(analysis)
            
            if st.button("Fazer o teste novamente", type="primary", use_container_width=True):
                st.session_state.test_started = False
                st.session_state.current_question = 0
                st.session_state.answers = {}
                st.session_state.randomized_questions = random.sample(questions, len(questions))
                st.rerun()

    components.html(
        read_html(),
        height=0,
        width=0,
    )

if __name__ == "__main__":
    main()
