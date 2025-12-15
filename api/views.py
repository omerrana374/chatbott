from rest_framework.decorators import api_view
from rest_framework.response import Response
from teacher_bot.chat_llm import call_llm
from teacher_bot.load_data import load_all_data
from teacher_bot.retriever import Retriever
from rest_framework import status
from teacher_bot.doc_loader import load_all_docs
from teacher_bot.vector_store import add_to_index
from django.views.decorators.csrf import csrf_exempt

retriever = Retriever()


@api_view(["GET"])
def test_data_view(request):
    data = load_all_data()
    return Response({"count": len(data), "sample": data[:2]})


@api_view(["POST"])
def retrieve_answer(request):
    """
    Input:  { "query": "teacher cannot attempt exam" }
    Output: top semantic matches with solutions
    """
    query = request.data.get("query", "")
    if not query:
        return Response(
            {"error": "query is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    results = retriever.search(query, top_k=3)

    return Response({"query": query, "results": results})


@csrf_exempt
@api_view(["POST"])
def chat(request):
    query = request.data.get("query", "")

    if not query:
        return Response({"error": "query is required"}, status=400)

    retrieved = retriever.search(query, top_k=3)
    threshold = 0.5

    relevant = [r for r in retrieved if r["distance"] < threshold]

    if len(relevant) == 0:
        return Response(
            {
                "query": query,
                "final_answer": "I’m not finding a clear answer to this in my current knowledge base. Please contact support for the most accurate information.",
                "retrieved": retrieved,
            }
        )

    retrieved_context = ""
    for idx, item in enumerate(relevant):
        retrieved_context += (
            f"Case {idx+1}:\n"
            f"Problem: {item['text']}\n"
            f"Solution: {item['solution']}\n\n"
        )

    prompt = f"""
    You are a support chatbot for teachers.

    User query:
    {query}

    Relevant solutions from the knowledge base:
    {retrieved_context}

    Rules:
    - Answer ONLY using the information provided above.
    - If the information does not directly answer the user query, say you do not have enough information.
    - Do NOT infer, guess, or generalize beyond the text.
    - Keep the answer short and clear.
    """

    final_answer = call_llm(prompt)

    return Response(
        {"query": query, "final_answer": final_answer, "retrieved": retrieved}
    )


@api_view(["POST"])
def upload_docs(request):
    """
    Reads all files from teacher_bot/docs/ and adds them to the FAISS index.
    """
    docs = load_all_docs()

    if not docs:
        return Response(
            {"error": "No docs found in teacher_bot/docs/"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    for doc in docs:
        add_to_index(doc["text"], source=doc["source"])

    return Response({"message": f"{len(docs)} documents embedded and added to index."})
