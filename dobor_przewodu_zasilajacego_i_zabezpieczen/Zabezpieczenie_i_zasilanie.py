import argparse

def main():
    parser = argparse.ArgumentParser(description="Program z argumentami")
    parser.add_argument("--GUI", type=int, choices=[0, 1], default=0, help="Włącz (1) lub wyłącz (0) GUI")
    parser.add_argument("--verbose", type=int, choices=[0, 1], default=0, help="Włącz tryb verbose (1) lub wyłącz (0)")
    parser.add_argument("--count", type=int, default=1, help="Ilość powtórzeń")
    parser.add_argument("--moc", type=int, default=1, help="Moc urzadzenia")

    args = parser.parse_args()

    if args.GUI:
        print("GUI jest WŁĄCZONE")
    else:
        print("GUI jest WYŁĄCZONE")

    if args.verbose:
        print("Tryb verbose jest WŁĄCZONY")

    print(f"Ilość powtórzeń: {args.count}")

if __name__ == "__main__":
    main()