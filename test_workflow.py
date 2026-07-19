from workflow.assistant_graph import assistant_graph


def main():

    query = {
        "query": "Latest AI news"
    }

    print("\n========== USER QUERY ==========\n")
    print(query["query"])


    response = assistant_graph.invoke(
        query
    )


    print("\n========== WORKFLOW RESPONSE ==========\n")
    print(response)


    print("\n========== FINAL ANSWER ==========\n")

    print(
        response.get(
            "answer",
            "No answer generated"
        )
    )


if __name__ == "__main__":

    main()