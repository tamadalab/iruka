# coding: UTF-8
import os
import json

def weighting_from_branch(types, branch_name):
    """
    ブランチ名から重み付けを行う。
    """
    if "fix" in branch_name:
        types["fix"] = types["fix"] * 2.0
        print("ブランチ名よりfixを重み付け")

    elif "release" in branch_name:
        types["release"] = types["release"] * 5.0
        print("ブランチ名よりreleaseを重み付け")

    elif "feature" in branch_name:
        types["feat"] = types["feat"] * 2.0
        print("ブランチ名よりfeatを重み付け")

    return types

def weighting_from_file_change(types, file, insertion, deletion):
    """
    ファイル名とファイルごとの追加行数、削除行数で重み付けを行う。
    """
    if "build.gradle" in file or "package.json" in file:
        types["build"] = types["build"] * 5.0
        print("ファイルよりbuildを重み付け")

    elif file.endswith(".md"):
        types["docs"] = types["docs"] * 5.0
        print("ファイルよりdocsを重み付け")

    elif "test/java/" in file or file.endswith("Test.java") or file.endswith("test.js") or "tests/" in file:
        types["test"] = types["test"] * 5.0
        print("ファイルよりtestを重み付け")

    elif ".travis.yml" in file or ".github/workflows" in file or ".circleci/config.yml" in file:
        types["ci"] = types["ci"] * 5.0
        print("ファイルよりciを重み付け")
    
    # fixとfeatの重み付け、追加行と削除行の比較
    # ここは修正が必要
    if insertion > deletion:
        types["feat"] = types["feat"] * 2.0
        print("変更行数よりfeatを重み付け")

    else:
        types["fix"] = types["fix"] * 2.0
        print("変更行数よりfixを重み付け")
        
    return types

def main():

    commitsID = []
    with open ('commitID.txt') as f:
        for line in f:
            commitsID.append(line[:-1])
    
    print(commitsID)
    # gitコマンドでファイル取得
    """
    os.system('git diff HEAD --name-only > file_name.txt')
    os.system('git rev-parse --abbrev-ref HEAD > branch_name.txt')
    os.system('git diff HEAD --numstat > stat.txt')
    """
    commits_len = len(commitsID)
    for j in range(commits_len - 1):
        commit1 = commitsID[j]
        commit2 = commitsID[j+1]
        os.system('git diff --name-only %s %s > file_name.txt' % (commit1, commit2))
        os.system('git branch --contains %s > branch_name.txt' % (commit1))
        os.system('git diff --numstat %s %s > stat.txt' % (commit1, commit2))
    
        # ファイルパス
        file_name_file = 'file_name.txt'
        branch_file = 'branch_name.txt'
        stat_file = 'stat.txt'

        # ファイル名のリスト
        file_list = []
        with open (file_name_file) as f:
            for line in f:
                file_list.append(line)

        file_list = [line.rstrip('\n') for line in file_list]

        # ブランチ名
        with open (branch_file) as f:
            branch_name = f.read()

        # 追加行、削除行、ファイル名のリスト
        with open (stat_file) as f:
            numstat_list = [line.split() for line in f]

        print(numstat_list)
        print(file_list)
        print(branch_name)
        
        # 各タイプのスコア
        types = {"build":1.0, "fix":1.0, "feat":1.0, "docs":1.0, "test":1.0, "ci":1.0, "release":1.0}

        # ブランチ名から重み付けをする
        types = weighting_from_branch(types, branch_name)

        # ファイル名、追加行数、削除行数から重み付けをする
        i = 0
        for file in file_list:
            print(numstat_list[i][0])
            print(numstat_list[i][1])
            if numstat_list[i][0] in '-':
                numstat_list[i][0] = 0
            if numstat_list[i][1] in "-":
                numstat_list[i][1] = 0
            types = weighting_from_file_change(types, file, int(numstat_list[i][0]), int(numstat_list[i][1]))
            i = i+1

        # タイプの値を昇順で出力
        types2 = sorted(types.items(), key=lambda x:x[1], reverse=True)
        print(types2)
        max_key = max(types, key=types.get)
        print(max_key)

        f = open('commit_type.txt', 'a')
        f.write(max_key + '\n')

if __name__ == "__main__":
    main()