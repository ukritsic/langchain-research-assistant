from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from retrieval import format_docs_for_prompt

SYSTEM = """
You are a research assistant.
- Use ONLY the provided context to answer.
- Synthesis across documents; reconcile conflicts explicitly.
- Provide structured, concise findings with bullet points.
- After each key claim, cite sources like [source | p.N].
- If information is missing or uncertain, state that clearly.
"""

ANSWER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),
    (
        "human",
        (
            "Research question: {question}\n\n"
            "Context (excerpts):\n{context}\n\n"
            "Write a structured answer with headings (Findings, Evidence, Gaps),"
            " include citations like [source | p.N]."
        ),
    ),
])

def build_answer_chain(retriever):
    llm = ChatOpenAI(model="gpt-5-mini", temperature=0)
    chain = (
        {"context": retriever | format_docs_for_prompt, "question": RunnablePassthrough()}
        | ANSWER_PROMPT
        | llm
        | StrOutputParser()
    )
    return chain