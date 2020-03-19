import os

def create_file(filepath):
    file_dir = os.path.dirname(filepath)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    with open(filepath, 'w', encoding='ansi') as f:
        f.write(filepath)

if __name__ == '__main__':
    problem_list = [
        '1.2-3', '2.2-3', '2.3-7', '3.1-1', '4.1-5', '4.2-3',
        '4.3-2', '4.3-9', '4.4-2', '4.5-1', '4.5-2', '4.5-4',
        '4.5-5', '6.4-2', '6.5-5', '7.1-2'
    ]

    for problem in problem_list:
        create_file('./%s/README.md' % problem)
