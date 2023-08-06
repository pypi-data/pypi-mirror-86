# hf_ctp_py_proxy
上期技术期货交易api之python封装，实现接口调用。支持windows linux.

## 环境需求
* VS2017
* python 3.6+

## 使用说明
* 运行 `pyton generate\\run.py` 生成所有文件
* C++编译
    * Windows
        * 环境要求 `vs2017`
        * 设置项目为x64,否则会提示找不到windows.h
        * 打开ctp_c\\ctp.sln
        * 编译ctp_quote 和 ctp_trade项目
        * 编译后生成的dll放在 `py_ctp/lib64` 目录下
    * Linux
        * 设置系统语言为：zh_CN.UTF-8
        * 复制 ctp_20180109\\*.so到 `py_ctp/lib64` 目录下
        * 进入 `py_ctp/lib64` 目录，执行以下指令, -Wl,rpath=指定so路径(需要与setup.py中的data_files配合使用)
            * 6.3.15
                1. 代码生成
                    ```bash
                    pip uninstall py-ctp -y && python generate/run.py v6.3.15_20190220
                    ```
                2. 编译 so
                    ```bash
                    cd py_ctp/lib64/ \
                    && \cp ../../v6.3.15_20190220/*.so . \
                    && g++ -shared -fPIC -Wl,-rpath . -o ./ctp_trade.so ../../ctp_c/trade.cpp thosttraderapi_se.so \
                    && g++ -shared -fPIC -Wl,-rpath . -o ./ctp_quote.so ../../ctp_c/quote.cpp  thostmduserapi_se.so \
                    && cd ../..
                    ```
                3. 测试
                    ```bash
                    python setup.py install && python test_trade.py
                    ```
                4. 上传
                    ```bash
                    sed -i "s#version=.*#version='6.3.15.`date '+%m%d'`',#g" setup.py \
                    && python setup.py sdist && twine upload -u haifengat dist/*6.3.15.`date '+%m%d'`*.gz \
                    && python setup.py bdist_wheel && twine upload -u haifengat dist/*6.3.15.`date '+%m%d'`*.whl
                    ```
            * 6.3.16
                1. 代码生成
                    ```bash
                    pip uninstall py-ctp -y && python generate/run.py v6.3.16_T1_20190508
                    ```
                2. 编译 so
                    ```bash
                    cd py_ctp/lib64/ \
                    && \cp ../../v6.3.16_T1_20190508/*.so . \
                    && g++ -shared -fPIC -Wl,-rpath . -o ./ctp_trade.so ../../ctp_c/trade.cpp thosttraderapi_se.so \
                    && g++ -shared -fPIC -Wl,-rpath . -o ./ctp_quote.so ../../ctp_c/quote.cpp  thostmduserapi_se.so \
                    && cd ../..
                    ```
                3. 测试
                    ```bash
                    python setup.py install && python test_trade.py
                    ```
                4. 上传
                    ```bash
                    sed -i "s#version=.*#version='6.3.16.`date '+%m%d'`',#g" setup.py \
                    && python setup.py sdist && twine upload -u haifengat dist/*6.3.16.`date '+%m%d'`*.gz \
                    && python setup.py bdist_wheel && twine upload -u haifengat dist/*6.3.16.`date '+%m%d'`*.whl
                    ```

* 代码管理
    ```bash
    eval `ssh-agent`
    ssh-add /home/code/gitee_rsa
    git push gitee
    ```
## 更新
### 20201104
更新:接口更新到6.3.15;不再支持32位; 解决lnx下so路径问题;解决合约过多导致的bug;


