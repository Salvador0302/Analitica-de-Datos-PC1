def test_imports():
    import importlib
    modules = [
        "src.main",
        "src.data_collection.scraper_example",
        "src.eda.eda_utils",
        "src.utils.logger",
    ]
    for m in modules:
        importlib.import_module(m)
