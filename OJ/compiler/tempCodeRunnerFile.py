with open(input_path, 'r') as input_file:
            with open(output_path, 'w') as output_file:
                process = subprocess.run(['python', code_path], stdin=input_file, stdout=output_file)
                if process.returncode != 0:
                    return "Runtime Error"