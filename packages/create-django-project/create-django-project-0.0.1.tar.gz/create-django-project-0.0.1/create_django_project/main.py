from ._parser import args
from .config import ProjectSetup


def main():
    project_setup = ProjectSetup(args)
    project_setup.execute()


if __name__ == "__main__":
    main()
