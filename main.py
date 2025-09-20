import argparse

from cli import cmd_ingest, cmd_ask, cmd_shell

def main():
    parser = argparse.ArgumentParser(description="Multi-Document Research Assistant (LangChain)")
    sub = parser.add_subparsers(required=True)

    # ingest
    p_ing = sub.add_parser("ingest", help="Ingest local docs and optional URLs")
    p_ing.add_argument("--urls", type=str, default="", help="Comma-separated URLs to fetch and index")
    p_ing.set_defaults(func=cmd_ingest)

    # single shot
    p_ask = sub.add_parser("ask", help="Ask a research question")
    p_ask.add_argument("question", type=str, help="Your research question")
    p_ask.add_argument("--k", type=int, default=6, help="Top-k documents to retrieve")
    p_ask.add_argument("--no-multiquery", action="store_true", help="Disable multi-query expansion")
    p_ask.add_argument("--reingest", action="store_true", help="Rebuild index before asking")
    p_ask.add_argument("--urls", type=str, default="", help="Comma-separated URLs to fetch and index")
    p_ask.set_defaults(func=cmd_ask)

    # shell (interactive)
    p_shell = sub.add_parser("shell", help="Interactive shell to ask multiple research questions")
    p_shell.add_argument("--k", type=int, default=6, help="Top-k documents to retrieve")
    p_shell.add_argument("--no-multiquery", action="store_true", help="Disable multi-query expansion")
    p_shell.add_argument("--reingest", action="store_true", help="Rebuild index before starting")
    p_shell.add_argument("--urls", type=str, default="", help="Comma-separated URLs to fetch and index")
    p_shell.set_defaults(func=cmd_shell)

    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
    else:
        args.func(args)

if __name__ == '__main__':
    main()