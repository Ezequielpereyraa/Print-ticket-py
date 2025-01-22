def check_dependencies():
    dependencies = ["os", "sys", "psutil", "escpos"]
    missing_dependencies = []

    for dep in dependencies:
        try:
            __import__(dep)
        except ImportError:
            missing_dependencies.append(dep)

    if missing_dependencies:
        print("Las siguientes dependencias no están instaladas:")
        for dep in missing_dependencies:
            print(f"- {dep}")
    else:
        print("Todas las dependencias están correctamente instaladas.")

if __name__ == "__main__":
    check_dependencies()
