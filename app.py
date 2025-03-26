import gradio as gr
from utils import (
    fetch_articles_for_company,
    process_articles_parallel,
    comparative_analysis,
    generate_hindi_tts_bytes
)
import base64

def analyze_company(company):
    if not company.strip():
        return "⚠️ Please enter a company name.", None

    # Fetch articles and process
    articles = fetch_articles_for_company(company)
    articles = process_articles_parallel(articles)
    comparison = comparative_analysis(articles)

    final_sentiment = comparison['Overall Sentiment Conclusion']
    summary_text = f"{company} ke news coverage ke anusar overall sentiment {final_sentiment} hai."

    # Generate audio
    audio_bytes = generate_hindi_tts_bytes(summary_text)

    # Prepare text output
    text_output = f"**Overall Conclusion:** {final_sentiment}\n\n"
    text_output += f"### Comparative Analysis:\n{comparison}\n\n"

    # Add audio download option
    if audio_bytes:
        b64_audio = base64.b64encode(audio_bytes.read()).decode()
        download_link = f'<a href="data:audio/mp3;base64,{b64_audio}" download="{company}_summary.mp3">📥 Download Hindi Audio Summary</a>'
        text_output += download_link
    else:
        text_output += "\n⚠️ Audio generation failed."

    return text_output, audio_bytes if audio_bytes else None

demo = gr.Interface(
    fn=analyze_company,
    inputs=gr.Textbox(label="Enter Company Name"),
    outputs=[gr.Markdown(label="📊 Analysis Result"), gr.Audio(label="Hindi Audio Summary")],
    title="📈 Company News Summarizer & Sentiment Insights (Gradio App)",
    description="Enter a company name to fetch recent news, generate summaries, perform sentiment analysis, and get a Hindi audio summary.",
    allow_flagging="never"
)

if __name__ == "__main__":
    demo.launch()
