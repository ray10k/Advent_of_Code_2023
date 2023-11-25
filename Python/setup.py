from pathlib import Path
from shutil import rmtree



if __name__ == "__main__":
    template = ""
    template_path = Path(__file__).parent / "day_template.txt"
    with open(template_path) as template_file:
        template = template_file.read()
    
    if input("About to delete the 'days' directory and rebuild clean. Continue? (y/n)")[0].lower() == 'y':
        days_directory = Path(__file__).parent / "src" / "days"
        if days_directory.exists():
            rmtree(days_directory)
        days_directory.mkdir()
        for day in range(1,26):
            day_fmt = f"{day:0>2}"
            with (days_directory / f"day{day_fmt}.py").open("w") as day_file:
                day_file.write(template.replace(">day_number<",day_fmt))
        print("Setup complete.")
    else:
        print("Closing.")