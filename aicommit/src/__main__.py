from .aicommit import main
from .pr_description_gen import generate_description
if __name__ == "__main__":
    main()
    print('Start generating PR description...')
    generate_description()
    print('PR description generated successfully!')
