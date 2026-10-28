#!/usr/bin/env python3
import os
import sys
import re
import argparse

# Códigos de colores para imitar a la Norminette
RED = '\033[91m'
GREEN = '\033[92m'
CYAN = '\033[96m'
RESET = '\033[0m'

def check_line(line, line_num, filepath, module):
    errors = []
    clean_line = line.rstrip('\n')
    
    # 1. Reglas de Estilo y Legibilidad
    if len(clean_line) > 80:
        errors.append(f"Línea {line_num}: Excede los 80 caracteres (tiene {len(clean_line)}).")
    
    if '\t' in line:
        errors.append(f"Línea {line_num}: Uso de tabulaciones detectado. Usa 2 espacios.")
        
    # 2. Funciones y Keywords prohibidas por 42
    if re.search(r'\b(printf|malloc|calloc|realloc|free)\s*\(', line):
        errors.append(f"Línea {line_num}: Función de C prohibida (printf/alloc/free).")
        
    if re.search(r'\busing\s+namespace\b', line):
        errors.append(f"Línea {line_num}: 'using namespace' está prohibido (-42).")
        
    if re.search(r'\bfriend\b', line):
        errors.append(f"Línea {line_num}: 'friend' está prohibido (-42).")

    # 3. Restricción de STL (Depende del módulo)
    if module < 8:
        if re.search(r'#include\s+<(vector|list|map|algorithm)>', line):
            errors.append(f"Línea {line_num}: STL prohibida en módulos < 08.")

    return errors

def check_file(filepath, module):
    errors = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            for i, line in enumerate(lines):
                line_errors = check_line(line, i + 1, filepath, module)
                errors.extend(line_errors)
                
            # Extra: Comprobar Header Guards en .hpp
            if filepath.endswith('.hpp'):
                content = "".join(lines)
                filename_upper = os.path.basename(filepath).replace('.', '_').upper()
                if not re.search(r'#ifndef', content) or not re.search(r'#define', content):
                    errors.append("Faltan los Header Guards (#ifndef, #define).")
                    
    except Exception as e:
        return [f"Error al leer el archivo: {str(e)}"]
        
    return errors

def get_files_to_check(paths):
    files_to_check = []
    for path in paths:
        if os.path.isfile(path) and path.endswith(('.cpp', '.hpp', '.h')):
            files_to_check.append(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(('.cpp', '.hpp', '.h')):
                        files_to_check.append(os.path.join(root, file))
    return files_to_check

def main():
    parser = argparse.ArgumentParser(description="Norminette personalizada para C++ en 42.")
    parser.add_argument('paths', nargs='+', help="Archivos o directorios a revisar.")
    parser.add_argument('-m', '--module', type=int, default=0, help="Número del módulo de C++ (0-9).")
    
    args = parser.parse_args()
    files = get_files_to_check(args.paths)
    
    if not files:
        print(f"{CYAN}No se encontraron archivos .cpp o .hpp para revisar.{RESET}")
        return

    all_ok = True
    for filepath in files:
        errors = check_file(filepath, args.module)
        
        if errors:
            all_ok = False
            print(f"{RED}Error:{RESET} {filepath}")
            for error in errors:
                print(f"  {error}")
        else:
            print(f"{GREEN}OK!{RESET} {filepath}")

    if not all_ok:
        sys.exit(1)

if __name__ == '__main__':
    main()
