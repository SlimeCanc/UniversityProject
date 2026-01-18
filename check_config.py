import os
from dotenv import load_dotenv


def check_environment():
    print("🔍 Checking environment configuration...")
    print("=" * 50)

    env_path = '.env'
    if os.path.exists(env_path):
        print(f"✅ .env file found")
        load_dotenv()
    else:
        print("❌ .env file not found")
        return False

    required_vars = {
        'SECRET_KEY': os.environ.get('SECRET_KEY'),
        'DATABASE_URL': os.environ.get('DATABASE_URL')
    }

    all_good = True
    for var_name, var_value in required_vars.items():
        if var_value:
            status = "✅ OK"
        else:
            status = "❌ MISSING"
            all_good = False
        print(f"{var_name}: {status}")

    print("=" * 50)

    if all_good:
        print("🎉 Configuration is ready!")
    else:
        print("⚠️ Please check your configuration")

    return all_good


if __name__ == '__main__':
    check_environment()