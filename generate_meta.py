#!/usr/bin/env python3
"""
CTCMD模块信息生成脚本
用于自动扫描所有latest版本包，提取版本和依赖信息，生成meta.json文件
"""

import json
import os
import zipfile
import tempfile
import shutil
from pathlib import Path
from datetime import datetime


def find_latest_packages(base_dir):
    """查找所有latest版本包"""
    latest_packages = []
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path):
            for file in os.listdir(item_path):
                if file.endswith('_latest.zip'):
                    latest_packages.append({
                        'name': item,
                        'path': os.path.join(item_path, file)
                    })
    return latest_packages


def extract_package(zip_path, extract_to):
    """解压包到指定目录"""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def read_module_info(module_dir, module_name):
    """读取模块的depends.txt和version.txt文件"""
    module_info = {
        'version': '未指定',
        'latest': '未指定',
        'depends': [],
        'path': f'{module_name}/{module_name}',
        'files': []
    }
    
    # 查找模块子目录
    module_subdir = os.path.join(module_dir, module_name)
    if not os.path.exists(module_subdir):
        return module_info
    
    # 读取所有文件
    for item in os.listdir(module_subdir):
        item_path = os.path.join(module_subdir, item)
        if os.path.isdir(item_path):
            module_info['files'].append(item)
        else:
            module_info['files'].append(item)
            
            # 读取版本信息
            if item == 'version.txt':
                try:
                    with open(item_path, 'r', encoding='utf-8') as f:
                        version = f.read().strip()
                        module_info['version'] = version
                        module_info['latest'] = version
                except Exception as e:
                    print(f"读取版本文件失败 {item_path}: {e}")
            
            # 读取依赖信息
            elif item == 'depends.txt':
                try:
                    with open(item_path, 'r', encoding='utf-8') as f:
                        depends = f.read().strip().split('\n')
                        module_info['depends'] = [d.strip() for d in depends if d.strip()]
                except Exception as e:
                    print(f"读取依赖文件失败 {item_path}: {e}")
    
    return module_info


def generate_meta_json(base_dir):
    """生成meta.json文件"""
    # 查找所有latest包
    packages = find_latest_packages(base_dir)
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        modules = {}
        
        # 处理每个包
        for package in packages:
            extract_dir = os.path.join(temp_dir, package['name'])
            extract_package(package['path'], extract_dir)
            
            # 读取模块信息
            module_info = read_module_info(extract_dir, package['name'])
            modules[package['name']] = module_info
        
        # 构建元数据
        metadata = {
            "packages": list(modules.keys()),
            **modules
        }
        
        # 写入meta.json文件
        output_path = os.path.join(base_dir, 'meta.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        return output_path


def main():
    """主函数"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = script_dir
    
    generate_meta_json(base_dir)


if __name__ == "__main__":
    main()