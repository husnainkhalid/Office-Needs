import argparse
from api.app import crud_import

def main():
    parser = argparse.ArgumentParser(description="Import Excel data into SurgicalOps DB")
    parser.add_argument("--data-dir", type=str, required=True, help="Folder containing Excel files")
    parser.add_argument("--db-url", type=str, required=True, help="SQLite DB path, e.g., sqlite:///./data/surgicalops.db")
    args = parser.parse_args()

    db_path = args.db_url.replace("sqlite:///", "")
    result = crud_import.import_all(db_path, args.data_dir)
    print(f"Import done: {result['products']} products, {result['clients']} clients, "
          f"{result['client_pricing']} pricing rows, {result['stock']} stock rows.")

if __name__ == "__main__":
    main()
