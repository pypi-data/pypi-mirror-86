from git import Repo

def write_md(commit='HEAD'):
    commit_message = get_commit_message()
    filename = convert_commit_message_to_filename(commit_message)
    f = open(filename, 'w')

    repo = Repo('.')
    raw_diff = repo.git.diff('{}^'.format(commit), '{}'.format(commit))
    diff_info = get_diff_info(raw_diff)
    f.write('# {}'.format(get_commit_message()))
    f.write('\n')
    for diff in diff_info:
        
        file_contents = read_file(diff['filename'])
        f.write('Update the contents of `{}` with the following code:'.format(diff['filename']))
        f.write('\n')
        f.write('```javascript')
        f.write('\n')
        for line in file_contents.split('\n'):
            f.write(line)
            f.write('\n')
        f.write('```')
        f.write('\n')
        
        f.write('*Changes made to `{}`*:'.format(diff['filename']))
        f.write('\n')
        f.write('```diff')
        f.write('\n')
        
        for line in diff['content']:
            f.write(line)
            f.write('\n')
        f.write('```')
        f.write('\n')

    f.close()

def convert_commit_message_to_filename(commit_message):
    filename = ''
    found_colon = False
    for i in range(len(commit_message)):
        curr = commit_message[i]
        if curr == ' ' and commit_message[i-1] == ':':
            filename += '_'
        elif curr == ' ' and not found_colon:
            pass
        elif curr == ' ' and found_colon:
            filename += '-'
        elif curr == ':':
            found_colon = True
        else:
            filename += curr
    return '{}.md'.format(filename)

def print_diff(commit='HEAD'):
    repo = Repo('.')
    raw_diff = repo.git.diff('{}^'.format(commit), '{}'.format(commit))
    diff_info = get_diff_info(raw_diff)
    for diff in diff_info:
        print('# {}'.format(get_commit_message()))
        file_contents = read_file(diff['filename'])
        print('Update the contents of `{}` with the following code:'.format(diff['filename']))
        print('```javascript')
        for line in file_contents.split('\n'):
            print(line)
        print('```')
        
        print('*Changes made to `{}`*:'.format(diff['filename']))
        print('```diff')
        
        for line in diff['content']:
            print(line)
        print('```')

def get_commit_message():
    repo = Repo('.')
    raw_message = list(repo.iter_commits('master'))[0].message
    cleaned_message = _remove_newline_character(raw_message)
    
    return cleaned_message

def _remove_newline_character(string):
    return string[:-1]

def read_file(path):
    filepath = '{}'.format(path)
    file = open(filepath, 'r')
    contents = file.read()
    file.close()
    
    return contents

def get_diff_info(raw_diff):
    contents = clean_diff(raw_diff)
    raw_filename_lines = _get_filename_lines(raw_diff)
    filenames = clean_filename_lines(raw_filename_lines)

    filename_contents = zip(filenames, contents)
    diff_info = [{'filename': filename, 'content':content} for filename, content in filename_contents]

    return diff_info

def clean_filename_lines(raw_filename_lines):
    filenames = []

    for line in raw_filename_lines:
        cleaned = line.split(' ')[-1][2:]
        filenames.append(cleaned)
    
    return filenames

def _get_filename_lines(raw_diff):
    lines = raw_diff.split('\n')

    return [line for line in lines if line[:10]=='diff --git']

def clean_diff(raw_diff):
    lines = raw_diff.split('\n')
    
    diff_bounds = get_diff_bounds(lines)
    
    all_lines = get_all_lines(lines, diff_bounds)
    all_filtered_lines = []
    for line_list in all_lines:
        curr_filtered_line = filter_lines(line_list, ['\ No newline at end of file', ''])
        curr_filtered_line_multi = clean_multi_part_diffs(curr_filtered_line)
        all_filtered_lines.append(curr_filtered_line)
    
    return all_filtered_lines

def clean_multi_part_diffs(all_filtered_lines):
    for i in range(len(all_filtered_lines)):
        curr_line = all_filtered_lines[i]
        if curr_line[:2] == '@@':
            all_filtered_lines[i] = '...'
    return all_filtered_lines

def filter_lines(lines, exclude):
    return [line for line in lines if line not in exclude]

def get_start_diff_line_number(lines):
    for i in range(len(lines)):
        curr_line = lines[i]
        if curr_line and curr_line[0] == '@':
            return i + 1
    return -1

def get_start_diff_line_numbers(lines):
    line_numbers = []
    for i in range(len(lines)):
        curr_line = lines[i]
        if curr_line and curr_line[0] == '@':
            line_numbers.append(i+1)
    return line_numbers

def get_end_diff_line_numbers(lines):
    line_numbers = []
    for i in range(len(lines)):
        curr_line = lines[i]
        if curr_line and curr_line[:4] == 'diff' and i != 0:
            line_numbers.append(i-1)

    line_numbers.append(len(lines)-1)

    return line_numbers

def get_diff_bounds(lines):
    start_lines = get_start_diff_line_numbers(lines)
    end_lines = get_end_diff_line_numbers(lines)
    diff_bounds = zip(start_lines, end_lines)
    return diff_bounds

def get_line_within_bounds(lines, first, last):
    return lines[first:last]

def get_all_lines(lines, diff_bound_pairs):
    all_lines = []
    for first, last in diff_bound_pairs:
        curr_line = get_line_within_bounds(lines, first, last+1)
        all_lines.append(curr_line)
    return all_lines

