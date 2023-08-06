import argparse


def parse_args():
    parser = argparse.ArgumentParser("appname")
    subparsers = parser.add_subparsers(dest="command")

    generate_parser = subparsers.add_parser(
        "generate", help="generate random app names"
    )
    generate_parser.add_argument("number", type=int, help="number names to generate")
    generate_parser.add_argument(
        "--min-length", type=int, default=4, help="minimum length of names to generates"
    )
    generate_parser.add_argument(
        "--max-length", type=int, default=7, help="maximum length of names to generates"
    )
    generate_parser.add_argument(
        "--tlds",
        type=str,
        default="com,fr,io",
        help="comma separated list of TLDs without spaces (e.g: com,fr)",
    )
    generate_parser.add_argument(
        "--exclusive",
        action="store_true",
        default=False,
        help="Decide wether domain should be available for all TLDs",
    )
    generate_parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Name of the file were output will be stored",
    )

    args = parser.parse_args()
    if getattr(args, "command", None) is None:
        parser.print_help()
        exit(0)
    return args


def main():
    args = parse_args()

    if args.command == "generate":
        from .generator import RandomNameGenerator

        generator = RandomNameGenerator(
            min_length=args.min_length,
            max_length=args.max_length,
            exclusive=args.exclusive,
            tlds=args.tlds.split(","),
        )

        generator.generate(
            args.number, output=args.output
        )


if __name__ == "__main__":
    main()
