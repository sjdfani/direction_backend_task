import subprocess


def run_makemigrations():
    subprocess.run(
        ('docker-compose', 'run', 'web', 'python', 'manage.py', 'makemigrations'))


def run_migrate():
    subprocess.run(
        ('docker-compose', 'run', 'web', 'python', 'manage.py', 'migrate'))


def run_createsuperuser():
    subprocess.run(
        ('docker-compose', 'run', 'web', 'python', 'manage.py', 'createsuperuser'))


def run_startapp(app_name: str):
    subprocess.run(
        ('docker-compose', 'run', 'web', 'python', 'manage.py', 'startapp', app_name))


def run_docker_build():
    subprocess.run(('docker-compose', 'build'))


def run_docker_up():
    subprocess.run(('docker-compose', 'up'))


def run_docker_build_up():
    subprocess.run(('docker-compose', 'up', '--build'))


def main():
    print("\n")
    print("Choose a command to run:")
    print("1. Django Makemigrations")
    print("2. Django Migrate")
    print("3. Django Createsuperuser")
    print("4. Django StartApp")
    print("5. Docker Build")
    print("6. Docker Up")
    print("7. Docker Build Then Up")
    choice = input("Enter your choice: ")
    print("\n")

    if choice == "1":
        run_makemigrations()
    elif choice == "2":
        run_migrate()
    elif choice == "3":
        run_createsuperuser()
    elif choice == "4":
        app_name = input("Enter app name: ")
        run_startapp(app_name)
    elif choice == "5":
        run_docker_build()
    elif choice == "6":
        run_docker_up()
    elif choice == "7":
        run_docker_build_up()
    else:
        print("Invalid choice. Exiting.")


if __name__ == "__main__":
    main()
