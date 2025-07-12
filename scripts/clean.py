"""
Clean up temporary files and cache
"""

import os
import shutil
import glob

def clean_cache():
    """Remove Python cache files"""
    print("Cleaning Python cache files...")
    
    # Remove __pycache__ directories
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                cache_path = os.path.join(root, dir_name)
                print(f"Removing: {cache_path}")
                shutil.rmtree(cache_path)
    
    # Remove .pyc files
    pyc_files = glob.glob('**/*.pyc', recursive=True)
    for pyc_file in pyc_files:
        print(f"Removing: {pyc_file}")
        os.remove(pyc_file)

def clean_build():
    """Remove build artifacts"""
    print("Cleaning build artifacts...")
    
    build_dirs = ['build', 'dist', '*.egg-info', 'src/financial_data_fetcher.egg-info']
    for pattern in build_dirs:
        for path in glob.glob(pattern):
            if os.path.isdir(path):
                print(f"Removing directory: {path}")
                shutil.rmtree(path)
            else:
                print(f"Removing file: {path}")
                os.remove(path)

def clean_test():
    """Remove test artifacts"""
    print("Cleaning test artifacts...")
    
    test_dirs = ['.pytest_cache', '.coverage', 'htmlcov']
    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            print(f"Removing: {test_dir}")
            if os.path.isdir(test_dir):
                shutil.rmtree(test_dir)
            else:
                os.remove(test_dir)

def clean_logs():
    """Remove log files"""
    print("Cleaning log files...")
    
    log_files = glob.glob('**/*.log', recursive=True)
    for log_file in log_files:
        print(f"Removing: {log_file}")
        os.remove(log_file)

def clean_temp_data():
    """Remove temporary data files"""
    print("Cleaning temporary data files...")
    
    temp_patterns = [
        'data/*.json',
        'data/*.csv',
        'data/*.db',
        '*.tmp',
        '*.temp',
        'demo_financial_data.json'
    ]
    
    for pattern in temp_patterns:
        for file_path in glob.glob(pattern):
            print(f"Removing: {file_path}")
            os.remove(file_path)

def main():
    """Main cleanup function"""
    print("=== FINANCIAL DATA FETCHER CLEANUP ===\n")
    
    try:
        clean_cache()
        print()
        
        clean_build()
        print()
        
        clean_test()
        print()
        
        clean_logs()
        print()
        
        clean_temp_data()
        print()
        
        print("✅ Cleanup completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
