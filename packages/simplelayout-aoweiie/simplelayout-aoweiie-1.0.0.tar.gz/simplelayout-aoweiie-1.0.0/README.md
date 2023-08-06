[![Work in Repl.it](https://classroom.github.com/assets/work-in-replit-14baed9a392b3a25080506f3b7b6d57f295ec2978f6f33ec97e36a161684cbe9.svg)](https://classroom.github.com/online_ide?assignment_repo_id=3611573&assignment_repo_type=AssignmentRepo)
# simplelayout-generator

本次作业将实现生成器的数据生成部分，也就是 1-simplelayout-cli 中的主要逻辑部分。同时考察 package、module 的相关知识。

## 要求

- 目录结构为 

```
simplelayout
│  ├─cli
│  │  └─__init__.py
│  │  └─cli_generate.py
│  ├─generator
│  │  └─__init__.py
│  │  └─core.py
│  │  └─utils.py
```

- 符合 PEP 8 代码规范
- 将所需第三方 package 放到 `requirements.txt` 中
- 按照 `TODO `提示完成相应功能点
  1. `/simplelayout/cli/cli_generate.py`
  2. `/simplelayout/cli/__init__.py`
  3. `/simplelayout/generator/core.py`
  4. `/simplelayout/generator/utils.py`
  5. `/simplelayout/__main__.py`
- 通过相应单元测试
- 目标：将`simplelayout`以脚本方式运行，接口参数与作业 `1-simplelayout-CLI` 一致，即

  ```bash
  python -m simplelayout --board_grid 100 --unit_grid 10 --unit_n 3 --positions 1 15 33 --outdir dir1/dir2 --file_name example
  ```

## 参考

- mat 文件存储 [scipy.io.savemat](https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.savemat.html#scipy.io.savemat)
- [`__main__`](https://docs.python.org/3/library/__main__.html)

## 评分标准

|       要点        | 分值  |
| :---------------: | :---: |
|     代码规范      |   1   |
| generate_matrix() |   2   |
|      main()       |   2   |
|   save_matrix()   |   1   |
|    save_fig()     |   1   |
|    make_dir()     |   1   |
|       总分        |   8   |

