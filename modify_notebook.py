import json

# ノートブックを読み込む
with open('COMPAS_MLP_lecture_1.ipynb', 'r') as f:
    notebook = json.load(f)

# 変更を加える
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        # test_sizeの変更（5割に）
        if 'X_train_val, X_test, y_train_val, y_test = train_test_split(X, y,test_size=0.2, random_state=42)' in ''.join(cell['source']):
            for i, line in enumerate(cell['source']):
                if 'test_size=0.2' in line:
                    cell['source'][i] = line.replace('test_size=0.2', 'test_size=0.5')
        
        # ネットワークの定義変更
        if 'self.linear_relu_stack = nn.Sequential(' in ''.join(cell['source']) and 'nn.ReLU()' in ''.join(cell['source']):
            # 活性化関数をReLUからTanhに変更し、中間層を1層のみに変更
            if 'model = NeuralNetwork().to(device)' in ''.join(cell['source']):
                new_content = []
                in_network_def = False
                for line in cell['source']:
                    if 'self.linear_relu_stack = nn.Sequential(' in line:
                        in_network_def = True
                        new_content.append(line)
                        new_content.append('            nn.Linear(14710,128),\n')
                        new_content.append('            nn.Tanh(),\n')
                        new_content.append('            nn.Linear(128,2)\n')
                    elif in_network_def and ')' in line and not any(x in line for x in ['nn.Linear', 'nn.ReLU', 'nn.Tanh']):
                        in_network_def = False
                        new_content.append(line)
                    elif not in_network_def or not any(x in line for x in ['nn.Linear', 'nn.ReLU', 'nn.Tanh']):
                        new_content.append(line)
                cell['source'] = new_content

# 変更を保存
with open('COMPAS_MLP_lecture_1_modified.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print("Modified notebook saved as COMPAS_MLP_lecture_1_modified.ipynb") 