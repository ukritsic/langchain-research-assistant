from ingestion import ingest
from retrieval import build_retriever
from answer import build_answer_chain


def cmd_ingest(args):
    urls = args.urls.split(",") if args.urls else []
    ingest(urls)

def cmd_ask(args):
    if args.reingest:
        urls = args.urls.split(",") if args.urls else []
        ingest(urls)
    retriever = build_retriever(k=5, use_multi_query=not args.no_multiquery)
    chain = build_answer_chain(retriever)
    print("\n=== Answer ===\n")
    print(chain.invoke(args.question))

def cmd_shell(args):
    """Interactive CLI for asking multiple research questions.
    Commands (prefix with :)
    :help Show commands
    :quit / :q / :exit Exit
    :k <int> Set top-k and rebuild retriever
    :multi <on|off> Toggle multi-query expansion and rebuild
    :reingest Rebuild the index (uses current --urls)
    :urls <csv> Set URLs to (re)ingest on :reingest
    :show Show current settings
    """

    urls = args.urls or ""
    if args.reingest:
        ingest(urls.split(",") if urls else None)

    current_k = args.k
    use_multiquery = not args.no_multiquery

    def rebuild():
        nonlocal retriever, chain
        retriever = build_retriever(k=current_k, use_multi_query=use_multiquery)
        chain = build_answer_chain(retriever)

    retriever = None
    chain = None
    rebuild()

    print("Multi-Document Research Assistant — Interactive Shell")
    print("Type a question, or :help for commands.")

    while True:
        try:
            q = input("ask (:help for cmds) > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("Stop agent")
            break

        if not q:
            continue

        if q.startswith(':'):
            parts = q.split()
            cmd = parts[0][1:].lower()

            if cmd in {"quit", "q", "exit"}:
                break
            elif cmd == "help":
                print(cmd_shell.__doc__)
            elif cmd == "k" and len(parts) >= 2:
                try:
                    current_k = int(parts[1])
                    rebuild()
                    print(f"set k={current_k}")
                except ValueError:
                    print("invalid k; must be an integer")
            elif cmd in {"multi", "mq"} and len(parts) >= 2:
                val = parts[1].lower()
                use_multiquery = val in {"on", "true", "1", "yes"}
                rebuild()
                print(f"multi-query={'on' if use_multiquery else 'off'}")
            elif cmd == "reingest":
                ingest(urls.split(",") if urls else None)
                rebuild()
                print("reingested and retriever rebuilt")
            elif cmd == "urls":
                if len(parts) >= 2:
                    urls = " ".join(parts[1:]).strip()
                    print(f"set urls={urls}")
                else:
                    print(f"urls: {urls or '(none)'}")
            elif cmd == "show":
                print(f"k={current_k}, multi-query={'on' if use_multiquery else 'off'}, urls={urls or '(none)'}")
            else:
                print("unknown command. type :help")
            continue

        print(chain.invoke(q))