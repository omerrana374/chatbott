from rest_framework.decorators import api_view
from rest_framework.response import Response
from teacher_bot.chat_llm import call_llm
from teacher_bot.load_data import load_all_data
from teacher_bot.retriever import Retriever
from rest_framework import status

retriever = Retriever()


@api_view(["POST"])
def chat(request):
    message = request.data.get("message", "")
    return Response({"response": f"Bot received: {message}"})


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


@api_view(["POST"])
def chat(request):
    query = request.data.get("query", "")

    if not query:
        return Response({"error": "query is required"}, status=400)

    retrieved = retriever.search(query, top_k=3)

    retrieved_context = ""
    for idx, item in enumerate(retrieved):
        retrieved_context += (
            f"Case {idx+1}:\n"
            f"Problem: {item['text']}\n"
            f"Solution: {item['solution']}\n\n"
        )

    prompt = f"""
    You are a support chatbot for teachers.

    User query:
    {query}

    Here are the top 3 relevant solutions from the knowledge base:
    {retrieved_context}

    Write a single helpful answer using ONLY the information above.
    Do not invent new information. Combine key points succinctly.
    """

    final_answer = call_llm(prompt)

    return Response(
        {"query": query, "final_answer": final_answer, "retrieved": retrieved}
    )
