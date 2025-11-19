import os
import shutil

from block_markdown import (
     markdown_to_html_node,
     extract_title
)

dir_path_public   = "./public"
dir_path_static   = "./static"
dir_path_content  = "./content"
dir_path_template = "./template.html"

def sync_content():
    print('Copying static files...')
    copy_files(dir_path_static, dir_path_public)
    print('Generating dynamic files...')
    print(f' Using template: {dir_path_template}')
    generate_pages(dir_path_content, dir_path_template, dir_path_public)

def prepare_target_folder():
    print('Preparing target folder...')
    if os.path.exists(dir_path_public):
        print(f' Removing {dir_path_public}')
        shutil.rmtree(dir_path_public)

    os.mkdir(dir_path_public)
    print(f' Creating {dir_path_public}')

def copy_files(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    
    for source_item in os.listdir(source_dir):
        source_item_path = os.path.join(source_dir, source_item)
        target_item_path = os.path.join(target_dir, source_item)
        print(f" * {source_item_path} -> {target_item_path}")
        if os.path.isfile(source_item_path):
            shutil.copy(source_item_path, target_item_path)
        else:
            copy_files(source_item_path, target_item_path)

def generate_pages(source_dir, template_path, target_dir):
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    
    for source_item in os.listdir(source_dir):
        source_item_path = os.path.join(source_dir, source_item)
        target_item_path = os.path.join(target_dir, source_item)
        if os.path.isfile(source_item_path):
            target_filename, _ = os.path.splitext(target_item_path)
            target_item_path = target_filename + ".html"
            print(f" * {source_item_path} -> {target_item_path}")
            generate_page(source_item_path, template_path, target_item_path)
        else:
            print(f" * {source_item_path} -> {target_item_path}")
            generate_pages(source_item_path, template_path, target_item_path)

def generate_page(from_path, template_path, dest_path):
    with open(from_path, 'r') as file:
        md_content = file.read()
    with open(template_path, 'r') as file:
        template_content = file.read()
    title = extract_title(md_content)
    html_content = markdown_to_html_node(md_content).to_html()
    generated_content = template_content.replace('{{ Title }}', title).replace('{{ Content }}', html_content)
    with open(dest_path, "w") as f:
        f.write(generated_content)

