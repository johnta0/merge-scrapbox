from pathlib import Path
import json


def read_json(path: Path) -> dict:
    """Read JSON file and return as dictionary
    Args:
        path (Path): Path to JSON file
    Returns:
        dict: Loaded JSON data
    """
    return json.loads(path.read_text())


def write_json(d: dict, output_path: Path):
    """Write dictionary to JSON file
    Args:
        d (dict): Dictionary to write to JSON
        output_path (Path): Path to output JSON file
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(d, ensure_ascii=False, indent=2))


def edit(d: dict) -> dict:
    """
    どのように編集するか？
    - プロフィールページは消す
    - 全てに project 名の タグを付ける
    - 元は <project 名> のコンテンツであったことを明記する

    最終的に必要なのは pages プロパティのみ
    """

    def _filter_profile_pages(pages: list, excluded_titles: list) -> list:
        """Filter out profile and help pages from the page list
        Args:
            pages (list): List of pages
            excluded_titles (list): List of page titles to exclude
        Returns:
            list: Filtered list of pages
        """
        return [page for page in pages if page['title'] not in excluded_titles]


    project_name = d["name"]
    
    pages: list = d["pages"]
    
    excluded_titles = ['Scrapboxの使い方', 'j0hnta0', 'Get started'] # REPLACE_ME
    pages[:] = _filter_profile_pages(pages, excluded_titles=excluded_titles)
    
    for page in pages:
        lines: list = page['lines']
        lines.insert(1, f'このページは元々 「[{project_name}]」プロジェクトにあったものをマージしたものです')
        lines.insert(1, f'#{project_name}') # caution: list.insert() は O(n) なので効率的ではない

    ret_dict = {"pages": pages}

    return ret_dict


def get_output_path(p: Path) -> Path:
    return Path(str(p).replace("exported", "to_import", 1))


def main():
    EXPORTED_JSON_FILES_PATHS = list(Path("exported").glob("**/*.json")) # REPLACE_ME
    # EXPORTED_JSON_FILES_PATHS = [Path('exported/private/cafewifi.json')]

    for path in EXPORTED_JSON_FILES_PATHS:
        # read json as dict
        d = read_json(path)

        # edit exported file
        edited_d = edit(d)

        # write file to to_import folder
        output_path = get_output_path(path)
        write_json(edited_d, output_path)


if __name__ == "__main__":
    main()
